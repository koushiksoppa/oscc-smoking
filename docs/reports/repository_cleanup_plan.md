# Repository cleanup plan and proposed final architecture

**Prepared 14 November 2026** by inspecting the repository.

> ## NOTHING HAS BEEN DELETED, MOVED, RENAMED OR OVERWRITTEN
>
> This is a **plan**. Every file remains exactly where it was. No Git history was rewritten and
> nothing was committed. Each item below carries a classification for the reviewer to act on, or
> not.

**Scope inspected:** 104 tracked files, 47 untracked, plus caches. Searched for duplicates, obsolete
intermediates, superseded drafts, temporary files, stale reports, redundant workbooks, unused
scripts, unreferenced images, unnecessary documentation, empty directories and contradictory status.

## Classification

| Class | Meaning |
|---|---|
| **KEEP** | Essential research evidence or an active project component |
| **ARCHIVE** | Historical or superseded, but important for provenance. **Retained, relocated at most** |
| **REVIEW** | Possible redundancy requiring the reviewer's confirmation |
| **SAFE TO REMOVE** | Demonstrably unnecessary and reproducible |

## Never removable, under any classification

`data/raw/` exports · `data/raw/SHA256SUMS` · `data/screening/*.csv` · adjudication history ·
`docs/decisions/decision_log.md` · `docs/protocol/` · `data/extraction/` when it exists ·
risk-of-bias records · provenance documentation · Git history.

---

## 1. Headline findings

| # | Finding | Severity |
|---|---|---|
| 1 | **47 files are untracked**, including every current research memorandum, all deliverables and 5 reporting scripts. They carry no commit, no checksum and no provenance in a project whose discipline is provenance | **High** |
| 2 | **No duplicate files, no temporary files, no empty directories, no unreferenced images.** All 5 PNGs are referenced; `results/queues/` is referenced by live code | — |
| 3 | Three different test counts appear across documents (584, 599, 615) — but **every stale figure sits in a historical or self-pinned document**, and all operative documents say 615. **Not a defect** | None |
| 4 | `docs/reports/` mixes manuscripts, audits, roadmaps and speaker notes — eleven files of four different kinds | Medium |
| 5 | `build_manuscript.py`'s usage docstring cites `manuscript_draft.md`, the **superseded** draft, rather than `manuscript_final.md` | Low |
| 6 | `__pycache__` directories exist but are correctly gitignored | None |

---

## 2. Classification by file

### 2.1 KEEP — research evidence and active components

| Path | Why |
|---|---|
| `data/raw/**` + `SHA256SUMS` | **Immutable research input.** Never removable |
| `data/screening/*.csv` (4) | Human research records; not regenerable |
| `config/*.yaml` (3) | Operative configuration — sources, screening vocabulary, extraction schema |
| `docs/decisions/decision_log.md` | The register. 18 adopted, 4 proposed, 22 open |
| `docs/protocol/**` (3) | Provenance rules, eligibility criteria, anatomical scope |
| `docs/data_dictionary/**` (3) | Field definitions |
| `scripts/**` (38 files, 9 packages) | All referenced and tested |
| `tests/**` (20 files) | 616 collected |
| `docs/methods/` — pipeline, screening, extraction, intake, analysis validation, obtaining exports, verification architecture | Operative method documentation |
| `docs/methods/recommended_search_strategy.md` | **The adopted D023 strategy.** Operative |
| `docs/methods/p007_*.md` (2) | P007 is open; both are live |
| `docs/search/database_search_strategies.md`, `database_search_validation_checklist.md`, `phase_2k_manual_validation_log.md` | Operative search strategies and live validation records |
| `docs/reports/manuscript_final.md` + its DOCX/PDF | The operative manuscript |
| `docs/reports/supplementary_material.md` + DOCX/PDF | Operative supplement |
| `docs/reports/manuscript_status_note.md` | States what is and is not ready |
| `results/final_submission/**` (12) | Current submission package |
| `results/manuscript/extraction_workbook/**` (5) | Blank templates, deterministically regenerable, but shipped with the package |
| `results/queues/**` (5) | **Referenced by `scripts/screening/review_queue.py`** — live, not stale |
| `results/figures/prisma_flow.png` | Generated, embedded in the manuscript, deterministic |
| `results/validation/**` (6) | Stage validation reports; regenerable but are the audit trail |

### 2.2 ARCHIVE — historical, preserved for provenance

**Recommendation: retain in place, or relocate to `docs/archive/` with a banner. Do not delete.**

| Path | Why archive rather than keep | Why not remove |
|---|---|---|
| `docs/reports/manuscript_draft.md` | Superseded by `manuscript_final.md` (598 vs 660 lines) | It is the earlier manuscript of record; its 4,770 figures document what was drafted then |
| `docs/reports/internal_audit_report.md` | A dated audit; its 584-test figure was true when written | **Rewriting a historical audit conclusion would falsify the record** |
| `docs/reports/phase_1c_deliverable_audit.md` | Dated audit of Phase 1C/1D | Same |
| `docs/project_completion_status.md` | **Self-pinned snapshot** — "verified at `0efdbd3`" | Editing it breaks its own provenance claim. The reviewer has already ruled: preserve unchanged |
| `docs/search/search_v1_pubmed.md` | Historical v1 strategy | The v1 export is lost; this is the only record of the query |
| `docs/search/search_v1r_pubmed_reexecution.md` | Record of the registered execution | **Evidence for the only registered search** |
| `docs/search/search_v2_pubmed.md` | Superseded draft, now banner-labelled | Historical record of what was drafted |
| `docs/methods/search_strategy_audit.md` | Dated audit that found the C-1 defect | Historical reasoning |
| `docs/methods/p007_p013_decision_memorandum.md` | Superseded by the separate P007 and P013 memoranda | Records the joint reasoning |
| `docs/methods/p013_design_block_decision.md` | Phase 2F evaluation; §6.3 explicitly superseded | Its §1.1 holds **the only surviving verbatim copy of the original P013 wording**, which the register no longer contains |
| `docs/methods/p013_decision_proposal.md` | The proposal adopted as D023 | Record of what was authorised |
| `docs/methods/grey_literature_scope_decision.md` | The proposal adopted as D022 | Same |
| `docs/methods/database_coverage_assessment.md` | Feeds the open P007 | Arguably KEEP while P007 is open |
| `docs/methods/protocol_decisions_for_researcher.md` | Partly superseded — its P013 section is closed | Other questions remain live |

### 2.3 REVIEW — requires the reviewer's confirmation

| # | Item | Question |
|---|---|---|
| R1 | **47 untracked files** | Commit them? They are the project's current state and carry no provenance until committed. **This is the most consequential item in this plan** |
| R2 | `docs/reports/` holds 11 files of 4 kinds | Split into `docs/manuscript/`, `docs/reports/`, `docs/archive/`? See §3 |
| R3 | `docs/methods/` holds 12 tracked + 9 untracked files, mixing live method docs with closed-decision memoranda | Separate `docs/methods/` from `docs/decisions/memoranda/`? |
| R4 | `results/manuscript/extraction_workbook/` | Deterministically regenerable from `build_workbook.py`. Keep in the repo, or generate on demand? Either is defensible |
| R5 | `results/validation/` | Regenerable, but they are the stage audit trail. Keep tracked |
| R6 | `docs/reports/manuscript_draft.md` | Archive, or keep alongside the final? |

### 2.4 SAFE TO REMOVE

| Item | Why | Caveat |
|---|---|---|
| `__pycache__/` (11 directories) | Build artefacts, regenerated on import, **already gitignored** | Removal is cosmetic — they are not in the repository |
| *(nothing else)* | **No duplicate, temporary, obsolete-intermediate or unreferenced file was found** | — |

**This is a deliberately short list.** Searching for removable files found almost none: there are no
stray `.tmp`, `.bak` or editor files, no empty directories, no unreferenced images, and no
unused scripts. Pre-edit copies made during this session were written to the scratchpad, outside
the repository, by design.

---

## 3. One small correction, proposed not applied

`scripts/reporting/build_manuscript.py`'s usage docstring reads:

```
python -m scripts.reporting.build_manuscript --source docs/reports/manuscript_draft.md
```

It cites the **superseded** draft. The operative source is `manuscript_final.md`. A one-line
docstring fix — **not made**, since this phase changes nothing.

---

## 4. Proposed final repository structure

**Proposed only. No file has been moved.** The aim is that each directory answers one question, and
that the provenance boundaries the project already enforces become visible in the layout.

```
oscc-smoking-meta-analysis/
│
├── protocol/                      ← PROTOCOL AND METHODS
│   ├── provenance_rules.md
│   ├── eligibility_criteria.md
│   ├── anatomical_histological_scope.md
│   └── decisions/
│       ├── decision_log.md            the register — 18 adopted, 4 proposed, 22 open
│       └── memoranda/                 proposals behind adopted decisions (D022, D023, P007)
│
├── search/                        ← SEARCH STRATEGIES AND LOGS
│   ├── strategies/
│   │   ├── adopted_pubmed.md          the D023 query (currently recommended_search_strategy.md)
│   │   └── database_translations.md   Embase, Scopus, WoS, IndMED
│   ├── logs/
│   │   ├── validation_log.md
│   │   └── access_verification_record.md
│   └── archive/                       v1, v1r, v2 historical records
│
├── data/
│   ├── raw/                       ← RAW SOURCE RECORDS (immutable + SHA256SUMS)
│   ├── processed/                 ← PROCESSED RECORDS (generated, gitignored)
│   ├── screening/                 ← SCREENING AND ELIGIBILITY (tracked; not regenerable)
│   └── extraction/                ← EXTRACTION + RISK OF BIAS (tracked when it exists)
│
├── scripts/                       ← CODE, unchanged: common, acquisition, validation,
│   └── …                            dedup, screening, extraction, analysis,
│                                     visualization, reporting
│
├── results/
│   ├── validation/                    stage reports
│   ├── figures/                       PRISMA flow, forest, funnel
│   └── analysis/                      pooled results, when they exist
│
├── manuscript/                    ← MANUSCRIPT
│   ├── manuscript.md                  source
│   ├── supplementary.md
│   └── build/                         generated DOCX/PDF
│
├── reports/                       ← TECHNICAL DOCUMENTATION AND DELIVERABLES
│   ├── project_report/                report + presentation + speaker notes
│   └── roadmap/                       completion roadmap, analysis requirements
│
├── docs/archive/                  ← SUPERSEDED, retained for provenance
│
└── tests/                         ← TESTS
```

### What this changes, and what it must not

| Preserved exactly | Why |
|---|---|
| `data/raw/` paths and `SHA256SUMS` | **Checksums are path-relative.** Moving a raw export breaks verification. Do not move |
| `data/screening/` paths | Hard-coded in `scripts/screening/` and in 110 tests |
| `config/` paths | Referenced by `scripts/common/config.py` and the schema loader |
| Git history | Never rewritten |

**Consequence:** a restructure touching `data/` or `config/` requires code and test changes in the
same commit, and re-verification of every checksum afterwards. **The `docs/` reorganisation is
low-risk; the `data/` reorganisation is not, and is not recommended.**

**Recommended sequencing if adopted:**

1. Commit the 47 untracked files **first**, so the move is visible as a move rather than as a
   deletion plus an addition.
2. Reorganise `docs/` only — zero code impact.
3. Leave `data/`, `config/`, `scripts/` and `tests/` paths **unchanged**.
4. Run the suite and re-verify all checksums after each step.

---

## 5. Recommended order of action

| # | Action | Risk | Authorisation needed |
|---|---|---|---|
| 1 | **Commit the 47 untracked files** | Low | **Yes** |
| 2 | Fix the `build_manuscript.py` docstring | None | Yes |
| 3 | Decide R2/R3/R6 — the `docs/` reorganisation | Low | Yes |
| 4 | Decide R4/R5 — regenerable artefacts | None | Yes |
| 5 | **Do not restructure `data/`, `config/`, `scripts/` or `tests/`** | High | Not recommended |

---

## 6. What this document does not do

- It does **not** delete, move, rename or overwrite any file.
- It does **not** rewrite Git history, commit or push.
- It does **not** alter raw exports, checksums, screening decisions, protocol decisions or
  provenance documentation.
- Every classification is a **recommendation** for the reviewer.
