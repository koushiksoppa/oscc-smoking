# P007 — database access verification record

**Purpose.** A human-completable evidence record for verifying database access **before** any
formal search is executed.

**This record does not resolve P007 and does not authorise any search.** It is an instrument for
collecting evidence. P007 closes only when the researcher reviews the completed record and makes a
recorded decision on database coverage.

**Status when created:** 13 November 2026. **P007: OPEN.**
**Created without signing in to any account and without executing any database search.**

---

## 1. Scope, and its relationship to P007

P007 asks which databases the review will search. Its approved wording is conditional:

> "…subject to confirmed institutional access, one citation-indexing database (preferably Scopus,
> or Web of Science if Scopus is unavailable). Embase will be included if access can be confirmed
> before the formal search."

Those conditions cannot be settled by reasoning. They are facts about what the researcher's account
can actually do, and only the researcher can establish them.

| | |
|---|---|
| **This record provides** | A fixed evidence standard, a per-database template, and a place to record outcomes and their dates |
| **This record does not provide** | Any verification. Every status below is either carried forward from existing evidence or blank |
| **Who completes it** | The researcher, signed in to their own institutional account |
| **What closes P007** | A separate, recorded decision made after this record is complete |

**Related decisions.** **D023** (adopted 2026-11-13) settles the search *form* — no study-design
block — and is independent of P007. **D011** requires one registry entry per database × execution,
each with its own strategy document, date, count and checksum. **D022** governs grey literature.
None of these is affected by this record.

---

## 2. Publisher full-text access is not bibliographic database access

This distinction is the one most likely to produce a false positive, so it is stated before the
template rather than after it.

| | Full-text access | Bibliographic database access |
|---|---|---|
| What it gives you | The PDF of an article you have **already identified** | The ability to **discover** articles you do not yet know about |
| Typical route | Publisher platform, ONOS, a consortium journal deal, an open-access copy | A subscription to the database itself (Embase, Scopus, Web of Science) |
| What it does for this review | Helps obtain the **85 full texts** at the retrieval stage — a real and separate benefit | Produces the **records to screen** |
| Can it substitute? | **No** | — |

**One Nation One Subscription (ONOS)** is referenced by the institution's library and provides
journal access across major publishers, **including Elsevier journals**. Elsevier also publishes
Embase and owns Scopus. **Access to Elsevier journals does not confer access to Embase or Scopus.**
If a library response mentions ONOS or "we have Elsevier", that is an answer about full text and
must be recorded as such, not as database access.

**Equally, do not record these as access:**

- A database appearing on a library web page, in a LibGuide, or in a consortium brochure.
- A search box that loads but returns "your institution does not subscribe" on execution.
- A trial or walk-in arrangement that will have lapsed before the search is executed.
- A colleague's or supervisor's personal account.

---

## 3. The execute-and-export verification standard

A database counts as **verified** only when **all seven** steps below succeed and are recorded. The
standard is deliberately higher than "the page opens", because this pipeline requires a preserved,
checksummed export (D011): a database that searches but will not export is unusable here.

| # | Step | What to record | Why it matters |
|---|---|---|---|
| 1 | **Institutional login or access route** | On-campus IP, VPN, Shibboleth/institutional sign-in, or other | Off-campus access often differs from on-campus; most of the work will not happen on campus |
| 2 | **Search interface opens** | Yes/No, and the exact interface and URL | An interface that loads is necessary but far from sufficient |
| 3 | **A trivial test query executes and returns a count** | The query used and the count returned | This is where an unsubscribed database usually fails. Suggested query: `oral cancer AND smoking` — deliberately trivial, and **not** the review's strategy |
| 4 | **At least one record exports successfully** | Yes/No, and how many records the export contained | The single most important step, and the one most often skipped |
| 5 | **Export format recorded** | RIS, BibTeX, CSV, NBIB, plain text, other | Determines whether the parsing stage can read it at all |
| 6 | **Persistent identifiers and bibliographic fields inspected** | Which of PMID, DOI, Embase accession, Scopus EID, WoS UT are present; whether title, authors, year, journal and **abstract** are present | Deduplication matches on normalised DOI, then PMID, then a title+author+year fingerprint. An export without identifiers degrades deduplication to fingerprint matching; an export without abstracts cannot be screened at title and abstract |
| 7 | **Export restrictions and record limits documented** | Maximum records per export, any daily or session cap, whether bulk export is disabled, any licence restriction on retaining records | A 500-record export cap against an ~8,190-record strategy is a workflow constraint that must be known **before** execution, not discovered during it |

**The test query is not the search.** Step 3 exists to prove the subscription works. It is not a
search of record, produces no yield, and must never be registered under D011.

**Record the evidence, not just the conclusion.** For each database, save a screenshot or the
exported file itself to a location you name in the record. "It worked" is not evidence; an export
file with a date is.

---

## 4. How to classify a failure

A failed check is a finding, and **the kind of failure determines the next action.** Do not record
a bare "no".

| Failure type | How it presents | What it means | Next action |
|---|---|---|---|
| **Technical failure** | Page will not load, server error, interface broken, timeout | Says nothing about subscription | Retry on another network and another day before concluding anything |
| **Authentication failure** | Login rejected, session expires, Shibboleth loop, "not recognised" | The subscription may exist; **your route to it** does not | Ask the library about your credentials and the remote-access route |
| **Subscription absence** | Interface loads, then "your institution does not have access", or the database is absent from the institutional list and the library confirms it | The institution does not hold it | Pursue consortium, reciprocal or paid routes (§6), or record the gap as a coverage limitation |
| **Export restriction** | Search executes, results display, but export is disabled, capped below the strategy's volume, or offers no usable format | Partially accessible — searchable but not harvestable | Record as **partially accessible**. Decide whether a capped export can be batched, or whether the database is unusable under D011 |

**Record the date of every attempt, including failed ones.** A negative result dated and recorded
is reportable under PRISMA-S; an undocumented absence is not.

---

## 5. Per-database verification sections

> **All fields below are blank by design.** Pre-filled rows carry only evidence that already exists
> in the repository, and each says what kind of evidence it is.

### 5.1 Embase

**Carried-forward status (13 November 2026): NOT IDENTIFIED in publicly available institutional
library information; availability UNKNOWN.** Embase does not appear on the library's published
database page, and no biomedical database appears there. **Absence from a public list is not proof
of absence** — a consortium or unlisted route may exist. This is the highest-value addition and the
one with the longest lead time if it must be requested, so it is listed first.

| Field | Entry |
|---|---|
| Date checked | |
| Access route | |
| Search interface accessible? | |
| Test query executed? (query and count) | |
| Export successful? (number of records) | |
| Export format | |
| Persistent identifiers present | |
| Other bibliographic identifiers present | |
| Export restrictions / record limits | |
| Evidence location | |
| Failure type, if any (§4) | |
| **Outcome** | ☐ verified ☐ unavailable ☐ partially accessible ☐ not tested |
| Notes | |

### 5.2 Scopus

**Carried-forward status (13 November 2026): PUBLICLY ADVERTISED by the institution's library;
individual access UNVERIFIED.** A subscription statement is not access.

| Field | Entry |
|---|---|
| Date checked | |
| Access route | |
| Search interface accessible? | |
| Test query executed? (query and count) | |
| Export successful? (number of records) | |
| Export format | |
| Persistent identifiers present | |
| Other bibliographic identifiers present | |
| Export restrictions / record limits | |
| Evidence location | |
| Failure type, if any (§4) | |
| **Outcome** | ☐ verified ☐ unavailable ☐ partially accessible ☐ not tested |
| Notes | |

### 5.3 Web of Science

**Carried-forward status (13 November 2026): PUBLICLY ADVERTISED by the institution's library;
individual access UNVERIFIED.**

**Additional field required.** Web of Science coverage depends on which editions and year ranges
are subscribed. **Without these the search is not reproducible**, so they are recorded here even if
Web of Science is not ultimately used.

| Field | Entry |
|---|---|
| Date checked | |
| Access route | |
| Search interface accessible? | |
| **Editions subscribed** (from the collection selector) | |
| **Year ranges covered** | |
| Test query executed? (query and count) | |
| Export successful? (number of records) | |
| Export format | |
| Persistent identifiers present | |
| Other bibliographic identifiers present | |
| Export restrictions / record limits | |
| Evidence location | |
| Failure type, if any (§4) | |
| **Outcome** | ☐ verified ☐ unavailable ☐ partially accessible ☐ not tested |
| Notes | |

### 5.4 IndMED

**Carried-forward status (13 November 2026): UNTESTED.** No attempt has been made to reach it, and
its continued maintenance and public searchability are unverified. It is free, so the question is
reachability rather than subscription.

| Field | Entry |
|---|---|
| Date checked | |
| Access route (URL and interface) | |
| Search interface accessible? | |
| Test query executed? (query and count) | |
| Export successful? (number of records) | |
| Export format | |
| Persistent identifiers present | |
| Other bibliographic identifiers present | |
| Export restrictions / record limits | |
| Evidence location | |
| Failure type, if any (§4) | |
| **Outcome** | ☐ verified ☐ unavailable ☐ partially accessible ☐ not tested |
| Notes | |

**If IndMED is unreachable**, the South Asian regional gap does not disappear with it. D022 and the
P007 memorandum require it to be addressed by documented hand-searching of named journals over a
stated date range, or declared as a coverage limitation with its likely direction of effect.

### 5.5 PubMed — existing evidence only

**Carried-forward status: VERIFIED. No new search is to be executed for this record.**

| Field | Entry |
|---|---|
| Date checked | On or after 25 October 2026 (bounded by index dates; exact execution date unrecorded — see P009) |
| Access route | Free; no institutional subscription required |
| Search interface accessible? | **Yes** — demonstrated by an executed search |
| Test query executed? | **Not applicable.** A full search was executed and registered as `pubmed_v1r` |
| Export successful? | **Yes — 194 records** |
| Export format | PubMed/MEDLINE `.nbib` |
| Persistent identifiers present | **PMID on all 194**; DOI present on a subset |
| Other bibliographic identifiers present | Title, authors, year, journal, abstract, MeSH terms (on 152 of 194), Entrez dates |
| Export restrictions / record limits | None encountered at this volume |
| Evidence location | `data/raw/pubmed/pubmed-v1r-reexecution-194.nbib`; SHA-256 `1d153fa8…27e4ca1e` in `data/raw/SHA256SUMS`; registry entry `pubmed_v1r` in `config/sources.yaml` |
| Failure type, if any | None |
| **Outcome** | ☑ **verified** |
| Notes | This is the only executed and registered search in the project. The corrected no-design-block strategy (D023) has **not** been executed against PubMed or anything else |

---

## 6. Follow-up routes: library, consortium, reciprocal access

To be used where §5 records an **unavailable** or **partially accessible** outcome. Record each
request and its reply, with dates — an unanswered request is itself a documented finding.

**A single message to the library covers most of it.** Four questions, phrased to avoid the
full-text confusion in §2:

1. Do we have access to **Embase** (the bibliographic database published by Elsevier — not Elsevier
   journal content, and not ONOS) by any route, including consortium access?
2. Which **Web of Science editions and year ranges** does our subscription cover?
3. Is **off-campus remote access** available to me for Scopus and Web of Science, and how do I
   authenticate?
4. Are there **export limits** on any of these — a maximum number of records per export, or any
   restriction on bulk download?

| # | Route | Who to contact | Date requested | Date replied | Outcome |
|---|---|---|---|---|---|
| 1 | Institutional library (the four questions above) | | | | |
| 2 | Consortium route (e-ShodhSindhu or equivalent) | | | | |
| 3 | Reciprocal access at a medical institution (regional medical college, ICMR centre, dental college) | | | | |
| 4 | Paid single-session or short-term access | | | | |
| 5 | Supervisor or department — existing departmental subscription | | | | |

**On route 3.** A single supervised session is often enough to execute one search and export the
results. The export is what this project needs; the subscription itself is not. If that route is
used, the session date, institution and interface must be recorded, and the export registered under
D011 like any other.

---

## 7. What this record does not do

- It does **not** resolve **P007**, which remains **OPEN**.
- It does **not** authorise any formal search to be executed.
- It does **not** modify the decision register, **D023**, **D010**, any protocol document, any
  search record, or any screening or extraction data.
- It does **not** claim access to any database. Every status in §5 is either blank or carried
  forward with its evidence class named.
- It records **no** search date, yield or record count other than those already established for
  `pubmed_v1r`.

**After this record is complete**, the remaining steps before a formal search are: decide and record
the final database coverage (closing P007); write a strategy document per accessible database,
translating the adopted no-design-block query (D023) into each platform's syntax; measure a
screening rate on a prespecified sample, as D023 requires; and review the deduplication matching
rules against multi-database input, which has never been exercised — the single executed search
produced zero duplicates.

---

## Sources for the carried-forward statuses in §5

The institutional statuses were established on 12 November 2026 by reading publicly available
library pages, read-only and **without signing in**:

- [NITR Library — Databases](https://library.nitrkl.ac.in/index.php/resources/electronic-resources/databases)
- [NITR Library — Home](https://library.nitrkl.ac.in/)
- [NIT Rourkela Shibboleth Identity Provider](https://idp.nitrkl.ac.in/) — noted as the remote-access
  route; not used.

The PubMed status derives from the repository itself: `config/sources.yaml`, the registered export,
and `data/raw/SHA256SUMS`.
