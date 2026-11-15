# Smoked Tobacco and Oral Cavity Squamous Cell Carcinoma

**A systematic review protocol, reproducible review infrastructure, and interim study-selection report.**

> **Research question.** Is smoked tobacco use associated with an increased risk of squamous cell
> carcinoma of the oral cavity?

> **Status, stated plainly.** This repository contains a specified protocol, a validated and tested
> review and meta-analysis implementation, and a provisional study-selection record. **No systematic
> review has been completed and no meta-analysis has been performed.** No study has been judged
> eligible at full text, no datum has been extracted, no risk of bias has been appraised, and no
> pooled clinical estimate exists. See [Research status](#9-research-status-and-limitations).

---

## 1. Research objectives

| # | Objective | Status |
|---|---|---|
| O1 | Specify a review protocol as explicit, dated, individually scoped decisions | **Achieved** — 24 adopted |
| O2 | Checksum-gated acquisition that detects any alteration of a raw export | **Achieved** |
| O3 | Deduplication with an explicit identifier hierarchy and no silent merging | **Achieved** |
| O4 | A screening workflow that structurally separates machine suggestion from human decision | **Achieved** |
| O5 | A reproducible blinded verification sample with a canonical sampling frame | **Achieved (drawn, unanswered)** |
| O6 | A documented extraction schema with header-only templates | **Achieved** — 93 fields |
| O7 | A meta-analysis implementation with refusal gates, validated against published formulas | **Achieved** |
| O8 | Reproducible report, presentation and figure generation | **Achieved** |
| O9 | **Answer the research question** | **Not achieved** — requires the reviewer's own screening, extraction and appraisal |

## 2. Methodology

Reporting follows **PRISMA 2020**, **PRISMA-S** for the search, **MOOSE** for observational
synthesis, and the **Cochrane Handbook v6.5** for statistical method.

The review's governing principle is that **an automated suggestion can never satisfy a decision
field.** Every screening row records a `decision_basis` of either `adopted_from_suggestion` or
`independently_adjudicated`, and the two are never reported as one number. The PRISMA flow counts
independently adjudicated decisions only; adopted suggestions are reported separately and explicitly
outside the flow.

Three gates refuse in sequence: extraction requires full-text includes, synthesis requires extracted
estimates, and the analysis command rejects any row marked synthetic.

**Eligibility (PECO).** Human adults; any smoked tobacco (cigarettes, bidis, cigars, pipes, other
combusted products — smokeless tobacco and betel quid are treated as confounders, not exposures);
never-smoker reference for the primary analysis with study-defined non-smoker references in a
prespecified sensitivity analysis; oral-cavity cancer with squamous histology confirmed or a stated
majority of at least 90%. Case–control and cohort designs. Anatomical subsite definitions remain
open (see limitations).

## 3. Repository structure

```
config/         sources.yaml (one entry per database x search execution), screening.yaml, extraction.yaml
data/raw/       immutable exports + SHA256SUMS (append-only, line-ending conversion disabled)
data/screening/ screening worksheets and the blinded verification sample (tracked, not regenerable)
docs/protocol/  provenance rules, eligibility criteria, anatomical and histological scope
docs/decisions/ the dated decision register
docs/methods/   pipeline, screening, extraction, analysis validation, search strategy
docs/search/    search versions, database translations, manual validation log
docs/reports/   report, manuscript, supplementary and presentation sources
scripts/        common | acquisition | validation | dedup | screening | extraction | analysis | reporting | visualization
tests/          671 tests
results/        validation reports, figures, queues, final deliverables
```

Script-generated datasets under `data/processed/` are deliberately **not** published: they are
regenerable from the tracked raw export, and the pipeline refuses stale derived data.

## 4. Technology and dependencies

Python **3.14**, standard library wherever possible. Four pinned direct dependencies:

```
pyyaml==6.0.3          # configuration
pytest==9.1.1          # test suite
scipy==1.18.1          # chi2, normal and t distributions; linregress
matplotlib==3.11.2     # figures, and PDF typesetting
```

NumPy is deliberately not pinned — no module imports it directly; it arrives transitively. DOCX and
PPTX are written as raw OOXML with the standard library's `zipfile`, so no document library is
required.

## 5. Installation

```bash
git clone https://github.com/koushiksoppa/oscc-smoking.git
cd oscc-smoking
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt     # Windows
# .venv/bin/python -m pip install -r requirements.txt       # Linux / macOS
```

## 6. Running the pipeline

Every stage is a module, run with `-m` from the repository root. Each re-verifies provenance before
reading, writes a report to `results/validation/`, and exits non-zero on missing, altered or invalid
input.

```bash
.venv/Scripts/python -m scripts.acquisition.verify_raw --source pubmed_v1r --report-only
.venv/Scripts/python -m scripts.acquisition.parse_citations --source pubmed_v1r
.venv/Scripts/python -m scripts.validation.validate_citations --source pubmed_v1r
.venv/Scripts/python -m scripts.dedup.deduplicate
.venv/Scripts/python -m scripts.screening.validate_screening --stage ta
.venv/Scripts/python -m scripts.screening.prisma
```

`--report-only` inspects and proposes; `--register` writes the authoritative checksum. Inspecting a
file and declaring it the research input are deliberately separate acts.

Regenerating the deliverables:

```bash
.venv/Scripts/python -m scripts.reporting.build_manuscript --source docs/reports/official_systematic_review_and_meta_analysis_report.md --stem Official_Systematic_Review_and_Meta_Analysis_Report --outdir results/final_submission
.venv/Scripts/python -m scripts.reporting.build_final_presentation
.venv/Scripts/python -m scripts.reporting.build_report_figures
.venv/Scripts/python -m scripts.reporting.build_workbook
```

The analysis command refuses to run while no eligible estimate exists — that refusal is the intended
behaviour, not a failure:

```bash
.venv/Scripts/python -m scripts.analysis.run_analysis    # refuses: nothing to pool
```

## 7. Tests

```bash
.venv/Scripts/python -m pytest
```

**In this snapshot: 671 collected — 664 pass, 7 skipped, 0 failed.**
**In the development repository: 671 collected — 670 pass, 1 skipped.**

The difference is entirely expected, and the seven skips are not failures or weakened assertions:

| Skipped | Why |
|---|---|
| 1 test | **By design in both repositories.** The raw-source test for the *original* 138-record export, which is lost and recorded as missing — a test demanding that file would be a false failure |
| 6 tests | **Only in this snapshot.** `tests/test_draw_provenance.py` proves the blinded verification sample is byte-for-byte what was first drawn, by reading the pre-migration worksheet out of **development commit `c704582`** via `git show`. This repository is published without that history, so the input does not exist here. The tests are guarded by `requires_development_history` and report: *"Requires historical development commit c704582, which is not included in the standalone submission snapshot."* |

**Their assertions are unchanged and are still enforced in the development repository,** where all
671 tests run and the historical draw is verified against the commit that produced it. A skipped
provenance check is **not** a passed provenance check, and nothing here claims otherwise.

> **One prerequisite for a green run.** `data/processed/` is not published (it is regenerable, and
> the pipeline refuses stale derived data), so run the three acquisition commands in
> [§6](#6-running-the-pipeline) once after cloning. Until then one further test fails, because
> `prisma.gather()` has no deduplication index to read. Regenerating it reproduces the original
> exactly: **194 records in, 194 unique reports, 0 duplicates.**

Tests use MEDLINE-format fragments and structural stubs with no bibliographic content, created in
temporary directories only. No synthetic record is ever written under `data/`.

## 8. Reports and presentation

| Deliverable | Path | Extent |
|---|---|---|
| Official systematic review and meta-analysis report | `results/final_submission/Official_Systematic_Review_and_Meta_Analysis_Report.{docx,pdf}` | 35 pages, 12 chapters, 7 appendices, 4 figures |
| Final research project report | `results/final_submission/Final_Research_Project_Report.{docx,pdf}` | 21 pages, 4 figures |
| Presentation | `results/final_submission/Final_Research_Project_Presentation.pptx` | 15 slides |
| Speaker notes | `results/final_submission/Final_Presentation_Speaker_Notes.{docx,pdf}` | 8 pages, all 15 slides |
| Supplementary material | `results/manuscript/Smoked_Tobacco_and_Oral_Cavity_SCC_Supplementary_Material.{docx,pdf}` | 7 pages |
| Extraction workbook | `results/manuscript/extraction_workbook/` | 3 header-only templates + data dictionary |

DOCX and PDF are produced from one parsed document model, so a heading, table or figure present in
one is present in the other. Earlier dated snapshots are retained alongside the current deliverables
as part of the audit trail.

**Figures** (all generated from repository data at build time, none hand-drawn or transcribed):
`prisma_flow.png`, `pipeline_architecture.png`, `record_status.png`, `data_flow.png`,
`tech_stack.png`.

## 9. Research status and limitations

### What has actually been done

| Measure | Value |
|---|---|
| Registered search executions | 1 (`pubmed_v1r`, PubMed, unfiltered) |
| Records identified | **194** · SHA-256 `1d153fa80edd6bc9…27e4ca1e`, verified |
| Parsed / unique reports / duplicates removed | **194 / 194 / 0** — no record loss |
| Provisional title/abstract classifications | **194** — 109 provisionally excluded with a reason, 85 carried forward |
| **Independently adjudicated screening decisions** | **0** |
| Blinded verification sample | 40 reports, 120 response cells, **0 answered** |
| Full texts sought / retrieved / assessed | **0 / 0 / 0** |
| Studies included · estimates extracted · appraisals | **0 · 0 · 0** |
| Pooled clinical estimates | **0** |
| Decision register | 24 adopted · 4 proposed · **12 open** |

### Limitations that must be read with any use of this repository

1. **No meta-analysis has been performed.** The statistical implementation is complete and tested
   against published formulas; it has never been run on research data, and it refuses to be.
2. **No independent human screening exists.** All 194 title/abstract classifications were adopted
   from automated suggestions. The formal PRISMA flow therefore reports 0 screened, 0 excluded and
   0 taken forward. These are **provisional classifications**, not screening results.
3. **One database, with a superseded query.** The adopted search strategy has never been executed.
   Two exploratory validation observations bound its expected volume — a counts-only E-utilities
   interrogation returning 8,190 (12 November 2026) and a web-interface submission displaying 8,195
   (14 November 2026) — and **neither retrieved or exported any record.** Neither is a search yield.
4. **Database coverage is unresolved** (P007). No subscription database access has been verified.
   PubMed alone does not constitute a systematic search.
5. **Twelve numbered methodological questions remain open**, including all nine anatomical and
   histological scope questions (P014–P022) and the risk-of-bias instrument (P023). A further
   eligibility question — whether populations restricted to premalignant oral lesions are in scope,
   affecting 14 of the 85 carried-forward reports — is open and deliberately unnumbered.
6. **Not prospectively registered** (P006). The provisional classification pass preceded
   registration; this is recorded as a declared deviation.
7. **The original search is unrecoverable.** A first export of 138 records is lost and is never
   recreated or substituted; its execution date is unknown and is not inferred. The re-execution's
   date awaits the reviewer's own verification.
8. **A count discrepancy is disclosed, not reconciled.** Against the re-execution, 194 unfiltered
   and 150 filtered are verified; the documented 138 is not. The residual is exactly
   194 − 44 − 3 − 138 = 9 records, or exactly 12 if the three post-pause records are not attributed.
   It remains unexplained, and no count has been altered to reconcile it.
9. **Statistical limitations, accepted and declared.** REML has self-consistency testing only and no
   external cross-validation. No Hartung–Knapp–Sidik–Jonkman interval, no Mantel–Haenszel or Peto
   method (so zero-cell data has no route), and no dose–response model.
10. **Single-reviewer design** throughout, reported as a limitation under PRISMA 2020 items 8 and 9.
    The review is never described as independently duplicated.

## 10. Provenance

This repository is a **clean published snapshot** of a verified commit. It is not the development
history.

| | |
|---|---|
| Development and provenance repository | **https://github.com/koushiksoppa/oscc-smoking-meta-analysis** |
| Source commit | **`cf8a4a9b036db475d28dcea07ae58d1c4fb78fed`** |
| Snapshot contents | The complete tracked tree of that commit, byte-identical except for the two files named below |
| Deliberately changed | **`README.md`** — rewritten for this standalone repository. **`tests/test_draw_provenance.py`** — six tests gained a `skipif` guard so they skip, rather than fail, when development commit `c704582` is absent. No assertion was altered, and no provenance datum was touched |
| Excluded | Git history, virtual environments, caches, and `data/processed/` (regenerable from the tracked raw export) |

All research data, protocol documents, the decision register, analysis code and deliverables are
byte-identical to the source commit — verified by SHA-256 against the development repository,
including the raw export, both screening worksheets, the report PDF and the presentation.

The originating repository retains the full commit history, including dated snapshots of earlier
report versions and the decision register's development. **Consult it for the audit trail**; this
repository is the final submitted artefact.

## 11. Acknowledgements and disclosure

**Author and reviewer.** Soppa Shiva Sai Koushik — National Institute of Technology, Rourkela.

**Development and Research Responsibility.** The project software, testing infrastructure,
documentation and reporting workflow were developed under the author's direction and review. All
research-related decisions, including eligibility criteria, screening adjudication, risk-of-bias
assessment and interpretation of evidence, remain the author's responsibility. Automated outputs
were used only as technical support and were not treated as independent research judgements or
substitutes for human review: screening *suggestions* are stored in a separate file, are never
written into a decision field, and that separation is enforced in code and reported in every output.

**Methodological sources.** PRISMA 2020 (Page et al.), PRISMA-S (Rethlefsen et al.), MOOSE (Stroup
et al.), the Cochrane Handbook for Systematic Reviews of Interventions v6.5, DerSimonian & Laird
(1986), Higgins & Thompson (2002), Egger et al. (1997) and Cohen (1960). Full citations appear in
the report's reference list.

---

*No clinical finding about smoked tobacco and oral cavity squamous cell carcinoma is reported in
this repository, because the evidence required to support one has not yet been extracted.*
