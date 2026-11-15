# Project completion status

Established by inspecting the repository, not from memory. Every figure below was verified at
`0efdbd3` on `main`; this document is committed in the child of that commit, so HEAD is one ahead
of the state described. **670 passed, 1 skipped by design** (671 collected).

## The distinction this document exists to make

| | |
|---|---|
| **A working research pipeline** | Code that carries out each stage reproducibly, with provenance guarantees and gates that refuse invalid states. **This project has one**, through screening infrastructure, extraction validation and statistical analysis. |
| **A completed systematic review** | A review in which a human reviewer has screened records, retrieved full texts, judged eligibility, extracted data with source locations, appraised risk of bias and synthesised the result. **None of those has been completed.** |

A decision is **recorded** for all 194 reports at title/abstract, but every one of them was adopted
from an automated suggestion and **none has been independently adjudicated**. Under D010 a
suggestion cannot satisfy a decision field, so the formal PRISMA flow reports **0 screened, 0
excluded, 0 taken forward**, and the 194 appear in a separate provisional section. There are no
included studies, no extracted values, no risk-of-bias assessments and no pooled estimate. Every
statistical number in the repository comes either from a published methods source or from synthetic
test fixtures, and both are labelled as such.

---

## 1. Engineering completion

### Implemented and validated

| Component | Evidence |
|---|---|
| Source registry — one entry per database × search **execution** (D011) | `config/sources.yaml`; 19 tests |
| NBIB parser and intake checksum gate | `scripts/acquisition/`; 26 tests; refuses an unregistered or altered export |
| Citation validation | `scripts/validation/validate_citations.py`; 18 tests; PASS 0 errors 0 warnings on `pubmed_v1r` |
| Deduplication — identifier and fingerprint matching, similar titles flagged and never merged | `scripts/dedup/`; 52 tests; one authoritative matching computation, pinned |
| Screening worksheets, controlled vocabulary, decision provenance | `scripts/screening/`; 103 + 34 + 20 tests |
| Adjudication provenance — five-field requirement, shared validator, `--final` gate | `worksheet.adjudication_problems`, used by the validator, the full-text carry-forward and the PRISMA gatherer |
| PRISMA accounting — formal/provisional split, five full-text attribution states, 11 identities | `scripts/screening/prisma.py`; 49 tests |
| PRISMA flow figure | `scripts/visualization/prisma_diagram.py`; 29 tests |
| Blinded verification instrument, pre-specified acceptance rule | `scripts/screening/verify_sample.py`; 54 tests |
| Canonical sampling-frame digest (D020) | 20 tests covering every required invariance and sensitivity |
| Human review queues, generated from current data | `scripts/screening/review_queue.py`; 20 tests |
| Extraction schema, template and validator | `scripts/extraction/`; 62 tests |
| Statistical implementation — fixed-effect, DerSimonian–Laird, REML, heterogeneity | `scripts/analysis/`; 43 tests; D015 records its validation and its limits |
| Reproducibility | the derived datasets rebuild **byte-for-byte** from the immutable raw export |

### Known software limitations

- **REML has no external validation.** It is tested for self-consistency and limiting behaviour
  only; D015 records this and requires a cross-check against an established implementation before
  any REML estimate appears in a manuscript.
- No Hartung–Knapp–Sidik–Jonkman interval, which the Cochrane Handbook favours when k > 2 and
  τ² > 0 — the likely situation here. No Mantel–Haenszel or Peto methods, so rare-event and
  zero-cell data have no route. No meta-regression or dose–response model.
- The pooled estimate, weights and τ² have no external reference check (D015).
- **Risk of bias is specified but not implemented**, because the domains are the instrument and no
  instrument has been chosen (P023).
- The historical verification-sample digest is platform-dependent by construction. D020 fixes this
  for future draws; the existing sample's digest is recorded rather than recomputable on an LF
  checkout. Disclosed in `docs/methods/screening.md`.
- `data/screening/*.csv` are not pinned in `.gitattributes`, so their line endings follow
  `core.autocrlf`. This is why the historical digest is CRLF-specific.

---

## 2. Scientific completion

| Stage | Status | What is actually true |
|---|---|---|
| Search | **PARTIALLY COMPLETE** | `pubmed_v1r` executed and registered (194 records, unfiltered per D013). `pubmed_v1` (138) is lost and recorded as `export_missing` (D005); its search date is unrecoverable (P009). v2 is drafted and syntax-validated but **not executed**, and its volume is unresolved (P013). **PubMed alone is not a systematic search** — other databases remain unresolved (P007). |
| Deduplication | **COMPLETE AND VERIFIED** | 194 records → 194 unique reports, 0 duplicates, 0 pairs needing review. Reproducible byte-for-byte. |
| Title/abstract screening | **BLOCKED BY HUMAN REVIEW** | 194 decisions recorded, **all adopted from an automated suggestion, 0 independently adjudicated**. Formal flow: 0 screened. Not a completed stage. |
| Blinded verification | **BLOCKED BY HUMAN REVIEW** | Sample drawn (40 of 194, seed recorded). **0 of 120 response cells completed.** No agreement rate, no kappa, no acceptance outcome exists. |
| Full-text retrieval | **NOT STARTED** | 85 provisional rows exist; **no full text sought, retrieved or recorded**. |
| Full-text screening | **NOT STARTED** | No eligibility decision recorded for any report. |
| Data extraction | **BLOCKED BY MISSING EVIDENCE** | Schema, template and validator built and tested. `data/extraction/` does not exist, because no study has been included. |
| Risk of bias | **REQUIRES USER DECISION** | Table specified, instrument not chosen (P023). No study has been included, so nothing could be appraised yet in any case. |
| Statistical synthesis | **BLOCKED BY MISSING EVIDENCE** | Implementation built and tested against published values and hand-worked arithmetic. `run_analysis` **refuses to run**: no included studies, no extracted estimates. |
| PRISMA | **PARTIALLY COMPLETE** | Identification and the provisional screening outcome reconcile under all 11 identities. Formal screening and every full-text cell are `0` or `<pending>`, correctly. |
| Manuscript | **NOT STARTED** | Nothing to report yet. |

**No stage of the review is scientifically complete.** Deduplication is complete as an engineering
operation on the records retrieved; it does not make the search complete.

---

## 3. Human work remaining

Enumerated per record in `results/queues/`, regenerated from current data.

| Task | Records | Required human action | Evidence needed | Reviewer field | Date field | Status | Dependency | Next action |
|---|---|---|---|---|---|---|---|---|
| Title/abstract adjudication | **194** | Judge each record from its own title and abstract, independent of the suggestion shown | Title + abstract (in the worksheet) | `reviewer` | `screened_date`, `adjudicated_date` | 0 of 194 done | none — can start now | `results/queues/ta_adjudication.csv` |
| Blinded verification | **40** (120 cells) | Record a blinded judgement per sampled record | Title + abstract, **without** consulting the recorded decision | `your_decision` | n/a | 0 of 120 cells | none — independent of the rest | `results/queues/blinded_verification.csv`, then `verify_sample --score` |
| Full-text retrieval | **85** | Obtain each full text; record status and source | The article itself | n/a | n/a | 0 of 85 | provisional until the TA decision is adjudicated | `results/queues/ft_retrieval.csv` |
| Full-text eligibility | **0 assessable** | Assess against D008/D009 | Retrieved full text | `reviewer` | `screened_date`, `adjudicated_date` | none retrieved | retrieval | blocked |
| Study linkage (`report_id` → `study_id`) | unknown | Decide which reports describe one population (D004) | Retrieved full texts | `extracted_by` | `extraction_date` | not started | full-text inclusion | blocked |
| Data extraction | unknown | Extract with a page/table/figure location for every value | Retrieved full texts | `extracted_by` | `extraction_date` | not started | inclusion | blocked |
| Risk-of-bias appraisal | unknown | Appraise each included study | Retrieved full texts | `assessed_by` | (to be added) | not started | P023 **and** inclusion | blocked |

Enumerable today, in units that are not added together: **194 distinct reports**,
**319 task instances** (194 + 40 + 85 adjudication, verification and retrieval tasks, some on the
same records), and **120 verification response cells**, of which **0** are complete. A response
cell is not a task instance; the 85 retrieval tasks have no response cells at all. The remaining
work cannot be enumerated because the included set does not exist.

No automated suggestion substitutes for any of these.

---

## 4. User decisions remaining

Full text of each in `docs/decisions/decision_log.md`. Recommendations below are **recommendations,
not adopted decisions**.

| ID | Status | Question | Options | Consequence | Recommendation |
|---|---|---|---|---|---|
| **D016–D019** | **Proposed** | Adopt the adjudication-provenance rules now implemented and enforced? | adopt / revise / reject | Decisions recorded under them are not protocol-conformant until adopted | Adopt; they are implemented, tested and already enforced |
| **D021** | **Drafted; not in the register** | Adopt the blinded verification acceptance methodology — sample size, record-level agreement, thresholds, asymmetry sweep, incomplete-response refusal, kappa treatment? | adopt / revise | Pre-specified 2026-11-01 and implemented, but no register entry adopts it, so the acceptance rule is an implementation convention rather than protocol. Adopting after an agreement rate is known would be post hoc | Adopt **before** the verification sample is scored |
| **P003** | **Resolved — D025** | Is an undefined "non-smoker" reference group eligible? | both eligible; `never_smoker` primary, `non_smoker_undefined` sensitivity | Never promoted to primary; reported *not estimable* below k = 3 | Adopted 2026-11-14 |
| **P004** | **Resolved — D026** | Which contrast is primary? | ever vs never primary; current and former secondary | Dose–response narrative and tabular only, never pooled (D015(e)) | Adopted 2026-11-14 |
| **P006** | Pending | Prospective registration (PROSPERO/OSF)? | register / declare unregistered | The title/abstract pass was performed without registration — a deviation that must be reported either way | Declare the deviation explicitly |
| **P007** | Pending | Which other databases? | Embase / Scopus / WoS / LILACS / combinations | **PubMed alone is not a systematic search.** Affects whether the review can be called systematic | — |
| **P009** | **Resolved — D027** | Historical v1 search date | permanently unverified | v1 unrecoverable; `pubmed_v1r.search_date` stays null pending the reviewer's personal verification | Adopted 2026-11-14 |
| **P010** | **Resolved — D028** | Test fixture and synthetic-content policy | strict, no carve-out | Provenance rule 6 retained in full; the synthetic demonstration was removed from the repository | Adopted 2026-11-14 |
| **P012** | **Resolved — D029** | The record-count residual in the 138 reconciliation | document as unresolved | Exactly 194 − 44 − 3 − 138 = 9, or 12 if the three post-pause records are not attributed; 138 is an unverified historical claim | Adopted 2026-11-14 |
| **P013** | Pending | v2 retrieves 4,770 records against v1r's 194 | screen all / add a second screener / v1r primary + v2 supplementary / narrow v2 | Determines the review's sensitivity; ~20 hours of single-reviewer work | — |
| **P014–P022** | Pending | Anatomical and histological scope (lip, soft palate, straddling ICD codes, site purity, SCC variants) | see each entry | Determines eligibility for individual reports. **P021/P022 require the WHO Blue Book, which was inaccessible** | — |
| **P023** | **Pending (new)** | Risk-of-bias instrument, and which confounders the confounding domain requires | NOS / ROBINS-E / NOS per domain without a total | Determines what the reviewer looks for in every study; changing it later means reassessing everything | **ROBINS-E**, or NOS-per-domain if the workload is prohibitive — `docs/methods/risk_of_bias_options.md` |
| **Unnumbered** | Pending | Are populations restricted to **premalignant oral lesions** in scope? | in / out of scope | Affects 14 of the 85 reports taken forward. **No identifier covers this yet** | Assign an identifier and settle before full-text assessment |
| **Unnumbered** | Pending | Stage assignment of exclusion reasons in `config/screening.yaml` | endorse / revise | Still a proposal; decisions made under it are not protocol-conformant until endorsed | Endorse |

None of these blocks the engineering that remains.

---

## 5. Final completion matrix

| Workstream | Status | Evidence | Remaining blocker | Next action |
|---|---|---|---|---|
| Provenance rules and registry | COMPLETE AND VERIFIED | `config/sources.yaml`, 19 tests | none | — |
| Acquisition and intake gate | COMPLETE AND VERIFIED | 26 tests; checksum gate refuses altered input | none | — |
| Citation validation | COMPLETE AND VERIFIED | PASS, 0 errors 0 warnings | none | — |
| Deduplication | COMPLETE AND VERIFIED | 52 tests; byte-for-byte reproducible | none | — |
| Screening infrastructure | COMPLETE AND VERIFIED | `--final` gate enforced | none | — |
| Adjudication provenance (D016–D019) | IMPLEMENTED BUT NOT VALIDATED | implemented and enforced; **Proposed**, not adopted | reviewer adoption | adopt or revise D016–D019 |
| Draw provenance (D020) | COMPLETE AND VERIFIED | ADOPTED 2026-11-10; 20 tests | none | — |
| Title/abstract screening | BLOCKED BY HUMAN REVIEW | 194 adopted, 0 adjudicated | reviewer time | work `ta_adjudication.csv` |
| Blinded verification | BLOCKED BY HUMAN REVIEW | 0/120 cells | reviewer time | work `blinded_verification.csv` |
| Multi-sample verification (M-2) | NOT IMPLEMENTED (design only) | `docs/methods/verification_sample_architecture.md` | 4 unresolved questions; no EXTEND verdict exists | leave design-only |
| Full-text retrieval | NOT IMPLEMENTED | 85 provisional rows, 0 sought | TA adjudication; reviewer time | work `ft_retrieval.csv` |
| Full-text screening | NOT IMPLEMENTED | no decision recorded | retrieval | — |
| Study linkage | NOT IMPLEMENTED | no `study_id` assigned | full-text inclusion | — |
| Extraction | BLOCKED BY MISSING EVIDENCE | schema + validator, 62 tests | no included studies | — |
| Risk of bias | REQUIRES USER DECISION | table specified, instrument absent | **P023** | settle P023 |
| Statistical synthesis | BLOCKED BY MISSING EVIDENCE | 43 tests; `run_analysis` refuses | no extracted estimates | — |
| PRISMA | PARTIALLY COMPLETE | 11 identities reconcile | formal counts need adjudication | — |
| Search completeness | REQUIRES USER DECISION | PubMed only | **P007, P013** | settle P007 and P013 |
| Reproducibility | COMPLETE AND VERIFIED | byte-for-byte rebuild; pinned deps; no absolute paths, no credentials | none | — |
| Neutral terminology | COMPLETE AND VERIFIED | 0 vendor references in tracked materials or history | none | — |
| Documentation | COMPLETE AND VERIFIED | README, AGENTS.md and methods guides match the code | none | — |
| Manuscript | NOT IMPLEMENTED | — | every stage above | — |

---

## What would make this a completed review

In order, and none of it generatable:

1. Settle **P007** and **P013** — decide the databases and the v2 volume, or accept and declare
   that the search is PubMed-only and not fully systematic.
2. Adjudicate the **194** title/abstract records independently, and complete the **120** blinded
   verification cells.
3. Adopt or revise **D016–D019**; settle **P023**, the premalignant-lesion scope and the exclusion-
   reason stage assignment.
4. Retrieve and assess the full texts; assign `study_id`s; extract with a source location for every
   value; appraise risk of bias.
5. **P003 and P004 are settled (D025, D026).** The remaining blockers to synthesis are P023 and the
   adjusted-model selection rule — and cross-check REML externally before reporting
   it (D015).
