# Project completion roadmap

**Prepared 14 November 2026** by inspecting the repository's actual files, data and code — not from
previous progress summaries. Every status below was re-derived at the time of writing.

> ## The distinction this document exists to enforce
>
> **The technical infrastructure is substantially complete. The scientific review has barely begun.**
>
> Fifteen pipeline stages exist; five have run on real data. **Zero studies are included, zero
> estimates extracted, zero risk-of-bias assessments made, and no pooled estimate exists.** The
> formal search has never been executed against any database.
>
> Infrastructure completion is **not** review completion, and this roadmap is organised so the two
> cannot be confused.

## Verified state at the time of writing

| Fact | Value |
|---|---|
| Registered search executions | **1** (`pubmed_v1r`, 194 records) |
| Formal searches under the adopted D023 strategy | **0** |
| Unique reports after deduplication | 194 |
| Title/abstract classifications | 194, **all `adopted_from_suggestion`** |
| **Independently adjudicated decisions** | **0 of 194** |
| Verification sample response cells completed | **0 of 120** |
| Full texts retrieved / assessed | **0 / 0** |
| Studies included | **0** |
| Estimates extracted | **0** (`data/extraction/` does not exist) |
| Risk-of-bias assessments | **0** |
| Pooled estimates | **0** |
| Adopted decisions / proposed / open questions | 18 / 4 / 22 |
| Test suite | 615 passed, 1 skipped |

---

## Legend

**Status** — `COMPLETE`, `PARTIAL`, `BUILT NOT RUN`, `NOT STARTED`, `BLOCKED`.
**Human?** — whether the work requires the human reviewer and cannot be generated.
**Programmatic?** — whether a tool can complete it once its inputs exist.

---

## 1. Protocol and research decisions

| | |
|---|---|
| **Status** | `PARTIAL` |
| **Evidence** | `docs/decisions/decision_log.md`: 18 adopted (D001–D015, D020, D022, D023), 4 proposed (D016–D019), 22 open questions. `docs/protocol/` holds the provenance rules and eligibility criteria |
| **Missing** | D016–D019 never adopted though implemented and enforced in code. D021 drafted, never registered. 22 open questions, of which **P014–P022 plus the premalignant-lesion question block full-text eligibility**. P003/P004 leave two extraction fields `unresolved`. P006 (registration) outstanding. P023 (risk-of-bias instrument) outstanding |
| **Dependencies** | None — these are decisions, not work products |
| **Next action** | Adopt or revise D016–D019; register or renumber D021; resolve the ten scope questions **before** full-text screening |
| **Human?** | **Yes, entirely.** These are the reviewer's decisions |
| **Programmatic?** | No. Drafting proposals is; deciding is not |

## 2. Database coverage and search strategies

| | |
|---|---|
| **Status** | `PARTIAL` — strategies drafted, coverage undecided |
| **Evidence** | `docs/search/database_search_strategies.md` (5 databases translated); `docs/methods/recommended_search_strategy.md` (adopted D023 query); `docs/methods/p007_database_coverage_decision.md`; `docs/methods/p007_access_verification_record.md` (blank, awaiting the researcher) |
| **Missing** | **P007 is open.** No database access beyond PubMed is verified. Embase not listed by the institution; Scopus and Web of Science advertised but unverified; IndMED untested. Four of five translations are untested drafts; 5 Emtree headings unconfirmed |
| **Dependencies** | P007 ← access verification ← the researcher |
| **Next action** | Complete `p007_access_verification_record.md` in the live interfaces, then close P007 with a recorded decision |
| **Human?** | **Yes** — access verification requires signing in |
| **Programmatic?** | Translation yes (done); verification no |

## 3. Formal search execution

| | |
|---|---|
| **Status** | `NOT STARTED` |
| **Evidence** | `config/sources.yaml` holds 2 entries: `pubmed_v1` (`export_missing`) and `pubmed_v1r` (registered, 194 records). **Neither is the adopted D023 strategy** |
| **Missing** | **Everything.** The adopted query has never been executed as a formal search in any database. The existing 194-record set comes from the superseded v1 query, which the project itself describes as narrower than its own protocol |
| **Dependencies** | P007 (which databases) → PC-1 decision (dead term) → D023's screening-rate condition → D011 registration authorisation |
| **Next action** | Decide PC-1; verify access; measure a screening rate on 200 records; then execute and register each search |
| **Human?** | **Yes** — execution, export and registration are the researcher's acts |
| **Programmatic?** | Partially — parsing, validation and checksum registration are automated once an export exists |

## 4. Record identification and deduplication

| | |
|---|---|
| **Status** | `COMPLETE` for `pubmed_v1r`; will need re-running for the real search |
| **Evidence** | `data/processed/citations/pubmed_v1r_citations.csv` (194 parsed); `data/processed/dedup/report_index.csv` (194 reports, 0 duplicates, 0 `needs_review`). 63 tests across `test_dedup.py` and `test_dedup_authority.py` |
| **Missing** | **Cross-database deduplication is untested in practice.** The rules have only ever run on one source that produced zero duplicates. Multi-database input will produce real duplicates and records lacking PMIDs — Embase conference abstracts in particular |
| **Dependencies** | Stage 3 |
| **Next action** | Review the matching rules against multi-database input **before** the first multi-source run |
| **Human?** | No, except adjudicating `needs_review` pairs |
| **Programmatic?** | **Yes** |

## 5. Title-and-abstract screening

| | |
|---|---|
| **Status** | `BLOCKED` — provisional only |
| **Evidence** | `data/screening/screening_ta.csv`: 194 rows, all with `decision_basis = adopted_from_suggestion`; 109 provisional exclusions (63 `wrong_outcome`, 33 `wrong_design`, 10 `review_or_meta`, 2 `not_english`, 1 `wrong_population`), 85 carried forward. **0 independently adjudicated.** `validate_screening --stage ta --final` fails on this state, by design |
| **Missing** | **194 independent adjudications**, plus the 120 verification response cells and their agreement scoring. A decision-log entry describing how the provisional pass was conducted is still outstanding and is needed for PRISMA item 8 |
| **Dependencies** | The scope questions (§1) should be resolved first, or adjudication will be done twice. **If the search is re-executed under D023, this record set changes entirely** |
| **Next action** | **Do not adjudicate these 194 yet.** Settle P007 and the search first; the record set will change |
| **Human?** | **Yes, absolutely.** Cannot be generated (D010) |
| **Programmatic?** | No. Suggestions may order records for presentation; they may never satisfy a decision field |

## 6. Full-text retrieval and screening

| | |
|---|---|
| **Status** | `NOT STARTED` |
| **Evidence** | `data/screening/screening_ft.csv`: 85 rows, **every reviewer field empty**. All 85 are `ft_provisional_sought`; `ft_sought` is 0 |
| **Missing** | Retrieval of every full text; eligibility assessment of every one |
| **Dependencies** | §5 adjudication → scope questions resolved → the eligibility gate, which refuses without adjudicated includes |
| **Next action** | Blocked. ONOS may assist with obtaining full texts once there are texts to obtain |
| **Human?** | **Yes** |
| **Programmatic?** | Retrieval logistics partly; eligibility no |

## 7. Data extraction

| | |
|---|---|
| **Status** | `BUILT NOT RUN` |
| **Evidence** | Schema: 34 study + 47 estimate fields in `config/extraction.yaml`; blank workbook at `results/manuscript/extraction_workbook/` (93 documented fields, 0 rows). `data/extraction/` **does not exist**. 62 tests |
| **Missing** | All extraction. Two fields (`comparator_type`, `exposure_contrast`) are `unresolved` pending P003/P004 |
| **Dependencies** | §6 includes; P003, P004 |
| **Next action** | Blocked by the extraction gate, which refuses without included studies |
| **Human?** | **Yes** |
| **Programmatic?** | Validation yes; extraction no |

## 8. Risk-of-bias assessment

| | |
|---|---|
| **Status** | `NOT STARTED` — **instrument not chosen** |
| **Evidence** | `config/extraction.yaml` `risk_of_bias` block: 12 structural fields, `status: provisional`, `depends_on: P023`. Domain names and judgement categories **deliberately absent**. A test asserts no instrument is named anywhere |
| **Missing** | The instrument itself (P023), the domain definitions it brings, and every assessment |
| **Dependencies** | **P023** — and it is the researcher's decision, not a coding task |
| **Next action** | Decide P023 (Newcastle–Ottawa, ROBINS-E or another), then populate the domain list from the chosen instrument |
| **Human?** | **Yes** |
| **Programmatic?** | Schema population yes, once P023 is decided; judgements no |

## 9. Effect-size calculation

| | |
|---|---|
| **Status** | `BUILT NOT RUN` |
| **Evidence** | `scripts/analysis/effects.py`: `from_ci`, `from_counts`, `from_log_se`; log-scale handling for OR/RR/HR; CI-asymmetry check at 10%; `validate_set` enforces one estimate per study, refuses mixed measures, refuses synthetic/real mixing |
| **Missing** | No input. **See §E-gap below: the `Estimate` object carries no adjustment or subgroup information** |
| **Dependencies** | §7 |
| **Next action** | Close the adjustment/subgroup gap before extraction begins, so the data model supports the planned analyses |
| **Human?** | Selecting which estimate per study is a reviewer decision (`selected_for_analysis`) |
| **Programmatic?** | **Yes**, for the computation |

## 10. Meta-analysis

| | |
|---|---|
| **Status** | `BUILT NOT RUN` — **gate refuses** |
| **Evidence** | `scripts/analysis/meta.py`: inverse-variance fixed-effect and random-effects, DerSimonian–Laird and REML estimators of τ², prediction interval at ≥3 studies. `run_analysis.py` refuses without estimates and rejects any row marked synthetic. 48 tests |
| **Missing** | Every input. **Pooling may not be appropriate even when estimates exist** — the protocol pre-specifies criteria for *not* pooling |
| **Dependencies** | §7, §9 |
| **Next action** | None possible. Do not run with zero studies |
| **Human?** | The decision whether to pool at all |
| **Programmatic?** | **Yes**, once estimates exist |

## 11. Heterogeneity and sensitivity analyses

| | |
|---|---|
| **Status** | `PARTIAL BUILD` |
| **Evidence** | Cochran's Q with χ² p-value, I², τ² implemented. Leave-one-out implemented |
| **Missing** | **No subgroup machinery exists at all** (§E-gap). Five subgroup analyses are pre-specified in the manuscript and **none can currently be performed**. Risk-of-bias-stratified sensitivity analysis additionally depends on P023 |
| **Dependencies** | §10; P023; the adjustment/subgroup data-model gap |
| **Next action** | Implement subgroup pooling and carry subgroup fields into `Estimate` — **before** extraction, so the schema and analysis agree |
| **Human?** | No |
| **Programmatic?** | **Yes** |

## 12. Publication-bias assessment

| | |
|---|---|
| **Status** | `BUILT NOT RUN`, and **may never be appropriate** |
| **Evidence** | Egger's regression and funnel plots implemented; `MIN_STUDIES_EGGER = 10` refuses below ten studies |
| **Missing** | Inputs. **If fewer than ten studies are included, no test will run and none should be reported** |
| **Dependencies** | §10 |
| **Next action** | None. Do not promise this analysis |
| **Human?** | No |
| **Programmatic?** | Yes, conditionally |

## 13. PRISMA reporting

| | |
|---|---|
| **Status** | `COMPLETE` as machinery; `PARTIAL` as content |
| **Evidence** | `scripts/screening/prisma.py` with 11 reconciliation identities and the formal/provisional split; `scripts/visualization/prisma_diagram.py` generating a deterministic figure; `results/validation/prisma_counts.md` |
| **Missing** | The flow reports zeros because the work is undone. **PRISMA-S** requires per-database strategies, dates and counts — none exists. The PRISMA 2020 and PRISMA-S **checklists themselves are not completed** (supplementary S12) |
| **Dependencies** | All upstream stages |
| **Next action** | Complete the checklists at submission; the flow fills itself from data |
| **Human?** | Checklist completion yes |
| **Programmatic?** | The flow and figure: **yes** |

## 14. Systematic review manuscript

| | |
|---|---|
| **Status** | `PARTIAL` — correctly an interim report |
| **Evidence** | `docs/reports/manuscript_final.md` → DOCX/PDF in `results/manuscript/`. Sections 3.3–3.9 and the Conclusion marked *Not yet available*. Status note at `docs/reports/manuscript_status_note.md` |
| **Missing** | Every results section; the conclusion; references 7–8 (pending P023); supplementary S9, S10, S12 |
| **Dependencies** | §6–§12 |
| **Next action** | Leave as an interim report. **Do not retitle or fill placeholder sections with anything but real extracted evidence** |
| **Human?** | Yes, for interpretation |
| **Programmatic?** | Generation yes; content no |

## 15. Reproducibility and repository organisation

| | |
|---|---|
| **Status** | `GOOD` with identified debt |
| **Evidence** | 615 passed, 1 skipped (616 collected). Pinned dependencies. Checksum-gated raw data. Deterministic generation verified for the PRISMA figure, the workbook and the report figures. 104 tracked files; **47 untracked** |
| **Missing** | **47 untracked files including every current research memorandum and all deliverables** — they carry no commit, no checksum and no provenance. Repository structure has grown organically; `docs/reports/` now mixes manuscripts, audits and roadmaps |
| **Dependencies** | None |
| **Next action** | Commit the untracked work; then restructure per `docs/reports/repository_cleanup_plan.md` |
| **Human?** | Authorisation only |
| **Programmatic?** | **Yes** |

---

## E-gap — the statistical data-model gap, stated once

Two findings from the Part E audit bear on several stages above and are recorded here so they are
not lost in the per-stage tables.

**1. The analysis layer cannot see adjustment status.** The extraction schema records 14 fields
relevant to adjustment and subgrouping — `adjustment`, `adjusted_for`, seven `adjusted_*` flags,
`exposure_contrast`, `product_types`, `comparator_type`, `outcome_site`, `selected_for_analysis`.
**None of them is carried into `scripts.analysis.effects.Estimate`**, which holds only `study_id`,
`log_estimate`, `se`, `measure`, `derivation`, `source_location`, `synthetic` and `notes`.

Consequence: the code **cannot distinguish an adjusted estimate from a crude one**, and cannot
restrict a pooled analysis to alcohol-adjusted estimates — one of the five pre-specified subgroup
analyses.

**2. There is no subgroup machinery.** No function in `scripts/analysis/` performs subgroup pooling,
and no field identifies a subgroup. The manuscript pre-specifies five subgroup analyses — product
type, region, anatomical subsite, risk-of-bias level, alcohol-adjusted versus unadjusted. **None is
currently implementable.**

**Why this matters now rather than later.** Both are cheap to fix while `data/extraction/` is empty
and expensive once it is populated, because the extraction schema and the analysis data model would
then have to be migrated together. **This is the single most valuable piece of engineering work
available before the review resumes.**

---

## Dependency map

```
P007 access verification ──┐
PC-1 dead-term decision ───┼──▶ FORMAL SEARCH ──▶ parse ──▶ deduplicate ──┐
screening-rate measurement ┘                                              │
                                                                          ▼
P014–P022 + premalignant scope ──────────────────────▶ TITLE/ABSTRACT ADJUDICATION (194+)
                                                                          │
                                   verification sample (120 cells) ◀──────┤
                                                                          ▼
                                                              FULL-TEXT RETRIEVAL
                                                                          │
P003, P004 ───────────────────────────────────────────▶ EXTRACTION ◀──────┤
E-gap fix (adjustment + subgroup fields) ─────────────▶     │             │
P023 instrument ──────────────────────────────▶ RISK OF BIAS              │
                                                            ▼             ▼
                                              EFFECT SIZES ──▶ META-ANALYSIS
                                                                          │
                                           subgroup machinery ────────────┤
                                                                          ▼
                                                        PRISMA ──▶ MANUSCRIPT
```

**Critical path:** P007 → formal search → adjudication → full text → extraction → synthesis.
**Everything downstream of the formal search depends on a record set that does not yet exist.**

---

## The ordering decision that matters most

**The existing 194 records should not be adjudicated yet.**

They come from the superseded v1 query. If the adopted D023 strategy is executed — which it must be
for the review to be defensible — the record set changes substantially: the corrected PubMed
strategy alone stands at roughly 8,190 records against the current 194, and any additional database
adds more.

Adjudicating 194 records now would mean doing that work against a record set about to be replaced.
**Settle P007, execute the search, and adjudicate once.**

---

## What this document does not do

- It does **not** execute a search, export records, create a D011 entry, change D023, or close P007.
- It does **not** create screening decisions, extraction data, risk-of-bias assessments or any
  pooled estimate.
- It does **not** delete, move or rename any file.
- Every status is derived from the repository as inspected on 14 November 2026.
