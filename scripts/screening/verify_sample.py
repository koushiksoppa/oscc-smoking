"""Blinded verification of a random sample of recorded title/abstract decisions.

    python -m scripts.screening.verify_sample --draw     # write the blinded sheet
    python -m scripts.screening.verify_sample --score    # unblind and report agreement

The recorded decisions were entered by adopting a suggestion set generated from the titles and
abstracts. A check of those decisions by whoever produced the suggestions would be circular, so
this module hands the reviewer a sample of records **without** the recorded decision and compares
the reviewer's independent judgement afterwards.

Everything is fixed before the sample is drawn, so the exercise cannot be post-hoc:

* **Sample size** — 40 of 194 (20.6%), simple random without replacement.
* **Seed** — derived from the data, never chosen, so the draw is auditable. **Two rules exist
  and are never conflated (D020).** The committed 40-record sample was drawn under the historical
  rule `file_bytes_crlf_v1` — the first 8 hex digits of the SHA-256 of the worksheet FILE BYTES,
  in the CRLF form it had on disk — and that seed, `DRAW_SEED`, is preserved verbatim and never
  recomputed. Draws made after D020 use `ordered_report_ids_v1`, the canonical sampling-frame
  digest, which is invariant to line endings and to later columns.
* **Agreement** — computed at the **record level**: one comparison per sampled record, between
  the recorded decision and the reviewer's `your_decision`. Only `your_decision` enters the rate.
  `your_reason_code` is validated and reported separately among concordant exclusions, and
  `your_notes` is never scored. Cohen's kappa is reported as a descriptive statistic and is
  **not** a verdict threshold.
* **Acceptance rule** — >= 95% agreement ADOPTS the unsampled remainder; >= 90% and < 95% is
  EXTEND; < 90% RE-SCREENS. Both thresholds are inclusive at their lower bound. **EXTEND is a
  classification and a workflow pause, not an automatic second draw**: nothing here draws or
  scores a second sample, and an extension needs a separately approved sampling frame,
  second-extension outcome, pooling rule and maximum extension count. RE-SCREEN is likewise a
  verdict, not a completed action: it requires a human to re-screen the population manually.
* **Incomplete responses cannot be scored.** A single blank or whitespace-only `your_decision`
  refuses the whole sheet — no rate, no kappa, no verdict, no report.
* **Asymmetry rule** — any record the reviewer would *include* that was recorded as *exclude*
  triggers a sweep of every record excluded under that same reason code, whatever the headline
  rate. Erroneous exclusion loses evidence irrecoverably; the opposite direction only costs
  retrieval effort, so it is recorded but triggers nothing.

The module never writes to `screening_ta.csv` and never changes a recorded decision.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import random
import sys
from collections import Counter

from scripts.common.config import VALIDATION_DIR, PipelineError
from scripts.screening import worksheet
from scripts.screening.show import load_languages
from scripts.screening.vocabulary import EXCLUDE, INCLUDE, TA, load_vocabulary

SAMPLE_SIZE = 40
ADOPT_AT = 0.95
EXTEND_AT = 0.90

# Provenance of the existing committed 40-record sample in data/screening/verification_sample.csv.
#
# The seed is derived from the worksheet, so it is tied to one specific state of that file. These
# two values describe the state the sample was actually drawn from, and they are recorded rather
# than re-derived: a later migration changes the worksheet's bytes, and re-deriving would then
# report a seed that never drew anything.
#
# They refer to `data/screening/screening_ta.csv` as committed at c704582, before the provenance
# migration added `suggestion`, `suggestion_reason_code`, `decision_basis` and `adjudicated_date`.
# The digest is of that file in the **CRLF** form it had on disk during the historical execution.
# Hashing the LF blob that Git stores for the same commit gives a different digest
# (9ce12867b8f11222963719e7aae9193493f1524b21477a95c664f0cca8f8270a, seed 2632001639), because
# SHA-256 covers the bytes including line endings; that value never drew this sample. Verified:
# seed_from(DRAW_SHA) reproduces the committed 40 report_ids, in order, from the c704582 worksheet.
DRAW_SHA = "5938922a529a7f7318824f4216b4b9ab05b920a14def7c15e72c15ea2a6076eb"
DRAW_SEED = 1496879658

# The rule that produced DRAW_SEED. Named so that it can never be confused with the canonical
# rule below: this one hashes the file's bytes, which is why it is platform-dependent.
DRAW_SEED_DERIVATION = "file_bytes_crlf_v1"

# ---------------------------------------------------------------------------------------------
# Canonical sampling-frame digest (D020). Governs FUTURE draws only.
#
# `DRAW_SHA` identifies a worksheet *file*; this identifies the *sampling frame* the draw
# procedure actually consumes. The distinction is the whole point: a frame digest is invariant
# to line endings and to later columns, neither of which the draw reads, and it changes when the
# units or their order change, which the draw does read.
#
# The historical seed is NOT re-derived from this. The two rules coexist, each labelled, and a
# sample records which one governs it.
# ---------------------------------------------------------------------------------------------
FRAME_DIGEST_RULE = "ordered_report_ids_v1"

# The canonical digest of the frame the committed 40-record sample was drawn from. Recorded so
# that the historical sample gains a platform-independent frame identity without its seed or its
# membership changing. Verified equal for the pre-migration (16-column) and post-migration
# (20-column) worksheets, because the frame did not change.
DRAW_FRAME_DIGEST = "37cc07e64054ef938229fbecec5f7da70f4c9ae419aae9f79b04d642574209ad"

SHOWN = ["report_id", "pmid", "doi", "pub_year", "first_author", "journal",
         "publication_types", "language", "title", "abstract"]
RESPONSE = ["your_decision", "your_reason_code", "your_notes"]
SHEET_FIELDS = SHOWN + RESPONSE


def sheet_path():
    return worksheet.SCREENING_DIR / "verification_sample.csv"


def digest(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seed_from(digest_hex: str) -> int:
    """The seed is derived from the data, so the draw is auditable and unchosen."""
    return int(digest_hex[:8], 16)


def canonical_frame(rows: list[dict]) -> bytes:
    """Serialise the sampling frame canonically, for hashing. D020.

    The specification, in full, so that a reviewer can reproduce it by hand:

    1.  **Fields included** — `report_id`, and nothing else.
    2.  **Field order** — not applicable; one field per unit.
    3.  **Record order** — worksheet file order, **preserved**, never sorted.
    4.  **Encoding** — UTF-8.
    5.  **Unicode normalisation** — NFC, applied to each identifier.
    6.  **Null and empty values** — refused. A unit with no identifier cannot be identified, so
        an empty or whitespace-only `report_id` raises rather than hashing as "".
    7.  **Serialisation** — the rule version, then a US-ASCII newline, then each identifier
        followed by a newline. The version is inside the hashed payload so that two rules can
        never produce the same digest for the same frame.
    8.  **Separator** — LF (0x0A) only. Never CRLF, whatever the file on disk uses.
    9.  **Hash** — SHA-256, lowercase hexadecimal, 64 characters.
    10. **Frame rows** — every row of the title/abstract worksheet, in file order. No filtering,
        no subsetting, no deduplication.

    Why `report_id` alone faithfully identifies the frame: `draw()` samples **positions**, by
    `random.Random(seed).sample(range(len(rows)), size)`, and then returns the rows at those
    positions. So the only things the draw procedure consumes are the *number* of units and
    *which unit sits at each position*. `report_id` is the screening unit of analysis (D004) and
    is unique across the worksheet, so the ordered sequence of `report_id` values determines
    both exactly. Including further columns would make the digest change when a title typo or an
    abstract re-import is corrected -- events that change no sampling unit and no position -- and
    would therefore misreport an unchanged frame as a different one. Excluding them keeps the
    digest sensitive to precisely what the draw depends on, and to nothing else.
    """
    import unicodedata
    out = [FRAME_DIGEST_RULE.encode("utf-8")]
    for i, r in enumerate(rows):
        rid = (r.get("report_id") or "").strip()
        if not rid:
            raise PipelineError(
                f"row {i} of the sampling frame has no report_id, so the sampling unit cannot "
                "be identified; the frame digest is undefined for such a frame"
            )
        out.append(unicodedata.normalize("NFC", rid).encode("utf-8"))
    return b"\n".join(out) + b"\n"


def frame_digest(rows: list[dict]) -> str:
    """SHA-256 of the canonical sampling frame. Platform-independent by construction."""
    return hashlib.sha256(canonical_frame(rows)).hexdigest()


def draw(rows: list[dict], size: int, seed: int) -> list[dict]:
    """A reproducible simple random sample, returned in worksheet order for readability."""
    if size < 1:
        raise PipelineError(f"sample size must be 1 or greater, got {size}")
    if size > len(rows):
        raise PipelineError(f"cannot draw {size} records from {len(rows)}")
    picked = random.Random(seed).sample(range(len(rows)), size)
    return [rows[i] for i in sorted(picked)]


def build_sheet(sample: list[dict], languages: dict[str, str]) -> list[dict]:
    """The blinded instrument. Carries no decision, reason, reviewer or note from the worksheet."""
    out = []
    for row in sample:
        entry = {f: "" for f in SHEET_FIELDS}
        for f in SHOWN:
            if f == "language":
                entry[f] = languages.get(row.get("record_id", ""), "")
            else:
                entry[f] = row.get(f, "")
        out.append(entry)
    return out


def read_csv(path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def kappa(pairs: list[tuple[str, str]]) -> float | None:
    """Cohen's kappa over however many categories appear. None when it is undefined.

    With no variation in either rater, expected agreement is 1 and kappa is 0/0. That is not a
    failure - raw agreement is still meaningful - so it is reported as undefined rather than
    raising or silently printing a misleading 0.
    """
    n = len(pairs)
    if not n:
        return None
    a = Counter(x for x, _ in pairs)
    b = Counter(y for _, y in pairs)
    po = sum(1 for x, y in pairs if x == y) / n
    pe = sum(a[k] * b[k] for k in set(a) | set(b)) / (n * n)
    if abs(1 - pe) < 1e-12:
        return None
    return (po - pe) / (1 - pe)


def score(sheet: list[dict], ta_rows: list[dict]) -> dict:
    """Compare the reviewer's blinded judgements with what is recorded."""
    vocab = load_vocabulary()
    recorded = {r["report_id"]: r for r in ta_rows}
    permitted = set(vocab.codes(TA))

    blank = [r["report_id"] for r in sheet if not (r.get("your_decision") or "").strip()]
    if blank:
        raise PipelineError(
            f"{len(blank)} row(s) have no your_decision: {', '.join(blank)}\n"
            "  Every sampled record needs an independent judgement before scoring."
        )

    pairs, discrepancies, reason_pairs, problems = [], [], [], []
    for r in sheet:
        rid = r["report_id"]
        if rid not in recorded:
            raise PipelineError(f"{rid} is not in the title/abstract worksheet")
        mine = (r["your_decision"] or "").strip()
        my_reason = (r.get("your_reason_code") or "").strip()
        theirs = (recorded[rid].get("decision") or "").strip()
        their_reason = (recorded[rid].get("reason_code") or "").strip()

        if mine not in vocab.decisions:
            problems.append(f"{rid}: {mine!r} is not a decision value")
            continue
        if mine == EXCLUDE and not my_reason:
            problems.append(f"{rid}: excluded with no reason code")
        elif mine == EXCLUDE and my_reason not in permitted:
            problems.append(f"{rid}: reason {my_reason!r} is not permitted at title/abstract")
        elif mine != EXCLUDE and my_reason:
            problems.append(f"{rid}: reason code recorded on a non-exclusion")

        pairs.append((theirs, mine))
        if theirs != mine:
            discrepancies.append({"report_id": rid, "recorded": theirs, "recorded_reason":
                                  their_reason, "reviewer": mine, "reviewer_reason": my_reason,
                                  "notes": (r.get("your_notes") or "").strip()})
        elif mine == EXCLUDE:
            reason_pairs.append((their_reason, my_reason, rid))

    if problems:
        raise PipelineError("the completed sheet is not internally valid:\n  "
                            + "\n  ".join(problems))

    n = len(pairs)
    agreed = sum(1 for x, y in pairs if x == y)
    rate = agreed / n if n else 0.0

    # Erroneous exclusion is the asymmetric risk: it removes evidence that no later stage can
    # recover, so one instance warrants sweeping every record excluded for the same reason.
    sweeps = sorted({d["recorded_reason"] for d in discrepancies
                     if d["recorded"] == EXCLUDE and d["reviewer"] == INCLUDE})
    sweep_sizes = {code: sum(1 for r in ta_rows
                             if (r.get("reason_code") or "").strip() == code) for code in sweeps}

    return {
        "n": n, "agreed": agreed, "rate": rate, "kappa": kappa(pairs),
        "discrepancies": discrepancies,
        "reason_agreed": sum(1 for a, b, _ in reason_pairs if a == b),
        "reason_total": len(reason_pairs),
        "reason_discrepancies": [(rid, a, b) for a, b, rid in reason_pairs if a != b],
        "verdict": verdict(rate),
        "sweeps": sweeps, "sweep_sizes": sweep_sizes,
        "population": len(ta_rows),
    }


def verdict(rate: float) -> str:
    if rate >= ADOPT_AT:
        return "ADOPT"
    if rate >= EXTEND_AT:
        return "EXTEND"
    return "RE-SCREEN"


VERDICT_TEXT = {
    "ADOPT": ("Agreement meets the pre-specified threshold. The decisions outside the sample are "
              "adopted as recorded, and this verification is reported in the methods."),
    "EXTEND": ("Agreement falls in the pre-specified middle band. This is a classification and a "
               "WORKFLOW PAUSE, not an automatic second draw: no second sample is drawn or scored "
               "here. An extension requires a separately approved sampling frame, "
               "second-extension outcome, pooling rule and maximum extension count, none of "
               "which is settled."),
    "RE-SCREEN": ("Agreement is below the pre-specified floor. The suggestion set is discarded as "
                  "a decision source and the population REQUIRES manual human re-screening. This "
                  "is a verdict, not a completed action: no record has been re-screened by "
                  "reaching it."),
}


def render(result: dict, current_sha: str, draw_seed: int | None = None,
           draw_sha: str | None = None, current_frame: str | None = None) -> str:
    """Render the scoring report.

    `draw_seed` and `draw_sha` describe the draw and belong under the pre-specified heading.
    `current_sha` describes the worksheet this scoring run read and is reported separately: it is
    not draw provenance, and labelling it as such would claim a seed that drew nothing.

    The draw pair defaults to the recorded constants, resolved on each call rather than bound at
    import, so there is one source of truth for them.
    """
    draw_seed = DRAW_SEED if draw_seed is None else draw_seed
    draw_sha = DRAW_SHA if draw_sha is None else draw_sha
    k = result["kappa"]
    moved = current_sha != draw_sha
    lines = [
        "# Title/abstract screening — blinded verification of a random sample", "",
        f"**Verdict: {result['verdict']}**", "",
        VERDICT_TEXT[result["verdict"]], "",
        "## Pre-specified before the sample was drawn", "",
        "| Parameter | Value |", "|---|---|",
        f"| Sample size | {result['n']} of {result['population']} "
        f"({result['n'] / result['population']:.1%}) |",
        "| Sampling | simple random, without replacement |",
        f"| Original draw seed | `{draw_seed}` |",
        f"| Seed derivation rule | `{DRAW_SEED_DERIVATION}` — the first 8 hex digits of the "
        "SHA-256 of the worksheet FILE BYTES, in the CRLF form it had on disk. Superseded by "
        f"`{FRAME_DIGEST_RULE}` (D020) for later draws; **not** re-derived here |",
        f"| Worksheet SHA-256 at the draw | `{draw_sha}` |",
        f"| Sampling-frame digest at the draw | `{DRAW_FRAME_DIGEST}` "
        f"(rule `{FRAME_DIGEST_RULE}`, platform-independent) |",
        "| Draw date | **UNVERIFIED** — no run log or date column was captured; a commit date "
        "is not evidence of when the draw was run |",
        "| Blinding | the recorded decision and reason were hidden from the reviewer |",
        f"| Adopt at | >= {ADOPT_AT:.0%} agreement |",
        f"| Extend at | >= {EXTEND_AT:.0%} and < {ADOPT_AT:.0%} |",
        f"| Re-screen below | {EXTEND_AT:.0%} |", "",
        "## This scoring run", "",
        "| Parameter | Value |", "|---|---|",
        f"| Current worksheet SHA-256 | `{current_sha}` |",
        f"| Same file as the draw | {'no' if moved else 'yes'} |",
        f"| Current sampling-frame digest | `{current_frame}` |" if current_frame else
        "| Current sampling-frame digest | not supplied to this report |",
        f"| Same sampling frame as the draw | "
        f"{('yes' if current_frame == DRAW_FRAME_DIGEST else 'NO — the frame itself has changed') if current_frame else 'not established'} |",
        "| Decisions compared against | the worksheet as it stands now |", "",
    ]
    if moved:
        lines += [
            "> **The worksheet has changed since the sample was drawn.** The sample and the "
            "original draw seed above are unaffected and remain the auditable record of the draw; "
            "re-deriving a seed from the current file would give a value that drew nothing. "
            "Agreement below is measured against the decisions recorded now. Scoring is not "
            "blocked by this.", "",
        ]
    lines += [
        "## Result", "", "| Metric | Value |", "|---|---|",
        f"| Agreement on include/exclude | **{result['agreed']} / {result['n']} "
        f"({result['rate']:.1%})** |",
        f"| Cohen's kappa | {'undefined (no variation in one or both raters)' if k is None else f'{k:.3f}'} |",
        f"| Reason-code agreement among concordant exclusions | "
        f"{result['reason_agreed']} / {result['reason_total']} |", "",
    ]

    if result["discrepancies"]:
        lines += ["## Decision discrepancies", "",
                  "| Report | Recorded | Reviewer | Direction |", "|---|---|---|---|"]
        for d in result["discrepancies"]:
            direction = ("**evidence lost if recorded stands**"
                         if d["recorded"] == EXCLUDE and d["reviewer"] == INCLUDE
                         else "retrieval effort only")
            rec = f"{d['recorded']}" + (f" (`{d['recorded_reason']}`)" if d["recorded_reason"] else "")
            rev = f"{d['reviewer']}" + (f" (`{d['reviewer_reason']}`)" if d["reviewer_reason"] else "")
            lines.append(f"| {d['report_id']} | {rec} | {rev} | {direction} |")
        lines.append("")
        for d in result["discrepancies"]:
            if d["notes"]:
                lines.append(f"- **{d['report_id']}** — {d['notes']}")
        lines.append("")
    else:
        lines += ["## Decision discrepancies", "", "None.", ""]

    if result["reason_discrepancies"]:
        lines += ["## Reason-code discrepancies among agreed exclusions", "",
                  "The decision matched; the recorded reason did not.", "",
                  "| Report | Recorded | Reviewer |", "|---|---|---|"]
        lines += [f"| {rid} | `{a}` | `{b}` |" for rid, a, b in result["reason_discrepancies"]]
        lines.append("")

    if result["sweeps"]:
        lines += ["## Asymmetry rule triggered", "",
                  "The reviewer would include a record that was excluded, so every record "
                  "excluded under the same reason is re-checked, independently of the headline "
                  "rate.", "", "| Reason code | Records to sweep |", "|---|---|"]
        lines += [f"| `{c}` | {result['sweep_sizes'][c]} |" for c in result["sweeps"]]
        lines.append("")
    else:
        lines += ["## Asymmetry rule", "",
                  "Not triggered: no record the reviewer would include was recorded as excluded.",
                  ""]

    lines += [
        "## What this measures, and what it does not", "",
        "Four things are deliberately distinguished:", "",
        "| Term | Meaning |", "|---|---|",
        "| **Automated suggestion** | A decision proposed by tooling from the title and "
        "abstract, recorded in `data/screening/ta_suggestions_<date>.csv`. Not a decision, and "
        "**not a reference standard**. |",
        "| **Human reviewer decision** | The value in `decision` in the title/abstract "
        "worksheet, entered by the reviewer. For this pass the reviewer adopted the suggestion "
        "set, so the two are identical. |",
        "| **Blinded verification sample** | A random subset re-judged by the reviewer without "
        "sight of the recorded decision. |",
        "| **Agreement** | The rate at which the reviewer's blinded judgement matched the "
        "recorded decision. |", "",
        "Because the recorded decisions are identical to the automated suggestions, the "
        "agreement reported here is **between one reviewer's blinded judgement and an "
        "automated suggestion set**. It is **not** inter-reviewer agreement, **not** "
        "independent duplicate screening by a second reviewer, and it does **not** treat the "
        "suggestions as ground truth: a discrepancy shows the two differ, not that either is "
        "correct. Report it as single-reviewer screening with an automation-assisted "
        "suggestion step and an internal blinded consistency check (D010, PRISMA 2020 item "
        "8).", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--draw", action="store_true", help="write the blinded verification sheet")
    g.add_argument("--score", action="store_true", help="unblind and report agreement")
    ap.add_argument("--size", type=int, default=SAMPLE_SIZE)
    args = ap.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    try:
        ta_path = worksheet.worksheet_path(TA)
        if not ta_path.exists():
            raise PipelineError(f"{ta_path.name} not found")
        ta_rows = read_csv(ta_path)
        sha = digest(ta_path)
        path = sheet_path()

        if args.draw:
            if path.exists():
                raise PipelineError(
                    f"{path.name} already exists and may hold the reviewer's judgements, so it "
                    "is not overwritten. Move it aside first if you really mean to redraw."
                )
            # A draw derives its seed from the worksheet in front of it. Scoring must not: it is
            # reporting on a draw that already happened, so it uses the recorded DRAW_SEED.
            #
            # D020: a NEW draw derives its seed from the canonical sampling-frame digest, not
            # from the file's bytes. The historical rule made the seed depend on line endings,
            # so the same worksheet seeded differently on Windows and Linux. This is the only
            # behavioural change; positional row sampling is untouched, and the historical
            # constants above are not recomputed, so the existing sample is unaffected.
            fdigest = frame_digest(ta_rows)
            seed = seed_from(fdigest)
            sample = draw(ta_rows, args.size, seed)
            sheet = build_sheet(sample, load_languages())
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=SHEET_FIELDS)
                w.writeheader()
                w.writerows(sheet)
            print(f"drew {len(sheet)} of {len(ta_rows)} records "
                  f"({len(sheet) / len(ta_rows):.1%}) with seed {seed}")
            print(f"  seed derivation:       {FRAME_DIGEST_RULE} (D020)")
            print(f"  sampling-frame digest: {fdigest}")
            print(f"  worksheet SHA-256:     {sha}  (file identity, not the seed source)")
            print(f"  -> {path.as_posix()}")
            print("  The recorded decision is NOT in this file. Fill your_decision, "
                  "your_reason_code and your_notes, then run --score.")
            return 0

        if not path.exists():
            raise PipelineError(f"{path.name} not found. Run --draw first.")
        result = score(read_csv(path), ta_rows)
    except PipelineError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    out = VALIDATION_DIR / "screening_verification.md"
    out.write_text(render(result, sha, current_frame=frame_digest(ta_rows)), encoding="utf-8")
    if sha != DRAW_SHA:
        print("WARNING: the worksheet has changed since the sample was drawn.", file=sys.stderr)
        print(f"  worksheet at the draw: {DRAW_SHA} (seed {DRAW_SEED})", file=sys.stderr)
        print(f"  worksheet now        : {sha}", file=sys.stderr)
        print("  The draw seed reported is the recorded one; it is not re-derived from this "
              "file. Agreement is measured against the decisions recorded now. Scoring "
              "continues.", file=sys.stderr)
    print(f"agreement {result['agreed']}/{result['n']} ({result['rate']:.1%})  "
          f"verdict={result['verdict']}")
    if result["sweeps"]:
        print(f"  asymmetry rule triggered for: {', '.join(result['sweeps'])}", file=sys.stderr)
    print(f"  -> results/validation/{out.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
