# Decision memorandum — P007 (database coverage) and P013 (retrieval volume)

**Status: recommendations for the reviewer. Neither question is adopted here, and the decision
register is unchanged.** Proposed wording is supplied so that, if a recommendation is accepted, it
can be entered as a decision with a date and a rationale. Until it is entered, nothing in this
memorandum has protocol force.

The two questions are presented together because they cannot sensibly be answered apart: the
database set determines the volume, and the volume determines whether the database set is screenable.

---

## Part 1 — P007: additional databases and supplementary methods

### 1.1 The question as recorded

> Additional databases (Embase, Scopus/Web of Science) and supplementary methods (reference lists,
> citation searching); constrained by institutional access.
> *Consequence:* search sensitivity; PRISMA/MOOSE expectations. *Needed by:* search v2.

### 1.2 Current position

One database searched: PubMed, one execution, 194 records, registered with a checksum. No other
database searched. No reference-list or citation checking performed. Institutional access to
subscription databases **not confirmed**.

### 1.3 Options

| Option | Content | Sensitivity | Screening load | Can the review be called systematic? |
|---|---|---|---|---|
| **A** | PubMed only | Lowest | Lowest | **No.** Must be reported as a non-systematic or single-database search |
| **B** | PubMed + Embase + reference-list checking | Defensible minimum | Moderate | Yes, with the omission of a citation index declared |
| **C** | **B + Scopus or Web of Science, with forward-citation checking + IndMED** | High | High | Yes |
| **D** | C + LILACS + grey literature | Highest | Highest | Yes, with the most complete claim |

### 1.4 Scientific implications

Embase is the consequential addition. It indexes several thousand journals absent from MEDLINE, with
stronger European, Asian and Latin American coverage, and it indexes conference abstracts. For this
question that coverage is not incidental: the adopted exposure definition explicitly admits bidis
and reverse smoking on the recorded grounds that a cigarette-only review would exclude much of the
most informative literature, particularly South Asian studies. A large part of that literature sits
in journals with incomplete MEDLINE coverage. **Omitting Embase therefore risks a shortfall
concentrated precisely in the exposure subgroup the protocol went out of its way to include.**

A citation index adds a retrieval mechanism that term-based searching cannot replicate: forward
citation chasing finds studies whose terminology no query anticipated. Reference-list checking of
included studies and of existing reviews is the cheapest high-yield method available and has not
been done.

IndMED addresses the regional gap directly. Its interface is weaker and its exports may lack
persistent identifiers, which complicates deduplication, but the gap it addresses is real.

Cochrane CENTRAL is a register of controlled trials. This review admits only case–control and cohort
studies of an unrandomisable exposure, so CENTRAL's core content is ineligible by design. Searching
it would add screening work for negligible expected yield.

### 1.5 Risk of bias or missed evidence

- **Option A** carries a material risk of selection bias of unknown direction. Single-database
  reviews systematically under-retrieve, and here the shortfall is likely to fall disproportionately
  on non-cigarette combusted products and on regional literature — the subgroups the review most
  wants to characterise.
- **Option B** reduces that risk substantially; the residual risk is studies reachable only by
  citation chasing.
- **Options C and D** reduce it further with diminishing returns; Scopus and Web of Science overlap
  heavily, so searching both is poor value.

### 1.6 Resource implications

| Option | Databases to write and execute | Access needed | Screening burden |
|---|---|---|---|
| A | 1 | none | lowest |
| B | 2 + reference lists | Embase | moderate |
| C | 3–4 + citation checking | Embase, and Scopus or WoS | high |
| D | 5+ | as C, plus grey-literature sources | highest |

Each database needs its own strategy document with platform-specific syntax, its own execution
record, and its own registry entry. A PubMed query cannot be pasted into Embase.

### 1.7 Recommendation

**Option C**, reduced to **Option B** if access to a citation index cannot be obtained.

**Rationale.** Option B is the floor below which the search cannot honestly be called systematic,
and Embase is non-negotiable for an exposure definition built around bidis and reverse smoking.
Option C adds the two mechanisms that term-based searching cannot supply — forward citation chasing
and regional coverage — at a cost that is real but proportionate. Option D's marginal yield does not
justify its cost under single-reviewer screening. Option A should be chosen only if access makes
anything else impossible, and then the review must be reported as a single-database search with the
limitation stated prominently rather than in passing.

Searching both Scopus and Web of Science is **not** recommended; choose whichever is accessible and
record which and why.

### 1.8 Proposed decision wording — **not adopted**

> ### D0xx — Database coverage (resolves P007)
> - **Status:** *(to be completed on adoption)*
> - **Type:** protocol (search)
> - **Decision:** The search comprises **PubMed/MEDLINE**, **Embase**, and **one citation index
>   (Scopus or Web of Science, whichever is institutionally accessible)**, supplemented by
>   **reference-list checking of every included study and of existing reviews on the question** and
>   **forward-citation checking of every included study**. **IndMED** is searched to address the
>   regional South Asian literature that the exposure definition makes material. **Cochrane
>   CENTRAL is not searched**, on the grounds that it registers controlled trials while this review
>   admits only observational designs of an unrandomisable exposure; this omission is reported with
>   that reason. LILACS and grey literature are not searched; this is reported as a limitation.
>   Each database receives its own strategy document with platform-specific syntax, its own
>   execution date and count, and its own registry entry with the export's checksum. No database
>   may be dropped to reduce workload without the omission being reported as a limitation.
> - **Rationale:** *(to be completed by the reviewer)*
> - **Conditional on:** confirmed institutional access. If a named database proves inaccessible,
>   that is recorded as an amendment with its date, and the review reports the reduced coverage.

---

## Part 2 — P013: retrieval volume

### 2.1 The question as recorded

> **v2 retrieval volume.** The drafted v2 query returns **4,770** records against v1r's 194 (counts
> validated 2026-10-29). Under single-reviewer screening (D010) that is roughly 20 hours of
> title/abstract work. Options: **(a)** screen all 4,770 — most sensitive, highest workload;
> **(b)** keep v2 as the primary search but add a second human screener for the title/abstract pass,
> revisiting D010; **(c)** treat v1r (194) as the primary set and v2 as a supplementary search,
> screening only v2 records not already in v1r — far less sensitive, and the shortfall must be
> stated as a limitation; **(d)** restrict the v2 design block to MeSH terms only, which drops the
> free-text aetiology terms and so loses unindexed records. **No option is adopted; the query is not
> narrowed for convenience.**

### 2.2 Two corrections to the premises

**First, the figures must be characterised precisely, and the recorded ones are now superseded.**
4,770 comes from a read-only syntax-validation run on 2026-10-29 of the **v2** query, performed by
automated tooling under the reviewer's direction and **not** a researcher-executed search. The
recommended query has since been corrected — a site-unrestricted histology term was removed from
its outcome block — and re-validated on **2026-11-12** by the same read-only method:

| Query | Without design block | With design block | Date |
|---|---|---|---|
| v2 draft | 7,875 | 4,770 | 2026-10-29 |
| **Recommended, corrected** | **8,190** | **5,008** | **2026-11-12** |

**P013 must be decided against the 2026-11-12 figures, not the 2026-10-29 ones**, because the
earlier pair describes a different and narrower term set. Both pairs are syntax-validation counts,
**not search yields**: nothing was exported and no registry entry exists. It is a documented measurement,
not an estimate — but it is **not a search yield**, because nothing was exported and the database
will have grown since. The same run measured **7,875** for the outcome-and-exposure blocks without a
design block.

**Second, the option set is now incomplete.** The audit identifies a further option the recorded
list does not contain: **removing the design block** rather than tightening it. The design block
removes roughly 39% of the outcome-and-exposure set while requiring no design label, and there is no
evidence that what it removes is ineligible. Design filters for observational reviews are discouraged
precisely because they are unreliable. This is option **(e)** below, and it is a sensitivity
*increase*, not a reduction.

### 2.3 Options

| Option | Content | PubMed volume | Sensitivity | Notes |
|---|---|---|---|---|
| **(a)** | Screen all of v2 | 5,008 at 2026-11-12 | Good | ~20 h title/abstract, single reviewer |
| **(b)** | v2 primary, add a second title/abstract screener | ~4,770 | Good | **Would revisit the single-reviewer decision** — a protocol change, and an improvement in its own right |
| **(c)** | v1r primary, v2 supplementary | 194 + unscreened remainder | **Low** | Rejected below |
| **(d)** | Restrict the design block to MeSH only | unmeasured | **Reduced** | Drops unindexed records — the 21.6% of the existing export with no MeSH |
| **(e)** | **Remove the design block** | **8,190 at 2026-11-12** | **Highest** | Not in the recorded option list; identified by this audit |

Volumes above are PubMed alone. Adding Embase and a citation index will increase the total by an
amount that **cannot be stated before execution**.

### 2.4 Scientific implications

**Option (c) is not a volume decision; it is a decision to keep a search that does not match the
protocol.** The v1r set was produced by a query requiring the literal phrase "oral squamous cell
carcinoma" or "OSCC". 68 of its 194 records say "oral cancer" and were retrieved only because they
*also* said OSCC. Treating that set as primary means the primary evidence base selects on phrasing
rather than on topic. The "supplementary" screening of v2-only records does not repair this: it
reclassifies most of the eligible literature as a secondary addendum. **Recommend against.**

**Option (d) removes exactly the records the strategy design was built to reach.** Pairing
controlled vocabulary with free text exists because 42 of 194 records (21.6%) carry no MeSH at all —
and those are the most recent, hence plausibly among the most relevant. MeSH-only restriction
discards them silently. **Recommend against.**

**Option (b) is the only option that improves the review's methodology rather than trading it.**
Single-reviewer screening is recorded as a resource constraint, declared openly, and is reported as
a limitation. A second title/abstract screener would remove that limitation, and it would also
resolve a separate problem: all 194 existing classifications were adopted from an automated
suggestion set and none has been independently adjudicated. A second screener changes the review's
standing more than any search decision can.

**Options (a) and (e) differ only in whether an unvalidated design filter is retained.**

### 2.5 Risk of bias or missed evidence

| Option | Principal risk |
|---|---|
| (a) | Residual loss from the design block, unquantified |
| (b) | None added; reduces existing risk |
| (c) | **Substantial.** Primary evidence base selects on phrasing; shortfall concentrated in studies saying "oral cancer" |
| (d) | **Substantial.** Silently discards unindexed records, which are the most recent |
| (e) | None added; highest sensitivity. Risk is practical, not methodological: a volume the reviewer cannot screen |

### 2.6 Resource implications

At a sustained 15 seconds per record for title/abstract screening — the figure already recorded —
PubMed alone implies roughly **21 hours** for option (a) at 5,008 records and roughly **34 hours** for option (e) at 8,190.
Those figures exclude Embase, any citation index, full-text retrieval and assessment. With Tier-1
or Tier-2 database coverage, title/abstract screening alone plausibly becomes a multi-week task for
one person. **This is the binding constraint on the whole review**, and it is the reason P013 should
be answered together with P007 rather than after it.

### 2.7 Recommendation

**Three separate questions, three separate decisions. They are deliberately not bundled.**

#### A. Should the study-design search block be removed? — *this is P013*

**Recommended: yes, remove it.** A search-method decision, and the only one of the three that P013
itself poses. Measured on 2026-11-12, the block removes approximately 39% of the
outcome-and-exposure set (8,190 → 5,008) while requiring no design label, and no evidence
establishes that the removed records are ineligible. If the resulting volume is not screenable,
the fallback is **option (a)** — retain the block and report the restriction as a limitation,
citing the 5,008-versus-8,190 comparison as the measured basis.

**A can be decided on its own**, today, without touching any other decision.

#### B. Should a second title/abstract screener be added? — *a resourcing decision, not P013*

**Recommended: yes, if resources permit** — but as a **separate decision with its own entry**, not
as part of P013. It is a resourcing question about capacity, not a question about search method. It
would also address a problem P013 does not touch: all 194 existing title/abstract classifications
were adopted from an automated suggestion set and none has been independently adjudicated.

**B is not required for A.** If B is refused, A still stands or falls on its own merits.

#### C. Should the one-human-reviewer methodology be amended? — *a protocol decision on D010*

**No recommendation offered here.** D010 records single-reviewer screening and extraction as a
resource constraint, declared openly and reported as a limitation. Amending it is a protocol change
that belongs in its own decision entry with its own rationale, and it is **not** within the scope of
a search-strategy memorandum.

Note that **B and C are not the same question**. Adding a second screener for the title/abstract
pass only is narrower than revising single-reviewer methodology across screening, extraction and
appraisal. B could be adopted as a bounded amendment; C is the general case. Which is intended must
be stated explicitly in whichever decision is written.

**Rationale.** The design block is a filter whose cost is invisible, and the strongest available
reason to retain it is workload. Workload is a real constraint, but it is better met by adding
screening capacity than by narrowing the search, because the first is declarable and the second is
not measurable. Options (c) and (d) both trade sensitivity for comfort in ways the protocol's own
retrieval decision already rejected in a closely analogous case: filters were removed from the
re-executed search precisely so that exclusions would be auditable at screening rather than
invisible at retrieval. The same logic applies to a design filter.

**A note on scope.** Option (b) revisits the single-reviewer decision. That is a protocol change in
its own right and should be recorded as its own decision, not folded into a search decision.

### 2.8 Proposed decision wording — **not adopted**

> ### D0xx — Retrieval volume and the design block (resolves P013)
> - **Status:** *(to be completed on adoption)*
> - **Type:** protocol (search)
> - **Decision:** The search of record applies **no study-design block**. Measured at the
>   2026-11-12 syntax validation of the corrected query, the design block removed
>   approximately 39% of the outcome-and-exposure set (8,190 → 5,008) while requiring no design
>   label, and no evidence
>   establishes that the removed records were ineligible. Design filters for observational reviews
>   are not used. **The retrieved volume is screened in full at title and abstract.** The v1r
>   194-record set is **not** treated as the primary evidence base: it was produced by a query
>   requiring a literal phrase that 68 of its own 194 records do not primarily use, so it selects
>   on phrasing rather than topic. Restricting any block to controlled vocabulary alone is
>   **rejected**, because 21.6% of the v1r export carries no index terms at all.
> - **Rationale:** *(to be completed by the reviewer)*
> - **Dependency:** if the volume proves unscreenable by one reviewer, the response is to add
>   screening capacity, recorded as its own decision, **not** to narrow the search. Any narrowing
>   that is nonetheless adopted must be recorded with the measured sensitivity cost and reported as
>   a limitation.

---

## Part 3 — Decision sequence

| Order | Decision | Why first |
|---|---|---|
| 1 | **P007** — database set | Determines how many strategies are needed and the total volume |
| 2 | **P013** — design block and volume | Depends on the P007 total |
| 3 | Second screener? *(separate decision)* | Determines whether the P013 volume is screenable, and would revisit single-reviewer screening |
| 4 | Known-item seed set and retrieval test | Must precede execution; requires reviewer-supplied studies |
| 5 | PRESS or equivalent peer review | Must precede execution |
| 6 | Execute and export, per database | Each with its own date, count, filters and checksum |

**Nothing in this memorandum is adopted.** The register is unchanged: P007 and P013 remain pending,
no decision identifier has been assigned, and the proposed wording above is a draft for the
reviewer's approval or revision.
