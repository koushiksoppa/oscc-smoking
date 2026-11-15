"""Final end-semester presentation.

    python -m scripts.reporting.build_final_presentation

Writes results/final_submission/Final_Research_Project_Presentation.pptx.

Reuses the OOXML writer in `build_presentation` — a .pptx is a ZIP of XML parts, and no third-party
presentation library is available or authorised — and supplies a different deck. Every figure quoted
on a slide is asserted against `scripts.screening.prisma.gather()` in
`tests/test_final_presentation.py`, so a slide cannot drift from the data it describes.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts.common.config import ROOT
from scripts.reporting.build_presentation import ACCENT, AMBER, GREEN, INK, MUTED, RED, build

OUT = ROOT / "results" / "final_submission" / "Final_Research_Project_Presentation.pptx"


def slides() -> list[dict]:
    B = INK
    return [
        {"kind": "title",
         "title": "Smoked Tobacco and Oral Cavity Squamous Cell Carcinoma",
         "lines": [
             "Is smoked tobacco use associated with an increased risk of squamous cell "
             "carcinoma of the oral cavity?",
             "",
             "A systematic review and meta-analysis project",
             "Soppa Shiva Sai Koushik  ·  14 November 2026"],
         "foot": "Interim project report: a developed and validated research pipeline with "
                 "preliminary record-processing results. No study included; no pooled estimate."},

        {"title": "Background and rationale",
         "lead": "Why this question, and why the method matters as much as the answer",
         "bullets": [
             ("Oral cavity SCC carries a high burden in South and South-East Asia", 0, B, False),
             ("The relevant exposure is broader than cigarettes: bidis, chuttas, cigars, pipes, "
              "reverse smoking", 0, B, False),
             ("Oral cavity is NOT interchangeable with oropharynx — different HPV-related "
              "aetiology, so pooling across sites dilutes the association", 0, B, False),
             ("Methodological gap: where automated screening is used, a worksheet rarely records "
              "whether a human judged each record or accepted a machine output in bulk",
              0, ACCENT, True),
             ("Those are different bodies of evidence, and they look identical in the file",
              1, MUTED, False)]},

        {"title": "Research objectives",
         "lead": "Eight infrastructure objectives achieved; the scientific objective is not",
         "bullets": [
             ("O1–O2  Recorded protocol; checksum-gated acquisition", 0, GREEN, False),
             ("O3–O4  Deduplication with no silent merging; screening that separates "
              "suggestion from decision", 0, GREEN, False),
             ("O5–O6  Blinded verification with a reproducible frame; 93-field extraction "
              "schema", 0, GREEN, False),
             ("O7–O8  Meta-analytic computation with declared limits; reproducible outputs",
              0, GREEN, False),
             ("O9  Produce a pooled estimate answering the review question", 0, RED, True),
             ("NOT ACHIEVED — blocked on reviewer work and open protocol decisions",
              1, RED, False)]},

        {"title": "Systematic review methodology",
         "bullets": [
             ("PRISMA 2020 · PRISMA-S · MOOSE · Cochrane Handbook v6.5", 0, B, False),
             ("Protocol committed 29 Oct 2026; screening records 1 Nov 2026 — specified in "
              "advance", 0, B, False),
             ("19 adopted decisions, 4 proposed, 22 open questions — each dated, with "
              "rationale and scope", 0, ACCENT, True),
             ("Eligibility: human adults · any smoked tobacco (D009) · oral-cavity SCC "
              "confirmed or ≥90% (D008) · case–control and cohort · English",
              0, B, False),
             ("13-code controlled vocabulary; 4 codes restricted to full text because an abstract "
              "cannot support them", 0, B, False)],
         "note": "Not prospectively registered, and the provisional pass preceded registration — "
                 "reported as a protocol deviation."},

        {"title": "Search strategy development",
         "lead": "The executed query is narrower than the protocol it serves — found by auditing it",
         "bullets": [
             ("68 of 194 records use the phrase ‘oral cancer’, which the v1 query does "
              "not require", 0, AMBER, False),
             ("98 of 194 matched the design block only through the single word ‘cohort’",
              0, AMBER, False),
             ("Corrected strategy ADOPTED: D023 removes the study-design block; D024 removes one "
              "dead quoted phrase", 0, GREEN, True),
             ("Per-line validation of all 88 query lines found exactly ONE dead term — "
              "PubMed reported QuotedPhraseNotFound", 0, B, False),
             ("Translations drafted for Embase, Scopus, Web of Science and IndMED; four remain "
              "untested pending access", 0, B, False)],
         "note": "Counts-only interrogation figures (8,190 / 5,008 / 8,195) are NOT search yields: "
                 "no record was retrieved, exported or screened."},

        {"title": "Literature acquisition",
         "bullets": [
             ("One registered search execution: pubmed_v1r — 194 records, unfiltered",
              0, GREEN, True),
             ("958,710 bytes · SHA-256 1d153fa8… · verified against "
              "data/raw/SHA256SUMS", 0, B, False),
             ("194 of 194 parsed; 194 unique PMIDs recovered", 0, B, False),
             ("191 English · 2 Chinese · 1 English+Portuguese — retrieved unfiltered "
              "by decision (D013), excluded at screening with a recorded reason", 0, B, False),
             ("42 of 194 (21.6%) carry no MeSH indexing at all — the most recent records",
              0, AMBER, False),
             ("pubmed_v1 (138 records) is LOST, recorded as export_missing, never substituted",
              0, RED, False)]},

        {"title": "Deduplication and screening results",
         "bullets": [
             ("Identifier hierarchy: normalised DOI → PMID → exact title+author+year "
              "fingerprint", 0, B, False),
             ("Near-identical titles flagged needs_review and NEVER merged automatically",
              0, ACCENT, True),
             ("194 records in → 0 duplicates → 0 needing review → 194 unique reports",
              0, GREEN, False),
             ("Automated classification: 109 provisional exclusions, 85 carried forward",
              0, AMBER, False),
             ("Reasons: 63 wrong outcome · 33 wrong design · 10 review · 2 not "
              "English · 1 population — these are SUGGESTED codes, not reviewer "
              "judgements", 0, RED, False)]},

        {"title": "PRISMA progress",
         "lead": "Formal and provisional counts are reported separately, never summed",
         "image": "record_status.png", "ratio": 0.40,
         "bullets": [
             ("194 identified → 194 unique → 109 / 85 provisional → "
              "0 FORMALLY screened → 0 included", 0, B, False)],
         "note": "0 of 194 independently adjudicated; 0 of 120 verification cells complete. "
                 "The zeros show the gates working, not a search that found nothing."},

        {"title": "Research pipeline architecture",
         "image": "pipeline_architecture.png", "ratio": 0.60,
         "note": "Colour is assigned from the repository at build time, so the diagram cannot drift "
                 "from what the code actually does. Three gates refuse in sequence."},

        {"title": "Data extraction framework",
         "bullets": [
             ("93 documented fields: 34 study-level + 47 estimate-level + 12 risk-of-bias",
              0, GREEN, True),
             ("Every field traced to config/extraction.yaml; blank workbook regenerates "
              "deterministically", 0, B, False),
             ("ZERO data rows — data/extraction/ does not exist, which is the correct state",
              0, RED, False),
             ("3 fields marked unresolved: tool/domain/judgement (P023). Comparator and "
              "contrast settled by D025 and D026", 0, AMBER, False),
             ("Risk-of-bias instrument NOT chosen — domain names and judgement categories "
              "deliberately absent, never invented", 0, ACCENT, True)]},

        {"title": "Meta-analysis methodology",
         "lead": "Implemented and tested; never run on research data, because no estimate exists",
         "bullets": [
             ("OR / RR / HR on the log scale; three SE routes — from CI, from 2×2 counts, "
              "as reported", 0, B, False),
             ("Fixed-effect and random-effects inverse-variance; DerSimonian–Laird and REML "
              "estimators of τ²", 0, B, False),
             ("Cochran's Q, I², τ², prediction intervals (k≥3), leave-one-out "
              "sensitivity analysis", 0, B, False),
             ("Zero cells REFUSED — no silent continuity correction; the choice stays with the "
              "reviewer", 0, ACCENT, True),
             ("Correlated estimates from one study cannot be pooled as independent: selection is "
              "required and refuses to guess", 0, ACCENT, True),
             ("Subgroups: 2 of 5 ready (product type, alcohol adjustment); 3 blocked on P014–"
              "P022, region scheme and P023", 0, AMBER, False)],
         "note": "No pooled estimate, forest plot of research data, I² or p-value exists. "
                 "Publication bias has NOT been assessed."},

        {"title": "Software validation and technical results",
         "bullets": [
             ("670 tests passed, 1 skipped by design, from 671 collected (the lost export's raw-source test)",
              0, GREEN, True),
             ("Record conservation: 194 in → 194 unique out → 0 lost", 0, B, False),
             ("Raw-export checksum verified · SHA-256 recorded and verified for 3 screening files · "
              "5 of 5 verification-seed constants unchanged", 0, GREEN, False),
             ("Deterministic generation confirmed by rebuilding to a clean path and comparing "
              "bytes", 0, B, False),
             ("Python 3.14.7 · pyyaml 6.0.3 · pytest 9.1.1 · scipy 1.18.1 · "
              "matplotlib 3.11.2 — pandas is NOT used anywhere", 0, B, False)]},

        {"title": "Limitations and unresolved decisions",
         "bullets": [
             ("One database; the executed query is narrower than its own eligibility criteria",
              0, RED, True),
             ("0 of 194 independently adjudicated · 0 of 120 verification cells complete",
              0, RED, False),
             ("0 full texts retrieved · 0 studies included · 0 estimates · "
              "0 risk-of-bias assessments · 0 pooled analyses", 0, RED, False),
             ("Automated suggestions unvalidated on this corpus; a false exclusion is invisible, "
              "a false inclusion is caught at full text", 0, AMBER, False),
             ("P007 open (no access verified) · P014–P022 scope · P023 instrument "
              "· not prospectively registered", 0, AMBER, False),
             ("REML externally unvalidated; no HKSJ, Mantel–Haenszel, Peto, meta-regression "
              "or dose–response", 0, AMBER, False)]},

        {"title": "Current scientific contribution",
         "lead": "What this reporting period actually delivered",
         "bullets": [
             ("A specified protocol: 19 adopted decisions, each with rationale, consequences and "
              "explicit scope", 0, GREEN, False),
             ("Checksum-gated acquisition that can record a lost export honestly rather than "
              "substituting for it", 0, GREEN, False),
             ("A screening model in which suggestion and judgement are separated at field level "
              "and enforced at three independent points in code", 0, GREEN, True),
             ("A 93-field extraction schema and a tested meta-analysis implementation with its "
              "limitations declared", 0, GREEN, False),
             ("670 tests, including regression tests that encode specific defects found and fixed",
              0, GREEN, False),
             ("A worksheet of 194 completed rows yields a formal screening count of ZERO — "
              "uncomfortable, and correct", 0, ACCENT, True)]},

        {"title": "Conclusion and future work",
         "bullets": [
             ("Researcher decisions first: P007 databases · P014–P022 scope · P023 "
              "instrument · P006 registration", 0, B, False),
             ("Then execute the adopted search and register each export under D011", 0, B, False),
             ("Then the reviewer's own work, which cannot be generated: adjudication, 120 "
              "verification cells, full texts, extraction, appraisal", 0, ACCENT, True),
             ("Do NOT adjudicate the current 194 yet — they come from the superseded query "
              "and the record set will change", 0, AMBER, True),
             ("Integrity properties usually asserted in a methods section have been made "
              "properties of a system: the pipeline refuses to produce an estimate it cannot "
              "justify", 0, GREEN, True)],
         "note": "This is an interim systematic review and meta-analysis project — not a "
                 "completed review, and not a completed meta-analysis."},
    ]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    result = build(slides(), Path(args.out))
    print(f"  presentation -> {args.out}")
    print(f"  {result['slides']} slides, {result['media']} embedded figures, "
          f"{result['bytes']:,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
