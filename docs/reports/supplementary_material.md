# Supplementary material

Companion to *Smoked tobacco use and the risk of squamous cell carcinoma of the oral cavity: a
systematic review protocol and interim report of study selection*.

Every figure in this document is derived from the project's committed data. Items marked **not yet
available** are those for which no data exist; no placeholder or illustrative content is supplied in
their place.

---

## S1. Search strategies

### S1.1 Strategy v1 — original, executed, export lost

```
("Oral Squamous Cell Carcinoma"[Title/Abstract] OR OSCC[Title/Abstract])
AND (smoking[Title/Abstract] OR cigarette[Title/Abstract])
AND ("case-control"[Title/Abstract] OR cohort[Title/Abstract])
```

| Item | Value |
|---|---|
| Database / platform | PubMed (NCBI) |
| Filters applied | Humans; English |
| Date searched | **Unknown; not recoverable from any surviving file** |
| Records retrieved | 138 — documented claim, unverified, no export survives |
| Export status | **Missing.** Not recreated and not substituted |

### S1.2 Strategy v1r — re-execution, registered

Query string identical to v1. **Filters: none.**

| Item | Value |
|---|---|
| Database / platform | PubMed (NCBI) |
| Date searched | **Not recorded.** Index dates bound it to on or after 25 October 2026 |
| Records retrieved | **194** |
| Export format | PubMed/MEDLINE `.nbib` |
| Export checksum (SHA-256) | `1d153fa80edd6bc97c92498bce8076873cc514f412de5113412fa71827e4ca1e` |
| Registry entry | `pubmed_v1r`, status `registered` |

### S1.3 Reconciliation of the 138, 150 and 194 counts

**Counts-only interrogation for strategy validation, not a formal literature search.** The 29
October 2026 figures below were obtained by submitting the query and reading back the number of
matching records. **No record was retrieved, downloaded, exported or screened; no export, checksum
or registry entry exists for them**, and no record reported in this review derives from them.

| Query as run | Count | Date |
|---|---|---|
| v1 query string, no filters | 194 | 29 October 2026 |
| v1 query string, Humans + English | 150 | 29 October 2026 |
| v1 query string, Humans + English, as documented | 138 | unknown |

Three records entered the database after the project was paused. The residual is **exactly nine
records**: 194 − 44 − 3 − 138 = 9, or **exactly 12** if the three post-pause records are not
attributed. It is an **exact arithmetic difference** against an **unverified** documented count of
138, not an approximate one, because 194 and 150 are both verified while 138 is a documented claim
with no surviving export. It **remains unexplained** and is **disclosed, never reconciled**
(**D029**, adopted 14 November 2026). The documented count has not been altered.

### S1.4 Corrected strategy — proposed, NOT executed

Prepared in response to an audit finding that the v1 query is narrower than the protocol's own
eligibility criteria. **No export exists and there is no registry entry.**

Outcome block (39 terms; every term names an oral-cavity site):

```
( "Mouth Neoplasms"[Mesh] OR "oral cancer"[tiab] OR "oral cancers"[tiab]
  OR "oral cavity cancer"[tiab] OR "oral cavity cancers"[tiab] OR "mouth cancer"[tiab]
  OR "mouth cancers"[tiab] OR "oral carcinoma"[tiab] OR "oral carcinomas"[tiab]
  OR "oral cavity carcinoma"[tiab] OR "oral neoplasm"[tiab] OR "oral neoplasms"[tiab]
  OR "mouth neoplasm"[tiab] OR "mouth neoplasms"[tiab] OR "oral cavity neoplasm"[tiab]
  OR "oral cavity neoplasms"[tiab] OR "oral malignancy"[tiab] OR "oral malignancies"[tiab]
  OR "oral squamous cell carcinoma"[tiab] OR "oral cavity squamous cell carcinoma"[tiab]
  OR "squamous cell carcinoma of the mouth"[tiab] OR OSCC[tiab]
  OR "oral epidermoid carcinoma"[tiab]
  OR "tongue cancer"[tiab] OR "tongue carcinoma"[tiab] OR "tongue neoplasm"[tiab]
  OR "tongue neoplasms"[tiab] OR "oral tongue"[tiab] OR "mobile tongue"[tiab]
  OR "buccal mucosa"[tiab] OR "buccal carcinoma"[tiab] OR "floor of mouth"[tiab]
  OR "gingival carcinoma"[tiab] OR "gingival cancer"[tiab] OR "gum cancer"[tiab]
  OR "hard palate"[tiab] OR "retromolar"[tiab] OR "alveolar ridge"[tiab] )
```

Exposure block:

```
( "Smoking"[Mesh] OR "Tobacco Smoking"[Mesh] OR "Cigarette Smoking"[Mesh]
  OR "Tobacco Products"[Mesh] OR smoking[tiab] OR smoker[tiab] OR smokers[tiab]
  OR smoked[tiab] OR cigarette[tiab] OR cigarettes[tiab] OR tobacco[tiab]
  OR "tobacco smoke"[tiab] OR "tobacco use"[tiab] OR "tobacco habit"[tiab]
  OR "tobacco habits"[tiab] OR "smoking habit"[tiab] OR "smoking habits"[tiab]
  OR "tobacco consumption"[tiab] OR bidi[tiab] OR bidis[tiab] OR beedi[tiab]
  OR beedis[tiab] OR cigar[tiab] OR cigars[tiab] OR cheroot[tiab] OR cheroots[tiab]
  OR "pipe smoking"[tiab] OR waterpipe[tiab] OR "water pipe"[tiab] OR "water-pipe"[tiab]
  OR hookah[tiab] OR hukka[tiab] OR shisha[tiab] OR shishas[tiab]
  OR narghile[tiab] OR narghila[tiab] OR nargile[tiab] OR narguile[tiab] OR goza[tiab]
  OR kretek[tiab] OR "clove cigarette"[tiab] OR "reverse smoking"[tiab]
  OR chutta[tiab] OR dhumti[tiab] OR chillum[tiab]
  OR "hand-rolled"[tiab] OR "hand rolled"[tiab]
  OR "roll-your-own"[tiab] OR "roll your own"[tiab] )
```

**Filters: none.** An optional study-design block is specified separately and is **not**
recommended for the primary search.

Smokeless tobacco and betel quid terms are **deliberately absent** from the exposure block; they are
confounders, not the exposure. Generic terms such as `tobacco` and `tobacco use` will nevertheless
retrieve smokeless-only studies, which are excluded at screening as a wrong exposure.

### S1.5 Syntax-validation record

**Counts-only interrogation for strategy validation — not a formal literature search and not the
search of record.** The counts below are of the **corrected proposed strategy**, which supersedes
the v2 draft validated on 29 October 2026. **No record was retrieved, downloaded, exported or
screened, and no registry entry exists.**

| Item | Value |
|---|---|
| Date | 12 November 2026 (UTC) |
| Platform | NCBI E-utilities `esearch.fcgi`, database `pubmed` |
| Method | HTTP POST, counts only; **no record retrieved, downloaded or exported** |
| Authentication | none; no API key, no sign-in, no account access |
| Errors or warnings | none; HTTP 200 |

| Line | Query | Count |
|---|---|---|
| 1 | Outcome block alone | 116,283 |
| 2 | Exposure block alone | 495,031 |
| 3 | Design block alone | 6,526,293 |
| 4 | **Outcome AND exposure — adopted primary query (D023)** | **8,190** |
| 5 | With the optional design block | **5,008** |

These are syntax-validation counts on the date shown. They are **not search yields**: nothing was
exported, no registry entry exists, and the database grows daily.

### S1.6 Peer review of the search

**Not performed.** No PRESS or equivalent peer review has been carried out on the v1, v1r or
proposed strategies. This is reported as a limitation.

### S1.7 Known-item retrieval test

**Not performed.** The repository contains no seed set of independently known eligible studies, and
none has been invented. Before the search of record is executed, the reviewer should assemble a seed
set of 10–20 studies known to be eligible, record them with persistent identifiers, and measure the
candidate strategy's recall against them. The result must be documented whatever it is.

---

## S2. Search strategy audit and database coverage

Full documents are held in the repository: `search_strategy_audit.md`,
`recommended_search_strategy.md`, `database_coverage_assessment.md` and the P007/P013 decision
memorandum.

Key measured findings from the committed export, used in the audit:

| Observation | Value |
|---|---|
| Records in the export | 194 |
| Records with no MeSH indexing at all | **42 (21.6%)** |
| Records containing "oral squamous cell carcinoma" | 153 |
| Records containing only the abbreviation OSCC | 36 |
| Records containing "oral cancer" | 68 |
| Records containing "mouth cancer" | 0 |
| Records matching the design block only via the word "cohort" | **98** |

---

## S3. Controlled vocabulary

**Decisions:** `include`, `exclude`, `unresolved`.

**Decision bases:** `adopted_from_suggestion` — the reviewer accepted an automated suggestion
without judging the record individually; `independently_adjudicated` — the reviewer judged the
record from its own evidence.

**Exclusion reasons by stage.**

| Code | Title/abstract | Full text |
|---|---|---|
| `wrong_population` | yes | yes |
| `wrong_outcome` | yes | yes |
| `wrong_exposure` | yes | yes |
| `wrong_design` | yes | yes |
| `review_or_meta` | yes | yes |
| `conference_abstract` | yes | yes |
| `animal_or_invitro` | yes | yes |
| `not_english` | yes | yes |
| `other` (requires justification) | yes | yes |
| `no_reference_group` | no | yes |
| `no_usable_data` | no | yes |
| `outcome_not_separable` | no | yes |
| `duplicate_publication` | no | yes |

The stage assignment is a **proposal awaiting endorsement**. Retrieval statuses (`sought`,
`retrieved`, `unavailable`) are not exclusion reasons; an unavailable full text is reported by
PRISMA as *not retrieved*.

---

## S4–S5. Screening worksheet and automated suggestion set

Held in the repository; their SHA-256 values are recorded below.

| File | Rows | SHA-256 |
|---|---|---|
| Title/abstract worksheet | 194 | `a68623477f81fb14c4b70ada70a5a9775cc8671e4b945152404bdb0c9794fe22` |
| Full-text worksheet | 85 | `e87d171243eeb56beca3cd53687f40f81d6e2210ee6110b3e27d2046918b159c` |
| Automated suggestion set | 194 | `e4dc15d61bb822e72daacd8677bc7e4050d62c9ff239773424189ec1157707b9` |

The suggestion set carries no decision, reviewer, date or approval column. Every one of the 194
recorded decisions equals its suggestion in both the decision value and the reason code, which is
why all 194 are labelled `adopted_from_suggestion`.

---

## S6. Blinded verification sample

| Item | Value |
|---|---|
| Sample size | **40 of 194 (20.6%)**, simple random without replacement |
| Seed | `1496879658` — the first 8 hex digits of the SHA-256 of the worksheet at the time of the draw |
| Worksheet digest at the draw | `5938922a529a7f7318824f4216b4b9ab05b920a14def7c15e72c15ea2a6076eb` |
| Draw date | **UNVERIFIED** — no run log; a commit date is not evidence of it |
| Response fields | `your_decision`, `your_reason_code`, `your_notes` — 3 per record, **120 cells** |
| **Completed** | **0 of 120** |
| Sheet checksum | `6b4f734375f94a513404a8275f0003c9ddbdffae92b82ede264f2450bc57e29a` |

**Pre-specified acceptance rule.** ≥95% agreement adopts the unsampled remainder; ≥90% and <95% is
EXTEND; <90% requires a full manual re-screen. Both thresholds are inclusive at their lower bound.

**EXTEND is a classification and a workflow pause, not an automatic second draw.** Four matters
governing any extension are unresolved: the outcome of a second EXTEND, the extension sampling
frame, pooling conditions, and any cap on extension samples.

**Pre-specified asymmetry rule.** Any record the reviewer would *include* that was recorded as
*exclude* triggers a sweep of every record excluded under that reason code, whatever the headline
rate. The opposite direction is recorded but triggers nothing.

**No agreement rate, kappa or verdict exists**, and no scoring report has been produced.

---

## S7. Decision record

| Status | Identifiers |
|---|---|
| **Adopted** | D001–D015, D020, D022–D029 (24 decisions) |
| **Proposed, implemented and enforced but not adopted** | D016, D017, D018, D019 |
| **Drafted, not entered in the register** | D021 — blinded verification acceptance methodology |
| **Open questions** | 12 numbered (P006, P007, P014–P022, P023), plus 2 unnumbered and 4 unnumbered extension matters. **P013 was resolved by D023 (2026-11-13); P003, P004, P009, P010 and P012 by D025–D029 (2026-11-14).** |

Decisions governing scope: the outcome definition; the exposure definition; single-reviewer
screening and extraction; separate registry entries per search execution; unfiltered retrieval with
language and species limits applied at screening; the identifier hierarchy
`record_id → report_id → study_id → estimate_id`; the canonical sampling-frame digest; and bounded
supplementary grey-literature searching, whose sources are conditional on an accessible interface
and none of which has been verified as reachable.

Note: eight resolved questions (P003, P004, P008, P009, P010, P011, P012 and P013) remain listed in
the register's pending section, each marked there as resolved by the decision that settled it. The
decisions themselves are adopted and their resolved status is not in doubt; what remains
unreconciled is the historical pending-section layout, a documentation defect recorded for later
correction.

---

## S8. Extraction schema and workbook

34 study-level fields and 47 estimate-level fields. Template workbooks with headers and **zero data
rows** accompany this document, together with a data dictionary of all 81 field definitions.

Three principles are enforced by validation: reported and calculated values never share a field;
missing is recorded explicitly as `NR`, `NA` or `UNCLEAR`, never blank, zero or inferred; and every
extracted number carries a source location naming the page, table or figure.

Three fields carry `status: unresolved` and cannot be treated as protocol-conformant until **P023**
is settled: `tool`, `domain` and `judgement`. `comparator_type` and `exposure_contrast` were settled
by **D025** and **D026** (14 November 2026) and are now enforced.

---

## S9. Characteristics of included studies

**Not yet available.** No study has been assessed for eligibility at full text.

## S10. Risk-of-bias assessments

**Not yet available.** No instrument has been selected and no study appraised. A template with the
instrument-agnostic provenance columns accompanies this document; domain names cannot be fixed until
the instrument is chosen.

---

## S11. Analysis code and validation record

All code is in the repository with pinned dependencies: Python 3.14, `scipy` 1.18.1, `matplotlib`
3.11.2, `pyyaml` 6.0.3, `pytest` 9.1.1. The full suite comprises 585 collected tests.

Declared validation limits of the statistical implementation: Cochran's Q and I² are checked against
published values and the fixed-effect and DerSimonian–Laird paths against hand-worked arithmetic;
the restricted maximum likelihood estimator is tested only for self-consistency and limiting
behaviour and has **no external validation**; there is no Hartung–Knapp–Sidik–Jonkman interval, no
Mantel–Haenszel or Peto method, and no meta-regression or dose–response model.

The synthesis entry point **refuses to run** while no included study and no extracted estimate
exist.

---

## S12. Reporting checklists

PRISMA 2020 and PRISMA-S checklists are **to be completed on submission**. They are not supplied
here because most items concern results that do not yet exist, and a checklist completed against
absent results would misrepresent the review's state.
