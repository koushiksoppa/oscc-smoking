# P007 — Database coverage: decision memorandum

**Status: the researcher has approved the P007 wording (section 8). P007 nevertheless remains OPEN,
and the decision register is unchanged.** The approved wording is conditional on institutional
access that has not been verified, so it states the *form* of the resolution rather than closing it;
it closes once the access checks in section 4 return.
No database was searched, no record retrieved, no query modified and no entry added to
`docs/decisions/decision_log.md`. P013 (whether the study-design block is retained) is a separate
question and is **not** decided here.

**Prepared:** 12 November 2026. **Wording approved:** 12 November 2026.
**Repository state:** `HEAD` `b5afaff`; no commit made.

---

## 1. Current P007 wording

Verbatim from `docs/decisions/decision_log.md`, the authoritative register:

> | P007 | Additional databases (Embase, Scopus/Web of Science) and supplementary methods (reference
> lists, citation searching); constrained by institutional access. | Search sensitivity;
> PRISMA/MOOSE expectations. | Search v2 |

Status: **open**. Listed as needed before "Search v2". The adopted decisions are D001–D015, D020 and
D022; D016–D019 are recorded as proposed, and D021 is **not** in the register. **Nothing in the
register fixes the database set.** D022 (bounded supplementary grey-literature searching, adopted
2026-11-13) was deliberately kept independent of P007: it concerns grey sources, not bibliographic
database coverage, and does not inherit P007's dependency on access verification.

The decisions that constrain P007:

| Decision | Bearing on database choice |
|---|---|
| **D009** | Exposure includes **bidi** and other non-cigarette combusted products. This is the single most important driver: it makes South Asian literature material to the review, and that literature is unevenly indexed in MEDLINE. |
| **D010** | **Single reviewer.** Every database added multiplies a screening load one person must carry. |
| **D013** | Retrieve unfiltered; exclude by language and species at screening. Raises yield per database. |
| **D008** | SCC histology confirmed or ≥90% — a full-text judgement, so retrieval must be sensitive rather than precise. |
| **D011** | One registry entry per database × execution. Each new database is a separate registered execution with its own date, count and checksum. |

---

## 2. Evidence reviewed

| Source | What it contributed |
|---|---|
| `docs/decisions/decision_log.md` | P007 wording and status; the adopted and proposed decisions; P012, P013, P014–P022 |
| `docs/methods/database_coverage_assessment.md` | The existing database-by-database assessment and its three tiers |
| `docs/methods/search_strategy_audit.md` | The C-1 outcome-block defect and the design-block analysis |
| `docs/methods/recommended_search_strategy.md` | The corrected PubMed strategy; 8,190 / 5,008 counts |
| `docs/methods/p007_p013_decision_memorandum.md` | The prior joint memorandum; the 4,770 / 7,875 figures |
| `docs/reports/manuscript_final.md` §2.2, Table 2 | How information sources are currently reported |
| `docs/reports/supplementary_material.md` S1 | Search strategies and syntax-validation records |
| `config/sources.yaml`, `data/raw/SHA256SUMS` | The only registered execution: `pubmed_v1r`, 194 records |
| NIT Rourkela Biju Patnaik Central Library, public pages | Publicly advertised database subscriptions (section 4) |

**Nothing in the repository records an institutional affiliation.** NIT Rourkela is named in the
task instruction, not in the project record. Section 4 treats it as the stated affiliation and
reports only what is publicly verifiable about it.

---

## 3. Database-by-database assessment

Access categories used throughout: **Confirmed** (evidence in the repository that it was used),
**Advertised** (the institution publicly lists it, which is not the same as the researcher having
working access), **No evidence**, **Unverified**.

### 3.1 PubMed / MEDLINE

| Dimension | Assessment |
|---|---|
| Relevance | **Core.** The principal index for cancer epidemiology; MeSH supports an exploded, reproducible strategy. |
| Expected unique contribution | The backbone of the search. Already yielded the 194-record set under the narrow v1 query. |
| Overlap with PubMed | — |
| Type | Bibliographic database |
| Access | **Confirmed.** Free; one execution registered with a checksum (`pubmed_v1r`). |
| Reproducible strategy? | **Yes** — already drafted, corrected and syntax-validated. |
| Classification | **CORE** |

### 3.2 Embase

| Dimension | Assessment |
|---|---|
| Relevance | **High — the most valuable addition.** Broader journal coverage than MEDLINE, with stronger European, Asian and Latin American representation, plus indexed conference abstracts. Directly relevant to the bidi/reverse-smoking literature D009 admits. |
| Expected unique contribution | Journals absent from MEDLINE; conference abstracts; earlier indexing. **No overlap percentage is asserted** — none has been measured for this question, and quoting a generic figure would be inventing evidence. |
| Overlap with PubMed | Substantial but incomplete. Embase contains all MEDLINE records plus its own. |
| Type | Bibliographic database |
| Access | **No evidence.** Embase is **not listed** among the publicly advertised databases of the stated institution (section 4). This is not proof of absence, but there is no evidence of access. |
| Reproducible strategy? | Yes, but requires a **rewrite into Emtree**, not a translation of MeSH. Non-trivial work. |
| Classification | **CORE if accessible; otherwise a declared limitation.** Not to be quietly omitted. |

### 3.3 Scopus

| Dimension | Assessment |
|---|---|
| Relevance | Broad multidisciplinary coverage; its citation graph is the practical instrument for **forward-citation searching**, a retrieval mechanism distinct from term matching. |
| Expected unique contribution | Journals outside MEDLINE and Embase; conference papers; some regional titles. Its main value here is citation searching rather than raw coverage. |
| Overlap with PubMed | High for indexed biomedical journals; the unique fraction is the non-MEDLINE and regional tail. |
| Type | Bibliographic database **and** the enabling tool for a supplementary discovery method. |
| Access | **Advertised.** Publicly listed by the stated institution's library. **Not verified** for this researcher. |
| Reproducible strategy? | Yes, but **no controlled vocabulary** — synonyms must be enumerated exhaustively. `TITLE-ABS-KEY()`, with `*` and `W/n` proximity. |
| Classification | **CONDITIONAL — core among the citation indexes; choose one of Scopus or Web of Science.** |

### 3.4 Web of Science Core Collection

| Dimension | Assessment |
|---|---|
| Relevance | Comparable role to Scopus: broad coverage plus a citation index. |
| Expected unique contribution | **Overlaps heavily with Scopus.** Searching both is poor value for marginal yield. Historically weaker non-English coverage than Embase. |
| Overlap with PubMed | High, as for Scopus. |
| Type | Bibliographic database and citation-searching tool |
| Access | **Advertised.** Publicly listed by the stated institution's library. **Not verified.** |
| Reproducible strategy? | Yes — `TS=()`, `NEAR/n`, `*`. **The subscribed editions must be recorded**, or the search is not reproducible, since coverage depends on them. |
| Classification | **CONDITIONAL — the alternative to Scopus, not an addition to it.** |

### 3.5 IndMED

| Dimension | Assessment |
|---|---|
| Relevance | **Potentially high for this specific question.** Indexes Indian biomedical journals with incomplete MEDLINE coverage — precisely where bidi, chutta and reverse-smoking studies appear. |
| Expected unique contribution | Regional studies invisible to the other databases. The gap it addresses is a genuine validity threat given D009. |
| Overlap with PubMed | Low — that is the point of including it. |
| Type | Bibliographic database (regional) |
| Access | **Unverified.** Its continued maintenance and public searchability have been uncertain; **no attempt has been made to reach it**, and nothing here establishes that it can be searched. |
| Reproducible strategy? | **Doubtful.** Limited Boolean support, unstable or absent controlled vocabulary, export formats that may lack persistent identifiers — which complicates deduplication. |
| Classification | **SUPPLEMENTARY, conditional on verified reachability.** If unreachable, the regional gap must be addressed another way (section 6), not dropped. |

### 3.6 LILACS

| Dimension | Assessment |
|---|---|
| Relevance | Moderate. Latin American and Caribbean literature; Brazilian oral-cancer epidemiology is substantial and relevant. |
| Expected unique contribution | Regional studies, largely disjoint from MEDLINE's indexed set. |
| Overlap with PubMed | Low. |
| Type | Bibliographic database (regional) |
| Access | **Openly available** (via the Virtual Health Library); **no subscription required**. Reachability has **not been tested by this project**. |
| Reproducible strategy? | Yes, with a simplified query; the interface and search date must be recorded. |
| Classification | **SUPPLEMENTARY.** Lower priority than the South Asian gap, which is the one D009 makes material. |

### 3.7 Cochrane CENTRAL

| Dimension | Assessment |
|---|---|
| Relevance | **Low — design mismatch.** CENTRAL is a register of controlled trials. This review admits only case–control and cohort studies of an exposure that cannot be ethically randomised. |
| Expected unique contribution | Minimal. |
| Overlap with PubMed | Largely derived from MEDLINE and Embase in any case. |
| Type | Specialised register |
| Access | Not investigated — moot, given the design mismatch. |
| Reproducible strategy? | Yes, but it would retrieve the wrong study designs. |
| Classification | **NOT RECOMMENDED.** Omission should be **reported with this reason**, so a reader sees it was considered and excluded on grounds, not overlooked. |

### 3.8 Reference-list and forward-citation searching

| Dimension | Assessment |
|---|---|
| Relevance | **High, and partly independent of query wording** — which matters here, because the executed query is narrower than the protocol. These methods catch studies no query anticipates. |
| Expected unique contribution | Backward: studies cited by included studies and by existing reviews. Forward: later studies citing them. |
| Overlap with PubMed | Deliberately different mechanism; overlap is incidental. |
| Type | **Supplementary discovery methods, not databases.** They must be reported as such and never counted as database coverage. |
| Access | **Reference-list checking needs no subscription** — it is the one high-value method available regardless of what the institution subscribes to. Forward-citation checking requires a citation index (Scopus or Web of Science). |
| Reproducible strategy? | Yes, if the seed set, the direction and the stopping rule are pre-stated and recorded. |
| Classification | **CORE as a group.** Reference-list checking should be treated as essential. |

### 3.9 Grey literature

| Dimension | Assessment |
|---|---|
| Relevance | Moderate. Theses and dissertations carry unpublished estimates, which bear directly on small-study and publication-bias assessment — the review pre-specifies such analyses. |
| Expected unique contribution | Unpublished or non-indexed estimates; some regional theses. |
| Overlap with PubMed | Low. |
| Type | Supplementary source |
| Access | **Unverified.** ProQuest dissertations not publicly listed by the stated institution. Shodhganga (Indian theses) is openly available but **untested here**. |
| Reproducible strategy? | Partially. A tool such as Google Scholar has no controlled vocabulary and unstable result ordering, so it is reproducible only to a **pre-stated stopping rule**, and its limitations must be reported. |
| Classification | **SUPPLEMENTARY, optional.** Justified mainly by the publication-bias analyses, not by expected yield. |
| **Trial registries** | **Not applicable** — observational exposure. |

---

## 4. Access status and verification gaps

### What is actually verified

| Claim | Status | Evidence |
|---|---|---|
| PubMed is accessible and has been searched | **VERIFIED** | `config/sources.yaml`; registered export; SHA-256 in `data/raw/SHA256SUMS` |
| The stated institution publicly lists **Scopus** | **PUBLICLY ADVERTISED** | Library database page |
| The stated institution publicly lists **Web of Science** | **PUBLICLY ADVERTISED** | Library database page |
| The stated institution lists **Embase** | **NOT LISTED** | Embase does not appear on the library's database page; no biomedical database appears |
| The researcher personally has working access to any of these | **NOT VERIFIED** | Cannot be established without the researcher signing in, which was not done |

**Method and its limits.** The institution's main domain returned HTTP 403 to this session; the
library subdomain was readable. The databases page lists MathSciNet, SciFinder, Prowess, **Web of
Science**, **Scopus**, ISID, J-Gate Plus (JCCC), CD-ROM databases and EPWRF India Time Series, with
access described as IP-based on campus and by remote sign-in off campus. **No medical or biomedical
database is listed**, which is consistent with an engineering institute's collection.

**Three cautions, stated plainly:**

1. **An institutional subscription statement is not access.** It may be out of date, may exclude a
   department, may require registration, or may have lapsed. Nothing here establishes that the
   researcher can run a search.
2. **Absence from a public list is not proof of absence.** Embase might be reachable through a
   consortium route (e-ShodhSindhu was referenced), through a partner institution, or through a
   subscription the page does not itemise.
3. **One Nation One Subscription (ONOS) is about full text, not searching.** It is referenced by the
   library and provides journal access across major publishers. That bears on **obtaining the 85
   full texts** — a real and separate benefit — but it does **not** provide a searchable bibliographic
   database and does not substitute for Embase.

### Verification checklist for the researcher

Run these yourself; each takes minutes and each answers a question this memorandum cannot.

1. **On campus (or on the institutional VPN), open the library's e-resources page.** Confirm
   Scopus and Web of Science both open **to a search box**, not to a paywall or a publisher pitch.
2. **For Web of Science, record which editions the subscription covers** — visible in the search
   interface under the collection selector. Without this the search is not reproducible.
3. **Search the library page and catalogue for "Embase".** If absent, ask the library directly
   whether Embase is available by any route, including consortium access.
4. **Ask the library these three questions in one message:**
   (a) Do we have Embase, by any route? (b) Which Web of Science editions and year ranges are
   subscribed? (c) Is off-campus remote access available to me, and how?
5. **Test off-campus access**, since much of the work will not happen on campus.
6. **If Embase is unavailable, ask whether a reciprocal or paid arrangement exists** with a nearby
   medical institution — for example a regional medical college or an ICMR centre. A single
   supervised session is often enough to execute and export one search.
7. **Test IndMED's reachability** and record the interface and date, or record that it is
   unreachable. Either outcome is a finding.
8. **Record the date and outcome of each check.** These become the PRISMA-S information-sources
   record, and a negative result is as reportable as a positive one.

---

## 5. Three configurations

No expected record counts or recall percentages are given for any unexecuted database. The only
measured figures in the project are PubMed counts-only syntax validations (8,190 without a design
block, 5,008 with one, 12 November 2026), which are **not** search yields.

### Configuration A — Minimum feasible

**PubMed/MEDLINE + reference-list searching.**

| Dimension | Assessment |
|---|---|
| Expected coverage | Lowest. MEDLINE-indexed literature plus whatever reference lists reach. |
| Feasibility | **Highest** — needs no subscription and no access verification. Executable today. |
| Reproducibility | **Highest.** One platform, controlled vocabulary, a documented reference-list protocol. |
| Additional workload | Lowest: one database, plus reference checking of included studies. |
| Limitations | Single-database search; no conference abstracts; no forward-citation searching; the regional gap D009 makes material is **unaddressed**. |
| Risk of missing studies | **High, and non-random.** Losses concentrate in non-MEDLINE journals and regional literature — the bidi and reverse-smoking studies. Because the loss is systematic rather than random, it can bias the pooled estimate, not merely widen it. |

### Configuration B — Recommended

**PubMed/MEDLINE + Embase (if accessible) + one of Scopus or Web of Science (if accessible) +
reference-list and forward-citation searching.**

| Dimension | Assessment |
|---|---|
| Expected coverage | Meets the normal expectation for a review of observational studies. |
| Feasibility | **Contingent on access.** Scopus/WoS are advertised; Embase is not evidenced. Realistically this may execute **without** Embase. |
| Reproducibility | Good, if each strategy is documented per platform and the WoS editions are recorded. Embase needs an Emtree rewrite. |
| Additional workload | Substantially higher — a second and third record set, genuine cross-database duplicates, and Emtree translation. Under D010 this is the binding constraint. |
| Limitations | If Embase proves unavailable, the configuration degrades to PubMed + one citation index, and that must be **declared**, not glossed. |
| Risk of missing studies | **Moderate**, and lower still if citation searching is done well. |

### Configuration C — Expanded

**PubMed + Embase + Scopus and/or Web of Science + IndMED (if accessible) + supplementary sources
(LILACS, grey literature).**

| Dimension | Assessment |
|---|---|
| Expected coverage | Highest, and the only configuration that addresses the regional gap directly. |
| Feasibility | **Lowest.** Requires Embase access that is not evidenced, IndMED reachability that is unverified, and a screening capacity a single reviewer does not plausibly have. |
| Reproducibility | **Weakest link is the regional and grey sources** — unstable interfaces, limited Boolean support, identifiers that complicate deduplication. |
| Additional workload | Highest by a wide margin. On the measured PubMed figures alone the title/abstract load is already tens of hours; each added database multiplies it. |
| Limitations | Risks a search that is begun and not finished, which is worse than a narrower search honestly reported. |
| Risk of missing studies | **Lowest** — if it is actually completed. |

---

## 6. Recommendation

### Is PubMed alone defensible?

**No — not as a systematic review of this question, and the reason is specific rather than
conventional.** D009 admits bidi and other non-cigarette combusted products, and the recorded
rationale is that a cigarette-only review would exclude the most informative literature. The studies
that make D009 worth having are concentrated in South Asian journals with incomplete MEDLINE
coverage. A PubMed-only search is therefore least sensitive **exactly where this review's exposure
definition is most distinctive**. The resulting loss is systematic, not random, so it threatens
validity rather than merely precision.

Two honest alternatives exist if nothing beyond PubMed can be obtained:

1. **Narrow the stated scope** — report a review of MEDLINE-indexed literature, with the coverage
   limitation in the title or abstract. Defensible, and less sensitive than intended.
2. **Keep the scope and declare the gap**, with its likely direction of effect, and strengthen
   reference-list checking to compensate partially. This is the better option, because reference
   lists of existing reviews reach the regional literature indirectly and cost nothing.

What is **not** defensible is searching one database and describing the result as a comprehensive
systematic search.

### Ideal versus executable

| | Configuration | Access reality |
|---|---|---|
| **Ideal** | Configuration C | Requires Embase and IndMED, neither evidenced. Screening capacity is the harder obstacle. |
| **Recommended** | Configuration B | Partly contingent: Scopus/WoS advertised, Embase not evidenced. |
| **Executable today with confirmed access only** | **PubMed + reference-list checking** (Configuration A) | The only configuration resting on verified access. |

### The recommendation

**Adopt Configuration B, resolved against verified access, in this order:**

1. **PubMed/MEDLINE** with the corrected strategy — core, access confirmed.
2. **One citation index — Scopus preferred, Web of Science if Scopus is unavailable.** Both are
   publicly advertised, so this is the **most likely addition to succeed**. Use it for term-based
   searching **and** forward-citation checking of included studies. If Web of Science is used,
   record the editions.
3. **Embase if and only if access is confirmed.** Pursue it actively — it is the highest-value
   addition — but do not assume it. If unavailable, **record the attempt and the outcome**, and
   report its absence as a coverage limitation with its likely direction of effect.
4. **Reference-list checking of all included studies and of existing reviews** — essential,
   subscription-free, and the main mitigation for whatever is missed.
5. **Address the South Asian gap explicitly by whichever route is reachable**: IndMED if it is
   reachable, otherwise documented hand-searching of named journals over a stated date range, or a
   qualified supplementary search to a pre-stated stopping rule. **Do not drop the gap silently** —
   it is the one most likely to bias this particular review.

**Scopus and Web of Science are alternatives, not additions.** Searching both is poor value.
**Cochrane CENTRAL is not recommended**, on design-mismatch grounds, and its omission should be
reported with that reason.

### Fallback if no subscription database can be accessed

Configuration A, **with the gap declared rather than concealed**:

- PubMed with the corrected strategy.
- Reference-list checking of all included studies **and of existing reviews on the question** — the
  single most valuable subscription-free method, and the main route to regional literature.
- Documented hand-searching of named South Asian journals over a stated date range, if feasible.
- An explicit limitations paragraph stating that one database was searched, why, what is likely to
  have been missed, and in which direction it could bias the estimate.
- The manuscript should then **not** describe the search as comprehensive.

> **Context added 13 November 2026.** The phrase "noted, not decided" in the heading below
> describes **P013's status when this memorandum was written**. **P013 was subsequently resolved by
> D023 on 13 November 2026**, which removes the study-design block from the primary search.
> **P007 itself remains open and is not resolved by D023**: no database access beyond PubMed has
> been verified. The section below is retained unchanged as written.

### Interaction with P013 — noted, not decided

Database choice and the design block both affect sensitivity, and they interact: a narrower design
block loses more when fewer databases are searched. **P013 is not decided here.** The only point
recorded for the P013 discussion is that if few databases prove accessible, the argument for
removing the design block strengthens, because the remaining search must carry more of the burden.

---

## 7. Decisions required from the researcher

| # | Decision | Depends on |
|---|---|---|
| 1 | Verify access to Scopus and Web of Science; choose **one** | Section 4 checklist, items 1–2 |
| 2 | Establish whether Embase is obtainable by any route | Checklist items 3–4, 6 |
| 3 | Decide whether the review proceeds **without** Embase if it cannot be obtained, and whether its absence is reported as a limitation or the scope is narrowed | Decision 2 |
| 4 | ~~Decide how the South Asian regional gap is addressed~~ — **SETTLED 12 Nov 2026**: IndMED where reachable, otherwise documented hand-searching of named journals, otherwise declared as a limitation (section 8.2) | — |
| 5 | Confirm the screening capacity the chosen set implies, under D010 | Interacts with P013 |
| 6 | Decide whether grey literature is searched, given the pre-specified publication-bias analyses | Still open; the approved wording is silent on grey literature |
| 7 | ~~Approve the final P007 wording~~ — **DONE 12 Nov 2026** (section 8) | — |
| 8 | Close P007 once decisions 1–3 and 5 return, by recording the wording in `docs/decisions/decision_log.md` | Requires separate authorisation |

---

## 8. Approved P007 wording

**Approved by the researcher on 12 November 2026.** **P007 remains OPEN**, and the decision register
is unchanged: the wording is itself conditional on institutional access that has not yet been
verified (section 4), so it cannot be converted into a closed decision until those checks return.
What is settled is the *form* the resolution will take; what is outstanding is the access evidence
that fills in its conditionals.

### 8.1 As supplied by the researcher — verbatim

> The systematic review will search PubMed/MEDLINE and, subject to confirmed institutional access,
> one citation-indexing database (preferably Scopus, or Web of Science if Scopus is unavailable).
> Embase will be included if access can be confirmed before the formal search. IndMED will be
> considered as a supplementary source if an accessible searchable interface is available.
> Reference-list checking of eligible studies and relevant systematic reviews will be undertaken,
> together with forward citation searching where accessible.
>
> The databases actually searched, their platforms, complete search strategies, search dates,
> coverage limitations, and record counts will be documented transparently. No database will be
> reported as searched unless the search has actually been executed and its results preserved.

This text is recorded unaltered. The two paragraphs below were **added at the researcher's direction
on the same date**, in response to two gaps identified in this memorandum; they are set out
separately so that the provenance of every sentence stays visible.

### 8.2 Additions authorised by the researcher

> **Regional coverage fallback.** Where IndMED has no accessible searchable interface, the South
> Asian regional gap created by the exposure definition (D009) will be addressed by documented
> hand-searching of named journals over a stated date range, or, where that is not feasible,
> declared as a coverage limitation with its likely direction of effect. The gap will not be dropped
> silently on the grounds that the database was unreachable.
>
> **Cochrane CENTRAL.** CENTRAL will not be searched, on the grounds that it registers controlled
> trials while this review admits only case–control and cohort studies of an exposure that cannot be
> randomised. The omission will be reported with that reason, so that it is visible as a considered
> exclusion rather than an oversight.

### 8.3 Consolidated wording

The text to be carried into the protocol and the manuscript, being 8.1 followed by 8.2:

> The systematic review will search PubMed/MEDLINE and, subject to confirmed institutional access,
> one citation-indexing database (preferably Scopus, or Web of Science if Scopus is unavailable).
> Embase will be included if access can be confirmed before the formal search. IndMED will be
> considered as a supplementary source if an accessible searchable interface is available.
> Reference-list checking of eligible studies and relevant systematic reviews will be undertaken,
> together with forward citation searching where accessible.
>
> Where IndMED has no accessible searchable interface, the South Asian regional gap created by the
> exposure definition (D009) will be addressed by documented hand-searching of named journals over a
> stated date range, or, where that is not feasible, declared as a coverage limitation with its
> likely direction of effect.
>
> Cochrane CENTRAL will not be searched, on the grounds that it registers controlled trials while
> this review admits only case–control and cohort studies; the omission is reported with that reason.
>
> The databases actually searched, their platforms, complete search strategies, search dates,
> coverage limitations, and record counts will be documented transparently. No database will be
> reported as searched unless the search has actually been executed and its results preserved.

### 8.4 What this wording commits the project to

| Commitment | Consequence |
|---|---|
| PubMed is unconditional | Already satisfied for the v1r execution; the corrected strategy still awaits execution. |
| One citation index, **preferably Scopus** | Resolves the Scopus-versus-Web-of-Science choice in advance, conditional on access. Both are publicly advertised by the institution, so this is the addition most likely to succeed. If Web of Science is used instead, D011 and reproducibility require the subscribed editions to be recorded. |
| Embase only **if confirmed before the formal search** | Sets a deadline as well as a condition: Embase cannot be added after the fact without that being a new execution under D011. A negative access result must be recorded, not left blank. |
| Reference-list checking is **unconditional** | The one high-value method needing no subscription, and the main mitigation for whatever the query misses. |
| Forward citation searching "where accessible" | Tied to the citation index above; if no citation index is obtained, this lapses and the lapse is reportable. |
| Regional gap has a **fallback** | The gap survives IndMED being unreachable; it must be addressed or declared either way. |
| CENTRAL excluded **with a stated reason** | Visible as a considered exclusion. |
| **Nothing is reported as searched unless executed and preserved** | Stricter than the wording this memorandum proposed, and consistent with D011 and the standing prohibition on reporting work that was not done. It binds the manuscript's Table 2, which currently lists every source as not searched. |

**What the wording deliberately leaves open:** whether Embase is obtainable, which citation index is
actually used, whether IndMED is reachable, and the screening capacity the resulting volume implies
under D010. Those are the access findings that must return before P007 can close.

## 9. Consequences of each option

| Option | For the review | For the manuscript |
|---|---|---|
| **A — PubMed only** | Systematic loss concentrated in regional and non-MEDLINE literature; the bidi evidence D009 was written to capture is most at risk | Cannot be described as a comprehensive systematic search. Needs an explicit limitation with direction of effect, and possibly a narrowed title. Reviewers are likely to challenge it. |
| **B — Recommended** | Meets the normal expectation for observational reviews; citation searching compensates partly for query wording | Reportable as a systematic search. If Embase is absent, one declared limitation instead of a structural flaw. PRISMA-S requires per-database strategies and dates. |
| **C — Expanded** | Best coverage; genuine risk of non-completion under single-reviewer screening | Strongest claim **if finished**. An abandoned expanded search is worse than a completed narrower one. |
| **Embase unobtainable, undisclosed** | — | **Not acceptable.** Violates the project's standing prohibitions: missing stays missing and is flagged. |
| **Deferring P007** | Blocks the corrected strategy's execution; the review stays at 194 records from a query narrower than its own protocol | Section 3.1 cannot advance; the manuscript remains an interim report. |

---

## 10. What this document does not do

- It records the researcher's **approved wording** for P007 (section 8), but does **not** close P007
  and does **not** alter `docs/decisions/decision_log.md`. Closing it is a separate act requiring
  separate authorisation, and the access findings in section 4 must return first.
- It does **not** resolve or discuss the merits of P013.
- No search was executed; no record was retrieved, downloaded or exported.
- No database access was tested by signing in, and no credential was requested or used.
- The 194-record screening population, raw data and protected checksums are untouched.
- No yield, recall figure or study count is estimated for any unexecuted database, because any such
  number would be invented.

---

## Sources consulted for section 4

- [NITR Library — Databases](https://library.nitrkl.ac.in/index.php/resources/electronic-resources/databases)
- [NITR Library — Home](https://library.nitrkl.ac.in/)
- [NIT Rourkela Shibboleth Identity Provider](https://idp.nitrkl.ac.in/) (remote-access route; not used)

Accessed 12 November 2026, read-only, without signing in.
