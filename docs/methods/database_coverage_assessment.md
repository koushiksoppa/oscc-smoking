# Database coverage assessment

**Status: assessment and recommendation only. No database other than PubMed has been searched.**
No claim is made here that any database was accessed, and no yield is estimated for any database
that has not been executed. Institutional access to the subscription databases below **has not been
confirmed** and is a precondition the reviewer must establish.

## 1. Current position

| Database | Searched? | Evidence |
|---|---|---|
| PubMed | **Yes** — one execution registered (194 records, unfiltered) | `config/sources.yaml`, registered export with checksum |
| Embase | **No** | no registry entry, no export |
| Scopus | **No** | — |
| Web of Science | **No** | — |
| Cochrane CENTRAL | **No** | — |
| Regional databases | **No** | — |
| Reference-list checking | **No** | — |
| Forward-citation checking | **No** | — |
| Trial registries | **No** | — |
| Grey literature | **No** | — |

**One database does not constitute a systematic search.** Reporting guidance for reviews of
observational studies expects multiple bibliographic sources plus reference-list and citation
checking. The review cannot presently be described as having a systematic search.

## 2. Assessment by database

### 2.1 PubMed / MEDLINE — **ESSENTIAL** (already searched)

**Relevance.** The principal biomedical index; near-complete coverage of the oral oncology and
cancer-epidemiology journals in which the eligible literature appears. Free, stable, and
reproducible by anyone.

**Additional literature it captures.** Already captured, in part. A re-executed and broadened
strategy will capture substantially more than the existing 194 records.

**Limitations.** Indexing lag — **42 of the 194 records in the existing export (21.6%) carry no
MeSH at all**, so any MeSH-dependent element of a strategy silently misses them; this is the
measured basis for pairing controlled vocabulary with free text in every block. Weaker coverage of
non-English-language journals and of regional South Asian titles than its overall size suggests. No
conference abstracts. Automatic term mapping can broaden a query in ways the written strategy does
not record.

**Essential or supplementary.** **Essential.**

**Syntax.** NCBI. `[Mesh]` auto-explodes; `[tiab]` for title and abstract. No proximity operator;
no wildcard inside a quoted phrase. Capture the "Search details" output to document automatic
expansion.

---

### 2.2 Embase — **ESSENTIAL**

**Relevance.** The single most important addition. Embase indexes roughly 8,500 journals, several
thousand of which are not in MEDLINE, with notably stronger European, Asian and Latin American
coverage — directly relevant where the exposure burden for bidi, chutta and reverse smoking is
greatest. It also indexes conference abstracts, a recognised source of otherwise unpublished
estimates.

**Additional literature it captures.** Journals absent from MEDLINE; conference proceedings;
earlier indexing of recent articles. The commonly cited finding that a MEDLINE-only search misses a
substantial minority of eligible studies in observational reviews is the reason Embase is treated as
essential rather than optional. **No specific overlap percentage is asserted here**, since none has
been measured for this question.

**Limitations.** Subscription-only; **access not confirmed**. Uses **Emtree**, not MeSH, so the
strategy must be rewritten rather than translated mechanically. Conference abstracts often lack the
detail needed for eligibility and extraction, and will generate screening work that ends in
exclusion for insufficient data. Deduplication against PubMed records is essential and must rely on
the established identifier hierarchy.

**Essential or supplementary.** **Essential.** If Embase is unavailable, that must be reported as a
limitation of the review, not quietly omitted.

**Syntax.** Elsevier embase.com. `'mouth cancer'/exp` for exploded Emtree; `:ti,ab,kw` for free
text, where `:kw` reaches author keywords that PubMed does not index. Explosion must be stated
explicitly with `/exp`. Export as RIS.

---

### 2.3 Scopus — **RECOMMENDED (choose one of Scopus or Web of Science)**

**Relevance.** Broad multidisciplinary coverage with strong citation infrastructure, which makes it
the practical tool for **forward-citation checking** — identifying studies that cite a known
eligible study. That is a distinct retrieval mechanism from term-based searching and catches studies
whose terminology the query does not anticipate.

**Additional literature it captures.** Journals outside both MEDLINE and Embase; conference papers;
some regional titles. Its citation graph supports both backward reference-list checking and forward
citation chasing in one interface.

**Limitations.** Subscription-only; **access not confirmed**. **No controlled vocabulary at all** —
everything is free text, so the strategy cannot rely on exploded headings and must enumerate
synonyms exhaustively. Abstract coverage is incomplete for older records. Author-keyword quality
varies.

**Essential or supplementary.** **Supplementary but strongly recommended** — and the citation
checking it enables should be regarded as essential in itself, by whatever means.

**Syntax.** `TITLE-ABS-KEY( )`. Supports `*` truncation and `W/n` proximity, neither available in
PubMed, which permits a more compact expression. Export as RIS or CSV.

---

### 2.4 Web of Science Core Collection — **ALTERNATIVE to Scopus**

**Relevance.** Comparable role: broad coverage plus a citation index supporting forward citation
searching.

**Additional literature it captures.** Overlaps heavily with Scopus. Searching both is usually poor
value for the marginal yield; **one of the two is sufficient** unless both are already available at
no additional cost.

**Limitations.** Subscription-only; **access not confirmed**. No controlled vocabulary. Coverage
depends on which editions the subscription includes, so the editions searched must be recorded or
the search is not reproducible. Historically weaker non-English coverage than Embase.

**Essential or supplementary.** **Supplementary.** Choose Scopus or Web of Science on the basis of
which is accessible; record which, and why.

**Syntax.** `TS=( )` searches topic — title, abstract, author keywords and KeyWords Plus. Supports
`NEAR/n` and `*`.

---

### 2.5 Cochrane CENTRAL — **NOT ESSENTIAL for this question**

**Relevance.** Low. CENTRAL is a register of controlled trials. This review admits only case–control
and cohort studies of an exposure that cannot be randomised, so CENTRAL's core content is
ineligible by design.

**Additional literature it captures.** Very little that is eligible. It may contain the odd cohort
embedded in a trial programme.

**Limitations.** Design mismatch with the review question.

**Essential or supplementary.** **Supplementary, and defensibly omitted.** If omitted, say so and
give this reason. Searching it to appear thorough would add screening work with negligible expected
yield.

**Syntax.** Wiley. `MeSH descriptor: [Mouth Neoplasms] explode all trees`, `:ti,ab,kw`.

---

### 2.6 Regional databases — **RECOMMENDED, specifically for South Asian literature**

**Relevance.** This is a substantive methodological point, not a formality. The adopted exposure
definition explicitly admits bidis and reverse smoking, and the rationale recorded for it is that a
cigarette-only review would exclude much of the most informative literature, particularly South
Asian studies where the exposure burden is greatest. Much of that literature appears in Indian
journals with incomplete MEDLINE coverage.

| Database | Coverage | Assessment |
|---|---|---|
| **IndMED** (ICMR-NIC) | Indian biomedical journals, many not in MEDLINE | **Recommended — but conditional on verified current accessibility.** See the caveat below |
| **LILACS** | Latin American and Caribbean | Optional. Relevant to Brazilian oral cancer epidemiology, which is substantial |
| **KoreaMed, J-STAGE** | Korean, Japanese | Low priority for this exposure |
| **African Index Medicus** | African journals | Low expected yield for this question; include if resources allow |

**Caveat on IndMED specifically — accessibility is not verified.** IndMED is named here on the
strength of its coverage, **not** on confirmation that it is currently maintained and publicly
searchable. Its availability has been uncertain in recent years and **no attempt has been made to
access it**; nothing in this assessment should be read as establishing that it can be searched.
Before it is relied upon, the reviewer must confirm that it is reachable and record the interface
and the date.

**Fallback if IndMED is inaccessible.** The regional gap is real whether or not that particular
database is reachable, so it must be addressed by other means rather than dropped:

1. **Documented hand-searching** of the principal Indian and South Asian journals publishing oral
   cancer epidemiology, over a stated date range, with the journals and range recorded so the
   search is reproducible.
2. **Reference-list checking** of included studies and of existing reviews, which reaches regional
   literature indirectly and requires no subscription.
3. **A clearly qualified supplementary source** — for example Google Scholar, searched to a
   pre-stated and recorded stopping rule — reported with its limitations stated plainly: no
   controlled vocabulary, unstable result ordering, and results that are not fully reproducible.

Whichever route is taken, the shortfall must be reported as a limitation with its likely direction
of effect, since it falls on the exposure subgroup the exposure definition was written to include.

**Limitations.** Interfaces are less capable — limited Boolean support, unstable or absent
controlled vocabulary, and export formats that may not carry persistent identifiers, which
complicates deduplication. Coverage is less stable over time, so the interface and the date searched
must be recorded carefully. Simplified queries and more manual screening should be expected.

**Essential or supplementary.** **Supplementary, but the regional gap is a genuine threat to
validity** given the exposure definition. Omitting regional databases entirely should be declared
as a limitation with its likely direction of effect stated.

---

### 2.7 Supplementary methods — **ESSENTIAL as a group**

| Method | Role | Notes |
|---|---|---|
| **Reference-list checking** of all included studies and of existing reviews | Catches studies no query anticipates | Low cost, high yield. Should be treated as essential |
| **Forward-citation checking** of included studies | Catches later studies | Requires Scopus, Web of Science or an equivalent |
| **Grey literature / theses** | Dissertations carry unpublished estimates | Optional; consider ProQuest if accessible |
| **Contacting authors** | Resolves missing data rather than finding studies | Relevant at extraction, not retrieval |
| **Trial registries** | Not applicable | Observational exposure |

---

## 3. Recommended database strategy

Three tiers, balancing comprehensiveness against confirmed access and single-reviewer capacity.

### Tier 1 — minimum defensible (recommended floor)

1. **PubMed/MEDLINE** — re-executed with the approved corrected strategy. **Essential**, and the
   only database access to which is already established
2. **Embase** — **essential if institutional access is available.** If it is not, that must be
   reported as a coverage limitation, not quietly omitted
3. **Reference-list checking** of all included studies and of existing reviews on the question —
   **recommended supplementary method**; free, requires no subscription, and reaches literature no
   query anticipates

A review searching fewer sources than this should not be described as systematic.

### Tier 2 — recommended

4. **Scopus or Web of Science** — **choose according to actual access and coverage**, not by
   preference. Scopus has broader abstract coverage; Web of Science coverage depends on the
   subscribed editions, which must be recorded or the search is not reproducible. Searching both is
   poor value for the marginal yield. Use whichever is obtained for **forward-citation checking**
   of included studies
5. **IndMED** *(conditional on verified accessibility; otherwise the fallback above)* — for the
   regional literature the exposure definition makes material

### Tier 3 — optional, resources permitting

6. **LILACS**
7. Grey literature and theses

**Cochrane CENTRAL is not recommended**, on the stated design-mismatch grounds, and its omission
should be reported with that reason.

### Interaction with screening capacity

Each database multiplies the screening load, and the load is already contested: the corrected
PubMed query alone measured **8,190 records without a design block, and 5,008 with one, at the
2026-11-12 syntax validation**. **D023 (2026-11-13) adopts the no-design-block form, so 8,190 is
the operative volume.** Both are counts-only interrogation figures, not search yields.
Adding Embase will add several thousand more, of unknown number until executed. Under single-reviewer
screening this is the binding constraint, and it is the substance of the open volume question. **No
database should be dropped merely to reduce workload without that trade being recorded as a
limitation**; equally, no database should be added that the reviewer cannot actually screen.

## 4. What must be established before any execution

1. **Confirm institutional access** to Embase and to Scopus or Web of Science. Access is **not
   confirmed** and nothing here assumes it.
2. **Settle the database set** as a recorded decision.
3. **Write one strategy document per database**, with platform-specific syntax, before executing
   any of them.
4. **Confirm that deduplication handles multi-database input.** The existing pipeline was exercised
   on a single source with 0 duplicates found; cross-database input will produce real duplicates and
   real ambiguous pairs, and the matching rules must be reviewed against records lacking PMIDs —
   Embase conference abstracts in particular.
5. **Settle the screening-capacity question** before committing to a volume the reviewer cannot
   screen.

## 5. Statement of what has and has not been done

- **Searched:** PubMed, once, with the v1 query string, unfiltered, 194 records, registered.
- **Not searched:** every other database listed above.
- **Not executed:** the drafted v2 strategy and the strategy recommended in
  `recommended_search_strategy.md`. The 4,770 / 7,875 figures (v2 draft, 2026-10-29) and the
  8,190 / 5,008 figures (corrected query, 2026-11-12) all come from read-only, counts-only
  syntax-validation runs performed by automated tooling under the reviewer's direction. They are
  **not** search yields and **not** researcher-executed searches. No record was retrieved,
  downloaded or exported by either run.
- **Not confirmed:** access to any subscription database.
- **Not estimated:** the yield of any unexecuted database. No number is offered, because any number
  would be invented.
