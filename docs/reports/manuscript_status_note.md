# Manuscript status note

**Subject:** the publishable systematic review manuscript, `manuscript_final.md` and its generated
DOCX and PDF.
**Date:** 13 November 2026.
**Purpose:** to state, in one page, what that manuscript currently is, what it is not, and what
evidence must exist before it can be submitted as a completed systematic review.

---

## 1. What the manuscript is

A **protocol and interim report of study selection**. Its title says so:

> *Smoked tobacco use and the risk of squamous cell carcinoma of the oral cavity: a systematic
> review protocol and interim report of study selection.*

It is a legitimate document in its present form. It reports a prespecified protocol, a search that
was executed and registered, a deduplication result, and a provisional selection pass whose
provisional status is stated throughout. It is **not** a draft that becomes a completed review by
adding a results paragraph.

## 2. What is ready

| Section | State |
|---|---|
| Title, abstract, keywords | Complete, and the abstract's Conclusion is marked *Not yet available* |
| 1. Introduction | Complete |
| 2. Methods (2.1–2.9) | Complete as a protocol, with open criteria flagged in place |
| 3.1 Search results | Complete — 194 records |
| 3.2 Study selection | Complete — formal and provisional counts reported separately |
| Figure 1, PRISMA flow | Complete, generated from the data, formal flow reading zero |
| 4. Discussion (4.1–4.7) | Complete for the current state, including limitations |
| Declarations | Complete |
| References | 8 methodological sources; items 7–8 need full detail on submission |
| Supplementary S1–S8, S11 | Available |

## 3. What is not ready

| Section | State | Blocked on |
|---|---|---|
| 3.3 Characteristics of included studies | *Not yet available* | No study included |
| 3.4 Participant and exposure characteristics | *Not yet available* | No extraction |
| 3.5 Risk of bias | *Not yet available* | No appraisal; instrument undecided (P023) |
| 3.6 Individual study findings | *Not yet available* | No extracted estimates |
| 3.7 Quantitative synthesis | *Not yet available* | No estimates to pool |
| 3.8 Subgroup and sensitivity analyses | *Not yet available* | No synthesis |
| 3.9 Publication bias | *Not assessed* | Not meaningful below ten studies |
| 5. Conclusion | *Not yet available* | No evidence supports one |
| Supplementary S9, S10 | *Not yet available* | No included studies, no appraisals |
| Supplementary S12 | To be completed on submission | PRISMA checklists |

These sections are **retained as marked placeholders rather than deleted**. That is deliberate: it
shows a reader what a completed review will contain and makes each absence auditable.

## 4. Evidence required before publication as a completed review

In dependency order. Items 1–7 are researcher decisions; items 8–13 are work.

| # | Required | Why it blocks publication |
|---|---|---|
| 1 | Verify database access; close **P007** | One database is not a systematic search |
| 2 | ~~Decide **P013**~~ — **resolved by D023 (2026-11-13)**: the primary search carries no study-design block | Done |
| 3 | Resolve **P014–P022** and the premalignant-lesion question | Eligibility cannot be applied consistently; affects 14 of 85 |
| 4 | Decide **P023** — appraisal instrument | Risk of bias cannot be assessed, and references 7–8 cannot be completed |
| 5 | Decide **P003**, **P004** — comparator and contrast | Two extraction fields remain `unresolved` |
| 6 | Adopt or revise **D016–D019**; register or renumber **D021** | Implemented in code but not protocol |
| 7 | Register the protocol (**P006**) | The deviation compounds with delay |
| 8 | Execute the corrected search; register each export | The current record set rests on a query narrower than its own criteria |
| 9 | **Independently adjudicate every title/abstract record** | The formal PRISMA flow reads zero until this is done |
| 10 | **Complete the 120 verification cells and score agreement** | No kappa, no acceptance verdict exists |
| 11 | Retrieve and assess full texts | No study can be included |
| 12 | Extract study and estimate data | Nothing to synthesise |
| 13 | Appraise risk of bias; run the synthesis; cross-check REML externally | The results sections depend on all of the above |

## 5. Rules that must hold until then

1. **The manuscript is not retitled** to remove "protocol and interim report" until items 8–13 are
   complete.
2. **No section marked *Not yet available* is filled with anything but real extracted evidence.**
3. **No pooled estimate, forest plot, funnel plot, heterogeneity statistic or p-value** appears in
   the manuscript until it is computed from extracted study data.
4. **The 194 provisional classifications are never reported as completed screening**, and their
   reason codes are never presented as a PRISMA exclusion table.
5. **No database is reported as searched** unless its search was executed and its results preserved
   (D022).

## 6. Relationship to the project report

The research project report, `Research_Project_Report.docx`, is a **separate document with a
different purpose**: it describes the pipeline, its implementation and its validation. The two must
not be merged, and neither substitutes for the other. The project report may legitimately describe
a complete and validated instrument while the manuscript correctly reports no synthesis, because
those are claims about different things.
