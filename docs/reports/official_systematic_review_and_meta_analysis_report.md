# Is Smoked Tobacco Use Associated with Increased Risk of Squamous Cell Carcinoma of the Oral Cavity?

## A Systematic Review and Meta-Analysis — Protocol, Methodology and Interim Report

**Official combined scientific report**

| | |
|---|---|
| **Author** | Soppa Shiva Sai Koushik |
| **Report date** | 14 November 2026 |
| **Repository** | `HEAD` `b5afaff`, 34 commits |
| **Document type** | Single integrated systematic review and meta-analysis report |
| **Review status** | **Protocol and infrastructure complete; evidence synthesis not commenced** |

---

## Project status statement

This document reports a systematic review and meta-analysis **in progress**. It is **not** a
completed systematic review and **not** a completed meta-analysis.

The following are true of the project at the date of this report, and each is verified against the
repository in Chapter 6:

- **No study has been judged eligible for inclusion.**
- **No effect estimate has been extracted.**
- **No risk-of-bias assessment has been made.**
- **No pooled clinical estimate, forest plot of research data, heterogeneity statistic or p-value
  exists**, and none appears in this report as a finding.
- **No title or abstract has been independently adjudicated by a human reviewer.** A set of 194
  provisional automated classifications exists; under the project's own rules these do **not**
  constitute screening.
- **The formal multi-database search has not been executed.** One historical PubMed export is
  available and registered.

A clinical conclusion about the association between smoked tobacco and oral cavity squamous cell
carcinoma is therefore **not drawn anywhere in this document**, and would be unsupported if it were.

What has been completed is a specified protocol, a validated record-processing and screening
architecture, a complete data-extraction schema, and a tested statistical implementation. Those are
reported here in full, together with an explicit account of what remains.

---

## Abstract

**Background.** Smoked tobacco is an established carcinogen of the upper aerodigestive tract.
Estimates of its association with squamous cell carcinoma arising specifically in the oral cavity
remain dispersed across a literature that frequently pools outcomes across head-and-neck subsites,
restricts exposure to cigarettes, and adjusts inconsistently for alcohol, smokeless tobacco and
betel quid.

**Objectives.** The scientific objective is to determine whether smoked tobacco use is associated
with increased risk of oral cavity squamous cell carcinoma. The objective achieved in the present
reporting period is the specification of a protocol and the construction and validation of a
reproducible review pipeline capable of answering that question without the provenance failures that
commonly undermine such reviews.

**Methods.** A protocol was specified in advance and recorded as twenty-four dated, adopted decisions.
One PubMed search execution was registered with a SHA-256 checksum, parsed, validated and
deduplicated. An automated procedure produced a provisional classification for every report. The
architecture records at field level whether each decision was *adopted from an automated suggestion*
or *independently adjudicated by a human reviewer*, and never sums the two. A 93-field extraction
schema, an inverse-variance meta-analysis module implementing fixed-effect and random-effects models
with DerSimonian–Laird and restricted maximum likelihood estimators of between-study variance, and a
subgroup-analysis module were implemented and tested.

**Results.** The registered historical search retrieved **194 records**, resolving to **194 unique
reports** with **0 duplicate pairs** and complete record conservation. An automated procedure
classified **109** reports for exclusion and **85** for retrieval. **None has been independently
adjudicated**, so the formal PRISMA flow reports **0 records screened** and **0 taken forward**.
**0 full texts have been sought, retrieved or assessed; 0 studies included; 0 estimates extracted; 0
risk-of-bias assessments made; and no meta-analysis performed.** A blinded verification sample of 40
reports is drawn and unanswered: **0 of 120 response cells complete**. The statistical software
passes **670 tests, with 1 skipped by design, from 671 collected**.

**Conclusion.** **No conclusion regarding the association between smoked tobacco and oral cavity
squamous cell carcinoma can be drawn from this work in its present state.** The review has delivered
a specified protocol and a validated instrument in which the distinction between machine output and
human judgement is enforced in code, and in which three sequential gates refuse to produce a
synthesis the evidence does not support. The remaining work is enumerated as a prioritised roadmap.

**Keywords:** mouth neoplasms; carcinoma, squamous cell; smoking; tobacco products; bidi; systematic
review; meta-analysis methodology; research reproducibility; PRISMA 2020; evidence synthesis.

---

## Table of contents

| Chapter | Title |
|---|---|
| — | Project status statement · Abstract · Keywords |
| — | List of tables · List of figures · List of abbreviations |
| **1** | **Introduction** |
| 1.1 | Background |
| 1.2 | Oral cavity squamous cell carcinoma |
| 1.3 | Smoked tobacco exposure |
| 1.4 | Biological and epidemiological rationale |
| 1.5 | Research gap |
| 1.6 | Research question |
| 1.7 | Aim and objectives |
| 1.8 | Significance |
| **2** | **Literature and methodological background** |
| 2.1 | Relevant epidemiological concepts |
| 2.2 | Exposure and outcome definitions |
| 2.3 | Systematic review methodology |
| 2.4 | Rationale for meta-analysis |
| 2.5 | Effect measures and their interpretation |
| **3** | **Protocol and eligibility criteria** |
| 3.1 | Question framework (PECO) |
| 3.2 | Inclusion and exclusion criteria |
| 3.3 | Anatomical and histological definitions |
| 3.4 | Controlled vocabulary of exclusion reasons |
| 3.5 | Protocol amendments and unresolved decisions |
| **4** | **Search strategy and information sources** |
| 4.1 | Strategy development |
| 4.2 | The adopted PubMed strategy |
| 4.3 | Planned strategies for other databases |
| 4.4 | Syntax validation |
| 4.5 | Historical search execution |
| 4.6 | Decisions D023 and D024 |
| 4.7 | Database access limitations |
| 4.8 | Grey-literature strategy |
| 4.9 | Search execution status |
| **5** | **Record processing and screening methodology** |
| 5.1 | Import, parsing and validation |
| 5.2 | Deduplication and the identifier hierarchy |
| 5.3 | Title and abstract classification workflow |
| 5.4 | Separation of automation from reviewer decision |
| 5.5 | Blinded verification sample |
| 5.6 | Full-text workflow |
| 5.7 | Data extraction design |
| 5.8 | Risk-of-bias framework |
| **6** | **Systematic review results and progress** |
| 6.1 | Identification |
| 6.2 | Deduplication and record conservation |
| 6.3 | Provisional classification |
| 6.4 | Verification status |
| 6.5 | Full-text and inclusion status |
| 6.6 | PRISMA-style flow |
| **7** | **Meta-analysis statistical methodology** |
| 7.1–7.12 | Effect measures through zero-cell handling |
| **8** | **Statistical software architecture and validation** |
| **9** | **Results and current status of quantitative synthesis** |
| **10** | **Discussion** |
| **11** | **Limitations and prioritised completion roadmap** |
| **12** | **Conclusion** |
| — | **References** |
| — | **Appendices A–G** |

*Page numbers are provided by the document footer. Headings are numbered consistently throughout.*

---

## List of tables

| Table | Title |
|---|---|
| 3.1 | PECO framework and eligibility criteria |
| 3.2 | Controlled vocabulary of exclusion reasons |
| 3.3 | Unresolved methodological decisions |
| 4.1 | Search executions and their status |
| 4.2 | Database coverage and verified access status |
| 4.3 | Counts-only interrogation figures |
| 5.1 | Identifier hierarchy |
| 5.2 | Extraction schema summary |
| 6.1 | Acquisition and composition of the registered export |
| 6.2 | Deduplication and record conservation |
| 6.3 | Title/abstract stage: formal versus provisional |
| 6.4 | Provisional exclusion reasons |
| 6.5 | Blinded verification status |
| 6.6 | Full-text attribution states |
| 6.7 | Verified numerical results |
| 7.1 | Standard-error derivation routes |
| 7.2 | Implemented statistical components |
| 7.3 | Prespecified subgroup dimensions and readiness |
| 8.1 | Statistical safeguards enforced in code |
| 8.2 | Test suite by module |
| 8.3 | Technology stack |
| 11.1 | Prioritised completion roadmap |
| A.1 | Adopted PubMed query, term blocks |
| D.1 | Extraction schema field counts |
| F.1 | Outstanding methodological decisions |
| G.1 | Validation and test summary |

## List of figures

| Figure | Title |
|---|---|
| 6.1 | Current state of the evidence base |
| 6.2 | PRISMA-style progress diagram |
| 8.1 | Pipeline architecture |
| 8.2 | Data flow and custody classes |
| 8.3 | Technology stack |

## List of abbreviations

| Abbreviation | Expansion |
|---|---|
| CI | Confidence interval |
| DL | DerSimonian–Laird estimator |
| HKSJ | Hartung–Knapp–Sidik–Jonkman |
| HR | Hazard ratio |
| MeSH | Medical Subject Headings |
| MOOSE | Meta-analysis Of Observational Studies in Epidemiology |
| OR | Odds ratio |
| OSCC | Oral squamous cell carcinoma |
| PECO | Population, Exposure, Comparator, Outcome |
| PRISMA | Preferred Reporting Items for Systematic reviews and Meta-Analyses |
| PRISMA-S | PRISMA extension for reporting literature searches |
| REML | Restricted maximum likelihood |
| RR | Risk ratio |
| SAP | Statistical analysis plan |
| SCC | Squamous cell carcinoma |
| SE | Standard error |
| τ² | Between-study variance |
| I² | Proportion of total variation attributable to heterogeneity |

---

# Chapter 1 — Introduction

## 1.1 Background

Evidence synthesis depends on two things being true at once: that the evidence was found, and that
the judgements applied to it were made. Systematic reviews are described as reproducible far more
often than they are. Search strategies are reported in prose that cannot be re-executed; screening
decisions are recorded without the basis on which they were made; the boundary between a tool's
output and a reviewer's judgement is left to the reader's assumption.

As automated classification becomes ordinary in screening workflows, that last point ceases to be a
documentation nicety and becomes a question about what the recorded evidence means. If a screening
worksheet shows 194 decisions and does not state how they arose, a reader cannot determine whether a
human read 194 abstracts or accepted 194 machine outputs in a single action. These are different
bodies of evidence, and they are indistinguishable in the file.

## 1.2 Oral cavity squamous cell carcinoma

Cancer of the oral cavity is among the more common malignancies worldwide, with an incidence
distributed unevenly: the burden falls disproportionately on South and South-East Asia. The dominant
histological type is squamous cell carcinoma (SCC), arising from the mucosal epithelium lining the
oral cavity — the lips, anterior two-thirds of the tongue, floor of mouth, buccal mucosa, gingivae,
retromolar trigone and hard palate.

The anatomical boundary matters more than it may appear. The oral cavity adjoins the oropharynx, and
the two are frequently reported together as "head and neck" cancer. They are not interchangeable for
aetiological purposes: oropharyngeal carcinoma has a substantial human papillomavirus-associated
component with a different risk-factor profile. A review that pools across these sites risks diluting
the association it sets out to measure.

## 1.3 Smoked tobacco exposure

For the oral cavity specifically, the relevant exposure is broader than cigarette smoking. Bidis —
small hand-rolled cigarettes common in South Asia — chuttas, cigars and pipes are all combusted
tobacco products. Reverse smoking, in which the lit end of the product is held inside the mouth, is
practised in parts of South India and is associated with palatal lesions.

A review restricted to cigarettes would exclude much of the most informative literature for the
populations in which disease burden is greatest.

## 1.4 Biological and epidemiological rationale

Combusted tobacco delivers a complex mixture of carcinogens directly to the oral mucosa, with
contact time and anatomical distribution varying by product and by smoking practice. Reverse smoking
places the combustion source intra-orally, altering which subsites receive the greatest exposure.
These mechanistic differences are the reason the exposure definition adopted here admits any
combusted product rather than cigarettes alone, and the reason product type is a prespecified
subgroup dimension.

Smokeless tobacco and betel quid are prevalent in the same populations and are independently
associated with oral malignancy. They are therefore treated as **confounders requiring adjustment**,
not as exposures.

## 1.5 Research gap

The gap this project addresses is not primarily a gap in the clinical literature. It is a gap between
the **claimed** and the **demonstrable** reproducibility of review workflows:

1. **Provenance of decisions.** Standard screening tools record a decision and a reason. They do not
   generally record whether the decision was formed by the reviewer or adopted from a suggestion, nor
   do they prevent the two from being counted together.
2. **Provenance of inputs.** Search exports are often described rather than preserved. When an export
   is lost, the loss is typically unrecorded, and a later re-run may silently substitute for it.
3. **Premature synthesis.** Nothing in a typical workflow prevents a pooled estimate from being
   computed on an incomplete or unverified dataset, nor distinguishes a null result from an empty one.

## 1.6 Research question

> **Is smoked tobacco use associated with an increased risk of squamous cell carcinoma of the oral
> cavity?**

The question is framed as an **association**. No causal claim will be made from observational data.

## 1.7 Aim and objectives

**Aim.** To determine whether smoked tobacco use is associated with increased risk of oral cavity
SCC, by systematic review and, where sufficient comparable evidence exists, meta-analysis.

**Table 1.1 — Objectives and verified status.**

| # | Objective | Status |
|---|---|---|
| O1 | Specify a protocol with explicit, recorded, dated decisions | **Achieved** |
| O2 | Checksum-gated acquisition detecting any alteration of a raw export | **Achieved** |
| O3 | Deduplication with an explicit identifier hierarchy and no silent merging | **Achieved** |
| O4 | Screening architecture separating suggestion from decision at field level | **Achieved** |
| O5 | Blinded verification with a reproducible sampling frame | **Achieved** — drawn, unanswered |
| O6 | Complete extraction schema with declared provenance per field | **Achieved** — 93 fields |
| O7 | Meta-analytic computation with declared validation and limitations | **Achieved** — implemented, never run on research data |
| O8 | Reproducible generation of manuscript, figures and data-collection instruments | **Achieved** |
| **O9** | **Produce a pooled estimate answering the review question** | **NOT ACHIEVED** |

## 1.8 Significance

If completed, the review would provide an oral-cavity-specific synthesis holding anatomical site,
histology and exposure definition constant — a combination the existing literature frequently does
not. Independently of that, the methodological contribution is a demonstration that integrity
properties usually asserted in prose can be enforced by a system.

---

# Chapter 2 — Literature and methodological background

## 2.1 Relevant epidemiological concepts

Observational designs admissible for an exposure that cannot be randomised:

| Design | Structure | Native measure |
|---|---|---|
| **Case–control** | Starts from people with and without the outcome; looks backwards at exposure | Odds ratio |
| **Cohort** | Starts from exposed and unexposed people; follows forward to outcome | Risk ratio or hazard ratio |
| Cross-sectional | Exposure and outcome measured at one time; cannot establish temporality | Prevalence — **not eligible** |
| Case series | No comparison group | **Not eligible** — no reference group |
| Randomised trial | Allocation at random | **Not applicable** — smoking cannot ethically be randomised |

The final row explains why Cochrane CENTRAL, a register of controlled trials, is not searched.

## 2.2 Exposure and outcome definitions

**Exposure (adopted decision D009).** Any smoked tobacco: cigarettes, bidis, cigars, pipes and other
combusted products. Product types are extracted per estimate. **Smokeless tobacco and betel quid are
not exposures**; they are extracted as potential confounders, as is alcohol.

**Outcome (adopted decision D008).** Cancer of the oral cavity where SCC is histologically confirmed,
or where SCC is a stated majority of at least 90% of cases. Estimates pooling the oral cavity with
oropharynx, larynx, pharynx or "head and neck" as a single outcome are **not eligible** unless an
oral-cavity-specific estimate is reported separately.

## 2.3 Systematic review methodology

The review follows **PRISMA 2020** for reporting, **PRISMA-S** for the search, **MOOSE** for
observational-study specifics, and the **Cochrane Handbook version 6.5** for synthesis methods.

## 2.4 Rationale for meta-analysis

Where several studies estimate the same association, a weighted synthesis yields a more precise
summary than any single study and permits formal examination of between-study variation. The
justification is conditional: pooling is appropriate only when the studies estimate a sufficiently
similar quantity. Chapter 7 states in advance the circumstances under which pooling will **not** be
performed.

## 2.5 Effect measures and their interpretation

All three admissible measures are ratios, and all are analysed on the natural-logarithm scale, where
the sampling distribution is approximately normal and symmetric. A ratio of 1 indicates no
association; values above 1 indicate higher odds or risk among the exposed.

The measures are **not interchangeable**: an odds ratio approximates a risk ratio only when the
outcome is rare. Mixing them in a single pooled analysis is refused by the software.

---

# Chapter 3 — Protocol and eligibility criteria

The protocol was specified before screening: the protocol directory was committed on 29 October 2026
and the screening records on 1 November 2026. **The review is not prospectively registered**;
registration remains an open question and the provisional classification pass preceded it. This is
reported as a protocol deviation.

## 3.1 Question framework (PECO)

**Table 3.1 — PECO framework and eligibility criteria.**

| Element | Criterion | Status |
|---|---|---|
| **P**opulation | Human adults; no restriction by country, sex or setting | Settled |
| **E**xposure | Any smoked tobacco: cigarettes, bidis, cigars, pipes, other combusted products (D009) | Settled |
| **C**omparator | Never-smokers, and/or study-defined "non-smokers"; recorded verbatim. Primary analysis restricted to never-smoker references | Settled (D025) |
| **O**utcome | Oral cavity cancer; SCC histologically confirmed or a stated majority ≥90% (D008) | Settled in part |
| Contrast | Ever versus never (primary); current and former versus never (secondary) | Settled (D026) |
| Designs | Case–control; cohort, prospective or retrospective | Settled |
| Effect data | OR, RR or HR with a 95% CI, or sufficient raw data to compute one | Settled |
| Language | Published in English (D013) | Settled |

## 3.2 Inclusion and exclusion criteria

A study is eligible when it reports an oral-cavity-specific effect estimate for a smoked tobacco
exposure against a non-smoking reference group, in a case–control or cohort design, with SCC
confirmed histologically or constituting a stated majority of at least 90% of cases.

## 3.3 Anatomical and histological definitions

The eligible anatomical region is the oral cavity. **The precise subsite list is not settled**: nine
numbered questions (P014–P022) and one unnumbered question concern anatomical and histological scope,
including the treatment of soft palate and uvula where staging and anatomical conventions genuinely
conflict, the handling of straddling topography codes, a site-purity threshold analogous to the
histological threshold, whether SCC variants count as SCC, and the status of adenosquamous and
sarcomatoid entities.

The unnumbered question — whether populations restricted to premalignant oral lesions are in scope —
**affects 14 of the 85 reports** provisionally carried forward.

## 3.4 Controlled vocabulary of exclusion reasons

Exclusion is recorded against thirteen fixed codes; free text may not substitute for a code.

**Table 3.2 — Controlled vocabulary.** Four codes are restricted to full text because they cannot be
judged from an abstract without guessing. The vocabulary therefore prevents a premature judgement.

| Code | Definition | Available at |
|---|---|---|
| `wrong_population` | Not human, not adult, or not a relevant population | ta, ft |
| `wrong_outcome` | Outcome is not oral-cavity SCC per D008, including prognostic studies | ta, ft |
| `wrong_exposure` | Not smoked tobacco, or smokeless / betel quid only | ta, ft |
| `wrong_design` | Not case–control or cohort | ta, ft |
| `review_or_meta` | Systematic review, meta-analysis, narrative review | ta, ft |
| `animal_or_invitro` | Animal, cell or in-vitro study | ta, ft |
| `conference_abstract` | Abstract with insufficient detail for reliable extraction | ta, ft |
| `not_english` | Not published in English | ta, ft |
| `other` | Requires written justification | ta, ft |
| `outcome_not_separable` | Oral cavity pooled with other head-and-neck sites | **ft only** |
| `no_reference_group` | No non-smoking or never-smoking comparator | **ft only** |
| `no_usable_data` | No effect estimate and no data from which to derive one | **ft only** |
| `duplicate_publication` | Same population already included; links to the retained report | **ft only** |

## 3.5 Protocol amendments and unresolved decisions

**Twenty-four decisions are adopted** (D001–D015, D020, D022–D029). **Four** (D016–D019) are
implemented and enforced in code but **not adopted as protocol**. **D021** was drafted and never
entered in the register.

**Table 3.3 — Twelve numbered questions remain open.**

| Group | Questions | Blocks |
|---|---|---|
| Registration | P006 | Prospective status |
| Database coverage | P007 | Formal search execution |
| Anatomical and histological scope | P014–P022 | Full-text eligibility |
| Risk-of-bias instrument | P023 | Appraisal; two schema fields |

Two amendments were adopted during this period and are described in §4.6.

---

# Chapter 4 — Search strategy and information sources

## 4.1 Strategy development

Three distinct search efforts are distinguished in the project record, because a database's content
and the filters actually applied may differ between runs.

**Table 4.1 — Search executions and status.**

| Execution | Filters applied | Records | Status |
|---|---|---|---|
| v1 (original) | Humans, English | 138 | **Export lost**, and its execution date is **unknown and unrecoverable** (D027). Not recreated or substituted; contributes no records |
| **v1r (re-execution)** | **none** | **194** | **Registered with a checksum. The sole evidence base for Chapter 6** |
| v2 draft | none | — | Drafted; counts-only validation 29 Oct 2026. **Superseded** |
| **Corrected strategy** | none | — | **Adopted (D023, D024); never executed** |

## 4.2 The adopted PubMed strategy

Two concept blocks joined by a single `AND`: an outcome block of 43 terms combining the exploded MeSH
heading `"Mouth Neoplasms"[Mesh]` with free-text phrasings and named subsites, and an exposure block
of 45 terms combining four MeSH headings with free-text product terms including `bidi`, `beedi`,
`cheroot`, `chutta`, `dhumti` and `"reverse smoking"`.

**No filters are applied** — no language, date, species or publication-type restriction. Language and
species are handled at screening with a recorded exclusion reason, which is auditable in a way a
database filter is not. The full query is reproduced in Appendix A.

Two properties are deliberate rather than oversights. **Bare anatomical terms** such as
`"buccal mucosa"` and `"floor of mouth"` carry no neoplasm qualifier and will retrieve
non-neoplastic studies; these are excluded at screening rather than at retrieval, because requiring a
cancer word beside every subsite term would lose studies naming the subsite in the title and the
malignancy only in the abstract. **Generic tobacco terms** will retrieve smokeless-only studies; no
smokeless-specific term appears anywhere in the exposure block, and such records are excluded at
screening as a wrong exposure. **Retrieval is not eligibility.**

## 4.3 Planned strategies for other databases

Translations exist for four further databases and are **untested drafts**. A PubMed query cannot be
pasted into another platform: field scope, controlled vocabulary and phrase handling all differ.

| Database | Vocabulary | Field tag | Principal translation issue |
|---|---|---|---|
| Embase | **Emtree**, not MeSH | `:ti,ab,kw` | Headings differ in name and hierarchy; five require confirmation in the thesaurus browser. `:ti,ab,kw` also searches author keywords, so it is **wider** than PubMed's `[tiab]` |
| Scopus | **None** | `TITLE-ABS-KEY()` | No controlled vocabulary at all, so the MeSH arm has no equivalent. Loose phrase matching; wildcard-inside-phrase behaviour unverified |
| Web of Science | **None** | `TS=()` | Topic field includes KeyWords Plus, the widest field of the four. Exact phrase matching, stricter than Scopus. Subscribed editions must be recorded or the search is not reproducible |
| IndMED | Variable | Variable | Query language undocumented; Boolean support unverified. A simplified staged approach is specified |

**Field scope is not equivalent across platforms**, and retrieval differences between them are
therefore partly an artefact of field scope rather than coverage. This must be reported rather than
smoothed over.

## 4.4 Syntax validation

The adopted PubMed query was validated line by line on 14 November 2026 by counts-only interrogation
of the NCBI E-utilities interface: each of the **88 individual query lines** was submitted alone and
its result count read back. **No record was retrieved; zero identifiers were returned across all 88
requests**, verified by counting identifier elements in every response.

**Exactly one line of 88 returned zero**, carrying PubMed's `QuotedPhraseNotFound` warning. This
independently confirmed an observation made separately in the PubMed web interface on the same date.
All remaining 87 lines returned non-empty counts.

## 4.5 Historical search execution

One export exists and is registered. It is the product of the **v1 query string re-executed without
filters**, not of the adopted strategy.

**The executed query is substantially narrower than the eligibility criteria it was meant to serve.**
It requires the literal phrase "Oral Squamous Cell Carcinoma" or "OSCC" in the title or abstract.
**68 of the 194** retrieved records use the phrase "oral cancer" — the dominant phrasing in
aetiological epidemiology — and were retrieved only because they also happened to contain a required
term. It reduces the exposure to "smoking" or "cigarette", omitting bidi, cigar and pipe terms
central to the exposure definition, and uses no controlled vocabulary. **98 of 194** matched its
design block only through the single word "cohort", which also captures prognostic studies of people
who already have the disease.

**Any synthesis based on this record set alone would rest on a search that does not match its own
protocol.** This is the most consequential limitation of the current evidence base.

## 4.6 Decisions D023 and D024

**D023 — no study-design block in the primary search** (adopted 13 November 2026). A design block is
a filter whose cost is invisible: the records it removes never appear for inspection. Any losses
would not be random — they would fall on studies naming their design only in the methods section and
on records without MeSH indexing, which are disproportionately the recent and regionally published
South Asian studies the exposure definition was written to capture. **42 of the 194 records in hand
carry no MeSH headings at all.** The block also admits cross-sectional studies, case series and
reviews, none eligible here, so it reduces volume without sorting designs.

> **The uncertainty recorded as part of D023.** Removing the design block increases the number of
> records retrieved, but **the number of additional eligible studies recovered is unknown and may be
> zero**. The decision prioritises search sensitivity over retrieval volume; **it does not establish
> that the broader strategy has greater empirical sensitivity**.

**D024 — removal of an ineffective quoted phrase** (adopted 14 November 2026). The term
`"epidermoid carcinoma of the mouth"[tiab]` is not matched as a phrase by PubMed: submitted alone it
returns zero results with a `QuotedPhraseNotFound` warning, and inside an `OR` group it contributed
nothing while failing silently. It was removed; `"oral epidermoid carcinoma"[tiab]` on the same
source line was retained. The unquoted variant, which returned 28 records, was **deliberately not
adopted**: removing the quotation marks changes what is searched and is a different search rather
than a repair, and no claim is made that those records are relevant or eligible. Expected retrieval
effect: **zero records lost**, recorded as an empirical interface observation of a specific date
rather than a guarantee of identical behaviour at a future execution.

## 4.7 Database access limitations

**Table 4.2 — Database coverage and verified access.**

| Source | Searched | Access status |
|---|---|---|
| PubMed / MEDLINE | **Yes** — one registered execution | **Confirmed** (free) |
| Embase | No | **No evidence of access** — not listed among the institution's advertised databases |
| Scopus | No | Publicly advertised; **individual access unverified** |
| Web of Science | No | Publicly advertised; **individual access unverified** |
| IndMED | No | **Reachability untested** |
| Cochrane CENTRAL | No | **Not recommended** — design mismatch |

An institutional subscription statement is not access; absence from a public list is not proof of
absence; and **access to a publisher's journals is not access to its bibliographic database**.
**P007 — which databases the review will search — remains open.**

## 4.8 Grey-literature strategy

A bounded supplementary grey-literature search is adopted (D022), justified by **search sensitivity**
rather than by any statistical test. Priority is given to South Asian theses and dissertations, where
the bidi and reverse-smoking literature is concentrated. Government and registry reports are treated
as **discovery sources** whose reference lists are checked, not as evidence: prevalence-only and
incidence-only reports are excluded as `no_usable_data`. A Google Scholar search is bounded by a
prespecified stopping rule — 200 results examined or 50 consecutive non-hits — which is **an
operational choice fixed in advance, not an established standard**, and which yields a search that is
reportable but **not repeatable**, because the relevance ordering is unstable.

**No grey-literature source has been searched, and no repository has been verified as reachable.**

## 4.9 Search execution status

**Table 4.3 — Counts-only interrogation figures.** **None of these is a search yield.** No record was
retrieved, exported or screened, and no registry entry exists for any of them.

| Query | Design block | Count | Date | Nature |
|---|---|---|---|---|
| Corrected strategy | none | 8,190 | 12 Nov 2026 | Counts-only interrogation |
| Corrected strategy | optional block | 5,008 | 12 Nov 2026 | Counts-only interrogation |
| Corrected strategy | none | 8,195 | 14 Nov 2026 | Web-interface check, exploratory |
| v2 draft (superseded) | with / without | 4,770 / 7,875 | 29 Oct 2026 | Counts-only, superseded query |

**The formal multi-database search has not been executed.** It is blocked on P007, on the measurement
of a screening rate required as a condition of D023, and on separate authorisation to register a new
execution.

---

# Chapter 5 — Record processing and screening methodology

## 5.1 Import, parsing and validation

The registered export is parsed from MEDLINE format into structured records. Every stage re-verifies
provenance before reading: the count and SHA-256 checksum recorded at registration must match the
file on disk, and a mismatch raises an error rather than proceeding. Each stage writes a validation
report and exits non-zero on missing, altered or invalid input.

## 5.2 Deduplication and the identifier hierarchy

**Table 5.1 — Identifier hierarchy (adopted decisions D004, D014).**

| Level | Identifier | Assigned by |
|---|---|---|
| 1 | `record_id` — one database record | Import |
| 2 | `report_id` — one unique publication after deduplication | Deduplication |
| 3 | `study_id` — one unique study population | **Human judgement at full text** |
| 4 | `estimate_id` — one reported effect estimate | Extraction |

**The unit of analysis is the `study_id`, and a `study_id` may appear at most once in any analysis.**

Matching proceeds normalised DOI → PMID → exact title+author+year fingerprint. Titles that are
similar but not identical are flagged `needs_review` and **never merged automatically**, because an
automatic merge on a near-match can silently delete a distinct study.

## 5.3 Title and abstract classification workflow

Each report receives a decision and, where excluded, exactly one reason code from the controlled
vocabulary. Eleven reconciliation identities must hold or the stage fails, among them:

```
ta_excluded + ta_included + ta_unresolved                  == ta_screened
ta_adjudicated + ta_adopted + ta_invalid + ta_unscreened   == ta_total
ft_sought + ft_provisional_sought + ft_invalid_source
          + ft_ineligible_source + ft_unattributed         == ft_rows
```

## 5.4 Separation of automation from reviewer decision

This is the central methodological commitment of the project.

| `decision_basis` | Meaning |
|---|---|
| `adopted_from_suggestion` | The reviewer accepted an automated suggestion without judging the record individually. **This is not independent adjudication** |
| `independently_adjudicated` | The reviewer judged the record from its own evidence |

A row counts as independently adjudicated **only when all five** of `decision`, `reviewer`,
`screened_date`, `decision_basis = independently_adjudicated` and `adjudicated_date` are recorded.
The separate `adjudicated_date` exists so that flipping the basis on a row already carrying the
bulk-adoption reviewer and date cannot convert a provisional record into a formal one without dating
the new act.

One shared function applies these rules for the validator, the full-text carry-forward and the PRISMA
accounting, so the three cannot disagree. The PRISMA flow **splits** formal from provisional counts,
and the validator in final mode **rejects** any row whose basis is `adopted_from_suggestion`.

## 5.5 Blinded verification sample

Forty of the 194 reports (20.6%) were drawn with a seeded, reproducible procedure, with the recorded
decision withheld. Three response columns give 120 cells. Acceptance thresholds were fixed in advance:
**≥95% ADOPT, 90–94.9% EXTEND, <90% RE-SCREEN.**

## 5.6 Full-text workflow

Full-text rows are attributed to one of five mutually exclusive states, decided **per row rather than
by subtraction**: `ft_sought`, `ft_provisional_sought`, `ft_invalid_source`, `ft_ineligible_source`,
`ft_unattributed`. A stale row whose source record has left the include set is counted in whichever
state explains it and reported, **never silently deleted**.

## 5.7 Data extraction design

**Table 5.2 — Extraction schema summary.**

| Table | Fields | Purpose |
|---|---|---|
| `studies` | **34** | One row per included study population |
| `estimates` | **47** | One row per reported effect estimate |
| `risk_of_bias` | **12** | One row per study per domain — **provisional, pending P023** |
| **Total** | **93** | Every field documented with type, requirement and status |

Missing is a value: `NR`, `NA` or `UNCLEAR` is recorded, never blank and never zero. Every extracted
estimate requires a `source_location` naming a page, table or figure.

## 5.8 Risk-of-bias framework

**The appraisal instrument has not been chosen** (P023). The schema carries twelve **structural**
fields — who assessed what, when, on what evidence — and the instrument's domain names and judgement
categories are **deliberately absent**, because they come from whichever instrument is selected and
are never invented. A software test asserts that no known instrument is named anywhere in the
generated data-collection workbook.

---

# Chapter 6 — Systematic review results and progress

Every value in this chapter was recomputed from the repository on 14 November 2026.

## 6.1 Identification

**Table 6.1 — Acquisition and composition of the registered export.**

| Property | Value |
|---|---|
| Registry entry | `pubmed_v1r` |
| File | `pubmed-v1r-reexecution-194.nbib` |
| Size | 958,710 bytes |
| SHA-256 | `1d153fa80edd6bc97c92498bce8076873cc514f412de5113412fa71827e4ca1e` |
| **Records in export** | **194** |
| Records parsed | 194 |
| Unique PMIDs recovered | 194 |
| Language: English | 191 |
| Language: Chinese | 2 |
| Language: English and Portuguese | 1 |
| Carrying MeSH indexing | 152 |
| **No MeSH indexing at all** | **42 (21.6%)** |

The language distribution follows directly from the decision to retrieve unfiltered (D013) and
explains why exclusion reasons appear that a filtered search would never have surfaced.

## 6.2 Deduplication and record conservation

**Table 6.2 — Record conservation.**

| Metric | Value |
|---|---|
| Records entering deduplication | 194 |
| Pairs merged on identifier or exact fingerprint | **0** |
| Pairs flagged `needs_review` | **0** |
| **Unique reports** | **194** |
| **Records lost** | **0** |

Zero duplicates is the expected outcome for a single-database search and is **not** evidence that the
stage works; the evidence is 63 tests exercising the matching rules on constructed cases.

## 6.3 Provisional classification

**Table 6.3 — Title/abstract stage: formal versus provisional.** These columns are not two views of
the same work. The formal column counts human adjudications, of which there are none.

| Quantity | Formal | Provisional |
|---|---|---|
| Reports with a recorded classification | **0** | 194 |
| Classified for exclusion | **0** | 109 |
| Classified for retrieval | **0** | 85 |
| Unresolved | 0 | 0 |
| Rows failing validation | 0 | — |

> **194 provisional classifications do not mean 194 records were formally screened.** All 194 rows
> carry `decision_basis = adopted_from_suggestion`; **zero carry `independently_adjudicated`**. Under
> the project's adopted rules a suggestion cannot satisfy a decision field, so **the formal PRISMA
> flow reports 0 records screened and 0 taken forward**. The validator in final mode fails on this
> state, as designed.

**Table 6.4 — Provisional exclusion reasons.** These are reason codes attached to automated
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

## 6.4 Verification status

**Table 6.5 — Blinded verification.**

| Property | Value |
|---|---|
| Reports sampled | **40** of 194 (20.6%) |
| Response columns | 3 |
| **Total response cells** | **120** |
| **Cells completed** | **0** |
| Agreement rate, kappa, acceptance outcome | **Do not exist** |

## 6.5 Full-text and inclusion status

**Table 6.6 — Full-text attribution states.**

| State | Count |
|---|---|
| `ft_sought` — valid, adjudicated include | **0** |
| `ft_provisional_sought` — valid include, adopted basis | **85** |
| `ft_invalid_source` | 0 |
| `ft_ineligible_source` | 0 |
| `ft_unattributed` | 0 |
| **Total rows** | **85** |

**Full texts sought: 0. Retrieved: 0. Assessed: 0. Studies included: 0.** Every reviewer field in the
full-text worksheet is empty, and `data/extraction/` does not exist.

## 6.6 PRISMA-style flow and verified results

![Figure 6.1. Current state of the evidence base, recomputed from the repository. Left: record attrition, with provisional counts distinguished from formal ones. Right: reviewer work completed against work outstanding — one row is complete, and it is the row recording machine output rather than human judgement.](results/final_submission/figures/record_status.png)

![Figure 6.2. PRISMA-style progress diagram. The formal flow counts independently adjudicated decisions only; adopted classifications are reported separately as a provisional outcome, outside the flow.](results/figures/prisma_flow.png)

**Table 6.7 — Verified numerical results.** Every value traceable to its source.

| # | Quantity | Value | Source |
|---|---|---|---|
| 1 | Records identified | **194** | `config/sources.yaml` → `pubmed_v1r` |
| 2 | Records imported and parsed | **194** | parsed citations file |
| 3 | Unique reports after deduplication | **194** | deduplication report index |
| 4 | Duplicate pairs removed | **0** | deduplication audit |
| 5 | Provisional classifications | **194** | title/abstract worksheet |
| 6 | Provisional exclusions | **109** | title/abstract worksheet |
| 7 | Reports carried forward (provisional) | **85** | title/abstract worksheet |
| 8 | **Independently adjudicated decisions** | **0** | `decision_basis` field |
| 9 | **Formal records screened (PRISMA)** | **0** | PRISMA accounting |
| 10 | Full-text rows, provisionally sought | **85** | full-text worksheet |
| 11 | Full texts formally sought | **0** | PRISMA accounting |
| 12 | Full texts retrieved | **0** | full-text worksheet |
| 13 | Full texts assessed | **0** | full-text worksheet |
| 14 | **Included studies** | **0** | `data/extraction/` absent |
| 15 | Extraction records | **0** | `data/extraction/` absent |
| 16 | Risk-of-bias assessments | **0** | `data/extraction/` absent |
| 17 | **Pooled clinical estimates** | **0** | no estimates exist |
| 18 | Verification sample | **40** reports (20.6%) | verification sample file |
| 19 | Verification response cells | **120** | 40 × 3 |
| 20 | **Cells completed** | **0** | verification sample file |
| 21 | Study-level schema fields | **34** | extraction configuration |
| 22 | Estimate-level schema fields | **47** | extraction configuration |
| 23 | Risk-of-bias schema fields | **12** | extraction configuration |
| 24 | Total documented fields | **93** | data dictionary |
| 25 | Records without MeSH indexing | **42** of 194 | parsed citations |
| 26 | Test suite | **670 passed, 1 skipped, from 671 collected** | pytest |
| 27 | Adopted decisions / proposed / open | **24 / 4 / 12** | decision register |

**Items 14 to 17 are zero because the work has not been done, not because the search found nothing.**
These are absences of evidence, not evidence of absence.

---

# Chapter 7 — Meta-analysis statistical methodology

This chapter describes methods **implemented and tested in software**. **None has been executed on
research data**, because no eligible estimate exists.

## 7.1 Effect measures

Three ratio measures are admissible — odds ratio, risk ratio and hazard ratio. All analysis is
conducted on the natural-logarithm scale and exponentiated only for presentation. Mixing measures in
one analysis is **refused** by the software.

## 7.2 Log transformation

For a ratio measure θ, the analysis quantity is:

```
y = ln(θ)
```

The sampling distribution of `ln(θ)` is approximately normal and symmetric, which the distribution of
θ itself is not. Confidence intervals are formed on the log scale and back-transformed.

## 7.3 Standard-error derivation

**Table 7.1 — Three implemented routes.**

| Route | Formula | When used |
|---|---|---|
| From a reported 95% CI | `SE = [ln(upper) − ln(lower)] / (2 × 1.959964)` | The usual case |
| From a 2×2 table | `SE = √(1/a + 1/b + 1/c + 1/d)` | Raw counts reported |
| As reported | `SE` taken directly | The paper gives it |

For a 2×2 table with cells *a* (exposed cases), *b* (exposed non-cases), *c* (unexposed cases) and
*d* (unexposed non-cases):

```
ln(OR) = ln(a) + ln(d) − ln(b) − ln(c)
```

Derived values are never typed by hand; the formula and inputs are recorded in a `derivation` field.
A consistency check compares the reported estimate against the geometric mean of its interval and
records asymmetry beyond a 10% relative gap, since mild asymmetry is normal when a source rounds.

## 7.4 Confidence intervals

```
95% CI = exp( y ± 1.959964 × SE )
```

## 7.5 Fixed-effect inverse-variance model

Each study contributes in proportion to its precision:

```
w_i = 1 / SE_i²

           Σ (w_i × y_i)                          1
ŷ_FE  =  ────────────────        SE(ŷ_FE)  =  ─────────
              Σ w_i                            √( Σ w_i )
```

The model assumes a single common true effect; all observed variation is sampling error.

## 7.6 Random-effects inverse-variance model

The true effect is assumed to vary between studies with variance τ²:

```
w*_i = 1 / ( SE_i² + τ² )

           Σ (w*_i × y_i)                          1
ŷ_RE  =  ─────────────────       SE(ŷ_RE)  =  ──────────
              Σ w*_i                           √( Σ w*_i )
```

A random-effects model is anticipated: observational studies differing in population, design and
adjustment make the assumption of one common true effect implausible.

## 7.7 Estimators of τ²

**DerSimonian–Laird**, a method-of-moments estimator derived from Cochran's Q:

```
            Q − (k − 1)
τ²_DL = max( ───────────── , 0 )            where  C = Σ w_i − ( Σ w_i² / Σ w_i )
                  C
```

**Restricted maximum likelihood (REML)**, solved iteratively to a fixed point. The estimator used is
**always named in output**, because the two can give materially different values when *k* is small.

## 7.8 Heterogeneity: Cochran's Q, I² and τ²

```
Q = Σ w_i ( y_i − ŷ_FE )²          distributed as χ² with k − 1 degrees of freedom

           Q − (k − 1)
I²  =  max( ───────────── , 0 ) × 100%
                 Q
```

I² is the proportion of total variation attributable to real between-study heterogeneity rather than
chance. The conventional 25%, 50% and 75% bands are treated as **descriptive guidance, not decision
thresholds**. τ² is reported for every random-effects model, with its estimator named.

## 7.9 Prediction intervals

Where τ² is non-zero and at least three studies contribute:

```
95% PI = exp( ŷ_RE ± t_(k−2) × √( τ² + SE(ŷ_RE)² ) )
```

The prediction interval describes the plausible range of the true effect in a **new** study from the
same population of studies, and is wider than the confidence interval for the mean.

## 7.10 Sensitivity and subgroup analyses

**Leave-one-out analysis** re-pools the set with each study omitted in turn, reporting the range of
pooled estimates. A result driven by a single study is thereby visible.

**Subgroup analysis** pools within strata and tests formally for a difference between them, using a
between-group Q on the subgroup summaries with *groups − 1* degrees of freedom.

**Table 7.3 — Prespecified subgroup dimensions and readiness.**

| Dimension | Source field | Status |
|---|---|---|
| Product type (cigarette-only vs mixed) | `estimates.product_types` | **Ready** |
| Alcohol adjustment | `estimates.adjusted_alcohol` | **Ready** |
| Anatomical subsite | `estimates.outcome_site` | **Blocked** — P014–P022; no settled category set |
| Geographical region | `studies.country` | **Blocked** — no country-to-region scheme has been chosen |
| Risk-of-bias level | risk-of-bias table | **Blocked** — P023; no instrument, so no judgement categories |

> **A documented discrepancy, not silently reconciled.** The statistical analysis plan lists **nine**
> candidate subgroup dimensions — design, adjusted versus unadjusted, product type, exposure
> contrast, dose–response tier, geographic region, anatomical subsite, risk-of-bias level, and
> alcohol-adjusted versus not. The manuscript names **five** as planned. The implementation follows
> the manuscript's five. **Which set is prespecified is an open question for the reviewer**, and it
> matters: anything run beyond the prespecified set must be declared post-hoc.

**A subgroup difference is supported only by the between-group test.** Observing that one subgroup's
interval excludes the null while another's does not is **not** evidence of a difference, and the
software attaches this warning to every subgroup result.

## 7.11 Publication bias and small-study effects

Egger's regression test and funnel plots are implemented. **Egger's test is refused below ten
studies**, where it is uninformative. If fewer than ten studies are included, **no test will be run
and none will be reported**. Funnel-plot asymmetry has causes besides publication bias — true
heterogeneity, poorer methodological quality in smaller studies, chance — and must be reported with
that caveat or not at all.

## 7.12 Dependence, adjustment and zero cells

**Multiple estimates from one study.** A study reporting several estimates is normal: different
contrasts, adjustment sets and subsites each produce a row. They are **correlated**, and pooling them
as independent studies would understate the standard error. The software requires exactly one
estimate per study to carry the reviewer's recorded primary marker and **refuses to choose**, naming
every candidate. **Nothing is discarded silently.** The project's position is **selection, not
modelling of dependence**; no multivariate or robust-variance method is implemented.

**Adjusted versus crude estimates.** These answer different questions. **Pooling them together is
refused by default**, naming the studies on each side; overriding requires an explicit flag so the
act is deliberate and visible. **No automatic selection of adjusted estimates is performed** — a rule
that preferred "most adjusted" could select the most favourable model, and the rule must be
prespecified by the reviewer.

**Zero cells.** A zero cell makes `ln(OR)` undefined. **No continuity correction is applied
automatically**: adding 0.5 silently would change the estimate without any record of it. The software
refuses the table and names the alternatives. **Consequence:** a study with a zero cell cannot
currently contribute, because neither the Mantel–Haenszel nor the Peto method is implemented.

## 7.13 Circumstances in which meta-analysis will not be performed

Pooling is inappropriate, and a structured narrative synthesis is reported instead, if any of the
following hold: fewer than three studies contribute to a contrast; the available estimates mix
non-comparable exposure categories that cannot be used without harmonisation; they mix adjusted and
unadjusted estimates without a defensible basis; comparator definitions are irreconcilable across
studies; or heterogeneity is so extreme that a summary estimate would misrepresent the evidence.

**Deciding not to pool is a legitimate result and is reported as such.**

---

# Chapter 8 — Statistical software architecture and validation

## 8.1 Architecture

![Figure 8.1. Pipeline architecture. Fifteen stages coloured by what the repository actually does: green where the code exists and has run on real data, amber where implemented and tested but never run, grey where no implementation exists.](results/final_submission/figures/pipeline_architecture.png)

![Figure 8.2. Data flow across four custody classes. Immutable inputs are checksum-gated; generated data is regenerable; human research records are tracked precisely because they cannot be regenerated. The suggestion file is deliberately separate from the decision file.](results/final_submission/figures/data_flow.png)

## 8.2 The estimate data model and provenance metadata

Each estimate entering an analysis carries, beyond its value and standard error: the derivation route
used; the `source_location` naming a page, table or figure; the originating `report_id` and
`estimate_id`; adjustment status and the **verbatim** covariate list; the adjustment-set label; a
marker for the study's primary adjusted estimate; alcohol-adjustment status; exposure contrast;
product types; outcome site; country; design; and risk-of-bias level where available.

A `provenance_problems()` check reports what is missing before an estimate may enter a research
synthesis — absent source location or report identifier, unknown adjustment status, or an "adjusted"
estimate with no covariate list. It **reports** rather than raises, because a software fixture may
legitimately lack these while a research estimate may not.

## 8.3 Safeguards enforced in code

**Table 8.1 — Statistical safeguards.**

| Safeguard | Behaviour |
|---|---|
| Mixed adjusted and crude estimates | **Refused by default**; overriding requires an explicit flag |
| Automatic adjusted-estimate selection | **Not performed.** The reviewer's rule is required |
| One estimate per study | **Enforced**; a repeated study identifier is refused |
| Correlated estimates | Selection refuses to guess and names every candidate |
| Zero cells | **Refused**, never silently corrected |
| Egger's test below 10 studies | **Refused** |
| Subgroup comparison with fewer than two qualifying groups | **No test performed**; the reason is recorded |
| Unclassifiable subgroup data | **Reported explicitly**, never imputed or reassigned |
| Mixed effect measures | Refused |
| Synthetic data mixed with real | Refused outright |
| Analysis with zero estimates | Refused |
| Post-hoc subgroup not in the prespecified set | Refused |

## 8.4 The three gates

Three stages refuse to proceed, each raising an error and exiting non-zero rather than producing an
empty artefact: **extraction** refuses without included studies; **synthesis** refuses without
extracted estimates; and the **analysis command** rejects any row marked synthetic. The purpose is
that *"no association was found"* and *"we have not looked"* can never be confused in the output.

## 8.5 Test suite

**670 tests passed, 1 skipped, from 671 collected**. The single skip is by design: it is the
raw-source test for the lost v1 export, and a test demanding a file recorded as missing would be a
false failure.

**Table 8.2 — Principal test modules.**

| Module | Tests | Focus |
|---|---|---|
| Screening accounting | 110 | Identities, adjudication rules, PRISMA split |
| Extraction schema | 62 | Field definitions, unresolved-field handling |
| Deduplication | 63 | Matching hierarchy, no silent merging |
| Analysis mathematics | 48 | Pooling, heterogeneity, estimators |
| Verification sampling | 44 | Reproducible draw, scoring refusals |
| Subgroups and adjustment | 30 | Dependence, missing data, adequate evidence |
| Search strategy | 24 | D023/D024 integrity, query structure |
| Draw provenance | 20 | Seed and frame-digest invariance |

Several tests exist because a specific defect was found and fixed, and each encodes the defect so it
cannot recur — among them a PRISMA banner that once read "0 of 194 reports carry a decision, but 194
were adopted", a self-contradiction that reached an embedded figure before being caught.

**Table 8.3 — Technology stack, verified against actual imports.**

| Component | Version | Role |
|---|---|---|
| Python | 3.14.7 | All application code |
| Standard library `csv` | — | **All** tabular data handling |
| `hashlib` | — | SHA-256 provenance |
| PyYAML | 6.0.3 | Configuration |
| pytest | 9.1.1 | Test suite |
| SciPy | 1.18.1 | χ², normal and t distributions; regression |
| Matplotlib | 3.11.2 | Figures and PDF typesetting |

**pandas is not used anywhere in this project**, and is named here because claiming unused tooling
would itself be a reproducibility failure. NumPy is not a direct dependency.

## 8.6 Reproducibility

Dependencies are pinned. Raw data is checksum-gated. Deterministic generation was verified by
rebuilding to a clean path and comparing bytes for the PRISMA figure, the data-collection workbook
and the report figures. A dated decision register records every methodological choice with its
rationale and its explicit scope.

---

# Chapter 9 — Results and current status of quantitative synthesis

**No quantitative synthesis has been conducted.**

| Output | Status |
|---|---|
| Included studies | **0** |
| Extracted effect estimates | **0** |
| Risk-of-bias assessments | **0** |
| Pooled clinical estimate | **None** |
| Clinical forest plot | **None** |
| Heterogeneity statistics (Q, I², τ²) for research data | **None** |
| Prediction interval | **None** |
| Subgroup analyses | **None performed** |
| Publication-bias assessment | **Not assessed** |

**Why pooling cannot be conducted.** Meta-analysis requires effect estimates extracted from studies
judged eligible. No study has been judged eligible, because no full text has been assessed; no full
text has been assessed, because no record has been independently adjudicated; and the record set
itself derives from a search the project has shown to be narrower than its own protocol. Each
dependency is reported in Chapter 6 and enumerated in Chapter 11.

The software refuses to proceed at each of these points rather than returning an empty result. **The
absence of a pooled estimate in this report is the designed behaviour of a correctly functioning
pipeline, not a reporting omission.**

**No odds ratio, risk ratio, hazard ratio, confidence interval, p-value, I², τ² or pooled estimate
appears anywhere in this report.** The report contains no such value of any kind, synthetic or
otherwise.

---

# Chapter 10 — Discussion

## 10.1 Work completed

The project has delivered a specified protocol recorded as twenty-four dated, adopted decisions, each
with its rationale, its consequences and an explicit statement of what it does not cover. It has
delivered checksum-gated acquisition capable of recording a lost export honestly rather than
substituting for it; deduplication with an explicit identifier hierarchy that never merges a
near-match silently; a screening architecture enforcing the separation of machine suggestion from
human judgement at three independent points in code; a complete 93-field extraction schema; and a
tested statistical implementation with its limitations declared rather than discovered.

## 10.2 Methodological strengths

The principal strength is that the integrity properties usually asserted in a methods section are
enforced by the system. A worksheet containing 194 completed rows yields a formal screening count of
**zero**. That number is uncomfortable and correct; a pipeline reporting 194 screened on this data
would be a worse instrument. The same philosophy produced three refusals that would otherwise be
conveniences: extraction without included studies, synthesis without estimates, and silent continuity
correction of zero cells.

## 10.3 Data integrity and reproducibility

Raw data is immutable and verified by checksum at every stage that reads it. Human research records
are tracked precisely because they cannot be regenerated, while derived data is regenerable and
never hand-edited. Deterministic generation is verified by rebuilding and comparing bytes.

## 10.4 Screening limitations and the asymmetry of automated error

The 109/85 split is the output of an automated procedure applied to titles and abstracts. It has
**never been validated against human judgement on this corpus**; the instrument for doing so exists
and is unanswered.

The error profile is likely **asymmetric**. A false inclusion is caught at full text and costs
reviewer time. **A false exclusion removes a study permanently and invisibly**: it never appears in
any later stage, and nothing downstream can detect it. This asymmetry is the reason the blinded
verification sample exists and the reason the suggestions must not be relied upon until it is
answered.

## 10.5 Search limitations

One database has been searched, with a query that demands a literal phrase most aetiological papers
do not use, omits the non-cigarette product terms central to the exposure definition, and uses no
controlled vocabulary. The corrected strategy addresses these defects but has not been executed.

## 10.6 Database access

No subscription database access has been verified. Embase, the single most valuable addition for this
question, does not appear among the institution's advertised databases. **P007 remains open**, and
resolving it requires actions only the researcher can take.

## 10.7 Unresolved protocol decisions

Twelve numbered questions remain open. The most consequential for the evidence base are the
anatomical and histological scope questions, one of which affects 14 of the 85 reports provisionally
carried forward, and the risk-of-bias instrument, which blocks both appraisal and a prespecified
sensitivity analysis.

## 10.8 Statistical implementation limitations

REML has no external validation; the pooled estimate has no external reference check; no
Hartung–Knapp interval is implemented, which the Cochrane Handbook favours when *k* is small and τ²
is non-zero; no Mantel–Haenszel or Peto method exists, so rare-event data has no route; and no
meta-regression or dose–response model is implemented. Three of the five prespecified subgroup
dimensions cannot currently be run.

## 10.9 Implications for evidence synthesis

The approach taken here suggests that where automated classification is used in screening, the
recorded data should distinguish the act of suggesting from the act of deciding at field level, and
reporting should count them separately. The cost is a set of uncomfortable zeros; the benefit is that
the zeros are true.

---

# Chapter 11 — Limitations and prioritised completion roadmap

## 11.1 Limitations

1. **One database searched**, with a query narrower than its own protocol.
2. **The original v1 export is lost**, recorded as lost and never substituted; a residual discrepancy
   of approximately nine records remains unexplained.
3. **No subscription database access verified.**
4. **No formal independent human screening exists** — 0 of 194 adjudicated.
5. **The verification sample is unanswered** — 0 of 120 cells; no agreement rate or kappa exists.
6. **No full text retrieved or assessed; no study included; no datum extracted; no risk of bias
   assessed; no meta-analysis performed.**
7. **Automated suggestions are unvalidated on this corpus**, with a plausibly asymmetric error
   profile.
8. **Twelve numbered methodological questions remain open.**
9. **Not prospectively registered**; the provisional pass preceded registration.
10. **Single-reviewer design**, reported under PRISMA items 8 and 9.
11. **Statistical gaps** as set out in §10.8.

## 11.2 Prioritised completion roadmap

**Table 11.1 — Work required, in dependency order.**

| # | Work | Depends on | Owner |
|---|---|---|---|
| 1 | **Resolve database access** — verify Scopus, Web of Science and Embase; test IndMED reachability | — | Researcher |
| 2 | **Finalise search sources and strategy**; close P007 with a recorded decision | 1 | Researcher |
| 3 | **Complete search validation** — confirm Emtree headings; verify phrase and truncation behaviour in each interface | 2 | Researcher |
| 4 | **Measure a screening rate** on a prespecified 200-record sample, as D023 requires | 2 | Reviewer |
| 5 | **Execute formal searches**; register each export under D011 with date, count and checksum | 2, 3, 4 | Researcher |
| 6 | **Complete independent reviewer screening** of every retrieved record | 5, 8 | **Reviewer — cannot be generated** |
| 7 | **Answer the 120 verification cells** and score agreement against the acceptance rule | 6 | **Reviewer** |
| 8 | **Resolve eligibility decisions** — P014–P022 and the premalignant-lesion question | — | Researcher |
| 9 | **Retrieve and assess full texts** | 6, 8 | Reviewer |
| 10 | **Extract study and effect data** | 9 | Reviewer |
| 11 | **Decide P023** and complete risk-of-bias assessments | 10 | Reviewer |
| 12 | **Prespecify remaining statistical choices** — adjusted-estimate selection rule, minimum studies per subgroup, zero-cell policy, primary measure | 10 | Researcher |
| 13 | **Conduct meta-analysis only if sufficient eligible data exist**; cross-check REML externally | 10, 11, 12 | Researcher |
| 14 | **Complete PRISMA 2020 and PRISMA-S checklists** and the results sections | 13 | Researcher |

Items 6, 7, 9, 10 and 11 are the human reviewer's work and **cannot be automated or generated**.

**One ordering recommendation.** The existing 194 records should **not** be adjudicated before the
search is settled. They derive from the superseded query, and executing the adopted strategy will
replace the record set. Adjudicating now would mean performing that work twice.

---

# Chapter 12 — Conclusion

This project has produced a specified systematic review protocol and a validated research pipeline
for evaluating the association between smoked tobacco use and squamous cell carcinoma of the oral
cavity. Twenty-four methodological decisions are adopted and dated; one search execution is registered
with a verified checksum; 194 records have been imported, validated and deduplicated with complete
record conservation; a 93-field extraction schema is specified; and a statistical implementation
providing fixed-effect and random-effects models, two estimators of between-study variance,
heterogeneity statistics, prediction intervals, sensitivity and subgroup analyses has been
implemented and validated across 670 tests.

**The scientific question posed by this review remains unanswered.** No study has been judged
eligible, no effect estimate extracted and no synthesis performed. **No conclusion is drawn here
regarding the association between smoked tobacco and oral cavity squamous cell carcinoma**, and any
such conclusion would be unsupported by the evidence this project has so far assembled.

The contribution of the present period is therefore methodological rather than clinical: a
demonstration that the provenance properties on which evidence synthesis depends — that raw data was
not altered, that an automated suggestion was not mistaken for a human judgement, and that no result
was computed before the evidence supporting it existed — can be made properties of a system rather
than assurances in prose. The clearest evidence that the design functions as intended is the set of
zeros reported in Chapter 6.

---

# References

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for
   reporting systematic reviews. *BMJ*. 2021;372:n71.
2. Rethlefsen ML, Kirtley S, Waffenschmidt S, et al. PRISMA-S: an extension to the PRISMA statement
   for reporting literature searches in systematic reviews. *Systematic Reviews*. 2021;10:39.
3. Stroup DF, Berlin JA, Morton SC, et al. Meta-analysis of observational studies in epidemiology
   (MOOSE): a proposal for reporting. *JAMA*. 2000;283(15):2008–2012.
4. Higgins JPT, Thomas J, Chandler J, Cumpston M, Li T, Page MJ, Welch VA, editors. *Cochrane
   Handbook for Systematic Reviews of Interventions*. Version 6.5. Cochrane; 2024.
5. DerSimonian R, Laird N. Meta-analysis in clinical trials. *Controlled Clinical Trials*.
   1986;7(3):177–188.
6. Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. *Statistics in Medicine*.
   2002;21(11):1539–1558.
7. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple,
   graphical test. *BMJ*. 1997;315(7109):629–634.
8. Cohen J. A coefficient of agreement for nominal scales. *Educational and Psychological
   Measurement*. 1960;20(1):37–46.

**No primary study is cited**, because no study has been assessed for eligibility. The references
above are the methodological sources on which the design relies. **No reference in this report was
invented**; each is a standard, verifiable methodological source.

---

# Appendix A — Adopted PubMed search strategy

**Table A.1 — Term blocks.** Full query reproduced in the repository at
`docs/methods/recommended_search_strategy.md` §2.

| Block | Composition | Terms |
|---|---|---|
| Outcome | `"Mouth Neoplasms"[Mesh]` exploded, plus free-text phrasings, histology terms and named subsites | 43 |
| Exposure | Four MeSH headings (`Smoking`, `Tobacco Smoking`, `Cigarette Smoking`, `Tobacco Products`), plus free-text product terms including bidi, beedi, cheroot, chutta, dhumti, reverse smoking | 45 |
| Design block | **Absent by decision D023** | 0 |
| Filters | **None** — no language, date, species or publication-type restriction | 0 |

The two blocks are joined by a single `AND`. Validation confirmed balanced parentheses, paired
quotation marks, exactly one top-level `AND`, no design terms and no filter tags.

# Appendix B — Eligibility criteria summary

See Tables 3.1 and 3.2. Eligible: human adults; any smoked tobacco; non-smoking comparator;
oral-cavity SCC confirmed or ≥90%; case–control or cohort; effect estimate with 95% CI or derivable;
English language. Ineligible designs: cross-sectional, case series, reviews, trials.

# Appendix C — PRISMA-style accounting

Formal flow: identified 194 → unique 194 → **screened 0** → sought 0 → retrieved 0 → assessed 0 →
**included 0**. Provisional section, reported outside the flow: 194 classified, 109 for exclusion, 85
for retrieval, 0 unresolved. Eleven reconciliation identities hold.

# Appendix D — Extraction schema summary

**Table D.1 — Field counts.**

| Table | Fields | Rows | Status |
|---|---|---|---|
| `studies` | 34 | 0 | Complete |
| `estimates` | 47 | 0 | Complete; both formerly unresolved fields settled by D025 and D026 |
| `risk_of_bias` | 12 | 0 | **Provisional**, pending P023 |
| **Total** | **93** | **0** | — |

# Appendix E — Statistical formulas

Collected for reference; derivations in Chapter 7.

```
y        = ln(θ)
SE_CI    = [ ln(upper) − ln(lower) ] / (2 × 1.959964)
SE_2x2   = √( 1/a + 1/b + 1/c + 1/d )
ln(OR)   = ln(a) + ln(d) − ln(b) − ln(c)
w_i      = 1 / SE_i²
w*_i     = 1 / ( SE_i² + τ² )
ŷ        = Σ(w_i y_i) / Σ w_i
SE(ŷ)    = 1 / √( Σ w_i )
Q        = Σ w_i ( y_i − ŷ_FE )²            ~ χ²(k−1)
I²       = max( (Q − (k−1)) / Q , 0 ) × 100%
τ²_DL    = max( (Q − (k−1)) / C , 0 )       C = Σw_i − (Σw_i² / Σw_i)
95% CI   = exp( y ± 1.959964 × SE )
95% PI   = exp( ŷ_RE ± t_(k−2) √( τ² + SE(ŷ_RE)² ) )
```

# Appendix F — Outstanding methodological decisions

**Table F.1.**

| ID | Question | Blocks |
|---|---|---|
| P006 | Prospective protocol registration | Registration status |
| P007 | Database coverage | **Formal search execution** |
| P014–P022 | Anatomical and histological scope (9 questions) | **Full-text eligibility** |
| P023 | Risk-of-bias instrument and confounder definition | **Appraisal; subgroup and sensitivity analyses** |
| — | Premalignant-lesion scope (unnumbered) | Eligibility; affects 14 of 85 |
| — | Nine SAP subgroups versus five in the manuscript | Subgroup reporting |
| — | Adjusted-estimate selection rule | Any pooled analysis |
| — | Minimum studies per subgroup | Subgroup analyses |
| — | Zero-cell policy | Rare-event studies |

Additionally, D016–D019 are implemented and enforced but not adopted as protocol, and D021 is drafted
but not registered.

# Appendix G — Validation and test summary

**Table G.1.**

| Check | Result |
|---|---|
| NBIB parser — records parsed | 194 of 194 |
| Unique PMIDs recovered | 194 of 194 |
| Deduplication — record conservation | 194 in, 194 out, 0 lost |
| Pairs requiring human review | 0 |
| Raw export checksum | **Verified** |
| Screening and processed data files | **8 present; SHA-256 recorded for 3 in the supplementary material and verified; no persistent manifest covers the rest** |
| Verification-seed constants | **5 of 5 unchanged** |
| Deterministic figure generation | Byte-identical on rebuild |
| Deterministic workbook generation | Byte-identical on rebuild |
| Per-line query validation | 88 of 88 lines; 0 records retrieved |
| **Test suite** | **670 passed, 1 skipped, from 671 collected** |
