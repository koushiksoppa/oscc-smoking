# P013 — Study-design block: decision memorandum

**Status: decision preparation only. P013 is NOT adopted by this document.**
No search was executed, no record retrieved or exported, the 194-record population is unchanged, no
screening decision was created, and D001–D022, P007 and the schemas are untouched.

**Prepared:** 13 November 2026. **Repository:** `HEAD` `b5afaff`.

---

## 1. Baseline, verified from the repository

### 1.1 P013 as currently registered — and an important mismatch

Verbatim from `docs/decisions/decision_log.md`:

> **P013 — v2 retrieval volume.** The drafted v2 query returns **4,770** records against v1r's 194
> (counts validated 2026-10-29). Under single-reviewer screening (D010) that is roughly 20 hours of
> title/abstract work. Options: **(a)** screen all 4,770 — most sensitive, highest workload;
> **(b)** keep v2 as the primary search but add a second human screener for the title/abstract
> pass, revisiting D010; **(c)** treat v1r (194) as the primary set and v2 as a supplementary
> search, screening only v2 records not already in v1r — far less sensitive, and the shortfall must
> be stated as a limitation; **(d)** restrict the v2 design block to MeSH terms only, which drops
> the free-text aetiology terms and so loses unindexed records. **No option is adopted; the query
> is not narrowed for convenience.**

**The registered question is not the question now being asked.** P013 as written is about
**retrieval volume**, and its four options are volume-management strategies. **None of (a)–(d) is
"remove the design block."** Option (d) is the opposite — it narrows the block further.

The option of removing the block entirely was identified later, by the search-strategy audit, and
is recorded in `docs/methods/p007_p013_decision_memorandum.md` as **option (e)**, explicitly
annotated "Not in the recorded option list; identified by this audit."

**Consequence for this decision.** Resolving "retain or remove the design block" cannot be done by
selecting from P013's registered options. It requires **replacing P013's wording**, which is why
section 6 proposes a replacement rather than an answer. The original figures also pre-date the
corrected query and must not be carried forward uncritically.

### 1.2 Status of the surrounding decisions

| Item | Status, as verified |
|---|---|
| **P007** — database coverage | **Open.** Wording approved 12 Nov 2026 but conditional on access verification. PubMed confirmed; Scopus and Web of Science publicly advertised but unverified; Embase not listed, no evidence of access |
| **D001–D015, D020, D022** | **Adopted** (17 decisions) |
| **D016–D019** | **Proposed** — implemented and enforced in code, not adopted as protocol |
| **D021** | **Not in the register** — the label is used in project documents for the drafted blinded-verification acceptance methodology |
| **D022** | **Adopted 13 Nov 2026** — bounded supplementary grey-literature searching |

### 1.3 The three decisions that constrain this one

**D008 (outcome).** Eligible outcome is oral cavity cancer with SCC histologically confirmed or a
stated majority of ≥90%. Estimates pooling the oral cavity with oropharynx, larynx, pharynx or
"head and neck" are **not eligible** unless an oral-cavity-specific estimate is reported separately.

**D009 (exposure).** Any smoked tobacco — cigarettes, **bidis**, cigars, pipes and other combusted
products. Smokeless tobacco and betel quid are **confounders, not exposures**.

**D010 (single reviewer).** Screening and extraction are performed by **one human reviewer**,
reported as a limitation under PRISMA items 8 and 9. Any automated pre-sort is stored in a separate
`suggestion` field that can never satisfy a `decision` field, and the review is never described as
independently duplicated.

**D010 is not reopened here.** Option (b) of the registered P013 — adding a second screener — would
revise D010, and that is a separate decision outside this memorandum's scope.

### 1.4 Eligible designs, from the protocol rather than from assumption

`docs/protocol/eligibility_criteria.md` admits exactly one line of designs:

> "Observational design: case–control or cohort (prospective or retrospective)."

**Table 1.1 — Study designs and their standing in this review.** This matters for P013 because a
design block's value depends on whether it separates eligible from ineligible designs. It largely
does not.

| Design | What it is | Standing here | Caught by a design block? |
|---|---|---|---|
| **Case–control** | Starts from people with and without the outcome; looks backwards at exposure. Yields an **odds ratio** | **ELIGIBLE** | Usually, but often only from the methods section, not the abstract |
| **Cohort** | Starts from exposed and unexposed people; follows forward to the outcome. Yields a **risk ratio** or **hazard ratio** | **ELIGIBLE** (prospective or retrospective) | Usually — but the word also catches ineligible prognostic cohorts |
| **Cross-sectional** | Measures exposure and outcome at one time point; cannot establish temporality | **NOT ELIGIBLE** — yields prevalence, not incidence risk | **Yes — and this is a problem.** `Epidemiologic Studies`[Mesh] explodes over `Cross-Sectional Studies`, so the block *admits* an ineligible design |
| **Case series** | Describes cases with no comparison group | **NOT ELIGIBLE** — no reference group, so no effect estimate (`no_reference_group`) | Inconsistently |
| **Reviews / meta-analyses** | Secondary synthesis | **NOT ELIGIBLE** as primary studies (`review_or_meta`), but their reference lists are checked | Often — reviews discuss risk factors and odds ratios |
| **Randomised trials** | Allocates exposure at random | **NOT APPLICABLE** — smoking cannot ethically be randomised. This is why Cochrane CENTRAL is not searched | Not relevant |

**The key observation.** The eligible/ineligible boundary here is **case–control and cohort versus
everything else**, but the proposed design block is built on `Epidemiologic Studies`[Mesh],
`Risk Factors`[Mesh], `Odds Ratio`[Mesh] and effect-measure free text. That block admits
cross-sectional studies, case series discussing risk factors, and reviews. **It is therefore not a
precision instrument with respect to this review's eligibility criteria.** It reduces volume; it
does not meaningfully sort eligible from ineligible designs.

### 1.5 Current screening population

194 records identified; 194 unique reports after deduplication (0 duplicates); 194 provisional
classifications, all `adopted_from_suggestion`; **0 independently adjudicated**; 109 provisionally
excluded, 85 carried forward; 0 full texts retrieved; 0 studies included.

---

## 2. Evidence from the existing searches

**Dates and query versions are kept strictly separate. These counts are not comparable across
rows.** Each was produced by a different query on a different date, and all of the multi-thousand
figures are **counts-only interrogations for strategy validation — not search yields**: nothing was
retrieved, exported or screened, and no registry entry exists for any of them.

**Table 2.1 — Recorded counts, by query version and date.**

| Query version | Design block | Count | Date | Nature |
|---|---|---|---|---|
| v1 as documented | `"case-control"[tiab] OR cohort[tiab]` | 138 | unknown | Documented claim; **export lost** |
| v1 string, Humans + English | same | 150 | 29 Oct 2026 | Counts-only |
| **v1r — the registered export** | same | **194** | on/after 25 Oct 2026 | **Executed, exported, checksummed** |
| v2 draft | broad block | 4,770 | 29 Oct 2026 | Counts-only |
| v2 draft | none | 7,875 | 29 Oct 2026 | Counts-only |
| **Corrected strategy** | optional block | **5,008** | **12 Nov 2026** | Counts-only |
| **Corrected strategy** | none | **8,190** | **12 Nov 2026** | Counts-only |

**The only legitimate within-version comparison is the last two rows**: for the *corrected* query on
12 November, the design block removes **3,182 records, or 38.9%** of the outcome-and-exposure set.
The 4,770 / 7,875 pair measures the same effect for the superseded v2 draft (39.4%) and must not be
mixed with it — the v2 draft contained a site-unrestricted histology term that has since been
removed.

### 2.1 What the 194-record corpus can and cannot tell us

Two properties of the existing export bear directly on P013.

**68 of 194 records use the phrase "oral cancer"** — the dominant phrasing in aetiological
epidemiology — which the v1 query does not require. They were retrieved only because they happened
to contain "Oral Squamous Cell Carcinoma" or "OSCC" as well. This is an *outcome*-block defect, not
a design-block one, and it is already fixed in the corrected strategy.

**98 of 194 matched the design block only through the single word "cohort"**, verified by
recomputation. The eligibility documentation records the consequence directly: `wrong_outcome`
"includes prognostic studies of survival or recurrence among people who already have OSCC, which
search v1 retrieves in quantity because of the term 'cohort'". **63 of the 109 provisional
exclusions are `wrong_outcome`** — the largest single category.

That is an argument *against* the design block on its own terms: the block's highest-yield term is
also the principal source of the corpus's largest category of ineligible records. It is not buying
precision; it is buying prognostic cohorts.

### 2.2 A test that cannot be run, and why that matters

The obvious question is: *how many eligible studies would a design block lose?* I tested the
corrected design block against all 194 exported records and against the 85 carried forward. **All
194 matched, and all 85 matched.**

**That result is worthless as evidence, and must not be cited as showing the block is safe.** The
corpus was itself produced by a query requiring `"case-control" OR cohort`, and both terms are in
the corrected block. Every record matches by construction. The test has **no discriminative power**.

**This is itself the finding: the loss a design block would cause cannot be estimated from any data
this project holds, because every record it holds already passed a design filter.** The 3,182
records the block removes from the corrected query have never been inspected and cannot be
characterised. A filter's cost is invisible precisely because the records it removes never appear.

One measurement is still informative. Of the 194, **19 (9.8%)** match the corrected block *only*
through a bare design label — "case–control" or "cohort" — with no effect-measure term and no
epidemiological MeSH heading. Among the 85 carried forward, **2 (2.4%)**. So the block's broader
terms do most of the work for records already in hand, but roughly one in ten still hangs on a
literal design word appearing in the title or abstract. For studies that name their design only in
the methods section — common in older and regionally published papers — that word is absent, and
the block would drop them without trace.

---

## 3. Option A versus Option B

**Table 3.1 — The two options compared.**

| Dimension | **A — retain the design block** | **B — remove it** |
|---|---|---|
| Records (corrected query, 12 Nov 2026) | 5,008 | 8,190 |
| Sensitivity | **Not established.** The removed records are never inspected, so whether any eligible study is lost cannot be known, and the number lost may be zero | **Not established.** Retrieval volume is higher by 3,182 records; the number of additional *eligible* studies recovered is unknown and may be zero |
| Precision | Marginally better; but the block admits cross-sectional studies, case series and reviews, so it does not sort eligible from ineligible designs | Lower; more ineligible records reach screening |
| Risk of missing eligible studies | **Unmeasurable, and may be zero.** ~1 in 10 records in hand hang on a bare design label, and studies naming their design only in the methods would be invisible to it — but whether the removed set contains any eligible study is unknown | Minimal from this cause |
| Effect on South Asian bidi and reverse-smoking studies | **Disproportionate.** Regionally published and older papers are least likely to carry a design label in the abstract or to be MeSH-indexed — 42 of 194 records here carry no MeSH at all | Neutral |
| Terminology and indexing variation | Block depends on indexing that is absent for the newest records and inconsistent for regional journals | Not affected |
| Screening workload | 3,182 fewer records to title/abstract screen | 3,182 more |
| Methodological standing | Design filters for observational reviews are discouraged as unreliable | Preferred |
| Practical risk | A search that is complete, but carries a gap of unknown size — possibly zero — that can never be established | **A search that is begun and not finished** |

**The honest statement of the trade.** Exactly one quantity on either side is measured: the
retrieval-volume difference of **3,182 records**. Option A buys that known reduction in workload
at the cost of an **unmeasured risk** to sensitivity; Option B accepts that known increase in
workload for an **unmeasured possible gain**. Neither the loss under A nor the gain under B is
established, and neither can be measured from the data this project holds: the number of eligible
studies at stake is unknown and **may be zero**. What *can* be said is where each cost would fall.
If the risk under A is real, it falls non-randomly — on exactly the regional and unindexed
literature that D009's exposure definition was written to capture — whereas the cost of B is
certain, falls on reviewer time, and is visible and manageable.

---

## 4. Recommendation

### Recommended: **Option B — remove the study-design block from the primary search.**

Five reasons, in order of weight:

1. **Any losses from retaining it would be non-random, and would fall where this review is most distinctive.**
   D009 admits bidi, chutta and reverse smoking; that literature is concentrated in South Asian
   journals, which are less consistently indexed. 42 of the 194 records in hand carry no MeSH
   headings at all, and those are the most recent. A block depending partly on MeSH explosion and
   partly on a literal design label is weakest exactly there. A systematic loss can bias a pooled
   estimate; a random one only widens it.
2. **The block does not do the job a design filter is supposed to do.** Built on
   `Epidemiologic Studies`[Mesh] and effect-measure terms, it admits cross-sectional studies, case
   series and reviews — all ineligible here. It reduces volume without sorting designs.
3. **Its highest-yield term actively harms precision.** "Cohort" is what pulls in prognostic
   studies of people who already have the disease, and `wrong_outcome` — 63 of 109 provisional
   exclusions — is the largest exclusion category in the corpus as a direct result.
4. **The cost of retaining it is unmeasurable, and will remain so.** The 3,182 removed records
   cannot be characterised from anything this project holds, and a filter whose cost cannot be
   stated cannot be reported honestly as a limitation beyond "an unknown number of eligible studies
   may have been excluded."
5. **It matches the stated research priority** — sensitivity, and avoiding the exclusion of eligible
   observational evidence even at the cost of screening workload.

### The case against this recommendation, stated fairly

Removal is **not** automatically correct, and two objections deserve a direct answer rather than
dismissal.

**The workload objection is serious.** 8,190 records at title and abstract, under a single
reviewer, is the binding constraint on the entire review. An unfinished search is worse than a
narrower one honestly reported: a review abandoned at 60% of its screening yields nothing, while a
completed design-filtered review yields a usable synthesis with a declared limitation. **If there
is genuine doubt that 8,190 can be screened to completion, Option A is the more defensible choice**,
and choosing it would be sound judgement rather than a concession — provided the restriction is
reported with the 5,008-versus-8,190 comparison as its measured basis.

**The second objection is that this is PubMed alone.** P007 is unresolved. If Scopus or Embase
access is confirmed, each adds an unknown further volume to the same single reviewer. Deciding P013
in isolation risks committing to 8,190 before knowing the total. **This argues for sequencing, not
for retaining the block**: see section 5.

---

## 5. Operational consequences

### 5.1 Workload — what is known and what is not

**The project has never measured its own screening rate, and no rate is invented here.** The 194
title/abstract classifications were adopted in bulk from automated suggestions in a single action;
no record was individually screened by a human, so no timing observation exists.

The "roughly 20 hours" figure in P013's registered wording, and the "21 hours / 34 hours" figures in
the earlier joint memorandum, both derive from an assumption of **15 seconds per record** — a figure
carried forward from P013's own text, **not an observation from this project**. It is reproduced
here only so that it is traceable, and it should not be treated as evidence.

**Table 5.1 — Workload in records, which is the only quantity actually known.**

| Option | Records to title/abstract screen (PubMed only) | Difference |
|---|---|---|
| A — with the design block | 5,008 | — |
| B — without | 8,190 | **+3,182 (+63.5%)** |

Any conversion to hours requires a screening rate, and the honest way to obtain one is to **measure
it**: see the recommendation below. Additional databases under P007 would add further unknown
volume, as would the grey-literature sources under D022.

### 5.2 Is Option B feasible under D010?

**Not demonstrably, and that is the correct answer at this point.** Feasibility cannot be assessed
without a screening rate, and no rate exists. What can be said:

- 8,190 is a **multi-day to multi-week** title/abstract task for one person at any plausible rate,
  before full-text retrieval, extraction and appraisal.
- It is not obviously impossible, and it is not obviously achievable.
- Committing to it blind is the main risk of adopting Option B.

### 5.3 Managing the workload without misrepresenting reviewer independence

These preserve D010 exactly as adopted. **None of them permits an automated suggestion to satisfy a
decision field, and none allows the review to be described as independently duplicated.**

1. **Measure the rate before committing.** Screen a prespecified random sample — 200 records, drawn
   with the existing seeded procedure — recording the start and end time. This converts the central
   unknown into an observation, costs a few hours, and produces a defensible projection. **This is
   the single most useful next action**, and it doubles as the beginning of the adjudication work
   that must happen anyway.
2. **Screen on title first, abstract only where the title does not decide.** A documented two-pass
   order within a single reviewer's work. It is a workflow choice, not a second reviewer.
3. **Use the automated suggestion set as a presentation order, never as a decision.** Records may be
   *ordered* by suggested relevance so that the reviewer meets likely-eligible records first. The
   decision field remains the reviewer's, the basis is recorded as `independently_adjudicated`, and
   the ordering is reported in the methods. This is explicitly permitted by D010's wording and
   changes nothing about what the data records.
4. **Screen in recorded batches with dates.** Progress becomes visible, and an interrupted search is
   recoverable rather than ambiguous.
5. **Sequence P013 execution after the P007 access answer** so that the total volume is known before
   the reviewer commits to any of it.
6. **If, after measurement, 8,190 is genuinely infeasible** — return to this decision and adopt
   Option A deliberately, reporting the restriction with its measured basis. **Do not silently
   narrow the query mid-search.**

What is **not** acceptable: describing the automated suggestions as a first-pass screen, counting
adopted suggestions towards the formal PRISMA flow, or presenting a suggestion-ordered workflow as
two-reviewer screening.

---

## 6. Proposed P013 wording

### 6.1 Current wording

As reproduced in §1.1 — a volume question with four options, none of which is "remove the block",
and whose figures pre-date the corrected query.

### 6.2 Recommended decision

**Remove the study-design block from the primary search** (Option B / the audit's option (e)),
subject to the sequencing in §5.3.

### 6.3 Exact proposed replacement wording

> **HISTORICAL RECORD — SUPERSEDED. NOT THE OPERATIVE DECISION RATIONALE.**
>
> The authoritative replacement P013 wording and the proposed decision-register entry live in
> **`docs/methods/p013_decision_proposal.md`** (13 November 2026), which separates the replacement
> *question* from the proposed *decision* and states the uncertainty explicitly.
>
> The draft below is retained **unaltered**, as the record of what was first proposed. It therefore
> still contains wording corrected on 13 November 2026 — in particular it asserts that losses
> follow from retaining the design block, which **is not established**: whether the removed set
> contains any eligible study is unknown and may be zero. **Nothing below may be quoted into the
> decision register, used as the rationale for adoption, or cited as the project's position.** If
> the two documents differ, the proposal memorandum governs.

**Not adopted. Offered for the researcher to accept, amend or reject.** If accepted, this closes
P013 and is recorded as a new decision.

> **D0xx — No study-design block in the primary search (resolves P013).**
>
> **Decision.** The primary search applies **no study-design block**. Retrieval is defined by the
> outcome and exposure blocks alone. On the corrected PubMed strategy this is **8,190 records at the
> counts-only validation of 12 November 2026**, against **5,008** with the optional block — a
> difference of 3,182 records, or 38.9%.
>
> **Rationale.** A design block is a filter whose cost is invisible: the records it removes never
> appear for inspection, and this project can never estimate that cost, because every record it
> holds was itself retrieved by a design-filtered query. The losses are not random — they fall on
> studies that name their design only in the methods section and on records without MeSH indexing,
> which are disproportionately the recent and regionally published South Asian studies that the
> exposure definition (D009) was written to capture. The block also fails to perform the function a
> design filter is for: built on `Epidemiologic Studies`[Mesh] and effect-measure terms, it admits
> cross-sectional studies, case series and reviews, all ineligible under the protocol. Its
> highest-yield term, "cohort", is the principal source of prognostic studies of people who already
> have the disease — the largest category of ineligible records in the existing corpus.
>
> **Consequences.** Title/abstract screening volume increases by 3,182 records for PubMed alone,
> before any additional database under P007 or any grey-literature source under D022. Under
> single-reviewer screening (D010) this is the binding constraint on the review. Screening-order
> aids and batching are permitted; an automated suggestion may order records but may never satisfy
> a decision field, and the review is not described as independently duplicated.
>
> **Conditions.** Before the formal search is executed, the reviewer measures an observed screening
> rate on a prespecified sample of 200 records and records it. **No screening rate is assumed.** If
> the measured rate shows the volume to be infeasible, this decision is revisited explicitly and the
> design block reinstated as a recorded change with the 5,008-versus-8,190 comparison as its basis.
> The query is never narrowed mid-search.
>
> **Scope.** This decision concerns the design block only. It does not resolve **P007** (database
> coverage), does not revise **D010** (single reviewer), and does not bear on the grey-literature
> provisions of **D022**.

### 6.4 Consequences of accepting

- The search of record is fixed, and the corrected strategy can be executed once P007 returns.
- The review avoids making an unsupported empirical claim about filter-related sensitivity loss:
  with no design filter applied there is no uninspected removed set, and so nothing to caveat.
  **This is not a claim that the search is more sensitive.**
- Screening workload rises by 63.5% for PubMed alone; the review's completion risk rises with it.
- `docs/methods/recommended_search_strategy.md` becomes the operative strategy with its optional
  block omitted; the manuscript's Table 3 and §2.3 gain the adopted position and the measured basis.

### 6.5 Consequences of rejecting

- **If Option A is adopted instead:** workload falls to 5,008 for PubMed; the review must report
  that a design filter was applied, that the removed records were never inspected, and that an
  unknown number of eligible studies may have been excluded — with the loss concentrated in the
  regional literature. This is reportable and defensible, but it is a permanent and unquantifiable
  limitation on the review's central claim to sensitivity.
- **If P013 is deferred again:** the corrected search cannot be executed, the evidence base remains
  the 194 records from a query the project itself describes as narrower than its own protocol, and
  the manuscript remains an interim report.

### 6.6 Required protocol and manuscript changes if accepted

| File | Change | Authorisation |
|---|---|---|
| `docs/decisions/decision_log.md` | Add the decision; mark P013 resolved | **Separate authorisation required** |
| `docs/methods/recommended_search_strategy.md` | Mark the no-design-block query as the adopted strategy | Separate |
| `docs/search/search_v2_pubmed.md` | Supersede the v2 draft explicitly | Separate |
| `docs/reports/manuscript_final.md` §2.3, Table 3 | Record the adopted strategy and the measured basis | Separate |
| `AGENTS.md` | Remove P013 from the open list | Separate |

None of these is made here.

---

## 7. Search-readiness assessment

**Table 7.1 — Blockers to executing the formal search.**

| # | Item | State | Blocking? |
|---|---|---|---|
| 1 | **Database access (P007)** | Open. PubMed confirmed; Scopus/WoS advertised but unverified; Embase no evidence of access | **YES** |
| 2 | **P013 — design block** | Open. This memorandum recommends; nothing is adopted | **YES** |
| 3 | **Grey-literature decision** | **D022 adopted 13 Nov 2026** | No |
| 4 | **Search syntax validation** | Corrected PubMed query syntax-validated 12 Nov 2026, counts-only | No, for PubMed |
| 5 | **Database-specific translations** | **Not written.** Embase needs an Emtree rewrite; Scopus/WoS have no controlled vocabulary and need synonym enumeration | **YES**, for any database beyond PubMed |
| 6 | **Search dates** | Not set; cannot be set before the strategy is fixed. The v1 execution date remains unrecoverable (P009) | No — set at execution |
| 7 | **Search documentation** | Per-database strategy documents required by D011; only PubMed drafted | **YES**, for non-PubMed |
| 8 | **Export preservation** | **Ready.** Checksum registration implemented, tested and exercised on `pubmed_v1r` | No |
| 9 | **Deduplication readiness** | Implemented and tested, but **exercised only on a single source with 0 duplicates found**. Cross-database input will produce real duplicates and records lacking PMIDs | **PARTIAL** — review the matching rules before multi-database input |
| 10 | **Screening-rate measurement** | Never measured; no observation exists | **YES**, if Option B is adopted |

### Verdict

> ## NOT READY
>
> Two decisions and two preparation tasks stand between the project and a defensible formal search:
> **P007** (which databases, and whether access exists), **P013** (this memorandum), the
> **database-specific query translations** for anything beyond PubMed, and a **measured screening
> rate** if the larger result set is adopted.
>
> **PubMed alone could be executed as soon as P013 is adopted** — its query is written and
> syntax-validated, and the export-preservation machinery is tested and proven. But executing
> PubMed before P007 is answered would mean registering a search execution and then, very likely,
> executing a second one later, which is additional screening work rather than less.
>
> **Recommended order:** resolve P013 → verify database access and close P007 → write the
> per-database strategies → measure the screening rate on a 200-record sample → execute and register
> each search in turn.

---

## 8. What this document does not do

- It does **not** adopt P013, and does not modify `docs/decisions/decision_log.md`.
- It does **not** modify P007, D001–D022, the schemas, the raw data or the 194-record population.
- It does **not** reopen D010; option (b) of the registered P013 would, and is out of scope.
- No search was executed; no record was retrieved or exported; no screening decision was created.
- No screening rate is asserted as observed, and no completion date is estimated.
