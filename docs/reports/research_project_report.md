# Development of a Reproducible Systematic Review and Meta-Analysis Pipeline for Evaluating the Association Between Smoked Tobacco Use and Oral Cavity Squamous Cell Carcinoma

**Research project report**

**Author.** Soppa Shiva Sai Koushik
**Report date.** 13 November 2026
**Repository state.** `HEAD` `b5afaff`, 34 commits
**Status of the research.** Protocol and infrastructure complete; evidence synthesis not begun

---

## Abstract

This report describes the design, implementation and validation of a reproducible software pipeline
for conducting a systematic review and meta-analysis of the association between smoked tobacco use
and squamous cell carcinoma of the oral cavity. It is a report about a **research instrument and the
protocol it enforces**, not a report of synthesised epidemiological findings.

The work delivers a specified review protocol with eighteen adopted methodological decisions, a
checksum-gated literature acquisition stage, a deduplication stage, a screening architecture that
distinguishes automated suggestions from human decisions at the level of individual data fields, a
93-field extraction schema, an implemented inverse-variance meta-analysis module, and a reporting
pipeline that generates manuscripts, figures and data-collection workbooks from source. The
implementation comprises 7,292 lines of application code and 5,957 lines of tests; the suite reports
**615 passed and 1 skipped**.

One database search has been executed and registered: a PubMed re-execution returning **194
records**, which deduplicated to **194 unique reports** with no duplicate pairs. An automated
procedure produced a provisional classification for all 194 reports, proposing 109 for exclusion
and 85 for retrieval. **None of those classifications has been independently adjudicated by a human
reviewer.** The project therefore reports **0 formally screened reports, 0 included studies, 0
extracted estimates, 0 risk-of-bias assessments and no pooled effect estimate.** A blinded
verification sample of 40 reports is drawn and unanswered: 0 of its 120 response cells are complete.

The central contribution is methodological. The pipeline treats the distinction between a machine
suggestion and a human judgement as a data-integrity property enforced by code rather than as a
convention observed by the operator. Three sequential gates refuse to proceed — eligibility
assessment without adjudicated includes, extraction without included studies, and analysis without
extracted estimates — so that an empty result cannot be mistaken for a null finding.

**Keywords:** systematic review methodology; meta-analysis; reproducible research; research
provenance; PRISMA 2020; oral cavity squamous cell carcinoma; smoked tobacco.

---

# Chapter 1 — Introduction

## 1.1 Oral cavity squamous cell carcinoma

Cancer of the oral cavity is among the more common malignancies worldwide, and its incidence is
distributed unevenly: the burden falls disproportionately on South and South-East Asia. The
dominant histological type is squamous cell carcinoma, which arises from the mucosal epithelium
lining the oral cavity. The anatomical region comprises the lips, the anterior two-thirds of the
tongue, the floor of the mouth, the buccal mucosa, the gingivae, the retromolar trigone and the
hard palate.

This anatomical definition matters more than it may appear. The oral cavity is adjacent to the
oropharynx, and the two are frequently reported together as "head and neck" or "oral and
oropharyngeal" cancer. They are not interchangeable for aetiological purposes: oropharyngeal
carcinoma has a substantial human papillomavirus-associated component with a different risk-factor
profile. A review that pools across these sites therefore risks diluting or distorting the
association it sets out to measure. The present protocol treats this as a substantive eligibility
question rather than a labelling convenience, and its consequences are developed in Chapter 2.

*The content of this section is established background knowledge drawn from the clinical and
epidemiological literature. It is not a finding of this project.*

## 1.2 Smoked tobacco exposure

Tobacco smoking is an established carcinogenic exposure for the upper aerodigestive tract. For the
oral cavity specifically, the relevant exposure is broader than cigarette smoking alone. Bidis —
small hand-rolled cigarettes common in South Asia — chuttas, cigars and pipes are all combusted
tobacco products, and reverse smoking, in which the lit end of the product is held inside the mouth,
is practised in parts of South India and is associated with palatal lesions.

A review restricted to cigarettes would therefore exclude much of the most informative literature
for the populations where the disease burden is greatest. This observation shapes the exposure
definition adopted here, and it propagates into the search strategy, the choice of databases and the
decision on grey literature, because the relevant studies are disproportionately published in
journals with incomplete international indexing.

*This section states background knowledge and the reasoning that motivated a protocol decision. The
decision itself (D009) is a product of this project.*

## 1.3 Research motivation

Two motivations drive this work, and they are different in kind.

The **substantive** motivation is that estimates of the association between smoked tobacco and
oral-cavity-specific squamous cell carcinoma remain dispersed across a literature that frequently
reports outcomes pooled across head-and-neck subsites, restricts exposure to cigarettes, and adjusts
inconsistently for alcohol, smokeless tobacco and betel quid. A synthesis that holds the anatomical
site, the histology and the exposure definition constant would be useful.

The **methodological** motivation is the more immediate one for this report. Systematic reviews are
frequently described as reproducible and frequently are not. Search strategies are reported in prose
that cannot be re-executed; screening decisions are recorded without the basis on which they were
made; the boundary between a tool's output and a reviewer's judgement is left to the reader's
assumption. As automated classification becomes ordinary in screening workflows, this last point
stops being a documentation nicety and becomes a question about what the recorded evidence means.
If a worksheet shows 194 decisions and does not say how they arose, a reader cannot tell whether a
human read 194 abstracts or accepted 194 machine outputs in a single action. The two are not the
same evidence, and a review that cannot distinguish them cannot be audited.

## 1.4 Research gap

The gap this project addresses is not a gap in the clinical literature. It is a gap between the
**claimed** and the **demonstrable** reproducibility of review workflows:

1. **Provenance of decisions.** Standard screening tools record a decision and a reason. They do not
   generally record whether the decision was formed by the reviewer or adopted from a suggestion,
   nor do they prevent the two from being counted together.
2. **Provenance of inputs.** Search exports are often described rather than preserved. When an
   export is lost, the loss is typically unrecorded, and a later re-run may silently substitute for
   it.
3. **Premature synthesis.** Nothing in a typical workflow prevents a pooled estimate from being
   computed on an incomplete or unverified dataset, nor distinguishes a null result from an empty
   one.

## 1.5 Problem statement

> Construct a systematic review and meta-analysis pipeline in which every recorded number is
> traceable to an immutable input, every decision records the basis on which it was made, the
> distinction between automated suggestion and human judgement is enforced by code rather than by
> convention, and no synthesis can be produced before the evidence required to support it exists.

## 1.6 Objectives

| # | Objective | Status |
|---|---|---|
| O1 | Specify a review protocol with explicit, recorded and dated methodological decisions | **Achieved** — 18 adopted, 4 proposed, 22 open questions tracked |
| O2 | Implement checksum-gated acquisition such that any alteration of a raw export is detected | **Achieved** — registered and verified |
| O3 | Implement deduplication with an explicit identifier hierarchy and no silent merging | **Achieved** — executed on the real data |
| O4 | Implement a screening architecture that separates suggestion from decision at field level | **Achieved** — enforced at three points in code |
| O5 | Implement a blinded verification mechanism with a reproducible sampling frame | **Achieved** — sample drawn; responses outstanding |
| O6 | Specify a complete extraction schema with declared provenance for every field | **Achieved** — 93 fields documented |
| O7 | Implement meta-analytic computation with declared validation and declared limitations | **Achieved** — implemented and tested; never run on real data |
| O8 | Generate manuscript, figures and workbooks reproducibly from source | **Achieved** — deterministic generation verified |
| O9 | Produce a pooled estimate answering the review question | **Not achieved** — blocked on reviewer work and on open protocol decisions |

Objective O9 is the scientific objective, and it is **not met**. This report does not present it as
met, and the distinction between O1–O8 and O9 is maintained throughout.

## 1.7 Research question

> **Is smoked tobacco use associated with an increased risk of squamous cell carcinoma of the oral
> cavity?**

The question is framed as an **association**. No causal claim will be made from observational data.
As of this report, **the question is unanswered by this project**: no study has been judged eligible
and no estimate has been pooled.

---

# Chapter 2 — Research methodology

## 2.1 Review design

The review is designed as a systematic review with meta-analysis of observational studies,
following PRISMA 2020 for reporting, PRISMA-S for the search, MOOSE for observational-study
specifics, and the Cochrane Handbook (v6.5) for synthesis methods. The protocol was specified before
screening: the protocol directory was committed on 29 October 2026, the screening records on 1
November 2026.

**The review is not prospectively registered.** Registration (PROSPERO or equivalent) is an open
question, and the provisional screening pass preceded any registration. This is a protocol
deviation and is reported as one rather than omitted.

## 2.2 PECO framework

For an observational review of an exposure, PECO is the appropriate framing.

**Table 2.1 — PECO framework and eligibility criteria.** The status column distinguishes settled
criteria from those still under decision; a criterion marked *Open* cannot be applied consistently
until it is resolved.

| Element | Criterion | Status |
|---|---|---|
| **P**opulation | Human adults; no restriction by country, sex or setting | Settled |
| **E**xposure | Any smoked tobacco: cigarettes, bidis, cigars, pipes and other combusted products (D009) | Settled |
| **C**omparator | Never-smokers, and/or "non-smokers" as defined by the study; recorded verbatim in all cases | **Open (P003)** |
| **O**utcome | Oral cavity cancer with SCC histologically confirmed, or a stated majority of at least 90% of cases (D008) | Settled in part — see §2.4 |
| Contrast | Primary exposure contrast (ever / current / former versus reference) | **Open (P004)** |
| Designs | Case–control; cohort, prospective or retrospective | Settled |
| Effect data | OR, RR or HR with a 95% confidence interval, or sufficient raw data to compute one | Settled |
| Language | Published in English (D013) | Settled |

## 2.3 Inclusion and exclusion criteria

A study is eligible when it reports an oral-cavity-specific effect estimate for a smoked tobacco
exposure against a non-smoking reference group, in a case–control or cohort design, with squamous
cell carcinoma confirmed histologically or constituting a stated majority of at least 90% of cases.

Estimates pooled across head-and-neck subsites are **ineligible** unless an oral-cavity-specific
estimate is reported separately. Smokeless tobacco and betel quid are treated as **confounders, not
exposures**, and adjustment for each is recorded per estimate.

Exclusion is recorded against a fixed controlled vocabulary; free text may not substitute for a
code. Thirteen codes are defined, nine available at title and abstract and four restricted to full
text on the grounds that they cannot be judged from an abstract without guessing.

**Table 2.2 — Controlled vocabulary of exclusion reasons.** Stage restriction is a deliberate design
choice: a code that requires the full text cannot be applied at title and abstract, so the
vocabulary itself prevents a premature judgement.

| Code | Definition | Available at |
|---|---|---|
| `wrong_population` | Not human, not adult, or not a relevant population | ta, ft |
| `wrong_outcome` | Outcome is not oral-cavity SCC per D008, including prognostic studies among people who already have the disease | ta, ft |
| `wrong_exposure` | Exposure is not smoked tobacco, or smokeless tobacco / betel quid only | ta, ft |
| `wrong_design` | Not case–control or cohort | ta, ft |
| `review_or_meta` | Systematic review, meta-analysis, narrative review | ta, ft |
| `animal_or_invitro` | Animal, cell or in-vitro study | ta, ft |
| `conference_abstract` | Abstract with insufficient detail for reliable extraction | ta, ft |
| `not_english` | Not published in English | ta, ft |
| `other` | Requires a written justification | ta, ft |
| `outcome_not_separable` | Oral cavity pooled with oropharynx / larynx / head and neck, no oral-specific estimate | **ft only** |
| `no_reference_group` | No non-smoking or never-smoking comparator | **ft only** |
| `no_usable_data` | No effect estimate and no data from which to derive one | **ft only** |
| `duplicate_publication` | Same study population already included; links to the retained `report_id` | **ft only** |

## 2.4 Criteria not yet settled

Ten questions of anatomical and histological scope remain open: the eligible subsite list; the
treatment of soft palate and uvula, where staging and anatomical conventions genuinely conflict; the
handling of straddling topography codes; a site-purity threshold analogous to the histological
threshold; whether squamous cell carcinoma variants count as squamous cell carcinoma; the status of
adenosquamous and sarcomatoid entities; and whether populations restricted to premalignant oral
lesions are in scope — which affects **14 of the 85** reports provisionally carried forward. Two of
these require a reference text that was not accessible during protocol development.

All must be resolved before full-text eligibility assessment begins. This is why the Outcome row of
Table 2.1 is marked *settled in part*: the histological threshold is fixed, the subsite boundary is
not.

## 2.5 Search strategy

Three search executions are distinguished in the project record, because a database's content and
the filters actually applied may differ between runs.

**Table 2.3 — Search executions and their status.** The distinction between an execution that
produced a preserved export and one that did not is fundamental: only the former contributes
records.

| Execution | Query | Filters applied | Records | Status |
|---|---|---|---|---|
| v1 (original) | see below | Humans, English | 138 | **Export lost.** Not recreated or substituted; contributes no records |
| v1r (re-execution) | identical to v1 | **none** | **194** | **Registered with a checksum; the evidence base for all work reported here** |
| v2 draft (expanded) | broader MeSH and free-text strategy | none | — | Drafted; counts-only validation 29 Oct 2026. Not executed; superseded |
| Corrected proposed strategy | v2 draft with a site-unrestricted histology term removed | none | — | Proposed; counts-only validation 12 Nov 2026. **Not executed** |

The query string, identical for v1 and v1r:

```
("Oral Squamous Cell Carcinoma"[Title/Abstract] OR OSCC[Title/Abstract])
AND (smoking[Title/Abstract] OR cigarette[Title/Abstract])
AND ("case-control"[Title/Abstract] OR cohort[Title/Abstract])
```

**Deviation from the v1 strategy, reported as such.** The re-execution was run without the Humans
and English database filters (D013). The Humans filter operates on an index term absent from records
not yet indexed — 42 of the 194 here, which are the most recent and plausibly among the most
relevant. Non-English and non-human records are instead excluded at screening with a recorded reason
code, which is auditable in a way a database filter is not. The consequence, which must be reported,
is that `not_english` and `wrong_population` appear as exclusion reasons that a filtered search would
never have surfaced.

**Limitations of the executed query.** The v1 string is substantially narrower than the eligibility
criteria it is meant to serve. It requires the literal phrase "Oral Squamous Cell Carcinoma" or
"OSCC" in the title or abstract; **68 of the 194** retrieved records use the phrase "oral cancer",
the dominant phrasing in aetiological epidemiology, and were retrieved only because they also
happened to contain one of the required terms. It reduces the exposure to "smoking" or "cigarette",
omitting bidi, cigar, pipe and other product terms central to the exposure definition, and uses no
controlled vocabulary at all. **98 of 194** matched the design block only through the single word
"cohort", which also captures prognostic studies of patients who already have the disease.

**Any synthesis based on this record set alone would rest on a search that does not match its own
protocol.** This is the single most important limitation of the project's current evidence base.

A corrected and substantially broader strategy has been prepared and syntax-validated but **not
executed**. It supersedes the v2 draft, from which it differs by the removal of a site-unrestricted
histology term that had allowed squamous cell carcinomas of other anatomical sites into the outcome
block — a defect that inflated retrieval by approximately 6,200 records.

## 2.6 Database coverage and limitations

**One bibliographic database, PubMed, has been searched.** A single database does not constitute a
systematic search.

**Table 2.4 — Database coverage and access status.** No subscription database access has been
verified; an institution's published subscription list is not evidence that a given researcher can
execute and export a search.

| Source | Role | Searched | Access status |
|---|---|---|---|
| PubMed / MEDLINE | Core | **Yes** — one registered execution | **Confirmed** (free) |
| Embase | Core if accessible | No | **No evidence of access** — not listed among the institution's advertised databases |
| Scopus | Conditional; preferred citation index | No | **Publicly advertised; not verified** |
| Web of Science | Alternative to Scopus | No | **Publicly advertised; not verified** |
| IndMED | Supplementary, regional | No | **Reachability unverified** |
| LILACS | Supplementary, regional | No | Open access; not tested |
| Cochrane CENTRAL | **Not recommended** | No | Design mismatch: registers controlled trials |
| Reference-list checking | Core supplementary method | No | Requires no subscription |
| Forward-citation checking | Supplementary method | No | Requires a citation index |

The approved coverage wording commits the review to PubMed plus, subject to confirmed access, one
citation index (preferably Scopus), with Embase included only if access is confirmed **before** the
formal search, and with reference-list and forward-citation checking undertaken. P007 remains open
pending access verification.

## 2.7 Grey literature

A bounded supplementary grey-literature search is adopted (D022, 13 November 2026), justified by
**search sensitivity** rather than by any statistical test. Priority is given to South Asian theses
and dissertations, which is where the bidi and reverse-smoking literature is concentrated.
Government and registry reports are treated as **discovery sources** whose reference lists are
checked, not as evidence of the association: prevalence-only and incidence-only reports are excluded
as `no_usable_data`. A Google Scholar search is bounded by a prespecified stopping rule — 200
results examined or 50 consecutive non-hits — which is an **operational choice fixed in advance, not
an established standard**, and which produces a search that is reportable but not repeatable.

No repository has been verified as reachable, and no grey-literature search has been executed.

## 2.8 PRISMA methodology

The project implements PRISMA 2020 flow accounting with one significant extension. Because all
current title/abstract classifications were adopted from automated suggestions, a conventional
PRISMA flow would report 194 screened and 85 sought — numbers that would imply human screening that
has not occurred.

The flow is therefore **split**:

- The **formal flow** counts independently adjudicated decisions only. It currently reports 0
  screened, 0 excluded and 0 taken forward.
- A **provisional section**, explicitly headed as not part of the flow, reports the 194 adopted
  classifications.

Full-text rows are attributed to one of five mutually exclusive states, decided per row rather than
by subtraction: `ft_sought`, `ft_provisional_sought`, `ft_invalid_source`, `ft_ineligible_source`
and `ft_unattributed`. Eleven reconciliation identities must hold or the run fails.

---

# Chapter 3 — System architecture and pipeline

## 3.1 Architecture overview

The pipeline comprises fifteen stages. Figure 3.1 shows them with their implementation status.

![Figure 3.1. Pipeline architecture. Each stage is coloured by what the repository actually does: green where the code exists and has been executed on the real data, amber where it is implemented and tested but has never run, grey where no implementation exists. The three gates are the design's central safety property.](results/final_submission/figures/pipeline_architecture.png)

The figure is generated from the repository at build time and is not drawn by hand, so it cannot
drift from the state it describes.

## 3.2 Data flow

![Figure 3.2. Data flow across four custody classes. Immutable inputs are checksum-gated; generated data is regenerable and never hand-edited; human research records are tracked precisely because they cannot be regenerated; outputs are produced from all three. The suggestion file is deliberately separate from the decision file.](results/final_submission/figures/data_flow.png)

The four custody classes are a design decision rather than a filing convention:

- `data/raw/` is **immutable**. A raw export is never edited, re-saved or re-encoded. If an export
  is lost it is recorded as lost and is not substituted.
- `data/processed/` is **generated** and may be deleted and rebuilt at any time.
- `data/screening/` and `data/extraction/` hold **human research work** and are tracked, because
  a screening decision cannot be regenerated from anything.
- `results/` is **generated** and is never hand-edited.

## 3.3 Stage-by-stage specification

**Table 3.1 — Pipeline stages: input, processing, output, validation and status.** "Built, not run"
means the implementation exists and is covered by tests but has never executed against real research
data; it is not a claim of completion.

| # | Stage | Input | Processing | Output | Validation | Status |
|---|---|---|---|---|---|---|
| 1 | Literature identification | Database query | Search executed by the researcher and exported | `.nbib` export | Count + SHA-256 recorded at registration | **Run** — 194 records |
| 2 | Record import | Registered export | MEDLINE parsing to structured records | `*_citations.csv`, `*_records.jsonl` | Field-level validation; query-block diagnostics | **Run** — 194 parsed |
| 3 | Deduplication | Parsed citations | Normalised DOI → PMID → exact title/author/year fingerprint | `report_index.csv`, `dedup_audit.csv` | Similar titles flagged `needs_review`, never auto-merged | **Run** — 0 duplicates |
| 4 | Report and study identity | Report index | Reviewer assigns `study_id` at full text | `studies.study_id` | A `study_id` may appear at most once per analysis | Built, not run |
| 5 | Title/abstract screening | Report index | Decision + reason code recorded per report | `screening_ta.csv` | 11 identities; `--final` rejects adopted bases | **Run** — 194 provisional |
| 6 | Independent adjudication | Screening worksheet | Reviewer judges each record from its own evidence | `decision_basis = independently_adjudicated` | Five fields required for a row to count as adjudicated | Built, **0 of 194 done** |
| 7 | Verification sampling | Screening worksheet | Seeded draw from a canonical frame digest | `verification_sample.csv` | Reproducible draw; 20 provenance tests | Built — **0 of 120 cells** |
| 8 | Full-text retrieval | Carried-forward reports | Obtain and record full texts | `full_text_status` | — | **Not implemented**; 0 retrieved |
| 9 | Eligibility assessment | Retrieved full texts | Eligibility decision + reason | `screening_ft.csv` | **Gate: refuses without adjudicated includes** | Built, refuses |
| 10 | Data extraction | Included studies | Reviewer records study and estimate fields | `data/extraction/*.csv` | **Gate: refuses without included studies** | Built, refuses |
| 11 | Risk-of-bias assessment | Included studies | Domain-level appraisal | `risk_of_bias.csv` | Instrument undecided (P023) | **Not implemented** |
| 12 | Effect-size preparation | Extracted estimates | log OR/RR/HR and SE from CI, counts or reported SE | `Estimate` objects | CI asymmetry and implied-OR checks | Built, not run |
| 13 | Meta-analysis | Prepared estimates | Inverse-variance pooling, fixed and random effects | Pooled result | **Gate: refuses without estimates; rejects synthetic data** | Built, refuses |
| 14 | Sensitivity and subgroup | Pooled result | Leave-one-out; planned subgroups | Analysis report | Egger refused below 10 studies | Built, not run |
| 15 | Manuscript and outputs | All of the above | Markdown to DOCX/PDF; figures; workbook | `results/` | Cross-format and data checks | **Run** |

## 3.4 The three gates

The gates are the architectural core and deserve explicit statement. Each raises `PipelineError` and
exits non-zero rather than producing an empty artefact:

1. **Extraction requires full-text includes.** Running the extraction template with no included
   study does not create an empty table; it refuses and explains why.
2. **Synthesis requires extracted estimates.** `run_analysis.py` refuses when no estimate file
   exists.
3. **The analysis CLI rejects anything marked synthetic.** A row carrying `synthetic = yes` cannot
   enter a pooled calculation.

The purpose is to make the difference between *"we found no association"* and *"we have not looked"*
impossible to confuse in the artefacts themselves.

---

# Chapter 4 — Technology stack and implementation

## 4.1 Stack as actually present

![Figure 4.1. Technology stack. Every component listed is imported by code in the repository; components deliberately absent are named explicitly at the foot of the figure.](results/final_submission/figures/tech_stack.png)

**Table 4.1 — Technology choices and the reason for each.**

| Component | Version | Used for | Why this choice |
|---|---|---|---|
| Python | 3.14.7 | All application code | Readable, strong standard library, no runtime to install beyond the interpreter |
| Standard library `csv` | — | **All tabular data handling** | Explicit, dependency-free, and preserves values as written. The pipeline must never silently coerce a value |
| `hashlib` (SHA-256) | — | Export registration, frame digests | Collision-resistant and reproducible across platforms |
| `zipfile` | — | DOCX and PPTX generation | OOXML files are ZIP containers; no third-party document library is needed |
| `difflib` | — | Near-duplicate title similarity | Deterministic similarity without a dependency |
| `unicodedata` | — | NFC normalisation in digests | Makes a digest invariant to encoding presentation |
| PyYAML | 6.0.3 | `config/*.yaml` | Human-editable configuration that a reviewer can read and amend |
| pytest | 9.1.1 | Test suite | Low-ceremony assertions; parametrisation |
| SciPy | 1.18.1 | chi², normal and t distributions; `linregress` | Established numerical implementations for the statistics that must be correct |
| Matplotlib | 3.11.2 | All figures; PDF typesetting | Deterministic raster and vector output without a browser toolchain |
| Git | — | Version control, 34 commits | Decision provenance and an auditable history |

## 4.2 Deliberately absent

The report states this explicitly because claiming unused tooling would itself be a reproducibility
failure:

- **pandas is not used.** No module in the repository imports it. All tabular work uses the standard
  library `csv` module. For a pipeline of this size the dependency would add weight without adding
  capability, and `csv` keeps values exactly as written.
- **NumPy is not a direct dependency.** No module imports it; it arrives transitively under SciPy
  and Matplotlib, which pin their own requirements more accurately than this project could.
- **No third-party document library.** DOCX and PPTX are written as OOXML through `zipfile`; PDF is
  typeset through Matplotlib. This was a constraint — installation was not authorised — and it is
  recorded as such.

## 4.3 Source map

**Table 4.2 — Source tree and responsibilities.** 7,292 lines of application code; 5,957 lines
of tests.

| Package | Files | Lines | Responsibility |
|---|---|---|---|
| `scripts/common/` | 2 | 163 | Repository root, source registry, `PipelineError` |
| `scripts/acquisition/` | 4 | 551 | Raw export inspection, count and checksum gate, registration |
| `scripts/validation/` | 2 | 239 | Citation field validation, query-block diagnostics |
| `scripts/dedup/` | 4 | 648 | Identifier hierarchy, fingerprinting, `needs_review` reporting |
| `scripts/screening/` | 9 | 2,283 | Worksheets, vocabulary, adjudication rules, PRISMA accounting, verification sampling |
| `scripts/extraction/` | 4 | 594 | Schema loading, template generation, extraction validation |
| `scripts/analysis/` | 5 | 706 | Effect-size preparation, pooling, heterogeneity, plots, CLI gate |
| `scripts/visualization/` | 2 | 281 | PRISMA flow diagram |
| `scripts/reporting/` | 6 | 1,827 | Manuscript, presentation, workbook and figure generation; deliverable audit |
| `tests/` | 20 | 5,957 | 616 collected tests |

**Key modules.**

- `scripts/common/config.py` — the source registry and `PipelineError`. Every provenance violation
  raises here and is never caught silently.
- `scripts/acquisition/verify_raw.py` — separates *inspecting* a file from *declaring* it the
  research input: `--report-only` writes a proposal, `--register` writes the authoritative checksum.
- `scripts/screening/worksheet.py` — `adjudication_problems()` is the single function applying the
  five-field adjudication rule, shared by the validator, the full-text carry-forward and the PRISMA
  gatherer, so the three cannot disagree.
- `scripts/screening/prisma.py` — formal/provisional accounting and the eleven identities.
- `scripts/screening/verify_sample.py` — the blinded draw, its two seed-derivation rules and their
  recorded provenance.
- `scripts/analysis/meta.py` — pooling, heterogeneity, Egger's test with its refusal threshold.
- `scripts/reporting/build_manuscript.py` — one Markdown parse feeding both the DOCX and the PDF
  writer, which makes format divergence structurally impossible.

---

# Chapter 5 — Numerical outputs and implementation results

Every number in this chapter was recomputed from the repository's own data files at report build
time. Nothing is transcribed from an earlier document.

## 5.1 Literature identification

**Table 5.1 — Registered search executions.** `pubmed_v1` exists in the registry solely to record
that its export is missing; an entry is never created for a merely drafted search.

| Registry entry | Execution type | Status | Expected records | Export |
|---|---|---|---|---|
| `pubmed_v1` | historical | `export_missing` | 138 (documented claim, unverified) | **none — lost** |
| `pubmed_v1r` | re_execution | `registered` | 194 | `pubmed-v1r-reexecution-194.nbib` |

**The registered export.** 958,710 bytes; SHA-256
`1d153fa80edd6bc97c92498bce8076873cc514f412de5113412fa71827e4ca1e`. Verification of this checksum
succeeds at the time of writing.

**Table 5.2 — Composition of the 194-record export.** The language and indexing distribution is the
direct consequence of D013 (retrieve unfiltered, exclude at screening) and explains why exclusion
reasons appear that a filtered search would never have produced.

| Property | Count |
|---|---|
| Records in the export | 194 |
| Unique PMIDs | 194 |
| Language: English | 191 |
| Language: Chinese | 2 |
| Language: English and Portuguese | 1 |
| Records carrying MeSH indexing | 152 |
| Records with no MeSH indexing at all | 42 |

## 5.2 Deduplication

**Table 5.3 — Deduplication outcome.** A result of zero duplicates is expected for a single-database
search and is not evidence that the stage is untested: the matching rules are exercised by 52 tests
plus 11 authority tests.

| Metric | Value |
|---|---|
| Records entering deduplication | 194 |
| Pairs merged on identifier or exact fingerprint | 0 |
| Pairs flagged `needs_review` | 0 |
| Unique reports after deduplication | **194** |

## 5.3 Screening: provisional classifications, not decisions

This is the most important numerical result in the report, and the one most easily misread.

**Table 5.4 — Title/abstract stage.** The formal and provisional columns are not two views of the
same work. The formal column counts human adjudications, of which there are none.

| Quantity | Formal | Provisional |
|---|---|---|
| Reports with a recorded classification | **0** | 194 |
| Classified for exclusion | **0** | 109 |
| Classified for retrieval | **0** | 85 |
| Unresolved | 0 | 0 |
| Rows failing validation | 0 | — |

All 194 rows carry `decision_basis = adopted_from_suggestion`; **0 carry
`independently_adjudicated`.** Under D010 and D016 a suggestion cannot satisfy a decision field, so
the formal PRISMA flow reports 0 screened. `validate_screening --stage ta --final` fails on this
state, as it is designed to.

**Table 5.5 — Provisional exclusion reasons.** These are the reason codes attached to automated
suggestions that were adopted in bulk. They are **not** reviewer judgements and must not be reported
as a PRISMA exclusion table.

| Reason code | Count | Share of 109 |
|---|---|---|
| `wrong_outcome` | 63 | 57.8% |
| `wrong_design` | 33 | 30.3% |
| `review_or_meta` | 10 | 9.2% |
| `not_english` | 2 | 1.8% |
| `wrong_population` | 1 | 0.9% |
| **Total** | **109** | **100%** |

![Figure 5.1. Current state of the evidence base. The left panel shows record attrition, with provisional counts distinguished from formal ones; the right panel shows reviewer work completed against work outstanding. Every bar is recomputed from the repository at build time.](results/final_submission/figures/record_status.png)

**What Figure 5.1 means.** The left panel's last two bars are zero not because the search found
nothing, but because the human work that would make them non-zero has not been done. The right panel
makes the same point from the other direction: one row is complete, and it is the row that records
machine output rather than human judgement.

## 5.4 Full text

**Table 5.6 — Full-text stage attribution.** Each of the five states is decided per row, never by
subtraction, so the table cannot be made to balance by inference.

| State | Count |
|---|---|
| `ft_sought` (valid, adjudicated include) | **0** |
| `ft_provisional_sought` (valid include, adopted basis) | 85 |
| `ft_invalid_source` | 0 |
| `ft_ineligible_source` | 0 |
| `ft_unattributed` | 0 |
| **Total rows** | **85** |

Full texts retrieved: **0**. Eligibility decisions recorded: **0**. Every reviewer field in the
full-text worksheet is empty.

## 5.5 Blinded verification

**Table 5.7 — Verification sample.** The sample exists and is reproducible; the responses do not
exist.

| Property | Value |
|---|---|
| Reports sampled | 40 |
| Sampling fraction of 194 | 20.6% |
| Response columns per row | 3 (`your_decision`, `your_reason_code`, `your_notes`) |
| Total response cells | 120 |
| **Cells completed** | **0** |
| Agreement rate, kappa, acceptance outcome | **Do not exist** |

The draw's provenance is recorded under the historical rule `file_bytes_crlf_v1` with seed
`1496879658` and a canonical frame digest under `ordered_report_ids_v1`. The draw **date** is
recorded as UNVERIFIED and is not inferred from any commit date.

## 5.6 Extraction and appraisal schema

**Table 5.8 — Extraction schema.** The schema is complete and documented; it contains no data,
because no study has been included.

| Table | Fields | Data rows | Schema source |
|---|---|---|---|
| `studies` | 34 | **0** | `config/extraction.yaml` → `studies` |
| `estimates` | 47 | **0** | `config/extraction.yaml` → `estimates` |
| `risk_of_bias` | 12 | **0** | `config/extraction.yaml` → `risk_of_bias` (**provisional, P023**) |
| **Total documented fields** | **93** | **0** | `data_dictionary.csv` |

Five fields are marked `unresolved` because they depend on protocol decisions not yet made:
`comparator_type` (P003), `exposure_contrast` (P004), and `tool`, `domain` and `judgement` (all
P023). The risk-of-bias instrument has **not** been chosen; its domain names and judgement
categories are deliberately absent, and a test asserts that no known instrument is named anywhere in
the workbook.

`data/extraction/` **does not exist** on disk. This is the correct state: the directory is created
only when a study has been included.

## 5.7 Search strategy counts

**Table 5.9 — Database interrogation counts.** These are **counts-only interrogations for strategy
validation. None is a search yield**; no record was retrieved, downloaded, exported or screened, and
no registry entry exists for any of them. Counts describe a database on the day they were taken.

| Query | Without design block | With design block | Date |
|---|---|---|---|
| v1 string, unfiltered | — | 194 | 29 Oct 2026 |
| v1 string, Humans + English | — | 150 | 29 Oct 2026 |
| v1 string, as documented in the v1 strategy | — | 138 | unknown |
| v2 draft | 7,875 | 4,770 | 29 Oct 2026 |
| **Corrected strategy (adopted, D023)** | **8,190** | **5,008** | **12 Nov 2026** |

A residual discrepancy of approximately nine records between the documented 138 and the ~147 implied
by the re-execution **remains unexplained** and is recorded as an open question. The documented count
has not been altered to remove the discrepancy.

## 5.8 Automated test results

**Table 5.10 — Test suite by module, as collected.** 616 tests collected; **615 passed, 1 skipped**.
The single skip is the raw-source test for `pubmed_v1`, skipped by design because that export is
recorded as missing.

| Test module | Tests |
|---|---|
| `test_screening.py` | 110 |
| `test_extraction.py` | 62 |
| `test_dedup.py` | 52 |
| `test_analysis.py` | 48 |
| `test_screening_show.py` | 47 |
| `test_verify_sample.py` | 44 |
| `test_prisma_diagram.py` | 32 |
| `test_review_queue.py` | 29 |
| `test_backfill_provenance.py` | 28 |
| `test_validation_rules.py` | 23 |
| `test_source_registry.py` | 20 |
| `test_prisma_attribution.py` | 20 |
| `test_draw_provenance.py` | 20 |
| `test_intake.py` | 17 |
| `test_build_presentation.py` | 16 |
| `test_nbib_format.py` | 15 |
| `test_build_workbook.py` | 13 |
| `test_dedup_authority.py` | 11 |
| `test_parse_citations.py` | 7 |
| `test_raw_sources.py` | 2 |
| **Total** | **616** |

## 5.9 What this chapter does not report

No odds ratio, risk ratio, hazard ratio, confidence interval, p-value, I², τ², pooled estimate,
forest plot or funnel plot appears anywhere in this report, because **no eligible study estimate
exists**. Publication bias has **not** been assessed. No study has been judged eligible. These are
absences of evidence, not evidence of absence, and the pipeline is built so that they cannot be
presented as the latter.

---

# Chapter 6 — Statistical analysis methodology

This chapter describes **implemented capability and planned analysis**. Nothing in it has been
executed on research data, because no estimate exists to execute it on.

## 6.1 Effect measures

For observational studies of a binary exposure and a binary outcome, the admissible measures are the
odds ratio, risk ratio and hazard ratio. All computation is performed on the **logarithmic scale**,
where the sampling distribution is approximately normal, and results are exponentiated only for
presentation.

Three routes to a standard error are implemented in `scripts/analysis/effects.py`:

| Route | Method | When used |
|---|---|---|
| `from_ci` | SE derived from the reported 95% confidence interval | The usual case |
| `from_counts` | SE from the 2×2 cell counts | When raw counts are reported |
| `from_log_se` | SE as reported | When the paper gives it directly |

Derived values are never typed by hand: `log_estimate_calc` and `se_calc` are marked DERIVED in the
schema, and the formula and inputs used are recorded in a `derivation` field. A consistency check
compares the reported estimate against the geometric mean of its interval and reports asymmetry
beyond a 10% relative gap, since mild asymmetry is normal when a source rounds its interval.

## 6.2 Pooling

Inverse-variance weighting is implemented for both models:

- **Fixed-effect:** weights are the reciprocal of each estimate's variance.
- **Random-effects:** weights are the reciprocal of within-study variance plus the between-study
  variance τ². Two estimators of τ² are implemented: **DerSimonian–Laird** and **restricted maximum
  likelihood**.

A random-effects model is anticipated, since observational studies of this exposure differ in
population, design and adjustment, and an assumption of one common true effect would not be
credible.

## 6.3 Heterogeneity

Cochran's Q is implemented with its χ² p-value, and I² is derived as the proportion of total
variation attributable to between-study heterogeneity rather than to chance. The conventional
interpretive bands — approximately 25%, 50% and 75% for low, moderate and substantial heterogeneity
— are treated as descriptive guidance, not thresholds for a decision. τ² is reported for
random-effects models.

**Criteria for not pooling are specified in advance.** A narrative synthesis is the stated
alternative where pooling is not defensible, and pooling will not proceed across different
anatomical sites without a valid oral-specific estimate, across smokeless and smoked tobacco, across
incompatible exposure contrasts, or across duplicate or overlapping estimates treated as independent
studies.

## 6.4 Subgroup and sensitivity analyses

Planned subgroups, contingent on sufficient studies: product type (cigarette-only versus mixed),
geographical region, anatomical subsite, risk-of-bias level, and alcohol-adjusted versus unadjusted
estimates. Implemented sensitivity analysis: **leave-one-out influence analysis**. Restriction by
risk of bias is planned but depends on P023.

## 6.5 Small-study effects

Egger's regression test and funnel plots are implemented, and the implementation **refuses to run
Egger's test below ten studies** (`MIN_STUDIES_EGGER = 10`), because the test is uninformative with
few studies and is widely advised against below that number. Funnel-plot asymmetry has several
possible causes besides publication bias — true heterogeneity, poorer methodological quality in
smaller studies, chance — and the implementation's documentation states this rather than equating
asymmetry with bias.

**No assessment of small-study effects has been performed, and none is promised.** If fewer than ten
studies are ultimately included, no such test will run at all.

## 6.6 Declared implementation limitations

These are stated in the repository and are repeated here because a reader entitled to the numbers is
entitled to their caveats:

- The **REML estimator has no external validation**. It is tested for self-consistency — its τ² is a
  fixed point of its own update — and for limiting behaviour. That establishes that the
  implementation solves the equation it encodes, not that the equation is correctly specified. Any
  REML estimate must be cross-checked against an established implementation before publication.
- The pooled estimate, weights and τ² have **no external reference check**, because no published
  worked example with per-study data was accessible.
- **No Hartung–Knapp–Sidik–Jonkman interval** is implemented, which the Cochrane Handbook favours
  when the number of studies is small and between-study variance is non-zero — the likely situation
  here.
- **No Mantel–Haenszel or Peto method**, so rare-event and zero-cell data have no route.
- **No meta-regression and no dose–response model.**

---

# Chapter 7 — Validation and reproducibility

## 7.1 Automated test suite

**615 passed, 1 skipped**, from 616 collected, at the time of this report. The single skip is by
design: the raw-source test for `pubmed_v1` is skipped because that export is recorded as missing,
and a test that demanded a lost file would be a false failure.

Test weight is concentrated where the risk of silent error is greatest: 110 tests on screening
accounting, 62 on the extraction schema, 52 on deduplication, 48 on the analysis mathematics, 44 on
verification sampling and 20 on draw provenance.

## 7.2 Regression tests for specific defects

Several tests exist because a specific defect was found and fixed, and each encodes the defect so it
cannot return:

- **Banner arithmetic.** A PRISMA banner interpolated the formal count into a sentence about
  reports carrying a decision, producing the self-contradiction "0 of 194 reports carry a decision,
  but 194 were adopted". Two tests now assert the corrected wording, including that the output
  cannot be read as 194 completed human screening decisions.
- **Workbook provenance.** The extraction workbook once claimed to be generated by a script that
  contained no reference to it. A test now asserts that the README names the real generator and
  that the false claim is absent.
- **Headers-only guarantee.** A test monkeypatches the workbook writer to smuggle a data row and
  asserts that the generator refuses.
- **Instrument neutrality.** A test asserts that no known risk-of-bias instrument is named anywhere
  in the generated workbook, so the schema cannot imply a decision that P023 has not made.

## 7.3 Protected checksums and raw-data preservation

Two classes of protected value are verified:

**Table 7.1 — Protected provenance values.** All verify at the time of writing.

| Protected value | Content | Status |
|---|---|---|
| Raw export checksum | SHA-256 of the registered `.nbib` | **OK** |
| `DRAW_SHA` | Worksheet SHA-256 at the verification draw | Unchanged |
| `DRAW_SEED` | `1496879658` | Unchanged |
| `DRAW_SEED_DERIVATION` | `file_bytes_crlf_v1` | Unchanged |
| `FRAME_DIGEST_RULE` | `ordered_report_ids_v1` | Unchanged |
| `DRAW_FRAME_DIGEST` | Canonical frame digest | Unchanged |

Seven screening and processed data files are additionally verified byte-for-byte against a recorded
baseline: the title/abstract worksheet, the full-text worksheet, the suggestion file, the
verification sample, the parsed citations, the deduplication audit and the report index.

## 7.4 Decision provenance

Every screening row records five fields, and a row counts as independently adjudicated only when all
five are present: `decision`, `reviewer`, `screened_date`, `decision_basis` and `adjudicated_date`.
The separate `adjudicated_date` exists so that flipping the basis on a row already carrying the
bulk-adoption reviewer and date cannot convert a provisional record into a formal one without dating
the new act.

One shared function applies these rules for the validator, the full-text carry-forward and the
PRISMA gatherer, so the three cannot disagree with one another.

## 7.5 Deterministic generation

Three generators were verified to produce byte-identical output on repeated runs from a clean path:

| Artefact | Determinism check |
|---|---|
| PRISMA flow diagram | Regenerated to a scratch path; byte-identical |
| Extraction workbook | Two clean builds; byte-identical across all five files |
| Report figures | Two clean builds; byte-identical across all four figures |

The PRISMA figure embedded in the manuscript DOCX was additionally verified to be byte-identical to
the figure on disk, so the document cannot carry a stale image.

## 7.6 Cross-format validation

The manuscript and supplementary deliverables are validated by an independent harness that opens the
produced files rather than trusting the build log. DOCX text is read by parsing `word/document.xml`
with an XML parser; PDF text is recovered by decompressing the content streams and decoding the
string operands.

**Table 7.2 — Latest cross-format validation of the supplementary deliverable.**

| Check | Result |
|---|---|
| Headings present in PDF, in order | 19 / 19 |
| Table cells present in both formats | 164 / 164 |
| Numeric tokens present in both formats | 109 / 109 |
| Sampled prose sentences present in PDF | 80 / 80 |
| PDF pages carrying their own page number | 7 / 7 |
| Deliverable auditor | 0 failing checks |

## 7.7 Version control

34 commits on `main`. History is never rewritten and force-pushing is prohibited. Decisions are
recorded in a decision log with dates, rationale, consequences and an explicit statement of what each
decision does **not** do.

---

# Chapter 8 — Limitations

These are stated plainly because the project's value depends on them being stated.

## 8.1 The evidence base

1. **One database.** Only PubMed has been searched. A single database does not constitute a
   systematic search, and the shortfall falls hardest on exactly the literature the exposure
   definition was written to capture.
2. **The executed query is narrower than its own protocol.** It requires a literal phrase that 68 of
   194 retrieved records do not use as their primary terminology, omits bidi and other product
   terms, and uses no controlled vocabulary. This is the single most consequential limitation.
3. **The original v1 export is lost.** It is recorded as lost and not substituted. A residual
   discrepancy of about nine records remains unexplained.
4. **No subscription database access is verified.** Embase is not listed among the institution's
   advertised databases; Scopus and Web of Science are advertised but unverified for this
   researcher.
5. **P007 is open; P013 is resolved.** Database coverage is approved in wording but conditional
   on access verification, and no access beyond PubMed is verified. The design-block question was
   resolved by **D023 (2026-11-13)**: the primary search carries no study-design block, so
   retrieval stands at approximately 8,190 records rather than 5,008 — counts-only interrogation
   figures, not search yields — and the number of additional eligible studies recovered is unknown and may be zero.

## 8.2 The review work

6. **No formal independent human screening exists.** All 194 title/abstract classifications were
   adopted from automated suggestions in bulk. **0 of 194** have been independently adjudicated.
7. **The verification sample is unanswered.** 0 of 120 response cells are complete, so no agreement
   rate, no kappa and no acceptance outcome exists. The acceptance thresholds (≥95% ADOPT, 90–94.9%
   EXTEND, <90% RE-SCREEN) are recorded but have never been applied.
8. **No full text has been retrieved or assessed.** 0 of 85.
9. **No study has been included.** 0.
10. **No datum has been extracted.** 0 estimates; `data/extraction/` does not exist.
11. **No risk of bias has been assessed**, and the instrument itself is undecided (P023).
12. **No meta-analysis has been performed.** No pooled estimate, heterogeneity statistic, forest
    plot or funnel plot exists, and none should be inferred from this report.

## 8.3 Limitations of the provisional automated suggestions

The 109/85 split is the output of an automated procedure applied to titles and abstracts. Four
cautions apply:

- It has **never been validated** against human judgement on this corpus. The instrument for doing
  so — the blinded sample — exists and is unanswered.
- Its error profile is unknown and may be **asymmetric**: a false exclusion removes a study
  permanently and invisibly, whereas a false inclusion is caught at full text.
- The reason codes it assigned are **suggestions**, not reviewer judgements, and a PRISMA exclusion
  table built from them would misrepresent their provenance.
- Adoption in bulk means a single action produced 194 records; there is no per-record evidence that
  any individual title was considered.

## 8.4 Methodological limitations

13. **REML has no external validation**, and the pooled estimate has no external reference check.
14. **No HKSJ interval, no Mantel–Haenszel or Peto method, no meta-regression, no dose–response
    model.**
15. **Ten anatomical and histological scope questions are open**, one of which affects 14 of the 85
    carried-forward reports.
16. **Not prospectively registered**, and the provisional screening pass preceded registration.
17. **Study-level per-variable provenance is unenforced.** Where two reports of one study disagree
    on a descriptive variable, the source is recorded by a convention in a free-text field that the
    validator cannot check. A mandatory stop is defined if more than three studies are affected.

---

# Chapter 9 — Conclusion and future work

## 9.1 What has been achieved

The project has delivered a complete, tested and reproducible research instrument, together with the
protocol it enforces:

- **A specified protocol.** Eighteen adopted decisions, four implemented-but-proposed, and
  twenty-two open questions tracked with the stage each blocks. Each decision records its
  rationale, its consequences and what it does not do.
- **An eligibility framework.** A PECO specification, a thirteen-code controlled vocabulary with
  stage restrictions, and an explicit statement of which criteria remain unsettled.
- **Literature-management infrastructure.** Checksum-gated acquisition that distinguishes
  inspecting a file from declaring it the research input, with a registry that can record a lost
  export honestly rather than substituting for it.
- **Deduplication and screening architecture.** An explicit identifier hierarchy; near-duplicates
  flagged rather than merged; and a screening model in which the basis of every decision is a
  recorded field, enforced at three independent points in the code.
- **A data-extraction schema.** 93 documented fields across three tables, with five marked
  unresolved and tied to the specific decision each awaits.
- **Provenance and reproducibility safeguards.** Immutable raw data, protected checksums,
  deterministic figure and workbook generation, and three gates that refuse rather than produce an
  empty result.
- **A reporting pipeline.** Manuscript, supplementary material, figures and a blank extraction
  workbook generated from source, with an independent harness that validates the produced files.
- **Automated validation.** 616 tests, 615 passing and one skipped by design, including regression
  tests that encode specific defects found during development.

**What has not been achieved is the scientific objective.** No study has been included and no
estimate pooled. The project has built the instrument and specified the protocol; it has not yet
conducted the review.

## 9.2 Future work

**Table 9.1 — Work required to produce a results-bearing systematic review, in dependency order.**

| # | Work | Blocks | Owner |
|---|---|---|---|
| 1 | Verify institutional access to Scopus/Web of Science and establish whether Embase is obtainable | P007 closure | Researcher |
| 2 | ~~Decide P013~~ — **resolved by D023 (2026-11-13)**: no design block; retrieval ≈8,190 rather than ≈5,008 records | Done | — |
| 3 | Resolve the ten anatomical and histological scope questions, including premalignant lesions | Full-text eligibility | Researcher |
| 4 | Decide P023: risk-of-bias instrument and confounder definition | Appraisal; schema finalisation | Researcher |
| 5 | Decide P003 and P004: comparator and exposure contrast | Extraction; the SAP | Researcher |
| 6 | Adopt or revise D016–D019; register or renumber D021 | Protocol completeness | Researcher |
| 7 | Register the protocol (P006) | Prospective status | Researcher |
| 8 | Execute the corrected search and register each export | New evidence base | Researcher |
| 9 | **Independently adjudicate all title/abstract records** | The formal PRISMA flow | **Reviewer — cannot be generated** |
| 10 | **Complete the 120 verification response cells and score agreement** | Acceptance verdict | **Reviewer** |
| 11 | Retrieve full texts and assess eligibility | Inclusion | Reviewer |
| 12 | Extract study and estimate data | Synthesis | Reviewer |
| 13 | Appraise risk of bias using the chosen instrument | Sensitivity analysis | Reviewer |
| 14 | Run the synthesis; cross-check REML externally | The pooled estimate | Researcher |
| 15 | Complete the manuscript with results, PRISMA checklist and limitations | Publication | Researcher |

Items 9 to 13 are the human reviewer's work and **cannot be automated or generated**. Until item 9
is done, the formal PRISMA flow will correctly continue to read zero.

## 9.3 Concluding statement

This project demonstrates that the integrity properties usually described in a methods section —
that raw data was not altered, that a suggestion was not mistaken for a judgement, that no result
was computed before the evidence supporting it existed — can be made properties of a system rather
than assurances in prose. The pipeline refuses to produce a pooled estimate it cannot justify, and
the clearest evidence that it works as intended is precisely the set of zeros reported in Chapter 5.

The scientific question remains open, and this report does not pretend otherwise.

---

## References

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for
   reporting systematic reviews. *BMJ*. 2021;372:n71.
2. Rethlefsen ML, Kirtley S, Waffenschmidt S, et al. PRISMA-S: an extension to the PRISMA statement
   for reporting literature searches in systematic reviews. *Syst Rev*. 2021;10:39.
3. Stroup DF, Berlin JA, Morton SC, et al. Meta-analysis of observational studies in epidemiology
   (MOOSE): a proposal for reporting. *JAMA*. 2000;283(15):2008–2012.
4. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of
   Interventions*. Version 6.5. Cochrane; 2024.
5. DerSimonian R, Laird N. Meta-analysis in clinical trials. *Control Clin Trials*.
   1986;7(3):177–188.
6. Cohen J. A coefficient of agreement for nominal scales. *Educ Psychol Meas*. 1960;20(1):37–46.
7. Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. *Stat Med*.
   2002;21(11):1539–1558.
8. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple,
   graphical test. *BMJ*. 1997;315(7109):629–634.

No primary study is cited: no study has been assessed for eligibility, so the review has no included
or excluded study references to list. The references above are the methodological sources on which
the design relies.

---

## Appendix A — Decision register summary

**Table A.1 — Adopted decisions (17).**

| ID | Subject |
|---|---|
| D001 | Preserve the original PubMed search as v1 |
| D002 | Raw exports are read-only |
| D003 | Adopt the evidence-provenance rules |
| D004 | Separate identifiers for records, reports, studies and estimates |
| D005 | A lost export is not recreated |
| D006 | Checksum registration semantics |
| D007 | Tests contain no bibliographic content |
| D008 | Outcome definition |
| D009 | Exposure definition |
| D010 | Single-reviewer screening and extraction |
| D011 | Separate registry entries for separate search executions |
| D012 | Re-execution export renamed |
| D013 | Retrieve unfiltered; language and species limits at screening |
| D014 | Identifier priority for deduplication |
| D015 | Python + SciPy as the statistical implementation |
| D020 | Sampling-frame digest for verification draws |
| D022 | Bounded supplementary grey-literature searching |

**Proposed, implemented and enforced but not adopted (4):** D016 (adopting a suggestion does not
satisfy a decision field), D017 (the suggested reason code is preserved alongside the recorded one),
D018 (full-text decisions record their basis), D019 (the PRISMA flow separates adjudicated from
provisional outcomes).

**Drafted, not entered in the register:** D021 — blinded verification acceptance methodology.

**Open questions (22):** P003, P004, P006, P007, P009, P010, P012, P014–P022, P023, plus
unnumbered matters including the stage assignment of exclusion reasons and the premalignant-lesion
scope question.
