# Working conventions for this repository

This is a live systematic review and meta-analysis, not a demonstration project. Its outputs are
intended to support an academic manuscript. Read `docs/protocol/provenance_rules.md` before touching
anything; this file is the short operational summary.

## Standing prohibitions

1. **Never fabricate.** No invented citations, study characteristics, effect estimates, screening
   decisions, risk-of-bias judgements, statistics or search dates. Missing stays missing and is flagged.
2. **No synthetic data in `data/`.** Tests use MEDLINE format fragments and structural stubs with no
   bibliographic content, in pytest temp directories only (D007, D028). Provenance rule 6 is
   retained in full, with no carve-out for labelled demonstration artefacts.
3. **`data/raw/` is immutable.** Never edit, re-save, re-encode or recreate a raw export. The v1
   export is lost; it is **not** recreated or substituted. Any new retrieval is a separate execution
   with its own registry entry, date, count and checksum (D005, D011). Filenames are never reused.
   Never edit a recorded count to make validation pass — a disagreement is the finding.
4. **No commits, pushes or installs without explicit authorisation.** Git identity is currently unset.
   Never rewrite history or force-push. `main` is the working branch.
5. **No pooled analysis before the gate** in provenance rule 13 is met and the SAP is approved.
6. **Automated tooling is not a reviewer.** Screening and risk-of-bias decisions belong to the human
   reviewer (D010). Automated output goes in a `suggestion` field, never a `decision` field.
   Every recorded decision carries a `decision_basis` of `adopted_from_suggestion` or
   `independently_adjudicated`, and the two are never reported as one number. **All 194 current
   title/abstract decisions are `adopted_from_suggestion`; 0 are `independently_adjudicated`**, so
   the title/abstract outcome is a proposal awaiting adjudication, not a screening result.
7. **No causal language** from observational associations.
8. Material methodological decisions are escalated to the reviewer, not made silently, and are
   recorded in `docs/decisions/decision_log.md`.

## Layout

```
data/raw/        immutable exports + SHA256SUMS (append-only)
data/processed/  script-generated datasets
data/extraction/ study-level extraction data
docs/            protocol, search versions, decisions, methods, data dictionary
scripts/         common | acquisition | validation | dedup | screening | extraction | analysis
data/screening/  screening worksheets — TRACKED, not regenerable, unlike data/processed/
data/extraction/ extraction tables   — TRACKED, same reason
results/         validation reports, tables, figures — generated, never hand-edited
tests/
config/sources.yaml   one entry per database x search EXECUTION (D011)
```

A registry entry carries `execution` (historical / re_execution / new), `status`
(export_missing / awaiting_registration / registered), the `filters_applied` actually used, and
`count_source` for `expected_records`. An entry exists only when an export exists, or to record that
one is missing — never for a merely drafted search.

## Pipeline

```
raw export -> verify_raw (count + checksum gate) -> parse_citations -> validate_citations
           -> deduplicate -> screening -> extraction -> [risk of bias] -> synthesis -> [reporting]
```

Stages in brackets are not built. Every other stage is built and tested. Acquisition, validation
and deduplication have been run on real data. A **title/abstract pass has been recorded** for all
194 reports, but every one of those decisions was adopted from an automated suggestion and none has
been independently adjudicated, so it counts as a provisional outcome rather than a completed
screening stage. **Full-text retrieval, extraction, appraisal and synthesis have not run**, so no
study is yet judged eligible and no pooled estimate exists. Screening, extraction, appraisal and the
judgements behind them are the human reviewer's (D010) and cannot be generated.

Each stage re-verifies provenance before reading, writes a report to `results/validation/`, and
exits non-zero on missing, altered or invalid input. Three gates refuse in sequence: extraction
needs full-text includes, synthesis needs extracted estimates, and the analysis CLI rejects
anything marked synthetic.

Stage details: `docs/methods/pipeline.md`. Guides: `intake_checklist.md`, `screening.md`,
`extraction.md`, `analysis_validation.md`.

## Conventions

- Python 3.14 in `.venv`; stdlib only so far (`csv`, `json`, `hashlib`) plus `pyyaml` and `pytest`.
  Dependencies are added per stage and pinned in `requirements.txt`.
- Run modules with `-m` from the repository root: `.venv/Scripts/python -m scripts.acquisition.verify_raw --source pubmed_v1r`.
- Errors that violate a provenance rule raise `PipelineError` and are never caught silently.
- Identifiers: `record_id` → `report_id` → `study_id` → `estimate_id` (D004). The unit of analysis is
  `study_id`; a `study_id` may appear at most once per analysis.
- Inspecting a file and declaring it the research input are separate acts: `--report-only` writes a
  proposal, `--register` writes the authoritative checksum.

## Screening provenance

Two acts are distinguished everywhere, in the data and in the reporting:

| `decision_basis` | Meaning |
|---|---|
| `adopted_from_suggestion` | The reviewer accepted an automated suggestion without judging the record individually. The decision **and** its reason code equal what was suggested. This is **not** independent adjudication. |
| `independently_adjudicated` | The reviewer judged the record from its own evidence. A suggestion may exist; the decision may agree with it or differ from it. |

A row counts as **independently adjudicated** only when all five of these are recorded:
`decision`, `reviewer`, `screened_date`, `decision_basis = independently_adjudicated`, and
`adjudicated_date`. A basis recorded without a decision is rejected, so the decision itself is one
of the five requirements and not an assumption.
The separate `adjudicated_date` exists so that flipping the basis on a row already carrying the
bulk-adoption reviewer and date cannot convert a provisional record into a formal one without
dating the new act. One shared function, `worksheet.adjudication_problems`, applies these rules for
the validator, the full-text carry-forward and the PRISMA gatherer, so the three cannot disagree.

`validate_screening --stage <ta|ft> --final` **rejects** a stage that is incomplete (any report
unscreened or left `unresolved`) and **rejects any row whose basis is `adopted_from_suggestion`**.
Without `--final` both are warnings, so work in progress is not blocked.

The PRISMA flow separates the two. The **formal** flow counts independently adjudicated decisions
only; adopted decisions appear in a **provisional** section explicitly headed as not part of the
flow. Full-text rows are attributed to one of five mutually exclusive states, decided per row
rather than by subtraction: `ft_sought` (source is a valid, adjudicated include),
`ft_provisional_sought` (valid include, adopted basis), `ft_invalid_source` (the source row fails
validation), `ft_ineligible_source` (source is valid but no longer an include) and
`ft_unattributed` (no such report upstream). These identities must hold or the run fails:

```
ta_excluded + ta_included + ta_unresolved                         == ta_screened
ta_adjudicated + ta_adopted + ta_invalid + ta_unscreened          == ta_total
ft_sought + ft_provisional_sought + ft_invalid_source
          + ft_ineligible_source + ft_unattributed                == ft_rows
```

The full list of identities is in `docs/methods/screening.md`.

A **stale full-text row** — one whose source record has left the include set or the source data —
is counted in whichever of those states explains it and is reported, **never silently deleted**;
`worksheet --refresh` refuses outright when a row holding recorded work has left the source set.

A **blinded verification sample** exists at `data/screening/verification_sample.csv`: 40 of the 194
records (20.6%), with the recorded decision withheld. It has three response columns, so **120
response cells, of which 0 are currently completed**. Until it is filled in and scored, no
agreement rate, kappa or acceptance outcome exists.

Two seed-derivation rules exist and are never conflated. The existing sample was drawn under the
historical rule `file_bytes_crlf_v1`, which hashed the worksheet **file's bytes** as they stood on
disk before the M1 migration:

```
rule                           file_bytes_crlf_v1
worksheet SHA-256 at the draw  5938922a529a7f7318824f4216b4b9ab05b920a14def7c15e72c15ea2a6076eb
seed (first 8 hex digits)      1496879658
sampling-frame digest          37cc07e64054ef938229fbecec5f7da70f4c9ae419aae9f79b04d642574209ad
draw date                      UNVERIFIED
```

That seed reproduces the committed 40 records exactly, from either the pre- or post-migration
worksheet. Hashing the **current** worksheet's bytes gives seed `2793808711`, which selects a
different sample; the digest above is the one to audit against, and the draw date is not inferred
from any commit date.

**Later draws use `ordered_report_ids_v1` (D020, adopted 2026-11-10)**: the seed comes from a
canonical digest of the sampling frame — the ordered `report_id` sequence, UTF-8, NFC, LF-separated,
rule version inside the payload — which is invariant to line endings and to later columns, and
changes when the units or their order change. It is **not** applied retroactively: re-deriving the
existing sample under any other rule would select a different 40. Full specification and the
reproducible byte layout: `docs/methods/screening.md`.

D016–D019 record these rules and are **Proposed — awaiting the reviewer's adoption**. They are
implemented in code but not adopted as protocol.

## Current state

`pubmed_v1r` (194 records, the v1 query re-run unfiltered) is registered, parsed, validated and
deduplicated. `pubmed_v1`, the original 138-record execution, is lost and recorded as
`export_missing`.

**A title/abstract pass is recorded for all 194 reports, and none of it is independently
adjudicated.** 194 of 194 rows carry a decision, 0 are unscreened and 0 fail validation, but all
194 have `decision_basis = adopted_from_suggestion` and 0 have `independently_adjudicated`. The
formal PRISMA flow therefore reports **0 screened, 0 excluded, 0 taken forward**; the provisional
section reports 194 decisions — 109 excluded with a reason, 85 taken forward, 0 unresolved.
`validate_screening --stage ta --final` fails on this state, as it should.

The full-text worksheet exists with those 85 rows. All 85 are `ft_provisional_sought` and
`ft_sought` is 0; **every reviewer field is empty** — nothing has been retrieved or assessed. The
blinded verification sample is drawn but unanswered (0 of 120 response cells). A decision-log entry
describing how the title/abstract pass was conducted is still outstanding and is needed for PRISMA
item 8; D016–D019 record the provenance rules but are Proposed, not adopted.

Settled decisions are **D001–D015**, **D020** (sampling-frame digest for verification draws),
**D022** (bounded supplementary grey-literature searching, 2026-11-13), **D023** (no study-design
block in the primary search, 2026-11-13, resolving P013), **D024** (removal of an ineffective quoted
phrase, 2026-11-14) and **D025–D029** (reference group, exposure contrast, search dates, synthetic
content, count residual; all 2026-11-14) — **24 adopted**.
D016–D019 are
**Proposed** (suggestion/adjudication separation, suggested reason codes, full-text basis,
formal-versus-provisional PRISMA reporting). **D021 is not in the register**: the label is used in
project documents for the drafted blinded-verification acceptance methodology, which is why the
grey-literature decision took D022.
Open: P006 (PROSPERO), P007 (other databases), P014–P022 (anatomical and histological scope)
and P023 (risk-of-bias instrument) — **12 open**. **P013 is
resolved by D023**: the primary search carries **no study-design block**, so the corrected
PubMed strategy stands at 8,190 records rather than 5,008 — counts-only interrogation figures
of 2026-11-12, **not search yields** — and the number of additional eligible studies recovered is unknown and may be zero. The v2 draft is
superseded; the corrected strategy is drafted and syntax-validated but **not executed**. The stage assignment of exclusion reasons in
`config/screening.yaml` is still a proposal awaiting endorsement, and no identifier yet covers
whether populations restricted to premalignant oral lesions are in scope.
