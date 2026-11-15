"""PRISMA 2020 flow counts, computed from the datasets that exist.

    python -m scripts.screening.prisma

Every number is derived from real data or printed as `<pending>`. Nothing is estimated, and a
stage that has not been done produces `<pending>` rather than a zero — zero and "not yet done"
are different claims, and conflating them would misreport the review's progress.

Consistency identities are checked and reported; a violation is an error, because the flow
diagram must reconcile.
"""
from __future__ import annotations

import csv
import sys
from collections import Counter

from scripts.common.config import PROCESSED_DIR, VALIDATION_DIR, PipelineError, load_sources
from scripts.screening import worksheet
from scripts.screening.vocabulary import (ADJUDICATED, ADOPTED, EXCLUDE, FT, INCLUDE, TA,
                                          UNRESOLVED, load_vocabulary)

PENDING = "<pending>"


def read(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def gather() -> dict:
    """Collect every count the flow needs, marking absent stages as pending."""
    flow: dict = {"per_source": {}, "notes": []}

    cit_dir = PROCESSED_DIR / "citations"
    identified = 0
    for source in load_sources():
        if source.export_missing:
            flow["per_source"][source.source_id] = (
                f"{PENDING} — export missing; contributes no records unless recovered (D005)")
            continue
        path = cit_dir / f"{source.source_id}_citations.csv"
        if not path.exists():
            flow["per_source"][source.source_id] = f"{PENDING} — not yet parsed"
            continue
        n = len(read(path))
        flow["per_source"][source.source_id] = n
        identified += n
    flow["identified"] = identified if identified else PENDING

    index_path = PROCESSED_DIR / "dedup" / "report_index.csv"
    if index_path.exists():
        index = read(index_path)
        unique = len({r["report_id"] for r in index})
        flow["duplicates_removed"] = len(index) - unique
        flow["unique_reports"] = unique
    else:
        flow["duplicates_removed"] = flow["unique_reports"] = PENDING

    ta_path = worksheet.worksheet_path(TA)
    if ta_path.exists():
        ta = read(ta_path)
        flow["ta_total"] = len(ta)

        # The flow reports what was *done*, not what was *proposed*. A decision adopted from an
        # automated suggestion records what the tooling proposed and cannot satisfy a decision
        # field (D010), so it is counted in a provisional block that sits outside the flow.
        # Only independently adjudicated decisions reach the formal cells.
        # A claim of adjudication is not evidence of one. The same row-level check the
        # validator and the full-text carry-forward use decides what counts here, so all three
        # layers agree on what "adjudicated" means. A decided row that fails it is neither
        # formal nor provisional: it is counted as invalid and stays visible in the identity.
        vocab = load_vocabulary()

        def basis(r):
            return (r.get("decision_basis") or "").strip()

        # Validity is a property of any row, decided or not: a blank row is valid, it simply
        # carries no decision. Counting it as invalid would misreport an untouched record.
        all_valid = [r for r in ta if not worksheet.adjudication_problems(r, vocab)]
        decided = [r for r in ta if (r.get("decision") or "").strip()]
        valid = [r for r in all_valid if (r.get("decision") or "").strip()]
        adjudicated = [r for r in valid if basis(r) == ADJUDICATED]
        adopted = [r for r in valid if basis(r) == ADOPTED]
        flow["ta_invalid"] = len(decided) - len(valid)
        ta_rows_by_id = {r["report_id"]: r for r in ta}          # every row, valid or not
        ta_valid_basis = {r["report_id"]: basis(r) for r in all_valid}
        ta_valid_decision = {r["report_id"]: (r.get("decision") or "").strip()
                             for r in all_valid}

        formal = Counter((r.get("decision") or "").strip() for r in adjudicated)
        flow["ta_screened"] = len(adjudicated)
        flow["ta_excluded"] = formal.get(EXCLUDE, 0)
        flow["ta_included"] = formal.get(INCLUDE, 0)
        flow["ta_unresolved"] = formal.get(UNRESOLVED, 0)
        flow["ta_unscreened"] = len(ta) - len(decided)
        flow["ta_reasons"] = Counter((r.get("reason_code") or "").strip() for r in adjudicated
                                     if (r.get("decision") or "").strip() == EXCLUDE)
        flow["ta_adjudicated"] = len(adjudicated)
        flow["ta_adopted"] = len(adopted)

        prov = Counter((r.get("decision") or "").strip() for r in adopted)
        flow["prov_total"] = len(adopted)
        flow["prov_excluded"] = prov.get(EXCLUDE, 0)
        flow["prov_included"] = prov.get(INCLUDE, 0)
        flow["prov_unresolved"] = prov.get(UNRESOLVED, 0)
        flow["prov_reasons"] = Counter((r.get("reason_code") or "").strip() for r in adopted
                                       if (r.get("decision") or "").strip() == EXCLUDE)
    else:
        for k in ("ta_total", "ta_screened", "ta_excluded", "ta_included", "ta_unresolved",
                  "ta_unscreened", "ta_adopted", "ta_adjudicated", "ta_invalid", "prov_total",
                  "prov_excluded", "prov_included", "prov_unresolved"):
            flow[k] = PENDING
        flow["ta_reasons"] = {}
        flow["prov_reasons"] = {}
        ta_rows_by_id = ta_valid_basis = ta_valid_decision = None

    ft_path = worksheet.worksheet_path(FT)
    flow["ft_exists"] = ft_path.exists()
    if ft_path.exists():
        ft = read(ft_path)
        statuses = Counter((r.get("full_text_status") or "").strip() for r in ft)
        counts = Counter((r.get("decision") or "").strip() or "unscreened" for r in ft)
        retrieval_recorded = sum(n for status, n in statuses.items() if status)
        decided = len(ft) - counts.get("unscreened", 0)

        # A report carried forward from an adopted include descends from automated output, so
        # it is not a formal retrieval either. The two are counted separately.
        # `source_ta_decision_basis` is a convenience copy, not evidence. Each row is attributed
        # by looking its report up in the title/abstract worksheet and validating that row. A row
        # whose source is missing or invalid is counted as unattributed rather than quietly
        # dropped, so the total always reconciles.
        if ta_valid_basis is None:
            for k in ("ft_sought", "ft_provisional_sought", "ft_invalid_source",
                      "ft_ineligible_source", "ft_unattributed"):
                flow[k] = PENDING
        else:
            # Five mutually exclusive states, decided per row rather than by subtraction, so
            # each says *why* a report is where it is. A residual would merge them.
            buckets = Counter()
            for r in ft:
                rid = r.get("report_id", "")
                if rid not in ta_rows_by_id:
                    buckets["unattributed"] += 1          # no such report upstream
                elif rid not in ta_valid_basis:
                    buckets["invalid"] += 1               # the source row fails validation
                elif ta_valid_decision.get(rid) != INCLUDE:
                    buckets["ineligible"] += 1            # valid, but no longer an include
                elif ta_valid_basis[rid] == ADJUDICATED:
                    buckets["sought"] += 1
                else:                                     # a valid include is adopted or
                    buckets["provisional"] += 1           # adjudicated; nothing else remains
            flow["ft_sought"] = buckets["sought"]
            flow["ft_provisional_sought"] = buckets["provisional"]
            flow["ft_invalid_source"] = buckets["invalid"]
            flow["ft_ineligible_source"] = buckets["ineligible"]
            flow["ft_unattributed"] = buckets["unattributed"]
        flow["ft_rows"] = len(ft)
        flow["ft_screened"] = decided
        flow["ft_unscreened"] = counts.get("unscreened", 0)
        flow["ft_decided"] = bool(decided)

        # Retrieval and eligibility are separate acts, and an empty retrieval status means
        # nothing has been sought yet - not that every report arrived. Reporting "0 not
        # retrieved" and "all assessed" off empty columns would assert work never done.
        if retrieval_recorded:
            flow["ft_not_retrieved"] = statuses.get("unavailable", 0)
            flow["ft_assessed"] = len(ft) - statuses.get("unavailable", 0)
        else:
            flow["ft_not_retrieved"] = flow["ft_assessed"] = PENDING

        # Likewise a stage holding no decision has no includes and no excludes: it has not
        # been done. "Reports included: 0" there states a finding the data cannot support.
        if decided:
            flow["ft_excluded"] = counts.get(EXCLUDE, 0)
            flow["ft_included"] = counts.get(INCLUDE, 0)
            flow["ft_unresolved"] = counts.get(UNRESOLVED, 0)
            flow["ft_reasons"] = Counter(
                (r.get("reason_code") or "").strip() for r in ft
                if (r.get("decision") or "").strip() == EXCLUDE)
        else:
            for k in ("ft_excluded", "ft_included", "ft_unresolved"):
                flow[k] = PENDING
            flow["ft_reasons"] = {}
    else:
        for k in ("ft_sought", "ft_not_retrieved", "ft_assessed", "ft_excluded", "ft_included",
                  "ft_unresolved", "ft_screened", "ft_unscreened", "ft_provisional_sought",
                  "ft_rows", "ft_unattributed", "ft_invalid_source",
                  "ft_ineligible_source"):
            flow[k] = PENDING
        flow["ft_reasons"] = {}
        flow["ft_decided"] = False

    # study_id is assigned by the reviewer at full text (D004); the pipeline cannot infer it.
    flow["included_studies"] = PENDING
    flow["studies_in_synthesis"] = PENDING
    flow["notes"].append(
        "Included *studies* and studies in synthesis stay pending until the reviewer assigns "
        "study_id, since several reports can describe one population (D004).")
    return flow


def consistency(flow: dict) -> list[str]:
    """Identities the flow must satisfy. Only checked where both sides are known.

    Messages are deliberately ASCII: they are printed to stderr as well as written to a
    UTF-8 report, and a Windows cp1252 console raises UnicodeEncodeError on characters
    such as U+2212 MINUS SIGN - which would crash the run exactly when the flow fails to
    reconcile and the message matters most.
    """
    problems = []

    def known(*keys):
        return all(isinstance(flow.get(k), int) for k in keys)

    if known("identified", "duplicates_removed", "unique_reports"):
        if flow["identified"] - flow["duplicates_removed"] != flow["unique_reports"]:
            problems.append(
                f"identified ({flow['identified']}) minus duplicates removed "
                f"({flow['duplicates_removed']}) does not equal unique reports ({flow['unique_reports']})")
    if known("unique_reports", "ta_total") and flow["unique_reports"] != flow["ta_total"]:
        problems.append(
            f"unique reports ({flow['unique_reports']}) does not equal reports in the title/abstract "
            f"worksheet ({flow['ta_total']})")
    if known("ta_screened", "ta_excluded", "ta_included", "ta_unresolved"):
        if flow["ta_excluded"] + flow["ta_included"] + flow["ta_unresolved"] != flow["ta_screened"]:
            problems.append("title/abstract decisions do not sum to the number screened")
    # Every report is adjudicated, provisionally decided, or not screened - no fourth state.
    if known("ta_adjudicated", "ta_adopted", "ta_invalid", "ta_unscreened", "ta_total"):
        if (flow["ta_adjudicated"] + flow["ta_adopted"] + flow["ta_invalid"]
                + flow["ta_unscreened"]) != flow["ta_total"]:
            problems.append(
                f"adjudicated ({flow['ta_adjudicated']}) plus provisional ({flow['ta_adopted']}) "
                f"plus invalid ({flow['ta_invalid']}) plus not screened "
                f"({flow['ta_unscreened']}) does not equal the worksheet ({flow['ta_total']})")
    if known("ft_sought", "ft_provisional_sought", "ft_invalid_source",
             "ft_ineligible_source", "ft_unattributed", "ft_rows"):
        parts = (flow["ft_sought"] + flow["ft_provisional_sought"] + flow["ft_invalid_source"]
                 + flow["ft_ineligible_source"] + flow["ft_unattributed"])
        if parts != flow["ft_rows"]:
            problems.append(
                f"formal ({flow['ft_sought']}) plus provisional "
                f"({flow['ft_provisional_sought']}) plus invalid source "
                f"({flow['ft_invalid_source']}) plus ineligible source "
                f"({flow['ft_ineligible_source']}) plus unattributed "
                f"({flow['ft_unattributed']}) does not equal the full-text worksheet "
                f"({flow['ft_rows']})")
    # The formal flow counts adjudicated decisions and nothing else.
    if known("ta_screened", "ta_adjudicated") and flow["ta_screened"] != flow["ta_adjudicated"]:
        problems.append(
            f"formal reports screened ({flow['ta_screened']}) does not equal independently "
            f"adjudicated decisions ({flow['ta_adjudicated']}); a provisional outcome has leaked "
            "into the flow")
    if known("prov_excluded", "prov_included", "prov_unresolved", "ta_adopted"):
        if (flow["prov_excluded"] + flow["prov_included"] + flow["prov_unresolved"]
                != flow["ta_adopted"]):
            problems.append("provisional decisions do not sum to the provisional total")
    if known("ta_included", "ft_sought") and flow["ft_sought"] > flow["ta_included"]:
        problems.append(
            f"formal reports sought ({flow['ft_sought']}) exceeds independently adjudicated "
            f"title/abstract includes ({flow['ta_included']})")
    if known("ft_provisional_sought", "prov_included") and (
            flow["ft_provisional_sought"] > flow["prov_included"]):
        problems.append(
            f"provisional full-text rows ({flow['ft_provisional_sought']}) exceed provisional "
            f"title/abstract includes ({flow['prov_included']})")
    if known("ft_assessed", "ft_excluded", "ft_included", "ft_unresolved"):
        if flow["ft_excluded"] + flow["ft_included"] + flow["ft_unresolved"] > flow["ft_assessed"]:
            problems.append("full-text decisions exceed the number assessed")
    if isinstance(flow.get("ft_excluded"), int) and flow["ft_excluded"] != sum(
            flow["ft_reasons"].values()):
        problems.append(
            f"full-text exclusions ({flow['ft_excluded']}) does not equal sum of reason counts "
            f"({sum(flow['ft_reasons'].values())}) — every exclusion needs exactly one reason")
    return problems


def screening_banner(flow: dict) -> str:
    """State screening progress unambiguously.

    Without this, a reader can mistake "0 reports taken forward" for a finding — that nothing was
    eligible — when it means no record has been looked at yet. The two must never be confusable.
    """
    total, screened = flow.get("ta_total"), flow.get("ta_screened")
    if not isinstance(total, int) or not isinstance(screened, int):
        return ("> **SCREENING STATUS: NOT STARTED.** No title/abstract worksheet exists. "
                "Counts below describe the search only.")
    adopted = flow.get("ta_adopted")
    if isinstance(adopted, int) and adopted:
        adjudicated = flow.get("ta_adjudicated")
        adjudicated = adjudicated if isinstance(adjudicated, int) else 0
        recorded = adjudicated + adopted
        return (f"> **SCREENING STATUS: NOT INDEPENDENTLY ADJUDICATED.** {recorded} of {total} "
                f"reports carry a **provisional classification**, of which {adopted} were "
                f"**adopted from an automated suggestion** and only {adjudicated} were "
                f"**independently adjudicated**. Under D010 a suggestion cannot satisfy a decision "
                f"field, so **{adjudicated} reports have been screened by a human reviewer** and "
                "the counts below describe a **proposed** screening outcome, not a completed one."
                + full_text_banner(flow))
    if screened == 0:
        return (f"> **SCREENING STATUS: NOT SCREENED.** 0 of {total} reports have been screened. "
                "Every screening count below is therefore 0 because the work has not been done — "
                "**not** because nothing was eligible. No study has been judged eligible or "
                "ineligible, and no result may be inferred from this table.")
    if screened < total:
        return (f"> **SCREENING STATUS: IN PROGRESS.** {screened} of {total} reports screened, "
                f"{total - screened} awaiting. Counts below are provisional and will change."
                + full_text_banner(flow))
    return (f"> **SCREENING STATUS: TITLE/ABSTRACT COMPLETE.** All {total} reports screened. "
            "Full-text and synthesis stages may still be pending." + full_text_banner(flow))


def full_text_banner(flow: dict) -> str:
    """State full-text progress, or say nothing when there is no full-text worksheet.

    Building the worksheet creates 85 empty rows; without this, a reader meets a table of
    zeros where no report has been looked at. Returns "" for a flow that carries no
    full-text counts, so the title/abstract banner is unchanged when no worksheet exists.
    """
    sought, screened = flow.get("ft_sought"), flow.get("ft_screened")
    if not isinstance(sought, int):
        return ""
    if not isinstance(screened, int) or screened == 0:
        provisional = flow.get("ft_provisional_sought")
        extra = ""
        if isinstance(provisional, int) and provisional:
            extra = (f" A further {provisional} report(s) are **provisionally** sought, descending "
                     "from classifications that have not been independently adjudicated.")
        return (f" **FULL TEXT: NOT ASSESSED.** {sought} report(s) are formally sought for "
                f"retrieval and none has been assessed, so every full-text count below is pending, "
                f"**not** a finding that nothing was eligible.{extra}")
    if screened < sought:
        return (f" **FULL TEXT: IN PROGRESS.** {screened} of {sought} reports assessed; "
                "full-text counts are provisional.")
    return f" **FULL TEXT: COMPLETE.** All {sought} reports assessed."


def render(flow: dict, problems: list[str]) -> str:
    vocab = load_vocabulary()
    v = lambda k: flow.get(k, PENDING)  # noqa: E731
    lines = [
        "# PRISMA 2020 flow — generated counts", "",
        "Generated by `scripts/screening/prisma.py` from the datasets present. `<pending>` means "
        "**the stage has not been done**, which is not the same as zero.", "",
        f"**Reconciles: {'no — see Problems' if problems else 'yes'}**", "",
        screening_banner(flow), "",
        "## Identification", "", "| Item | Count |", "|---|---|",
    ]
    for source_id, n in flow["per_source"].items():
        lines.append(f"| Records identified — `{source_id}` | {n} |")
    lines += [
        f"| **Records identified, total** | **{v('identified')}** |",
        f"| Duplicate records removed | {v('duplicates_removed')} |",
        f"| **Unique reports** | **{v('unique_reports')}** |",
        "", "## Title/abstract screening — formal flow", "",
        "Counts **independently adjudicated decisions only**. A decision adopted from an "
        "automated suggestion cannot satisfy a decision field (D010), so it is reported in the "
        "provisional section below and is **not** part of this flow.", "",
        "| Item | Count |", "|---|---|",
        f"| Reports screened | {v('ta_screened')} |",
        f"| Reports excluded | {v('ta_excluded')} |",
        f"| Reports left unresolved | {v('ta_unresolved')} |",
        f"| **Reports taken forward** | **{v('ta_included')}** |", "",
        "| Reconciliation | Count |", "|---|---|",
        f"| Reports in the worksheet | {v('ta_total')} |",
        f"| … independently adjudicated (counted above) | {v('ta_adjudicated')} |",
        f"| … provisional, awaiting adjudication (not counted above) | {v('ta_adopted')} |",
        f"| … **invalid** — a recorded decision that fails validation (not counted above) | "
        f"{v('ta_invalid')} |",
        f"| … not yet screened | {v('ta_unscreened')} |", "",
    ]
    if flow["ta_reasons"]:
        lines += ["### Title/abstract exclusions by reason", "", "| Reason | Count |", "|---|---|"]
        lines += [f"| `{c}` | {n} |" for c, n in sorted(flow["ta_reasons"].items())]
        lines.append("")
    lines += [
        "## Provisional screening outcome — NOT part of the PRISMA flow", "",
        "Decisions proposed by automated tooling and adopted without individual adjudication. "
        "They are **proposals awaiting human adjudication**, not screening results, and must not "
        "be reported as flow counts. A record leaves this section the moment it is independently "
        "adjudicated; its original suggestion stays recorded in the worksheet.", "",
        "| Item | Count |", "|---|---|",
        f"| Records with a provisional decision | {v('prov_total')} |",
        f"| … provisionally excluded | {v('prov_excluded')} |",
        f"| … provisionally taken forward | {v('prov_included')} |",
        f"| … provisionally unresolved | {v('prov_unresolved')} |", "",
    ]
    if flow.get("prov_reasons"):
        lines += ["### Provisional exclusion reasons", "", "| Reason | Count |", "|---|---|"]
        lines += [f"| `{c}` | {n} |" for c, n in sorted(flow["prov_reasons"].items())]
        lines.append("")
    lines += [
        f"| Full-text rows carried from provisional includes | "
        f"{v('ft_provisional_sought')} |",
        f"| Full-text rows whose source record fails validation | "
        f"{v('ft_invalid_source')} |",
        f"| Full-text rows whose source is valid but no longer an include | "
        f"{v('ft_ineligible_source')} |",
        f"| Full-text rows with no source record at all | {v('ft_unattributed')} |",
        f"| Full-text rows in the worksheet | {v('ft_rows')} |", "",
        "## Full-text screening — formal flow", "", "| Item | Count |", "|---|---|",
        f"| Reports sought for retrieval | {v('ft_sought')} |",
        f"| … not yet assessed | {v('ft_unscreened')} |",
        f"| Reports not retrieved | {v('ft_not_retrieved')} |",
        f"| Reports assessed for eligibility | {v('ft_assessed')} |",
        f"| Reports excluded | {v('ft_excluded')} |",
        f"| Reports left unresolved | {v('ft_unresolved')} |",
        f"| **Reports included** | **{v('ft_included')}** |", "",
        "### Full-text exclusions by reason", "",
        "Every reason in the controlled vocabulary is listed so that a zero is visible as a zero.",
        "", "| Reason | Count |", "|---|---|",
    ]
    # A stage with decisions recorded has real zeros; one with none has not been done.
    decided = flow.get("ft_decided", flow.get("ft_exists"))
    for code in vocab.codes(FT):
        # A stage that exists but recorded no exclusions of this kind is a real zero; a stage
        # that has not run is pending. Printing 0 for the latter would misreport progress.
        n = flow["ft_reasons"].get(code, 0) if decided else PENDING
        lines.append(f"| `{code}` | {n} |")
    lines += [
        "", "## Included", "", "| Item | Count |", "|---|---|",
        f"| Reports of included studies | {v('ft_included')} |",
        f"| **Studies included in the review** (`study_id`) | {v('included_studies')} |",
        f"| Studies included in quantitative synthesis | {v('studies_in_synthesis')} |", "",
    ]
    if problems:
        lines += ["## Problems", ""] + [f"- {p}" for p in problems] + [""]
    lines += ["## Notes", ""] + [f"- {n}" for n in flow["notes"]] + [""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    try:
        flow = gather()
    except PipelineError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    problems = consistency(flow)
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    path = VALIDATION_DIR / "prisma_counts.md"
    path.write_text(render(flow, problems), encoding="utf-8")

    print(f"identified={flow['identified']}  duplicates={flow['duplicates_removed']}  "
          f"unique_reports={flow['unique_reports']}")
    print(f"ta_screened={flow['ta_screened']}  ta_included={flow['ta_included']}  "
          f"ft_included={flow['ft_included']}  studies={flow['included_studies']}")
    print(f"-> results/validation/{path.name}")
    if problems:
        print(f"RECONCILIATION FAILED ({len(problems)}):", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
