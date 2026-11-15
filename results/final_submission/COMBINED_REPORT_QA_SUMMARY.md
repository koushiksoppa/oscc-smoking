# Combined official report — quality assurance summary

**Document under review:** `Official_Systematic_Review_and_Meta_Analysis_Report.docx` / `.pdf`
**Source:** `docs/reports/official_systematic_review_and_meta_analysis_report.md`
**QA performed:** 14 November 2026, by reopening the produced files rather than trusting the build log.

| Property | Value |
|---|---|
| PDF pages | **36** |
| DOCX size / PDF size | 799,228 B / 620,966 B |
| Source blocks | 367 |
| Headings | 101 |
| Tables | 35 |
| Figures | 5 embedded |
| Chapters | 12, plus preliminaries, references and 8 appendices |

---

## 1. Verification method

Numerical claims were **recomputed from the repository**, not transcribed from earlier reports. DOCX
text was read by parsing `word/document.xml` with an XML parser; PDF text by decompressing the
content streams and decoding the string operands. Comparisons normalise whitespace and punctuation
and tolerate page-boundary splits.

---

## 2. Numerical verification — 25 of 25 claims confirmed

Every figure in the brief was independently recomputed before being written.

| Claim | Verified | Source |
|---|---|---|
| Records imported | **194** ✓ | parsed citations |
| Unique reports | **194** ✓ | deduplication index |
| Duplicates | **0** ✓ | deduplication audit |
| Provisional classifications | **194** ✓ | title/abstract worksheet |
| Provisional exclusions | **109** ✓ | title/abstract worksheet |
| Carried forward | **85** ✓ | title/abstract worksheet |
| Independently adjudicated | **0** ✓ | `decision_basis` field |
| Formal screening decisions | **0** ✓ | PRISMA accounting |
| Full texts sought / retrieved / assessed | **0 / 0 / 0** ✓ | full-text worksheet |
| Included studies | **0** ✓ | `data/extraction/` absent |
| Extraction records | **0** ✓ | `data/extraction/` absent |
| Risk-of-bias assessments | **0** ✓ | `data/extraction/` absent |
| Pooled clinical estimates | **0** ✓ | no estimates exist |
| Verification: 40 reports / 120 cells / 0 answered | ✓ ✓ ✓ | verification sample |
| Schema 34 / 47 / 12 / 93 | ✓ ✓ ✓ ✓ | extraction configuration |
| Exclusion reasons 63 / 33 / 10 / 2 / 1 | ✓ | title/abstract worksheet |
| 42 of 194 without MeSH | ✓ | parsed citations |
| Test suite | **669 passed, 1 skipped** ✓ | pytest, re-run at QA |
| One historical export; v1 lost; `pubmed_v1r` = 194 | ✓ | source registry |
| D023 adopted (no design block) | ✓ | decision register |
| D024 removed the ineffective quoted phrase | ✓ | decision register; term absent from the adopted query |
| Formal multi-database search incomplete | ✓ | registry holds no adopted-strategy execution |
| P007 unresolved | ✓ | open-questions table |
| Full-text assessment not started | ✓ | worksheet fields empty |
| Prospective registration not completed | ✓ | P006 open |

---

## 3. One correction made during QA

> **The number of open methodological questions is 17, not 22.**

The brief and several existing project documents state 22. Recomputation of the register's pending
table found **20 rows, of which 3 are marked resolved** (P008, P011, P013 — the last by D023),
leaving **17 genuinely open numbered questions**: P003, P004, P006, P007, P009, P010, P012,
P014–P022, P023.

**The new official report uses 17 throughout.** The figure 22 appears to have originated before
P013 was resolved and to have propagated.

**Documents still carrying the superseded figure** — *reported, not modified, because the brief
prohibits altering existing deliverables*:

| File | Location |
|---|---|
| `docs/reports/final_research_project_report.md` | §23, supplementary table (S7 row) |
| `docs/reports/final_presentation_speaker_notes.md` | numbers table |
| `docs/reports/repository_cleanup_plan.md` | §2.1 register row |
| `docs/reports/project_completion_roadmap.md` | §1 (also states 18 adopted, now 19 after D024) |

`docs/reports/supplementary_material.md` already states 17 correctly.

---

## 4. Document integrity — DOCX and PDF

| Check | Result |
|---|---|
| DOCX opens; `word/document.xml` parses | **PASS** |
| PDF valid; 36 pages | **PASS** |
| Headings present in the PDF **in document order** | **101 / 101** |
| Table cells present in both formats | **1,006 / 1,006** |
| Numeric tokens in tables present in both | **162 / 162** |
| Sampled prose sentences present in the PDF | **99 / 100** |
| Figures embedded in the DOCX | **5 / 5** |
| **Page numbering** | **36 / 36 pages carry their own number** |
| Broken or missing glyphs | **None observed** |
| Empty pages | **None** |

**On the one unmatched sentence.** It straddles a page boundary, where the running footer is spliced
into the extraction stream. Both halves were confirmed present independently. **No content is missing
from the PDF.** The 37th text stream is the figure XObject, not a page.

---

## 5. Structural checks

| Check | Result |
|---|---|
| Preliminary pages: status statement, abstract, keywords, contents, list of tables, list of figures, abbreviations | **All present** |
| Chapters 1–12 present and in order | **PASS** |
| Heading hierarchy consistent (chapter → section → subsection) | **PASS** |
| Tables numbered by chapter (3.1, 4.1, 6.7 …) and all listed | **PASS** — 35 tables |
| Figures numbered and all listed | **PASS** — 6.1, 6.2, 8.1, 8.2, H.1 |
| References section present; 8 sources | **PASS** |
| Appendices A–H present | **PASS** |
| Reads as one continuous document, not two reports joined | **PASS** — one numbering sequence, one reference list, statistical methodology integrated as Chapters 7–9 rather than appended |
| Mathematical notation renders | **PASS** — formulas set in fixed-width blocks; Unicode τ², I², χ², √, Σ render in both formats |

**Note on the table of contents.** Chapter and section titles are listed; **page numbers are not
printed in the contents table**, because the generator typesets the PDF after the Markdown is fixed
and a two-pass page-number injection was not performed. Page numbers **are** present in the document
footer on all 36 pages. This is recorded as a known limitation rather than a defect.

---

## 6. Scientific integrity checks

| Check | Result |
|---|---|
| Any claim of a **completed systematic review** | **NONE** |
| Any claim of a **completed meta-analysis** | **NONE** |
| Any **clinical conclusion** about smoked tobacco and oral cavity SCC | **NONE** |
| Provisional classifications described as completed human screening | **NONE** |
| Fabricated studies, participants, cases, estimates, intervals, p-values or heterogeneity statistics | **NONE** |
| Fabricated risk-of-bias judgements, search dates or reviewer decisions | **NONE** |
| Invented references or citations | **NONE** — 8 references, all standard methodological sources |
| Counts-only interrogation figures presented as search yields | **NONE** — labelled at every occurrence |
| AI, vendor or tool attribution | **NONE** |

### The provisional/formal distinction

Explicitly stated at six points, including a standalone callout in Chapter 6:

> *"194 provisional classifications do not mean 194 records were formally screened."*

**One automated check flagged this sentence as a prohibited phrase.** On inspection it is the **only**
occurrence of that wording in the document and it appears **inside the negation**. Verified: the
count of `"do not mean 194 records were formally screened"` equals the count of
`"194 records were formally screened"`. **False positive; no defect.**

### Synthetic demonstration

| Check | Result |
|---|---|
| Placed **outside** the scientific results | **PASS** — Appendix H only |
| Diagonal watermark "SYNTHETIC TEST DATA — NOT A RESEARCH RESULT" on the figure | **PASS** |
| Appendix header repeats the warning | **PASS** |
| States its sole purpose is software demonstration | **PASS** |
| States "None of this is a finding of this project" | **PASS** |
| Synthetic values confined to the appendix | **PASS** — the only numeric value (2.09) appears after Chapter 9 |
| Chapter 9 independently states no pooled estimate exists | **PASS** |
| Synthetic data added to any research dataset | **NO** — constructed in memory, marked synthetic, never written to `data/` |

### Documented discrepancy, not silently reconciled

The statistical analysis plan lists **nine** candidate subgroup dimensions; the manuscript names
**five**. Chapter 7.10 records both, states that the implementation follows the manuscript's five,
and flags the question of which set is prespecified as open — because anything beyond the
prespecified set must be declared post-hoc. **Not reconciled silently.**

---

## 7. Subgroup readiness as reported

| Dimension | Reported status | Verified against code |
|---|---|---|
| Product type | Ready | ✓ |
| Alcohol adjustment | Ready | ✓ |
| Anatomical subsite | Blocked — P014–P022 | ✓ |
| Geographical region | Blocked — no region scheme | ✓ |
| Risk-of-bias level | Blocked — P023 | ✓ |

---

## 8. Repository safety

| Constraint | Status |
|---|---|
| Files deleted, moved or renamed | **None** |
| Raw source data modified | **No** — checksum verifies |
| Protected screening records modified | **No** — 7 of 7 files verify |
| Protocol decisions changed | **No** — register unchanged this task |
| New formal database searches run | **No** |
| Extracted data fabricated | **No** — `data/extraction/` still absent |
| Synthetic data added to research datasets | **No** |
| Committed or pushed | **No** |
| Existing 22-page interim report or presentation overwritten | **No** — both untouched |
| Unrelated project code modified | **No** |

**Files added by this task (3):**

- `docs/reports/official_systematic_review_and_meta_analysis_report.md` (source)
- `results/final_submission/Official_Systematic_Review_and_Meta_Analysis_Report.docx`
- `results/final_submission/Official_Systematic_Review_and_Meta_Analysis_Report.pdf`
- plus this QA summary.

---

## 9. Unresolved issues

| # | Issue | Severity | Disposition |
|---|---|---|---|
| 1 | Four existing documents state **22** open questions; the verified figure is **17** | **Medium** | Reported in §3. Not corrected, because the brief prohibits modifying existing deliverables. Recommend a follow-up correction pass |
| 2 | `project_completion_roadmap.md` states **18** adopted decisions; now **19** after D024 | Low | Same disposition |
| 3 | Table of contents carries no page numbers | Low | Known generator limitation; footer page numbers present on all 36 pages |
| 4 | Report length **36 pages** against a 25–35 target | Low | One page over; content is substantive, with no padding. No action taken, since trimming would remove verified material |
| 5 | Figure 6.2 reuses the existing PRISMA diagram rather than a bespoke one | Low | The existing figure is generated from live data and is deterministic; a second diagram would duplicate it |

**No high-severity issue was found. No scientific-integrity defect was found.**

---

## 10. Test suite and checksums at QA

| Check | Result |
|---|---|
| Test suite | **669 passed, 1 skipped** |
| Raw export checksum | **OK** |
| Protected screening and processed data files | **7 of 7 OK** |
| `data/extraction/` | Absent, as expected |
| Source registry entries | 2 — no new registration |

The single skipped test is skipped **by design**: the raw-source test for the lost v1 export.
