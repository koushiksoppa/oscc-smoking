"""Stage 3: generate the screening worksheets the reviewer fills in.

    python -m scripts.screening.worksheet --stage ta             # create (refuses to overwrite)
    python -m scripts.screening.worksheet --stage ta --refresh    # add new records, keep decisions
    python -m scripts.screening.worksheet --stage ft              # built from title/abstract includes

The worksheet contains **no decisions**. Every decision column is written empty and is the human
reviewer's to complete (D010). Nothing here suggests, pre-sorts or ranks records: an automated
suggestion could not satisfy a `decision` field even if one existed, and none is produced.

Existing work is never destroyed. Plain creation refuses to touch an existing file; `--refresh`
merges on `report_id`, carrying every recorded decision across and adding only records that are
new. A row that holds a decision is never dropped, even if it has left the source set — that
would silently discard the reviewer's work, so it is reported as an error instead.
"""
from __future__ import annotations

import argparse
import csv
import sys

from scripts.common.config import PROCESSED_DIR, ROOT, PipelineError
from scripts.dedup.deduplicate import verify_provenance
from scripts.screening import vocabulary
from scripts.screening.vocabulary import ADJUDICATED, ADOPTED, FT, INCLUDE, STAGE_LABEL, TA

# NOT under data/processed/, which is gitignored as regenerable. Screening decisions are human
# research work that cannot be regenerated from anything, so they must be version-controlled.
SCREENING_DIR = ROOT / "data" / "screening"

# Columns the reviewer fills in. Everything else is derived and must not be edited.
DECISION_FIELDS = ["decision", "reason_code", "reviewer", "screened_date", "notes"]

# Title/abstract carries two further columns so that automated output and reviewer judgement are
# distinguishable in the data rather than only in a commit message (D010):
#   suggestion      — what the tooling proposed. Machine-written, never the reviewer's to edit,
#                     but it cannot be regenerated from upstream data so it is preserved, not
#                     recomputed, on --refresh.
#   decision_basis  — which act produced `decision`: adopting a suggestion, or judging the record.
TA_SUGGESTION_FIELDS = ["suggestion", "suggestion_reason_code"]
TA_DECISION_FIELDS = ["decision", "decision_basis", "reason_code", "reviewer", "screened_date",
                      "adjudicated_date", "notes"]
# Full text has no suggestion mechanism, but it still has to say how each decision came about,
# so the same basis column applies there without the suggestion columns.
FT_DECISION_FIELDS = ["decision", "decision_basis", "reason_code", "reviewer", "screened_date",
                      "adjudicated_date", "notes"]
TA_DERIVED = ["report_id", "record_id", "source_id", "pmid", "doi", "pub_year", "first_author",
              "journal", "publication_types", "title", "abstract"]
# `source_ta_decision_basis` describes how the *title/abstract* decision that carried this
# report forward was made. It is derived from the title/abstract worksheet and recomputed on
# every refresh, so adjudicating a source record promotes its full-text row automatically. It is
# distinct from this worksheet's own `decision_basis`, which describes the full-text decision.
FT_DERIVED = ["report_id", "record_id", "pmid", "doi", "pub_year", "first_author", "title",
              "source_ta_decision_basis"]
FT_RETRIEVAL = ["full_text_status", "full_text_source"]

FIELDS = {
    TA: TA_DERIVED + TA_SUGGESTION_FIELDS + TA_DECISION_FIELDS,
    FT: FT_DERIVED + FT_RETRIEVAL + FT_DECISION_FIELDS,
}
# What counts as the reviewer's own work, for "would a refresh destroy something?".
EDITABLE = {TA: TA_DECISION_FIELDS, FT: FT_RETRIEVAL + FT_DECISION_FIELDS}
# What a refresh must carry across. A suggestion is not reviewer work, but it is not derivable
# from upstream either, so dropping it would lose the provenance the schema exists to record.
PRESERVED = {TA: TA_SUGGESTION_FIELDS + TA_DECISION_FIELDS, FT: EDITABLE[FT]}


def worksheet_path(stage: str):
    return SCREENING_DIR / f"screening_{stage}.csv"


def read_csv(path) -> list[dict[str, str]]:
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def has_content(row: dict[str, str], stage: str) -> bool:
    """Whether a reviewer has recorded anything in this row."""
    return any((row.get(f) or "").strip() for f in EDITABLE[stage])


def adjudication_problems(row: dict[str, str], vocab) -> list[str]:
    """Row-level problems with a decision's completeness and provenance, stage-independent.

    Shared by the validator and by the full-text carry-forward, so that a row the validator
    would reject can never promote a report into the formal flow. Reason-code rules depend on
    the stage and stay in the validator.
    """
    rid = row.get("report_id", "?")
    decision = (row.get("decision") or "").strip()
    reviewer = (row.get("reviewer") or "").strip()
    screened = (row.get("screened_date") or "").strip()
    basis = (row.get("decision_basis") or "").strip()
    suggestion = (row.get("suggestion") or "").strip()
    adjudicated = (row.get("adjudicated_date") or "").strip()
    problems: list[str] = []

    if decision and decision not in vocab.decisions:
        return [f"{rid}: unknown decision {decision!r}; allowed: {list(vocab.decisions)}"]
    if decision and not reviewer:
        problems.append(f"{rid}: decision {decision!r} recorded with no reviewer")
    if decision and not screened:
        problems.append(f"{rid}: decision {decision!r} recorded with no screened_date")

    if "decision_basis" not in row and "suggestion" not in row:
        return problems

    bases = set(vocab.basis_codes())
    if suggestion and suggestion not in vocab.decisions:
        problems.append(
            f"{rid}: unknown suggestion {suggestion!r}; allowed: {list(vocab.decisions)}")
    if decision and not basis:
        problems.append(
            f"{rid}: decision {decision!r} recorded with no decision_basis — the record must say "
            "whether it was adjudicated or adopted from a suggestion (D010)")
    elif basis and basis not in bases:
        problems.append(f"{rid}: unknown decision_basis {basis!r}; allowed: {sorted(bases)}")
    elif basis and not decision:
        problems.append(f"{rid}: decision_basis {basis!r} recorded with no decision")
    elif basis == ADOPTED:
        if not suggestion:
            problems.append(
                f"{rid}: basis is {ADOPTED!r} but no suggestion is recorded — there is nothing "
                "that was adopted")
        elif suggestion != decision:
            problems.append(
                f"{rid}: basis is {ADOPTED!r} but decision {decision!r} differs from the "
                f"suggestion {suggestion!r}; a differing decision is not an adoption")
        elif "suggestion_reason_code" in row:
            reason = (row.get("reason_code") or "").strip()
            sug_reason = (row.get("suggestion_reason_code") or "").strip()
            if sug_reason != reason:
                problems.append(
                    f"{rid}: basis is {ADOPTED!r} but reason_code {reason or '(none)'!r} differs "
                    f"from the suggested {sug_reason or '(none)'!r}; changing the reason is an "
                    "adjudication, not an adoption")

    # An adjudication is a dated act. Without its own date, flipping the basis on a row that
    # already carries the bulk-adoption reviewer and date would silently convert a provisional
    # record into a formal one with no new evidence.
    if "adjudicated_date" in row:
        if decision and basis == ADJUDICATED and not adjudicated:
            problems.append(
                f"{rid}: basis is {ADJUDICATED!r} but no adjudicated_date is recorded — an "
                "adjudication must record when it was made")
        if adjudicated and basis != ADJUDICATED:
            problems.append(
                f"{rid}: adjudicated_date recorded but decision_basis is "
                f"{basis or '(none)'!r}; only an independent adjudication has one")
    return problems


def adopted_includes(ta_rows: list[dict[str, str]]) -> list[str]:
    """Title/abstract includes whose decision was adopted from a suggestion, not adjudicated.

    Carrying these into full text propagates automated output into the next stage, so callers
    warn by default and refuse under the final gate (D010).
    """
    return sorted(r["report_id"] for r in ta_rows
                  if (r.get("decision") or "").strip() == INCLUDE
                  and (r.get("decision_basis") or "").strip() == ADOPTED)


def source_rows(stage: str, strict: bool = False) -> list[dict[str, str]]:
    """Build the derived part of the worksheet from upstream data, verifying provenance first."""
    index_path = PROCESSED_DIR / "dedup" / "report_index.csv"
    if not index_path.exists():
        raise PipelineError(
            f"{index_path.name} not found. Run scripts.dedup.deduplicate first; screening is "
            "built from unique reports, not raw records."
        )
    index = read_csv(index_path)
    for source_id in sorted({r["source_id"] for r in index}):
        verify_provenance(source_id)        # raw checksum + raw-to-derived consistency

    citations = {}
    for source_id in sorted({r["source_id"] for r in index}):
        path = PROCESSED_DIR / "citations" / f"{source_id}_citations.csv"
        if not path.exists():
            raise PipelineError(
                f"{path.name} not found, though {source_id} appears in report_index.csv. "
                "Re-run parse_citations and deduplicate for this source."
            )
        for row in read_csv(path):
            citations[row["record_id"]] = row

    # One row per unique report: the primary record represents the group (D004).
    primaries = [r for r in index if r["is_primary"] == "yes"]
    if stage == TA:
        rows = []
        for r in sorted(primaries, key=lambda r: r["report_id"]):
            cit = citations.get(r["record_id"], {})
            rows.append({
                "report_id": r["report_id"], "record_id": r["record_id"],
                "source_id": r["source_id"], "pmid": r["pmid"], "doi": r["doi"],
                "pub_year": r["pub_year"], "first_author": r["first_author"],
                "journal": cit.get("journal", ""),
                "publication_types": cit.get("publication_types", ""),
                "title": r["title"], "abstract": cit.get("abstract", ""),
            })
        return rows

    # Full-text stage: only reports included at title/abstract reach it.
    ta_path = worksheet_path(TA)
    if not ta_path.exists():
        raise PipelineError(
            "the title/abstract worksheet does not exist, so there are no includes to carry "
            f"forward. Create it first: --stage {TA}"
        )
    ta_rows = read_csv(ta_path)
    adopted = adopted_includes(ta_rows)
    if adopted:
        message = (
            f"{len(adopted)} of the title/abstract includes were adopted from an automated "
            "suggestion and not independently adjudicated, so the full-text stage would be built "
            "on automated output (D010)")
        if strict:
            raise PipelineError(
                message + ". Adjudicate them, or re-run without --final to proceed anyway."
            )
        print(f"WARNING: {message}.", file=sys.stderr)
    # A title/abstract row the validator would reject must not promote its full-text row into
    # the formal flow, so the basis is carried forward only when the row is actually valid.
    vocab = vocabulary.load_vocabulary()
    included, invalid = {}, []
    for r in ta_rows:
        if (r.get("decision") or "").strip() != INCLUDE:
            continue
        basis = (r.get("decision_basis") or "").strip()
        if adjudication_problems(r, vocab):
            invalid.append(r["report_id"])
            basis = ""        # provenance cannot be asserted for an invalid row
        included[r["report_id"]] = basis
    if invalid:
        print(f"WARNING: {len(invalid)} title/abstract include(s) do not pass row validation, so "
              f"their provenance is left blank and they enter no formal count: "
              f"{', '.join(invalid[:10])}{' …' if len(invalid) > 10 else ''}.", file=sys.stderr)
    by_id = {r["report_id"]: r for r in primaries}
    rows = []
    for report_id in sorted(included):
        r = by_id.get(report_id, {})
        rows.append({
            "report_id": report_id, "record_id": r.get("record_id", ""), "pmid": r.get("pmid", ""),
            "doi": r.get("doi", ""), "pub_year": r.get("pub_year", ""),
            "first_author": r.get("first_author", ""), "title": r.get("title", ""),
            "source_ta_decision_basis": included[report_id],
            "full_text_status": "", "full_text_source": "",
        })
    return rows


def build(stage: str, refresh: bool = False, strict: bool = False) -> dict:
    rows = source_rows(stage, strict=strict)
    path = worksheet_path(stage)
    fields = FIELDS[stage]

    if path.exists() and not refresh:
        raise PipelineError(
            f"{path.name} already exists and may hold screening decisions, so it is not "
            f"overwritten. Use --refresh to add any new records while keeping every decision."
        )

    existing: dict[str, dict[str, str]] = {}
    if path.exists():
        for row in read_csv(path):
            existing[row["report_id"]] = row

    # A recorded decision must never be silently dropped.
    incoming_ids = {r["report_id"] for r in rows}
    orphaned = sorted(rid for rid, row in existing.items()
                      if rid not in incoming_ids and has_content(row, stage))
    if orphaned:
        raise PipelineError(
            f"{path.name}: these reports hold screening decisions but are no longer in the "
            f"source set: {', '.join(orphaned)}\n"
            "  Refusing to proceed: regenerating would discard recorded work. Investigate why "
            "they left the source set before refreshing."
        )

    added, carried = 0, 0
    out: list[dict[str, str]] = []
    for row in rows:
        merged = {f: "" for f in fields}
        merged.update({k: v for k, v in row.items() if k in fields})
        prior = existing.get(row["report_id"])
        if prior is None:
            added += 1
        else:
            for f in PRESERVED[stage]:
                merged[f] = prior.get(f, "")
            if has_content(prior, stage):
                carried += 1
        out.append(merged)

    SCREENING_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out)

    return {"stage": stage, "path": path, "rows": len(out), "added": added,
            "decisions_carried": carried}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stage", required=True, choices=[TA, FT])
    ap.add_argument("--refresh", action="store_true",
                    help="add new records while preserving every recorded decision")
    ap.add_argument("--final", action="store_true",
                    help="refuse to carry forward decisions that were adopted, not adjudicated")
    args = ap.parse_args(argv)
    try:
        vocabulary.load_vocabulary()          # fail early if the vocabulary is malformed
        result = build(args.stage, refresh=args.refresh, strict=args.final)
    except PipelineError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"{STAGE_LABEL[result['stage']]} worksheet: {result['rows']} rows "
          f"({result['added']} new, {result['decisions_carried']} with decisions preserved)")
    print(f"  -> {result['path'].relative_to(PROCESSED_DIR.parent.parent).as_posix()}")
    print("  Decision columns are empty by design; they are the reviewer's to complete (D010).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
