# P013 — proposed replacement wording and decision entry

> **ADOPTED. Authorised by the reviewer on 13 November 2026 and written to the decision register
> as D023; P013 is resolved. The register entry governs. This document is retained unaltered
> below as the record of what was proposed and on what basis.**

**Status at the time of writing: PROPOSAL ONLY.**
P013 was open when this was written. `docs/decisions/decision_log.md` is unmodified. D001–D022 are unchanged. P007 is
untouched and remains open. No search was executed, no record retrieved or exported, no screening or
extraction data changed, and no screening decision created.

**Prepared:** 13 November 2026. **Repository:** `HEAD` `b5afaff`.
**Basis:** `docs/methods/p013_design_block_decision.md` (Phase 2F evaluation).
**Authority:** this document supersedes §6.3 of that memorandum as the authoritative proposed
wording, so that only one version of the proposed text exists.

---

## 1. Why the registered P013 does not cover the question

P013 as registered is a **retrieval-volume** question. Its four options are volume-management
strategies:

| Registered option | What it proposes | Does it remove the design block? |
|---|---|---|
| (a) | Screen all 4,770 records | No — block retained |
| (b) | Add a second title/abstract screener, revisiting D010 | No — block retained |
| (c) | Treat v1r (194) as primary, v2 as supplementary | No — block retained |
| (d) | Restrict the design block to MeSH terms only | **No — narrows the block further** |

**None of (a)–(d) is "remove the design block."** Option (d) moves in the opposite direction.

The removal option was identified later, by the search-strategy audit, and is recorded in
`docs/methods/p007_p013_decision_memorandum.md` as **option (e)**, annotated there as "Not in the
recorded option list; identified by this audit."

Two further problems with answering P013 as written:

1. **Its figures are superseded.** P013 quotes 4,770 records from the **v2 draft** at 2026-10-29.
   That draft contained a site-unrestricted histology term, since removed. The corrected strategy's
   figures are 8,190 and 5,008, measured 2026-11-12, and are not comparable to 4,770.
2. **Its workload figure is an assumption, not an observation.** The "roughly 20 hours" derives from
   15 seconds per record. See §5.

**Therefore P013 cannot be resolved by selecting an option. Its wording must be replaced.** Section 2
proposes the replacement question; section 3 proposes the decision that would answer it.

---

## 2. Exact proposed replacement wording for P013

**Not adopted.** This replaces the P013 row in the open-questions table. It keeps P013 **open** and
restates it as the question actually at issue.

> | P013 | **Study-design block: retain or remove?** The corrected PubMed strategy retrieves
> **8,190** records with no study-design block and **5,008** with the optional block — a difference
> of **3,182 records (38.9%)**, both figures from a counts-only interrogation on 2026-11-12, neither
> a search yield. **Option A — retain:** lower screening volume; an **unmeasured and permanently
> unmeasurable risk to sensitivity** — the removed records are never inspected, so whether any
> eligible study is lost cannot be known, and the number lost may be zero; the block
> admits cross-sectional studies, case series and reviews, all ineligible under the protocol, so it
> reduces volume without sorting designs. **Option B — remove:** retrieves 3,182 more records,
> of which the number of additional *eligible* studies is **unknown**; 3,182 additional records at
> title and abstract for PubMed alone, before any further
> database under P007 or any grey-literature source under D022. The project has **no observed
> screening rate**, so neither option's workload can be expressed in time. Separate from **P007**
> (which databases) and from **D010** (single reviewer), neither of which this question reopens. |
> Determines the review's sensitivity and whether the search can honestly be called systematic. |
> Executing the corrected search |

---

## 3. Proposed decision-register entry

**PRESENTED, NOT WRITTEN.** `docs/decisions/decision_log.md` has not been modified. Writing this
entry requires explicit authorisation, and the identifier is left unassigned — the next free
identifier should be confirmed at the time of writing, since **D021 is not in the register** but is
used in project documents for the drafted blinded-verification acceptance methodology.

> ### D0xx — No study-design block in the primary search (resolves P013)
>
> - **Status:** Proposed *(date of authorisation)*.
> - **Type:** protocol (search strategy)
> - **Decision:** The primary search applies **no study-design block**. Retrieval is defined by the
>   outcome and exposure blocks alone. On the corrected PubMed strategy this is **8,190 records**
>   against **5,008** with the optional block, a difference of **3,182 records (38.9%)** — both
>   figures from a **counts-only interrogation on 2026-11-12**, neither a search yield. The optional
>   design block documented in `docs/methods/recommended_search_strategy.md` is **not appended** to
>   the primary query.
> - **Rationale.** A design block is a filter whose cost is invisible: the records it removes never
>   appear for inspection. **Whether any eligible study is lost is unknown and may be zero**, but
>   any loss that did occur would **not be random**: it would fall on studies that name their
>   design only in the methods section, and on records without MeSH indexing, which are
>   disproportionately the recent and regionally published South Asian studies that the exposure
>   definition (D009) was written to capture. **42 of the 194 records already in hand carry no MeSH
>   headings at all.** The block also fails to perform the function a design filter exists for:
>   built on `Epidemiologic Studies`[Mesh], `Risk Factors`[Mesh], `Odds Ratio`[Mesh] and
>   effect-measure free text, it admits cross-sectional studies, case series and reviews, none of
>   which is eligible under the protocol, which admits case–control and cohort designs only.
>   Its highest-yield free-text term, "cohort", is the principal source of prognostic studies of
>   people who already have the disease: `wrong_outcome` accounts for **63 of the 109** provisional
>   exclusions in the existing corpus, the largest single category.
> - **Uncertainty, recorded as part of the decision.** *Removing the design block increases the
>   number of records retrieved, but the number of additional eligible studies recovered is
>   unknown. The decision prioritises search sensitivity over retrieval volume; it does not
>   establish that the broader strategy has greater empirical sensitivity.* This statement is part
>   of the decision and is reported with it wherever the strategy is described (§4.2).
> - **Consequences.** Title/abstract screening volume increases by **3,182 records** for PubMed
>   alone, before any additional database under P007 or any grey-literature source under D022. Under
>   single-reviewer screening (D010) this is the binding constraint on the review. The increase is
>   stated in **records**; it is not converted to hours, because **no screening rate has been
>   observed** (§5).
> - **Preserving D010.** Screening-order aids and recorded batching are permitted. An automated
>   suggestion **may order records** for presentation so that likely-eligible records are met first;
>   it **may never satisfy a decision field**. Every eligibility decision remains independently
>   human-adjudicated, recorded with `decision_basis = independently_adjudicated` and its own
>   `adjudicated_date`, and the review is **not** described as independently duplicated. This
>   decision does not revise D010; option (b) of the superseded P013 would have, and is not adopted.
> - **Conditions.** Before the formal search is executed, the reviewer **measures** a screening rate
>   on a prespecified sample of 200 records, drawn with the existing seeded procedure, recording
>   start and end times. **No rate is assumed.** If the measured rate shows 8,190 to be infeasible,
>   this decision is revisited **explicitly**, the block reinstated as a recorded change, and the
>   5,008-versus-8,190 comparison cited as its basis. **The query is never narrowed mid-search.**
> - **Scope.** Concerns the design block only. It does **not** resolve **P007** (database coverage,
>   which remains open with no database access verified beyond PubMed), does **not** revise
>   **D010**, and does **not** bear on **D022**.
> - **Supersedes:** the registered P013 wording and its options (a)–(d), together with the 4,770 and
>   7,875 figures from the superseded v2 draft.
> - **Relies on:** D008, D009, D010, D011, D013.

---

## 4. Rationale and uncertainty statement

### 4.1 The recommendation

**Remove the design block (Option B).** The reasoning is in §3 and is not repeated.

### 4.2 The uncertainty, stated precisely

This is the part most easily overstated, so it is set out exactly.

> **Removing the design block increases the number of records retrieved, but the number of
> additional eligible studies recovered is unknown. The decision prioritises search sensitivity
> over retrieval volume; it does not establish that the broader strategy has greater empirical
> sensitivity.**

The distinction this draws is the one on which the whole decision turns, and it is easy to lose.

**What is demonstrated** is a difference in *retrieval volume*: 3,182 more records, measured. That
is an observation about counts.

**What is chosen** is a *principle*: that where the cost of a filter cannot be inspected, the review
prefers to inspect more records rather than fewer. That is a methodological preference.

**What is not established** is *empirical sensitivity*: that the broader strategy actually recovers
eligible studies the narrower one would have missed. No such comparison has been made, and none can
be made from data this project holds. The number of additional eligible studies could be
substantial, and **it could be zero**.

Volume is not sensitivity. A strategy that retrieves 3,182 more records has demonstrated only that
it retrieves 3,182 more records. Whether any of them is eligible is, at this point, unknown.

### 4.3 Why the 3,182 additional records have not been inspected

They have never existed as records in this project. The figures 8,190 and 5,008 come from a
**counts-only interrogation**: the query was submitted and the number of matching records read
back. **Nothing was retrieved, downloaded, exported or screened**, no registry entry exists, and no
title or abstract from that set has been seen. The 3,182 is a difference between two counts, not a
set of records in hand.

Inspecting them would require executing the search and preserving an export — which is precisely
what P013 and P007 must be settled before doing.

### 4.4 The circularity that prevents measurement

The obvious test — apply the design block to records already held and count the losses — **cannot
produce a valid answer here.**

The 194-record corpus was retrieved by the v1 query, which required
`"case-control"[tiab] OR cohort[tiab]`. Both terms are also in the corrected design block.
**Every record in the corpus therefore matches the block by construction.** Running the test gives
194 of 194 and 85 of 85 matching — a result with **no discriminative power whatsoever**.

**This result must never be cited as evidence that the design block is safe.** It is an artefact of
testing a filter against a corpus that the same filter produced. Any corpus this project could test
against has the same defect, because every record it holds passed a design-filtered query.

### 4.5 The 19/194 observation, and what it does not show

One measurement on the existing corpus is informative, within strict limits.

Of the 194 records, **19 (9.8%)** match the corrected design block **only** through a bare design
label — "case–control" or "cohort" — carrying no effect-measure term and no epidemiological MeSH
heading. Among the 85 provisionally carried forward, **2 (2.4%)**.

**What this does show.** The block's broader terms do most of the retrieval work for records of this
kind, but a minority still depend on a literal design word appearing in the title or abstract. For
studies that name their design only in the methods section — common in older and regionally
published papers — that word is absent.

**What this does not show.** It is **not** an estimate of how many eligible studies the block would
lose, and must not be reported as one. It describes records the block **retained**, not records it
would **remove**. The 9.8% figure is a property of a design-filtered corpus and says nothing
directly about the uninspected 3,182. It is offered as a reason for concern, not as a measurement of
harm.

---

## 5. Four classes of evidence, kept distinct

Conflating these is the main way a search strategy comes to be misreported. Every figure in this
proposal belongs to exactly one class.

| Class | What it means | Figures in this proposal |
|---|---|---|
| **1. Observed counts from existing records** | Recomputed from the registered export and the screening worksheets. Real records, in hand, inspectable | 194 identified; 194 unique; 109 provisionally excluded; 85 carried forward; 63 `wrong_outcome`; 68 using "oral cancer"; 98 matching on "cohort" alone; **19 (9.8%)** bare-label only; **2 (2.4%)** of the carried-forward; 42 with no MeSH |
| **2. Counts-only PubMed interrogations** | A query submitted and the result count read back. **No record retrieved, exported or screened; no registry entry.** Describes a database on the day taken | **8,190** and **5,008** (corrected strategy, 2026-11-12); 7,875 and 4,770 (superseded v2 draft, 2026-10-29); 194 and 150 (v1 string, 2026-10-29) |
| **3. Formal database searches** | Executed, exported, counted and checksummed; registered under D011 | **One only: `pubmed_v1r`, 194 records.** `pubmed_v1` (138) is recorded as `export_missing` and contributes no records |
| **4. Unmeasured screening workload** | Quantities the project has **not** observed | Screening rate; time to screen 5,008 or 8,190; completion date — **all unknown** |

**Class 2 figures are never described as yields.** **Class 4 quantities are never given a number.**

### 5.1 The 15-second figure is not used as an observed rate

P013's registered wording implies 15 seconds per record (4,770 × 15 s ≈ 20 hours), and the earlier
joint memorandum carried that forward to "21 hours" and "34 hours".

**That figure is an assumption inherited from P013's own text. This project has never observed it.**
The 194 title/abstract classifications were adopted in bulk from automated suggestions in a single
action; no record was individually screened by a human, so no timing observation exists anywhere in
the repository.

It is therefore **not used in this proposal**, and the proposed decision entry expresses workload in
**records only**. Obtaining a defensible rate requires measuring one — §7, action 4.

---

## 6. Consequences for the formal search strategy

### 6.1 If the proposal is accepted

| Area | Consequence |
|---|---|
| **Search of record** | The corrected PubMed query **without** the optional design block becomes the strategy to execute. `recommended_search_strategy.md` §2 is already written in that form |
| **Retrieval volume** | ~8,190 records from PubMed at execution, subject to database growth. The actual yield is recorded at execution and will differ from the validation count |
| **Screening volume** | +3,182 records at title and abstract, PubMed alone, before P007 databases or D022 grey sources |
| **Reporting** | The review can state that no design filter was applied, which removes the need to report an unquantifiable filter loss. It must **not** be reported as a more sensitive search: the uncertainty statement in §4.2 accompanies the strategy wherever it is described. PRISMA-S requires the full strategy and the date |
| **Other databases** | Each needs its own translation **without** a design block, for consistency. Embase requires an Emtree rewrite; Scopus and Web of Science have no controlled vocabulary |
| **Deduplication** | Cross-database input will produce real duplicates and records lacking PMIDs. The matching rules have been exercised only on a single source with 0 duplicates found and should be reviewed before multi-database input |
| **Manuscript** | §2.3 and Table 3 record the adopted strategy and the 8,190 / 5,008 basis; §2.6 and the limitations section are updated |

### 6.2 If the proposal is rejected in favour of retaining the block

Screening volume falls to ~5,008 for PubMed. The review must then report that a design filter was
applied, that the removed records were never inspected, and that **an unknown number of eligible
studies may have been excluded**, with the loss expected to fall disproportionately on regional and
unindexed literature. This is reportable and defensible, but it becomes a permanent and
unquantifiable limitation on the review's central claim to sensitivity.

This remains a legitimate choice, and §4.2 means it cannot be called the wrong one on evidence: the
benefit forgone is unmeasured.

### 6.3 If P013 is deferred again

The corrected search cannot be executed. The evidence base stays at the 194 records from a query the
project itself describes as narrower than its own protocol, and the manuscript remains a protocol
and interim report.

---

## 7. Actions required before formal search execution

| # | Action | Blocking? | Owner |
|---|---|---|---|
| 1 | **Authorise or reject this proposal.** If authorised, replace the P013 row (§2) and write the decision entry (§3) with a confirmed identifier | **Yes** | Researcher |
| 2 | **Resolve P007** — verify database access and fix the database set. **No access beyond PubMed has been verified**; Scopus and Web of Science are publicly advertised but unconfirmed, and Embase is not listed | **Yes** | Researcher |
| 3 | **Write per-database strategy documents** for every database in the final set, each without a design block. Only PubMed is drafted | **Yes** for non-PubMed | Researcher |
| 4 | **Measure a screening rate** on a prespecified 200-record sample, recording start and end times. This converts the one unknown that determines feasibility, and doubles as the start of the adjudication work that must happen regardless | **Yes** if removal is adopted | Reviewer |
| 5 | **Review the deduplication matching rules** against multi-database input, particularly records without PMIDs | Partial | Researcher |
| 6 | **Confirm export-preservation readiness** — already implemented, tested and exercised on `pubmed_v1r` | No | — |
| 7 | **Record the execution date** for each search at the time it is run, per PRISMA-S and D011 | At execution | Researcher |

Items outside this list — the anatomical and histological scope questions (P014–P022), the
risk-of-bias instrument (P023), and the comparator and contrast questions (P003, P004) — block
**screening, eligibility assessment and extraction**, not the execution of the search itself.

---

## 8. Verification

| Check | Result |
|---|---|
| Full test suite | **615 passed, 1 skipped** |
| Raw export checksum | **OK** |
| Seven screening and processed data files | **All OK** |
| `docs/decisions/decision_log.md` | **Unmodified** — P013 still open, no new decision written |
| D001–D022 | **Unchanged** |
| P007 | **Unchanged and open**; no database access claimed as verified |
| 194-record population | **Unchanged** |
| Screening decisions created | **None** — 0 of 194 still independently adjudicated |

---

## 9. What this document does not do

- It does **not** adopt P013, and does not modify the decision register.
- It does **not** assign a decision identifier; the next free one is confirmed at authorisation.
- It does **not** modify P007, D001–D022, the schemas, the raw data or the screening population.
- It does **not** revise D010.
- It does **not** execute a search, retrieve or export records, or create a screening decision.
- It does **not** assert an observed screening rate, a completion time or a completion date.
- It does **not** claim that removing the design block has a measured sensitivity benefit, or that
  the broader strategy has greater empirical sensitivity. It establishes a difference in retrieval
  volume only.
