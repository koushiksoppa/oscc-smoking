# Internal project completion and audit report

**Scope.** Internal engineering and research-governance record. Discusses implementation detail and
tooling. Kept separate from the manuscript draft (`manuscript_draft.md`) in this directory.

**Established by inspection at commit `7374b6d` on `main`,** with two uncommitted documentation
corrections in the working tree (§11). Every count below was verified against the data, not taken
from an earlier report.

---

## 1. Objectives and scope

**Review question.** Is smoked tobacco use associated with an increased risk of squamous cell
carcinoma of the oral cavity?

**Deliverable intended.** A reproducible systematic review and meta-analysis whose every number is
traceable to an immutable source and a dated human decision.

**Governing principle.** A working research pipeline and a completed systematic review are
different things. This project has the first. It does not have the second, and no stage of the
review is scientifically complete.

---

## 2. Decisions adopted and pending

### Adopted (16)

| ID | Subject |
|---|---|
| D001–D007 | Search preservation, raw-export immutability, provenance rules, identifier hierarchy, lost-export policy, checksum semantics, no bibliographic content in fixtures |
| **D008** | Outcome: oral cavity SCC, histologically confirmed or ≥90% stated majority; pooled head-and-neck outcomes ineligible |
| **D009** | Exposure: any smoked tobacco; smokeless tobacco and betel quid are confounders |
| **D010** | Single-reviewer screening and extraction; automated output is a suggestion, never a decision |
| D011–D012 | One registry entry per search execution; re-execution export renamed |
| **D013** | Retrieve unfiltered; apply language and species limits at screening (a declared deviation) |
| D014–D015 | Deduplication identifier priority; statistical implementation and its declared limits |
| **D020** | Canonical sampling-frame digest for verification draws (adopted 2026-11-10) |

### Proposed — implemented and enforced, **not adopted** (4)

| ID | Subject | Consequence of non-adoption |
|---|---|---|
| D016 | Adopting a suggestion does not satisfy a decision field | Screening recorded under it is not protocol-conformant |
| D017 | Suggested reason code preserved beside the recorded one | — |
| D018 | Full-text decisions record their basis | — |
| D019 | PRISMA reports adjudicated outcomes; provisional reported separately | The reporting split is in force but unratified |

### Drafted, **not in the register** (1)

**D021 — blinded verification acceptance methodology.** The sample size, record-level agreement
definition, thresholds, asymmetry sweep, incomplete-response refusal and kappa treatment are all
pre-specified (2026-11-01), implemented and tested, but **no register entry adopts them**. A
revised draft exists and awaits approval. Until adopted, the acceptance rule is a pre-specified
implementation convention, not protocol.

### Open questions (18 numbered, plus 6 unnumbered)

The register's Pending section holds **20** `P0xx` rows, but **two of them are resolved** and have
simply not been moved out: **P008** was resolved by **D015** and **P011** by **D013**. The number
of genuinely pending numbered questions is therefore **18**, not 20. See §13 risk 13 for the
register defect this exposes.

Alongside them sit **two unnumbered open questions** — the premalignant-lesion scope and the stage
assignment of exclusion reasons — and **four unnumbered extension matters** deferred in the
verification architecture (second-EXTEND outcome, extension sampling frame, pooling rules, maximum
extension count). **24 open matters in total**, of which 18 carry an identifier.


| ID | Question | Blocks |
|---|---|---|
| **P007** | Which other databases? | Search completeness; the review's claim to be systematic |
| **P013** | v2 retrieves 4,770 against v1r's 194 — feasibility under one reviewer | Search execution; the value of screening effort |
| **P003** | Is an undefined "non-smoker" reference group eligible? | Full-text assessment, synthesis |
| **P004** | Which exposure contrast is primary? | Extraction, synthesis |
| **P006** | Prospective registration | Nothing; a deviation to report |
| P009 | Historical v1 search date | Reporting only; unrecoverable |
| P010 | Test fixture policy | Nothing |
| P012 | ~9-record residual in the 138 reconciliation | Reporting of the v1 count |
| **P014–P022** | Anatomical and histological scope (9 questions) | Full-text assessment; two need an inaccessible reference text |
| **P023** | Risk-of-bias instrument **and** the confounder set defining "adequate" | Risk-of-bias assessment |
| *(unnumbered)* | Are premalignant-lesion populations in scope? | Full-text assessment — affects **14 of 85** |
| *(unnumbered)* | Stage assignment of exclusion reasons | Screening conformance |
| *(4, no IDs)* | Second-EXTEND outcome; extension sampling frame; pooling rules; maximum extensions | Nothing now — no verdict exists |

---

## 3. Search and screening status

### Search — PARTIALLY COMPLETE

| Execution | Filters | Records | Status |
|---|---|---|---|
| `pubmed_v1` | Humans, English | 138 | **Export lost.** `export_missing`; contributes nothing |
| `pubmed_v1r` | **none** | **194** | **Registered**, checksum-verified; the sole evidence base |
| v2 | none | 4,770 | **Drafted and syntax-validated; not executed** |

Search dates: v1 **unrecoverable**; v1r **not recorded**, bounded to on/after 2026-10-25 by index
dates. Neither is estimated.

**Principal risk.** The executed query requires the literal phrase "Oral Squamous Cell Carcinoma"
or "OSCC" plus "smoking" or "cigarette" plus a literal design term. It is materially narrower than
the protocol's own eligibility criteria and omits the "oral cancer" aetiological literature and
non-cigarette product terms. **One database is not a systematic search.**

### Title/abstract screening — BLOCKED BY HUMAN REVIEW

| Measure | Value |
|---|---|
| Reports in worksheet | 194 |
| Carrying a recorded classification | 194 |
| **`adopted_from_suggestion`** | **194** |
| **`independently_adjudicated`** | **0** |
| Rows with `adjudicated_date` | 0 |
| Failing validation | 0 |
| **Formal PRISMA: screened / excluded / taken forward** | **0 / 0 / 0** |
| Provisional: classifications / excluded / forward / unresolved | 194 / 109 / 85 / 0 |

Provisional exclusion reasons: `wrong_outcome` 63, `wrong_design` 33, `review_or_meta` 10,
`not_english` 2, `wrong_population` 1 (total 109).

`validate_screening --stage ta --final` **fails** on this state, as designed.

### Blinded verification — BLOCKED BY HUMAN REVIEW

40 of 194 (20.6%); seed `1496879658`, derived from the data; **0 of 120 response cells complete**;
no leakage columns; byte-identical to the commit that introduced it. **No agreement rate, kappa or
verdict has ever been computed**, and no scoring report exists.

---

## 4. Deduplication and record management — COMPLETE AND VERIFIED

194 records → **194 unique reports**, **0 duplicates**, **0 pairs** requiring human review.
Identifier hierarchy `record_id → report_id → study_id → estimate_id` enforced; record matching and
study-level grouping remain separate concepts, and similar titles are flagged, never merged.

Matching is computed **once** per run and its result passed downstream; `assign_report_ids` consumes
the precomputed groups and pairs and contains no call to the matching routine. Verified by call
counting and pinned by regression tests.

---

## 5. Human-review queue status

Generated from current data, in units that are not summed:

| Quantity | Count |
|---|---|
| Distinct reports across all queues | **194** |
| Task instances | **319** (194 + 40 + 85 + 0) |
| Verification records | 40 |
| **Verification response cells** | **120**, of which **0** complete |

| Queue | Task instances | Complete |
|---|---|---|
| `ta_adjudication.csv` | 194 | 0 |
| `blinded_verification.csv` | 40 | 0 |
| `ft_retrieval.csv` | 85 | 0 |
| `ft_assessment.csv` | 0 | — |

Overlap verified against identifiers: the 40 sampled records are a subset of the 194; the 85
retrieval records are the title/abstract includes; **17 records appear in both** the verification
and retrieval queues. Queues carry no reviewer, date or decision column; the blinded queue's column
list makes disclosure of a recorded decision impossible. Regeneration is byte-for-byte reproducible
and never writes to a worksheet.

---

## 6. Full-text, extraction and appraisal status

| Stage | Status | Evidence |
|---|---|---|
| Full-text retrieval | **NOT STARTED** | 85 provisional rows; 0 retrieval statuses recorded |
| Full-text assessment | **NOT STARTED** | 0 eligibility decisions |
| Study linkage (`study_id`) | **NOT STARTED** | no study identifier assigned |
| Data extraction | **BLOCKED BY MISSING EVIDENCE** | schema (34 study + 47 estimate fields), template and validator built and tested; `data/extraction/` does not exist |
| Risk of bias | **REQUIRES USER DECISION** | table specified instrument-agnostically; no instrument (P023); 0 assessments |

Full-text attribution: `ft_sought` **0**, `ft_provisional_sought` **85**, `ft_invalid_source` 0,
`ft_ineligible_source` 0, `ft_unattributed` 0. All 85 descend from an adopted classification, so
none is formally sought.

Extraction schema recently extended with seven descriptive capture fields — smoking duration,
pack-years, other cumulative exposure (each with its own unit field), matching variables and
exposure ascertainment method. All optional, none wired into any analysis, explicit missing codes
(`NR` / `NA` / `UNCLEAR`) preserved so that missing is never read as zero.

---

## 7. Statistical-analysis readiness — BLOCKED BY MISSING EVIDENCE

Implementation built and tested: effect-measure conversion, fixed-effect and DerSimonian–Laird
pooling, REML, Cochran's Q, I², τ², forest and funnel plots. `run_analysis` **refuses**: *"nothing
to pool"*. The refusal is correct and must not be bypassed.

**Declared implementation limitations** (recorded in the decision register): REML has no external
validation and must be cross-checked before publication; no Hartung–Knapp–Sidik–Jonkman interval;
no Mantel–Haenszel or Peto method, so rare-event and zero-cell data have no route; no
meta-regression or dose–response model; pooled estimate, weights and τ² have no external reference
check.

**Analysis-plan gaps dependent on evidence or decisions**: primary effect measure; whether designs
may be pooled; model and estimator; exposure contrast (P004); reference-group handling (P003); the
rule for choosing among several adjusted models in one paper (recommended, not adopted).

---

## 8. PRISMA reporting status — PARTIALLY COMPLETE

Identification and the provisional section reconcile. All **11 arithmetic identities** hold.
Formal screening and every full-text cell read `0` or *pending*, correctly.

Five full-text attribution states are mutually exclusive and exhaustive — verified across all 48
reachable input combinations — so no invalid, provisional, stale or unattributed row can inflate a
formal count. The flow figure retains its 5 main / 4 side box structure, with states that sit
outside the flow named in a footnote rather than given boxes.

---

## 9. Software validation and test results

```
.venv/Scripts/python -m pytest -q
584 passed, 1 skipped
```

The single skip is by design: a registry entry whose export is missing has no file to check.

Counts below are **collected test counts** taken from `pytest --collect-only`, not counts of
`def test` functions. The two differ because parametrised cases expand to several collected tests.

| Area | Collected tests | Files |
|---|---|---|
| Screening, provenance, PRISMA | **156** | `test_screening` 108, `test_prisma_attribution` 20, `test_backfill_provenance` 28 |
| Acquisition, intake, registry, citations | **84** | `test_validation_rules` 23, `test_source_registry` 20, `test_intake` 17, `test_nbib_format` 15, `test_parse_citations` 7, `test_raw_sources` 2 |
| Verification sample and draw provenance | **64** | `test_verify_sample` 44, `test_draw_provenance` 20 |
| Deduplication (incl. matching authority) | **63** | `test_dedup` 52, `test_dedup_authority` 11 |
| Extraction schema and validation | **62** | `test_extraction` 62 |
| Analysis | **48** | `test_analysis` 48 |
| Screening display | **47** | `test_screening_show` 47 |
| PRISMA diagram | **32** | `test_prisma_diagram` 32 |
| Review queues | **29** | `test_review_queue` 29 |
| **Total** | **585** | = 584 passed + 1 skipped |

**No test weakened, deleted or disabled** across the branch: 0 test functions removed, 0 files
deleted, 371 assertions added against 3 changed (all expectation-text updates tracking approved
behaviour changes, each replaced with a stronger assertion).

**Reproducibility.** The derived datasets rebuild **byte-for-byte** from the immutable raw export.
Dependencies pinned (`pyyaml==6.0.3`, `pytest==9.1.1`, `scipy==1.18.1`, `matplotlib==3.11.2`);
Python 3.14.7. No absolute local paths and no credentials in tracked files (three scanner hits
verified as false positives: a `.gitignore` comment and the words "secretion"/"Secretaría" in
genuine bibliographic content).

---

## 10. Data integrity and checksum verification

All five protected files verified at the time of writing:

| File | SHA-256 | Status |
|---|---|---|
| `data/raw/pubmed/pubmed-v1r-reexecution-194.nbib` | `1d153fa8…e4ca1e` | MATCH |
| `data/screening/verification_sample.csv` | `6b4f7343…57e29a` | MATCH |
| `data/screening/ta_suggestions_2026-11-01.csv` | `e4dc15d6…7707b9` | MATCH |
| `data/screening/screening_ta.csv` | `a6862347…94fe22` | MATCH |
| `data/screening/screening_ft.csv` | `e87d1712…8b159c` | MATCH |

**No scientific value has been altered.** Across the whole branch, 0 original column values changed
in either worksheet; decisions remain `include` 85 / `exclude` 109; `adjudicated_date` populated 0;
all 85 full-text reviewer fields empty. Every one of the 194 `suggestion` cells traces to the
committed audit artefact, and every `decision_basis` equals the value derived from the evidence.

**History.** 10 commits ahead of `origin/main`, 0 behind, strictly linear, all single-parent.
`origin/main` is an ancestor of HEAD — fast-forward only. No history rewritten on this branch; the
one `filter-branch` entry in the reflog predates the branch point and is already reflected upstream.
**Nothing pushed.**

---

## 11. Uncommitted work in the tree

Two documentation corrections, prepared and validated but **not committed**:

| File | Change |
|---|---|
| `scripts/screening/verify_sample.py` | Module docstring corrected: the stale pre-D020 seed statement now distinguishes historical `file_bytes_crlf_v1` from future `ordered_report_ids_v1`; record-level agreement, incomplete-response refusal and EXTEND-as-pause added. `VERDICT_TEXT` for EXTEND and RE-SCREEN no longer promise actions the code does not perform |
| `docs/methods/screening.md` | Three new subsections: how agreement is calculated; what each verdict means; who is being compared with whom |

No implemented value changed; 584 tests pass; checksums unaffected.

---

## 12. Outstanding tasks

### Human research work (enumerable now)

| Task | Volume | Dependency |
|---|---|---|
| Independently adjudicate title/abstract classifications | **194 reports** | none — can start now |
| Complete the blinded verification sample | **120 response cells** | none — independent |
| Retrieve full texts and record status | **85 reports** | provisional until adjudicated |
| Assess eligibility | 0 assessable | retrieval |
| Assign `study_id`s; extract with source locations; appraise risk of bias | unknown | inclusion; P023 |

### Decisions required

**P007** and **P013** first (search coverage and volume); then **D016–D019** adoption, **D021**
adoption, **P023**, the premalignant-lesion scope and the exclusion-reason stage assignment; then
**P003** and **P004** before synthesis.

### Engineering (optional, not blocking)

Pin `data/screening/*.csv` line endings in `.gitattributes` so the historical digest is recomputable
on a non-Windows checkout; consider enforcing the EXTEND workflow pause in code rather than only in
documentation; implement the risk-of-bias table once P023 is settled.

---

## 13. Limitations and risks

| # | Risk | Severity | Mitigation / status |
|---|---|---|---|
| 1 | **Search covers one database with a query narrower than the protocol** | **High** | Disclosed; P007/P013 open. Any synthesis on 194 records risks selection bias of unknown direction |
| 2 | 4,770-record v2 volume is infeasible for one reviewer at ~20 hours | **High** | P013 open; narrowing for convenience explicitly refused |
| 3 | No screening independently adjudicated | **High** | Enforced in data and reporting; 194-report queue generated |
| 4 | Single reviewer throughout | Medium | D010; declared as a PRISMA limitation |
| 5 | Ten scope questions unresolved, two needing an inaccessible reference text | Medium | Blocks full-text assessment |
| 6 | Original v1 export lost; ~9-record residual unexplained | Medium | D005; not recreated, not reconciled by editing a count |
| 7 | Search dates unrecorded | Low–Medium | Reported as unverified, never estimated |
| 8 | No prospective registration | Medium | P006; deviation to be reported |
| 9 | REML unvalidated externally; no HKSJ, MH or Peto | Medium | D015; cross-check required before publication |
| 10 | Verification measures one reviewer against automated suggestions, not inter-reviewer agreement | Medium | Stated wherever the exercise is described |
| 11 | Historical draw digest is CRLF-specific | Low | Disclosed; D020 fixes it for future draws |
| 12 | EXTEND pause is documentary, not code-enforced | Low | No verdict can exist until the sample is scored |
| 13 | **Register defect: P008 and P011 are resolved (by D015 and D013) but remain rows in the Pending section.** A reader counting pending questions from the register gets 20 where the true figure is 18 | Low | **Documentation defect requiring later review.** Not corrected here: the decision register is out of scope for this task, and moving a row is a change to the research record that the reviewer should make or authorise. No decision ID has been assigned or altered |

---

## 14. Recommended next steps

1. **Settle P007 and P013.** Everything downstream depends on whether the evidence base is 194
   records or several thousand. Adjudicating 194 records drawn from a query that misses most of the
   eligible literature may be effort spent on the wrong set.
2. **Adopt or revise D016–D019 and D021.** All are implemented and enforced; none is protocol.
   D021 should be adopted *before* the verification sample is scored, since adopting thresholds
   after a rate is known would be post hoc.
3. **Settle P023** — instrument and confounder definition — before any study is appraised, for the
   same reason.
4. **Complete the blinded verification sample** (120 cells). It is independent of every other
   decision and directly informs how far the automated suggestions can be relied upon.
5. **Adjudicate the 194 classifications**, or re-screen against whatever search scope P007/P013
   produces.
6. **Resolve the scope questions**, including assigning an identifier to the premalignant-lesion
   question, before full-text assessment.
7. Then: retrieval, eligibility assessment, linkage, extraction, appraisal, and synthesis only if
   the extracted evidence supports it.
8. **Do not push** until the branch is reviewed; 10 commits are pending.
