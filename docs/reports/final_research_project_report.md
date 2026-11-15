# Is Smoked Tobacco Use Associated with Increased Risk of Squamous Cell Carcinoma of the Oral Cavity? A Systematic Review and Meta-Analysis Project

**End-semester research project report**

**Author.** Soppa Shiva Sai Koushik
**Date.** 14 November 2026
**Repository.** `HEAD` `b5afaff`, 34 commits
**Project status.** **Interim systematic review and meta-analysis project.** A research pipeline has
been developed and validated, and preliminary record-processing results are reported. **No study has
been included and no pooled estimate exists.**

---

## 2. Abstract

**Background.** Smoked tobacco is an established carcinogen of the upper aerodigestive tract, yet
estimates of its association with squamous cell carcinoma arising specifically in the oral cavity
remain dispersed across a literature that frequently pools outcomes across head-and-neck subsites,
restricts exposure to cigarettes, and adjusts inconsistently for alcohol, smokeless tobacco and
betel quid.

**Objective.** To determine whether smoked tobacco use is associated with an increased risk of
squamous cell carcinoma of the oral cavity, and — the objective actually pursued in this reporting
period — to construct a reproducible pipeline capable of answering that question without the
provenance failures that commonly undermine such reviews.

**Methods.** A protocol was specified in advance, with twenty-four adopted methodological decisions
recorded in a dated register. One PubMed search execution was registered with a SHA-256 checksum,
parsed, validated and deduplicated. An automated procedure produced a provisional classification for
every report; the architecture records, at field level, whether each decision was *adopted from an
automated suggestion* or *independently adjudicated by a human reviewer*, and the two are never
summed. A 93-field extraction schema, an inverse-variance meta-analysis module with fixed-effect
and random-effects models, and a subgroup-analysis module were implemented and tested.

**Results.** The registered search retrieved **194 records**, which resolved to **194 unique
reports** with **0 duplicate pairs**. An automated procedure classified **109** reports for exclusion
and **85** for retrieval. **None of these classifications has been independently adjudicated**, so
the formal PRISMA flow correctly reports **0 records screened** and **0 taken forward**. **0 full
texts have been retrieved, 0 studies included, 0 estimates extracted, 0 risk-of-bias assessments
made and no meta-analysis performed.** A blinded verification sample of 40 reports is drawn and
unanswered: **0 of 120 response cells complete**. The software comprises 7,292 lines of application
code and 6,000 lines of tests; the suite reports **670 tests passed, 1 skipped, from 671 collected**.

**Conclusion.** *No conclusion about the association between smoked tobacco and oral cavity squamous
cell carcinoma can be drawn from this work in its present state.* What has been achieved is a
specified protocol and a validated instrument in which the distinction between machine output and
human judgement is enforced by code, and in which three sequential gates refuse to produce a
synthesis the evidence does not support. **This is an interim project report, not a completed
systematic review or meta-analysis.**

**Keywords:** mouth neoplasms; carcinoma, squamous cell; smoking; tobacco products; systematic
review methodology; research reproducibility; PRISMA 2020.

---

## 3. Introduction

Systematic reviews are described as reproducible far more often than they are. Search strategies are
reported in prose that cannot be re-executed; screening decisions are recorded without the basis on
which they were made; the boundary between a tool's output and a reviewer's judgement is left to the
reader's assumption. As automated classification becomes ordinary in screening workflows, that last
point stops being a documentation nicety and becomes a question about what the recorded evidence
means.

If a screening worksheet shows 194 decisions and does not say how they arose, a reader cannot tell
whether a human read 194 abstracts or accepted 194 machine outputs in a single action. Those are
different bodies of evidence, and they look identical in the file.

This project addresses a substantive clinical question — whether smoked tobacco is associated with
oral cavity squamous cell carcinoma — through a pipeline built so that such confusions are
structurally impossible. The present report describes what that pipeline does, what it has
processed, and, equally importantly, what it has refused to produce.

---

## 4. Background and scientific rationale

### 4.1 The disease

Cancer of the oral cavity is among the more common malignancies worldwide, with incidence
distributed unevenly: the burden falls disproportionately on South and South-East Asia. The dominant
histological type is squamous cell carcinoma, arising from the mucosal epithelium lining the oral
cavity — the lips, anterior two-thirds of the tongue, floor of mouth, buccal mucosa, gingivae,
retromolar trigone and hard palate.

This anatomical definition matters more than it may appear. The oral cavity adjoins the oropharynx,
and the two are frequently reported together as "head and neck" cancer. They are not interchangeable
for aetiological purposes: oropharyngeal carcinoma has a substantial human papillomavirus-associated
component with a different risk-factor profile. A review pooling across these sites risks diluting
the association it sets out to measure.

### 4.2 The exposure

For the oral cavity specifically, the relevant exposure is broader than cigarette smoking. Bidis —
small hand-rolled cigarettes common in South Asia — chuttas, cigars and pipes are all combusted
tobacco products, and reverse smoking, in which the lit end is held inside the mouth, is practised
in parts of South India and is associated with palatal lesions.

A review restricted to cigarettes would exclude much of the most informative literature for the
populations where disease burden is greatest. This observation drives the exposure definition
adopted here, and it propagates into the search strategy, database selection and the grey-literature
decision, because the relevant studies are disproportionately published in journals with incomplete
international indexing.

*Sections 4.1 and 4.2 state established background knowledge. The decisions derived from them are
products of this project.*

---

## 5. Research question and objectives

> **Is smoked tobacco use associated with an increased risk of squamous cell carcinoma of the oral
> cavity?**

Framed as an **association**. No causal claim is made from observational data.

**Table 5.1 — Objectives and their status.**

| # | Objective | Status |
|---|---|---|
| O1 | Specify a protocol with explicit, recorded, dated decisions | **Achieved** — 24 adopted, 4 proposed, 12 open questions |
| O2 | Checksum-gated acquisition detecting any alteration of a raw export | **Achieved** |
| O3 | Deduplication with an explicit identifier hierarchy and no silent merging | **Achieved** |
| O4 | Screening architecture separating suggestion from decision at field level | **Achieved** |
| O5 | Blinded verification with a reproducible sampling frame | **Achieved** — sample drawn, responses outstanding |
| O6 | Complete extraction schema with declared provenance per field | **Achieved** — 93 fields |
| O7 | Meta-analytic computation with declared validation and limitations | **Achieved** — implemented, never run on research data |
| O8 | Reproducible generation of manuscript, figures and workbooks | **Achieved** |
| O9 | **Produce a pooled estimate answering the review question** | **NOT ACHIEVED** |

O9 is the scientific objective. It is not met, and this report does not present it as met.

---

## 6. Review methodology

Designed as a systematic review with meta-analysis of observational studies, following **PRISMA
2020** for reporting, **PRISMA-S** for the search, **MOOSE** for observational specifics, and the
**Cochrane Handbook v6.5** for synthesis.

The protocol was specified before screening: the protocol directory was committed 29 October 2026,
the screening records 1 November 2026.

**The review is not prospectively registered.** Registration is an open question, and the provisional
screening pass preceded it. This is a protocol deviation and is reported as one.

### 6.1 The decision register

Every material methodological decision is recorded with its rationale, consequences, and an explicit
statement of what it does *not* cover.

**Table 6.1 — Decision register at 14 November 2026.**

| Status | Identifiers | Count |
|---|---|---|
| **Adopted** | D001–D015, D020, D022–D029 | **24** |
| Proposed — implemented and enforced, not adopted as protocol | D016–D019 | 4 |
| Drafted, not entered in the register | D021 — blinded verification acceptance methodology | 1 |
| **Open questions** | P006, P007, P014–P022, P023 | **12** |

---

## 7. Eligibility criteria

**Table 7.1 — PECO framework.**

| Element | Criterion | Status |
|---|---|---|
| **P**opulation | Human adults; no restriction by country, sex or setting | Settled |
| **E**xposure | Any smoked tobacco: cigarettes, bidis, cigars, pipes, other combusted products (D009) | Settled |
| **C**omparator | Never-smokers, and/or study-defined "non-smokers"; recorded verbatim. Primary analysis restricted to never-smoker references | Settled (D025) |
| **O**utcome | Oral cavity cancer, SCC histologically confirmed or a stated majority ≥90% (D008) | Settled in part |
| Contrast | Ever versus never (primary); current and former versus never (secondary) | Settled (D026) |
| Designs | Case–control; cohort, prospective or retrospective | Settled |
| Effect data | OR, RR or HR with 95% CI, or data to compute one | Settled |
| Language | English (D013) | Settled |

Estimates pooled across head-and-neck subsites are **ineligible** unless an oral-cavity-specific
estimate is reported separately. Smokeless tobacco and betel quid are **confounders, not exposures**.

### 7.1 Controlled vocabulary

Exclusion is recorded against thirteen fixed codes; free text may not substitute. Nine are available
at title and abstract; four — `outcome_not_separable`, `no_reference_group`, `no_usable_data`,
`duplicate_publication` — are **restricted to full text**, because they cannot be judged from an
abstract without guessing. The vocabulary itself therefore prevents a premature judgement.

### 7.2 Criteria not yet settled

Ten questions of anatomical and histological scope remain open, including whether populations
restricted to premalignant oral lesions are in scope — which affects **14 of the 85** reports
provisionally carried forward. All must be resolved before full-text eligibility assessment begins.

---

## 8. Information sources and search strategy

**One bibliographic database, PubMed, has been searched.** A single database does not constitute a
systematic search.

**Table 8.1 — Search executions.**

| Execution | Filters | Records | Status |
|---|---|---|---|
| v1 (original) | Humans, English | 138 | **Export lost**, and its execution date is **unknown and unrecoverable** (D027). Not recreated; contributes no records |
| **v1r (re-execution)** | **none** | **194** | **Registered with a checksum — the evidence base for all results below** |
| v2 draft | none | — | Drafted; counts-only validation 29 Oct 2026. **Superseded** |
| **Corrected strategy (adopted, D023/D024)** | none | — | **Adopted; never executed** |

### 8.1 Limitations of the executed query

The v1 string is substantially narrower than the eligibility criteria it serves. It requires the
literal phrase "Oral Squamous Cell Carcinoma" or "OSCC"; **68 of the 194** retrieved records use the
phrase "oral cancer" — the dominant phrasing in aetiological epidemiology — and were retrieved only
incidentally. It reduces the exposure to "smoking" or "cigarette", omitting bidi, cigar and pipe
terms central to the exposure definition, and uses no controlled vocabulary. **98 of 194** matched
the design block only through the single word "cohort", which also captures prognostic studies of
people who already have the disease.

**Any synthesis based on this record set alone would rest on a search that does not match its own
protocol.** This is the most consequential limitation of the current evidence base.

### 8.2 The adopted corrected strategy

A corrected strategy has been prepared, syntax-validated and adopted (**D023**: no study-design
block; **D024**: removal of one ineffective quoted phrase). It has **not been executed**.

Per-line validation of all 88 lines of the adopted query, by counts-only interrogation on 14
November 2026, found **exactly one dead term** — `"epidermoid carcinoma of the mouth"[tiab]`, which
PubMed reported as `QuotedPhraseNotFound`. It was removed under D024, with zero effect on retrieval
because it matched nothing.

> **On interrogation figures.** Counts-only interrogations returned 8,190 records for the corrected
> strategy without a design block and 5,008 with one (12 November 2026); a web-interface check
> returned 8,195 (14 November 2026). **None of these is a search yield.** No record was retrieved,
> exported or screened, and no registry entry exists for any of them. They are counts read back from
> a query on a date, and they must never be reported as records identified.

### 8.3 Database coverage status

| Source | Searched | Access |
|---|---|---|
| PubMed / MEDLINE | **Yes** — one registered execution | **Confirmed** (free) |
| Embase | No | **No evidence of access** — not listed by the institution |
| Scopus | No | Publicly advertised; **unverified** |
| Web of Science | No | Publicly advertised; **unverified** |
| IndMED | No | **Reachability untested** |
| Cochrane CENTRAL | No | **Not recommended** — registers trials; design mismatch |

Database-specific translations exist for all five databases; four are untested drafts. **P007 —
which databases the review will search — remains open.**

---

## 9. Record acquisition and deduplication

**Table 9.1 — Acquisition.**

| Property | Value | Source |
|---|---|---|
| Registered export | `pubmed-v1r-reexecution-194.nbib` | `config/sources.yaml` |
| File size | 958,710 bytes | filesystem |
| SHA-256 | `1d153fa80edd6bc97c92498bce8076873cc514f412de5113412fa71827e4ca1e` | `data/raw/SHA256SUMS` |
| Records in export | **194** | parsed count |
| Unique PMIDs | **194** | parsed records |

**Table 9.2 — Composition of the export.** The language and indexing distribution follows directly
from D013 (retrieve unfiltered, exclude at screening) and explains why exclusion reasons appear that
a filtered search would never have surfaced.

| Property | Count |
|---|---|
| English | 191 |
| Chinese | 2 |
| English and Portuguese | 1 |
| Carrying MeSH indexing | 152 |
| **No MeSH indexing at all** | **42 (21.6%)** |

**Table 9.3 — Deduplication.**

| Metric | Value |
|---|---|
| Records entering | 194 |
| Pairs merged on identifier or exact fingerprint | **0** |
| Pairs flagged `needs_review` | **0** |
| **Unique reports** | **194** |

Matching proceeds normalised DOI → PMID → exact title+author+year fingerprint. Similar-but-not-identical
titles are flagged `needs_review` and **never merged automatically**, because an automatic merge on a
near-match can silently delete a distinct study. Zero duplicates is the expected result for a
single-database search; the rules are evidenced by 63 tests, not by this outcome.

---

## 10. Title-and-abstract screening

**This section reports the single most important distinction in the project.**

**Table 10.1 — Title/abstract stage: formal versus provisional.**

| Quantity | Formal | Provisional |
|---|---|---|
| Reports with a recorded classification | **0** | 194 |
| Classified for exclusion | **0** | 109 |
| Classified for retrieval | **0** | 85 |
| Unresolved | 0 | 0 |
| Rows failing validation | 0 | — |

All 194 rows carry `decision_basis = adopted_from_suggestion`; **0 carry
`independently_adjudicated`**. Under D010 and D016 a suggestion cannot satisfy a decision field, so
the formal PRISMA flow reports 0 screened. The validator `validate_screening --stage ta --final`
**fails on this state, by design**.

**Table 10.2 — Provisional exclusion reasons.** These are reason codes attached to automated
suggestions adopted in bulk. **They are not reviewer judgements and must not be reported as a PRISMA
exclusion table.**

| Reason code | Count | Share of 109 |
|---|---|---|
| `wrong_outcome` | 63 | 57.8% |
| `wrong_design` | 33 | 30.3% |
| `review_or_meta` | 10 | 9.2% |
| `not_english` | 2 | 1.8% |
| `wrong_population` | 1 | 0.9% |
| **Total** | **109** | **100%** |

### 10.1 How adjudication is enforced

A row counts as independently adjudicated only when **all five** of `decision`, `reviewer`,
`screened_date`, `decision_basis = independently_adjudicated` and `adjudicated_date` are recorded.
The separate `adjudicated_date` exists so that flipping the basis on a row already carrying the
bulk-adoption reviewer and date cannot convert a provisional record into a formal one without dating
the new act. One shared function applies these rules for the validator, the full-text carry-forward
and the PRISMA gatherer, so the three cannot disagree.

### 10.2 Blinded verification

**Table 10.3 — Verification sample.**

| Property | Value |
|---|---|
| Reports sampled | **40** of 194 (20.6%) |
| Response columns | 3 |
| **Total response cells** | **120** |
| **Cells completed** | **0** |
| Agreement rate, kappa, acceptance outcome | **Do not exist** |

The draw is reproducible from a recorded seed and a canonical sampling-frame digest. Acceptance
thresholds (≥95% ADOPT, 90–94.9% EXTEND, <90% RE-SCREEN) are recorded but have never been applied.

---

## 11. Full-text eligibility status

**Table 11.1 — Five mutually exclusive attribution states, decided per row rather than by
subtraction.**

| State | Count |
|---|---|
| `ft_sought` (valid, adjudicated include) | **0** |
| `ft_provisional_sought` (valid include, adopted basis) | **85** |
| `ft_invalid_source` | 0 |
| `ft_ineligible_source` | 0 |
| `ft_unattributed` | 0 |
| **Total rows** | **85** |

**Full texts retrieved: 0. Eligibility decisions recorded: 0.** Every reviewer field in the
full-text worksheet is empty.

---

## 12. Data extraction framework

**Table 12.1 — Extraction schema.**

| Table | Fields | Data rows | Schema source |
|---|---|---|---|
| `studies` | **34** | **0** | `config/extraction.yaml` → `studies` |
| `estimates` | **47** | **0** | `config/extraction.yaml` → `estimates` |
| `risk_of_bias` | **12** | **0** | `config/extraction.yaml` → `risk_of_bias` (**provisional, P023**) |
| **Total documented fields** | **93** | **0** | `data_dictionary.csv` |

**`data/extraction/` does not exist.** This is the correct state: the directory is created only when
a study has been included.

Three fields are marked `unresolved` because they depend on a decision not yet made: `tool`,
`domain` and `judgement` (all P023). `comparator_type` and `exposure_contrast` were settled by D025
and D026 (14 November 2026) and are now enforced.

A blank workbook ships with the project — three header-only CSV templates, a 93-row data dictionary
and a README — generated deterministically by `scripts/reporting/build_workbook.py`, which **asserts**
the headers-only guarantee rather than assuming it.

---

## 13. Risk-of-bias methodology and current status

**Status: not started. The instrument has not been chosen.**

P023 asks which instrument applies to case–control and cohort studies — Newcastle–Ottawa, ROBINS-E,
or Newcastle–Ottawa reported per domain without a total score — and which confounders a study must
address for its comparability domain to be judged adequate.

The schema carries **12 structural fields** — who assessed what, when, and on what evidence — marked
`status: provisional`, `depends_on: P023`. **The instrument's domain names and judgement categories
are deliberately absent**, because they come from whichever instrument is chosen and are never
invented. A test asserts that no known instrument is named anywhere in the generated workbook.

**0 risk-of-bias assessments exist.**

---

## 14. Statistical analysis methodology

Everything in this section is **implemented and tested**. **None of it has been run on research
data**, because no estimate exists.

### 14.1 Effect measures

Only ratio measures are pooled — **OR, RR, HR** — each on the **log scale**, where the sampling
distribution is approximately normal, exponentiated only for presentation. Mixing measures in one
analysis is **refused**: they estimate different quantities.

**Three routes to a standard error:**

| Route | Method |
|---|---|
| `from_ci` | SE from the reported 95% CI on the log scale |
| `from_counts` | SE from the 2×2 table: √(1/a + 1/b + 1/c + 1/d) |
| `from_log_se` | SE as reported |

Derived values are never typed by hand; the formula and inputs are recorded in a `derivation` field.
A consistency check compares the reported estimate against the geometric mean of its interval and
flags asymmetry beyond 10%.

### 14.2 Zero cells

A zero cell makes ln(OR) undefined. **No continuity correction is applied automatically.** The code
refuses the table and names the alternatives — a 0.5 correction, Mantel–Haenszel, or Peto — leaving
the choice to the reviewer as a recorded decision. **Consequence:** a study with a zero cell cannot
currently contribute, because neither Mantel–Haenszel nor Peto is implemented.

### 14.3 Pooling and heterogeneity

| Component | Status |
|---|---|
| Fixed-effect inverse-variance | Implemented |
| Random-effects inverse-variance with τ² | Implemented |
| τ² by **DerSimonian–Laird** | Implemented |
| τ² by **REML** | Implemented — **no external validation** |
| **Cochran's Q** with χ² p-value | Implemented |
| **I²** | Implemented |
| **Prediction interval** | Implemented, requires ≥3 studies |
| **Leave-one-out** sensitivity | Implemented |
| Egger's test | Implemented — **refuses below 10 studies** |

A random-effects model is anticipated: observational studies differing in population, design and
adjustment make an assumption of one common true effect implausible. The τ² estimator is always
named in output. The 25/50/75% I² bands are treated as descriptive guidance, not decision
thresholds.

### 14.4 Multiple estimates from one study

A study reporting several estimates is normal, not an error: different contrasts, adjustment sets and
subsites all produce separate rows. **They are correlated**, and pooling them as independent studies
would understate the standard error.

Three safeguards: a repeated `study_id` in a pooled set is **refused**; `select_one_per_study`
requires the reviewer's recorded primary marker and **refuses to guess**, naming every candidate; and
**nothing is discarded silently** — the refusal states so explicitly.

The project's position is **selection, not modelling of dependence**. No multivariate or
robust-variance method is implemented.

### 14.5 Adjusted versus crude

The analysis layer now carries `adjustment`, the verbatim covariate list, the adjustment-set label,
a primary-estimate marker, alcohol-adjustment status, and full provenance back to a report and page.
**Pooling adjusted with crude estimates is refused by default**, naming the studies on each side;
overriding requires an explicit flag so that doing so is a deliberate, visible act.

### 14.6 Subgroup analyses

Five subgroups are prespecified in the protocol. **All five have machinery; two can run today.**

| Subgroup | Status |
|---|---|
| Product type (cigarette-only vs mixed) | **Ready** |
| Alcohol-adjusted vs not | **Ready** |
| Anatomical subsite | **Blocked — P014–P022**, no settled category set |
| Geographical region | **Blocked** — no country-to-region scheme chosen |
| Risk-of-bias level | **Blocked — P023** |

A between-group Cochran's Q tests for subgroup differences, computed only when at least two groups
meet the minimum study count. Unclassifiable estimates go to an explicit missing bucket, excluded
from the test and reported — never imputed.

> Every subgroup result carries the warning that **comparing whether each subgroup's interval
> excludes the null is not evidence of a difference.**

### 14.7 Criteria for not pooling

Pooling is inappropriate, and a narrative synthesis reported instead, if fewer than three studies
contribute to a contrast; if the available estimates mix non-comparable exposure categories; if they
mix adjusted and unadjusted without a defensible basis; if comparator definitions are irreconcilable;
or if heterogeneity is so extreme that a summary would misrepresent the evidence. **Deciding not to
pool is a legitimate result.**

---

## 15. Results and numerical progress

**Every value below was recomputed from the repository on 14 November 2026.**

**Table 15.1 — Verified numerical results.**

| # | Quantity | Value | Source |
|---|---|---|---|
| 1 | Records identified | **194** | `config/sources.yaml` → `pubmed_v1r` |
| 2 | Records imported and parsed | **194** | `pubmed_v1r_citations.csv` |
| 3 | Unique reports after deduplication | **194** | `dedup/report_index.csv` |
| 4 | Duplicate pairs removed | **0** | `dedup/dedup_audit.csv` |
| 5 | Provisional classifications | **194** | `screening_ta.csv` |
| 6 | Provisional exclusions | **109** | `screening_ta.csv` |
| 7 | Reports carried forward (provisional) | **85** | `screening_ta.csv` |
| 8 | **Independently adjudicated decisions** | **0** | `screening_ta.csv` |
| 9 | **FORMAL records screened (PRISMA)** | **0** | `prisma.gather()` |
| 10 | Full-text rows, provisionally sought | **85** | `screening_ft.csv` |
| 11 | Full texts formally sought | **0** | `prisma.gather()` |
| 12 | Full texts retrieved | **0** | `screening_ft.csv` |
| 13 | Full texts assessed | **0** | `screening_ft.csv` |
| 14 | **Included studies** | **0** | `data/extraction/` absent |
| 15 | Extraction records | **0** | `data/extraction/` absent |
| 16 | Risk-of-bias assessments | **0** | `data/extraction/` absent |
| 17 | **Pooled meta-analytic estimates** | **0** | no estimates exist |
| 18 | Verification sample | **40** reports (20.6%) | `verification_sample.csv` |
| 19 | Verification response cells | **120** | 40 × 3 |
| 20 | **Verification cells completed** | **0** | `verification_sample.csv` |
| 21 | Study-level schema fields | **34** | `config/extraction.yaml` |
| 22 | Estimate-level schema fields | **47** | `config/extraction.yaml` |
| 23 | Risk-of-bias schema fields | **12** | `config/extraction.yaml` |
| 24 | Total documented fields | **93** | data dictionary |
| 25 | Test suite | **670 passed, 1 skipped, from 671 collected** | pytest |
| 26 | Adopted decisions | **19** | `decision_log.md` |
| 27 | Open questions | **22** | `decision_log.md` |

**Items 14–17 are zero because the work has not been done, not because the search found nothing.**
These are absences of evidence, not evidence of absence.

![Figure 15.1. Current state of the evidence base. Left: record attrition, with provisional counts distinguished from formal ones. Right: reviewer work completed against work outstanding. Every bar is recomputed from the repository at build time.](results/final_submission/figures/record_status.png)

**What Figure 15.1 means.** The left panel's last two bars are zero not because the search found
nothing, but because the human work that would make them non-zero has not been done. The right panel
makes the same point from the other direction: one row is complete, and it is the row recording
machine output rather than human judgement.

### 15.1 Technical validation

**Table 15.2 — Pipeline validation.**

| Check | Result |
|---|---|
| NBIB parser — records parsed | 194 of 194 |
| Unique PMIDs recovered | 194 of 194 |
| Field validation | passed; reports in `results/validation/` |
| Deduplication — record conservation | 194 in, 194 unique out, 0 lost |
| Pairs requiring human review | 0 |
| **Raw export checksum** | **verified OK** against `data/raw/SHA256SUMS` |
| Screening and processed data files | **8 present; SHA-256 recorded for 3 in the supplementary material and verified; no persistent manifest covers the rest** |
| Verification-seed constants | **5 of 5 unchanged** |
| Deterministic figure generation | byte-identical on rebuild |
| Deterministic workbook generation | byte-identical on rebuild |
| **Test suite** | **670 passed, 1 skipped, from 671 collected** |

The single skipped test is skipped **by design**: it is the raw-source test for `pubmed_v1`, whose
export is recorded as missing, and a test demanding a lost file would be a false failure.

### 15.2 What is not reported

**No odds ratio, risk ratio, hazard ratio, confidence interval, p-value, I², τ², pooled estimate,
forest plot of research data or funnel plot appears anywhere in this report as a finding, because no
eligible study estimate exists.** Publication bias has **not** been assessed. **No such value of
any kind, synthetic or otherwise, appears anywhere in this document.**

---

## 16. Technical architecture and implementation

![Figure 16.1. Pipeline architecture. Fifteen stages coloured by what the repository actually does: green where the code exists and has run on real data, amber where implemented and tested but never run, grey where no implementation exists.](results/final_submission/figures/pipeline_architecture.png)

![Figure 16.2. Data flow across four custody classes. Immutable inputs are checksum-gated; generated data is regenerable; human research records are tracked precisely because they cannot be regenerated. The suggestion file is deliberately separate from the decision file.](results/final_submission/figures/data_flow.png)

### 16.1 Technology stack

![Figure 16.3. Technology stack as actually present in the repository.](results/final_submission/figures/tech_stack.png)

**Table 16.1 — Components, verified against actual imports.**

| Component | Version | Used for |
|---|---|---|
| Python | **3.14.7** | All application code |
| Standard library `csv` | — | **All tabular data handling** |
| `hashlib` (SHA-256) | — | Export registration, frame digests |
| `zipfile` | — | DOCX and PPTX generation as OOXML |
| `difflib` | — | Near-duplicate title similarity |
| `unicodedata` | — | NFC normalisation in digests |
| PyYAML | **6.0.3** | `config/*.yaml` |
| pytest | **9.1.1** | Test suite |
| SciPy | **1.18.1** | χ², normal and t distributions; `linregress` |
| Matplotlib | **3.11.2** | All figures; PDF typesetting |
| Git | — | Version control, 34 commits |

**Deliberately absent, and stated because claiming unused tooling would itself be a reproducibility
failure:** **pandas is not used anywhere** — no module imports it, and all tabular work uses the
standard-library `csv` module. **NumPy is not a direct dependency**; it arrives transitively under
SciPy and Matplotlib. **No third-party document library** — DOCX and PPTX are written directly as
OOXML through `zipfile`, a constraint worked within rather than around.

### 16.2 Source map

| Package | Files | Lines | Responsibility |
|---|---|---|---|
| `scripts/common/` | 2 | 163 | Repository root, source registry, `PipelineError` |
| `scripts/acquisition/` | 4 | 551 | Raw export inspection, count and checksum gate |
| `scripts/validation/` | 2 | 239 | Citation field validation, query diagnostics |
| `scripts/dedup/` | 4 | 648 | Identifier hierarchy, fingerprinting |
| `scripts/screening/` | 9 | 2,283 | Worksheets, vocabulary, adjudication, PRISMA |
| `scripts/extraction/` | 4 | 594 | Schema loading, templates, validation |
| `scripts/analysis/` | 6 | ~900 | Effect sizes, pooling, heterogeneity, subgroups |
| `scripts/visualization/` | 2 | 281 | PRISMA flow diagram |
| `scripts/reporting/` | 6 | 1,827 | Manuscript, presentation, workbook, figures |
| `tests/` | 22 | ~6,000 | 671 collected tests |

### 16.3 The three gates

The architectural core. Each raises an error and exits non-zero rather than producing an empty
artefact:

1. **Extraction refuses without full-text includes.**
2. **Synthesis refuses without extracted estimates.**
3. **The analysis CLI rejects any row marked synthetic.**

The purpose is that *"we found no association"* and *"we have not looked"* can never be confused in
the output.

---

## 17. Validation and software testing

**670 tests passed, 1 skipped, from 671 collected**.

Test weight is concentrated where silent error is most costly: 110 tests on screening accounting, 62
on the extraction schema, 63 on deduplication, 48 on the analysis mathematics, 44 on verification
sampling, 30 on subgroups and adjustment handling, 24 on the search strategy, and 20 on draw
provenance.

### 17.1 Regression tests encoding specific defects

Several tests exist because a specific defect was found and fixed:

- **Banner arithmetic.** A PRISMA banner once read "0 of 194 reports carry a decision, but 194 were
  adopted" — a self-contradiction that reached an embedded figure. Two tests now lock the corrected
  wording.
- **Workbook provenance.** The extraction workbook once claimed to be generated by a script that
  contained no reference to it. A test now asserts the README names the real generator.
- **Headers-only guarantee.** A test monkeypatches the workbook writer to smuggle a data row and
  asserts the generator refuses.
- **Instrument neutrality.** A test asserts no known risk-of-bias instrument is named anywhere in the
  generated workbook, so the schema cannot imply a decision P023 has not made.
- **Search-strategy integrity.** 24 tests assert the removed term is absent, the retained term
  present, the unquoted variant not added, no design block reintroduced, and the two operative query
  copies byte-identical.

### 17.2 Reproducibility

Pinned dependencies; checksum-gated raw data; deterministic generation verified by rebuilding to a
clean path and comparing bytes for the PRISMA figure, the extraction workbook and the report
figures; and a decision register with dated entries.

---

## 18. Discussion

The central contribution of this reporting period is methodological. The project treats the
distinction between a machine suggestion and a human judgement as a **data-integrity property
enforced by code**, rather than a convention observed by the operator. A `decision_basis` field is
required on every screening row; five fields must be present before a row counts as adjudicated; one
shared function applies the rule in three places so they cannot disagree; and the PRISMA flow splits
formal from provisional counts so that neither can be read as the other.

The consequence is visible in this report's results: a worksheet containing 194 completed rows yields
a formal screening count of **zero**. That number is uncomfortable and correct. A pipeline that
would report 194 screened on this data would be a worse instrument, and the clearest evidence the
design works is precisely the set of zeros in Table 15.1.

The same philosophy produced three refusals that would otherwise be conveniences: extraction refuses
without included studies, synthesis refuses without estimates, and zero cells are refused rather than
silently corrected with a continuity adjustment that would change an estimate without record.

Against this, the project's scientific progress is genuinely limited. One database has been searched,
with a query the project itself has shown to be narrower than its own protocol. The record set that
exists will be replaced when the adopted strategy is executed. No reviewer judgement has yet been
exercised on any record.

---

## 19. Methodological limitations

1. **One database.** PubMed only. A single database does not constitute a systematic search, and the
   shortfall falls hardest on the South Asian literature the exposure definition was written to
   capture.
2. **The executed query is narrower than its own protocol** — the most consequential limitation.
3. **The original v1 export is lost**, recorded as lost and not substituted; a residual discrepancy
   of about nine records remains unexplained.
4. **No subscription database access is verified.** P007 is open.
5. **No formal independent human screening exists.** 0 of 194 adjudicated.
6. **The verification sample is unanswered** — 0 of 120 cells, so no agreement rate or kappa exists.
7. **No full text retrieved or assessed; no study included; no datum extracted; no risk of bias
   assessed; no meta-analysis performed.**
8. **Automated suggestions are unvalidated on this corpus**, and their error profile may be
   asymmetric: a false inclusion is caught at full text, but **a false exclusion removes a study
   permanently and invisibly**.
9. **REML has no external validation**; the pooled estimate has no external reference check.
10. **No Hartung–Knapp interval, no Mantel–Haenszel or Peto method, no meta-regression, no
    dose–response model, no multivariate handling of correlated estimates.**
11. **Ten anatomical and histological scope questions are open**, one affecting 14 of 85 reports.
12. **Not prospectively registered**, and the provisional pass preceded registration.
13. **Single reviewer** (D010), reported under PRISMA items 8 and 9.

---

## 20. Future work

**Table 20.1 — Work required to produce a results-bearing review, in dependency order.**

| # | Work | Owner |
|---|---|---|
| 1 | Verify database access; close **P007** | Researcher |
| 2 | Resolve **P014–P022** and the premalignant-lesion question | Researcher |
| 3 | Decide **P023** — risk-of-bias instrument | Researcher |
| 4 | ~~Decide **P003**, **P004**~~ — **resolved by D025 and D026 (2026-11-14)**: comparator and contrast settled | — |
| 5 | Adopt or revise **D016–D019**; register or renumber **D021** | Researcher |
| 6 | Register the protocol (**P006**) | Researcher |
| 7 | Measure a screening rate on a 200-record sample (D023 condition) | Reviewer |
| 8 | Execute the adopted search; register each export under D011 | Researcher |
| 9 | **Independently adjudicate every title/abstract record** | **Reviewer — cannot be generated** |
| 10 | **Complete the 120 verification cells and score agreement** | **Reviewer** |
| 11 | Retrieve full texts; assess eligibility | Reviewer |
| 12 | Extract study and estimate data | Reviewer |
| 13 | Appraise risk of bias | Reviewer |
| 14 | Run the synthesis; cross-check REML externally | Researcher |

Items 9–13 are the human reviewer's work and **cannot be automated or generated**.

**One ordering recommendation.** The existing 194 records should **not** be adjudicated yet. They
come from the superseded v1 query, and the adopted strategy will replace the record set. Settle P007,
execute the search, and adjudicate once.

---

## 21. Conclusion

This project has delivered a specified review protocol and a validated research instrument. Twenty-four
adopted decisions are recorded with their rationale and scope; acquisition is checksum-gated;
deduplication is explicit and never silent; screening separates machine suggestion from human
judgement at field level and enforces that separation at three independent points; a 93-field
extraction schema is complete; and an inverse-variance meta-analysis module with fixed-effect and
random-effects models, heterogeneity statistics, prediction intervals, leave-one-out sensitivity
analysis and subgroup machinery is implemented and tested across 670 tests.

**The scientific question remains open.** No study has been judged eligible, no datum extracted and
no estimate pooled. This is an **interim systematic review and meta-analysis project**, not a
completed systematic review and not a completed meta-analysis, and nothing in this report should be
read as reporting an association between smoked tobacco and oral cavity squamous cell carcinoma.

What the work demonstrates is that the integrity properties usually asserted in a methods section —
that raw data was not altered, that a suggestion was not mistaken for a judgement, that no result
was computed before the evidence supporting it existed — can be made properties of a system rather
than assurances in prose.

---

## 22. References

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

**No primary study is cited**, because no study has been assessed for eligibility. The references
above are the methodological sources on which the design relies. No reference in this report was
invented; each is a standard, verifiable methodological source.

---

## 23. Supplementary material

| # | Content | Status |
|---|---|---|
| S1 | Search strategies: v1 as documented, v1r as executed, the adopted corrected strategy, with validation records | Available |
| S2 | Database-specific translations: PubMed, Embase, Scopus, Web of Science, IndMED | Available |
| S3 | Controlled vocabulary of screening decisions, exclusion reasons and decision bases | Available |
| S4 | Screening worksheet with per-record classification and decision basis | Available |
| S5 | Automated suggestion set, retained as an audit artefact | Available |
| S6 | Blinded verification sample and its acceptance rule | Drawn; **unanswered** |
| S7 | Decision register: 24 adopted, 4 proposed, 12 open, each dated | Available |
| S8 | Extraction schema, data dictionary and blank workbook | Available |
| S9 | Characteristics of included studies | **Not yet available** |
| S10 | Risk-of-bias assessments | **Not yet available** |
| S11 | Statistical analysis specification and validation record | Available |
| S12 | PRISMA 2020 and PRISMA-S checklists | To be completed on submission |
