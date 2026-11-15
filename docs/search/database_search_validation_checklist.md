# Database search strategy — validation checklist

**Companion to `docs/search/database_search_strategies.md`.** One checklist per database, to be
completed **in the live interface** before any formal search is executed.

**Status: all checklists blank except PubMed's syntax row, which records a counts-only
interrogation already performed.** Created 13 November 2026.

> **A strategy is not validated until it has been run in the actual database interface.** Nothing in
> the strategies document is empirically validated. Drafting a query and checking it parses are
> different acts, and both differ from executing a search.

| Constraint | State |
|---|---|
| Formal searches executed | **None** |
| P007 | **OPEN** — no access beyond PubMed verified |
| D011 registrations | **None** |
| Record counts | **None invented.** Count fields below are blank by design |
| Study-design block | **Absent from every strategy (D023)** |

---

## 1. How to use this checklist

Validation is **not** the same as searching, and the distinction must be preserved in what you
record:

| Act | What it produces | Registered under D011? |
|---|---|---|
| **Syntax validation** | Confirmation that the query parses and each line behaves as intended. May return a count | **No.** A count read back is not a yield |
| **Counts-only interrogation** | A number, recorded with its date and platform | **No** |
| **Formal search execution** | A retrieved, exported, counted and checksummed record set | **Yes** — this is the search of record |

Complete every row. **A failed check is a finding**: record what failed, classify it
(`docs/methods/p007_access_verification_record.md` §4 distinguishes technical, authentication,
subscription and export failures), and record the date. Do not leave a row blank to mean "no".

**Validate line by line, not just as a whole.** A compound query that returns results may still
contain a line contributing nothing — a misspelled controlled-vocabulary heading returns zero and
fails silently. Run each block alone, then each suspect line alone.

---

## 2. Checklist items, and what each is testing

| # | Item | What a pass means |
|---|---|---|
| 1 | **Syntax validity** | The query is accepted and executes without error |
| 2 | **Controlled vocabulary validity** | Every thesaurus heading exists as a **preferred term**, and its explosion covers what was intended. A heading that does not exist returns zero and does not warn |
| 3 | **Field-tag validity** | Each field tag is accepted and searches the fields expected. Field scope differs by platform — see the strategies document §2 |
| 4 | **Boolean grouping** | Parentheses bind as intended: the two blocks are joined by one `AND`, and every `OR` stays inside its own block. **The commonest catastrophic error is an `OR` escaping its group** |
| 5 | **Phrase-search behaviour** | Multi-word terms search as phrases, not as `AND` of their words. Quoting conventions differ by platform |
| 6 | **Truncation behaviour** | Wildcards expand as intended, are not silently ignored, and do not breach a variant cap |
| 7 | **Language and date restrictions** | **Confirmed ABSENT.** Language and species are handled at screening with a recorded exclusion reason |
| 8 | **Filters absent** | No publication-type, document-type, species or subject filter applied |
| 9 | **Study-design block absent** | No design term, design filter or methodology filter present — **required by D023** |

---

## 3. PubMed

**Date validated:** 2026-11-12 (syntax, counts-only). **Validated by:** scripted counts-only
interrogation via NCBI E-utilities, read-only, no sign-in. **Formal search: NOT executed.**

| # | Item | Status | Evidence / note |
|---|---|---|---|
| 1 | Syntax validity | **PASS** | Query accepted; HTTP 200; no errors or warnings |
| 2 | Controlled vocabulary validity | **Partially verified** | `"Mouth Neoplasms"[Mesh]`, `"Smoking"[Mesh]`, `"Tobacco Smoking"[Mesh]`, `"Cigarette Smoking"[Mesh]`, `"Tobacco Products"[Mesh]` are valid MeSH. **Per-heading explosion contents not individually confirmed** |
| 3 | Field-tag validity | **PASS** | `[Mesh]` and `[tiab]` accepted |
| 4 | Boolean grouping | **PASS** | Two blocks, one `AND`; block counts were obtained separately and behaved as expected |
| 5 | Phrase-search behaviour | **Assumed, not line-tested** | Quoted phrases accepted. Not confirmed term by term |
| 6 | Truncation behaviour | **N/A** | No truncation used; plurals enumerated deliberately |
| 7 | Language / date restrictions | **PASS — absent** | No limits applied |
| 8 | Filters absent | **PASS** | None |
| 9 | Study-design block absent | **PASS** | No design terms present |

**Outstanding for PubMed:** per-line verification (items 2 and 5), then formal execution, export,
count, checksum and D011 registration. **Execution date to be recorded at execution.**

| Field | Entry |
|---|---|
| Date of formal execution | |
| Records retrieved | |
| Export format | |
| Export checksum (SHA-256) | |
| Registry entry id | |

---

## 4. Embase

**Access not verified (P007 open). Emtree headings require confirmation.**

| # | Item | Status | Evidence / note |
|---|---|---|---|
| 1 | Syntax validity | ☐ pass ☐ fail ☐ not tested | |
| 2 | Controlled vocabulary validity — **confirm each `/exp` heading in the Emtree browser** | ☐ pass ☐ fail ☐ not tested | Record the **preferred term** confirmed for each of `'mouth tumor'`, `'tongue tumor'`, `'smoking'`, `'tobacco'`, `'tobacco use'`, and any substitution made: |
| 3 | Field-tag validity — `:ti,ab,kw` | ☐ pass ☐ fail ☐ not tested | Note that this is **wider** than PubMed `[tiab]` |
| 4 | Boolean grouping | ☐ pass ☐ fail ☐ not tested | |
| 5 | Phrase-search behaviour — single quotes | ☐ pass ☐ fail ☐ not tested | Confirm double quotes are **not** required |
| 6 | Truncation behaviour | ☐ pass ☐ fail ☐ not tested | None used in the draft. If added, record the operator |
| 7 | Language / date restrictions absent | ☐ pass ☐ fail ☐ not tested | |
| 8 | Filters absent — **no `[embase]/lim`, no `[article]/lim`** | ☐ pass ☐ fail ☐ not tested | Conference abstracts are retained for screening |
| 9 | Study-design block absent | ☐ pass ☐ fail ☐ not tested | |

| Additional field | Entry |
|---|---|
| Date validated | |
| Interface / URL | |
| Hyphen handling confirmed? (`water-pipe` vs `water pipe`) | |
| Export format available | |
| Persistent identifiers in export | |
| Export record cap | |
| Lines returning zero (possible dead headings) | |
| Outcome | ☐ validated ☐ failed ☐ not tested |

---

## 5. Scopus

**Access publicly advertised, individually unverified (P007 open). No controlled vocabulary exists.**

| # | Item | Status | Evidence / note |
|---|---|---|---|
| 1 | Syntax validity | ☐ pass ☐ fail ☐ not tested | |
| 2 | Controlled vocabulary validity | **N/A — none exists** | Record as a coverage limitation of this database |
| 3 | Field-tag validity — `TITLE-ABS-KEY()` | ☐ pass ☐ fail ☐ not tested | Wider than PubMed `[tiab]` |
| 4 | Boolean grouping | ☐ pass ☐ fail ☐ not tested | |
| 5 | Phrase-search behaviour — `"..."` is a **loose** phrase; `{...}` is exact | ☐ pass ☐ fail ☐ not tested | |
| 6 | **Truncation behaviour — wildcard inside a quoted phrase** | ☐ pass ☐ fail ☐ not tested | **The most likely failure point.** Confirm `"oral cancer*"` behaves as intended. If refused, expand to `"oral cancer" OR "oral cancers"` and record the change |
| 7 | Language / date restrictions absent | ☐ pass ☐ fail ☐ not tested | |
| 8 | Filters absent — no document-type limit | ☐ pass ☐ fail ☐ not tested | |
| 9 | Study-design block absent | ☐ pass ☐ fail ☐ not tested | |

| Additional field | Entry |
|---|---|
| Date validated | |
| Interface / URL | |
| `smok*` and `cigar*` accepted? | |
| Export format available | |
| Persistent identifiers in export (DOI, PMID, EID) | |
| Export record cap | |
| Query as actually run, if amended | |
| Outcome | ☐ validated ☐ failed ☐ not tested |

---

## 6. Web of Science Core Collection

**Access publicly advertised, individually unverified (P007 open). No controlled vocabulary exists.**

| # | Item | Status | Evidence / note |
|---|---|---|---|
| 1 | Syntax validity | ☐ pass ☐ fail ☐ not tested | |
| 2 | Controlled vocabulary validity | **N/A — none exists** | Record as a coverage limitation |
| 3 | Field-tag validity — `TS=()` | ☐ pass ☐ fail ☐ not tested | Includes **KeyWords Plus**; the widest field of the four platforms |
| 4 | Boolean grouping | ☐ pass ☐ fail ☐ not tested | |
| 5 | **Phrase-search behaviour — `"..."` is an exact phrase, stricter than Scopus** | ☐ pass ☐ fail ☐ not tested | |
| 6 | **Truncation behaviour — wildcard inside an exact phrase may be refused** | ☐ pass ☐ fail ☐ not tested | **The most likely failure point for this platform.** If `"oral cancer*"` is rejected, expand plurals and record the change. Also confirm the minimum-characters-before-wildcard rule |
| 7 | Language / date restrictions absent | ☐ pass ☐ fail ☐ not tested | Note separately that the **subscribed** year range may restrict coverage regardless |
| 8 | Filters absent | ☐ pass ☐ fail ☐ not tested | |
| 9 | Study-design block absent | ☐ pass ☐ fail ☐ not tested | |

| Additional field | Entry |
|---|---|
| Date validated | |
| Interface / URL | |
| **Editions subscribed** (required for reproducibility) | |
| **Year ranges covered** | |
| Export format available | |
| Persistent identifiers in export (DOI, UT) | |
| Export record cap | |
| Query as actually run, if amended | |
| Outcome | ☐ validated ☐ failed ☐ not tested |

---

## 7. IndMED

**Reachability untested. Query language undocumented in this repository — assume nothing.**

| # | Item | Status | Evidence / note |
|---|---|---|---|
| 1 | Syntax validity | ☐ pass ☐ fail ☐ not tested | Test whether a compound query is accepted at all |
| 2 | Controlled vocabulary validity | ☐ pass ☐ fail ☐ not tested ☐ **none exists** | Record which, if any |
| 3 | Field-tag validity | ☐ pass ☐ fail ☐ not tested ☐ **no field tags** | Assume a single general field unless shown otherwise |
| 4 | **Boolean grouping — is `AND` supported at all?** | ☐ pass ☐ fail ☐ not tested | If not, run concepts separately and intersect manually, and **record that this was necessary** |
| 5 | Phrase-search behaviour | ☐ pass ☐ fail ☐ not tested | Multi-word terms may be treated as `AND` of their words |
| 6 | Truncation behaviour | ☐ pass ☐ fail ☐ not tested | **Do not use `*` until confirmed** |
| 7 | Language / date restrictions absent | ☐ pass ☐ fail ☐ not tested | |
| 8 | Filters absent | ☐ pass ☐ fail ☐ not tested | |
| 9 | Study-design block absent | ☐ pass ☐ fail ☐ not tested | The staged queries contain no design term |

| Additional field | Entry |
|---|---|
| Date attempted | |
| Interface / URL | |
| Reachable? | ☐ yes ☐ no ☐ intermittent |
| Which of the 12 staged queries ran | |
| Manual intersection required? | |
| Export format available | ☐ none ☐ structured ☐ copy-paste only |
| Persistent identifiers in export | |
| Outcome | ☐ validated ☐ unreachable ☐ partially usable ☐ not tested |

**If unreachable:** record the attempt and date. The regional gap must then be addressed by
documented hand-searching of named journals over a stated date range, or declared as a coverage
limitation with its likely direction of effect (D022).

---

## 8. Cross-database checks, after individual validation

To be completed once more than one database validates. These test the **set**, not any single
strategy.

| # | Check | Status | Note |
|---|---|---|---|
| 1 | Every validated strategy contains the same two concepts and **no third block** | ☐ | Design-block absence is required by D023 |
| 2 | Field-scope differences recorded per database | ☐ | `[tiab]` vs `:ti,ab,kw` vs `TITLE-ABS-KEY` vs `TS=` are **not** equivalent |
| 3 | Any term dropped or amended per platform is recorded, with the reason | ☐ | Expanded plurals, dropped hyphen variants, substituted headings |
| 4 | Export formats are all parseable by the pipeline | ☐ | NBIB and RIS; anything else needs a parser |
| 5 | Persistent-identifier availability recorded per database | ☐ | Deduplication matches DOI → PMID → title+author+year fingerprint. A source without identifiers degrades to fingerprinting |
| 6 | **Deduplication matching rules reviewed for multi-database input** | ☐ | Exercised only on one source, which produced 0 duplicates. Cross-database input will produce real duplicates and records lacking PMIDs |
| 7 | One strategy document per database, as D011 requires | ☐ | With platform, interface, query as run, date, filters, count, export format and checksum |
| 8 | Screening-rate measurement completed | ☐ | Required by D023 before formal execution: 200 records, start and end times recorded |

---

## 9. What this checklist does not do

- It does **not** validate anything by existing. Every row except PubMed's syntax block is blank.
- It does **not** resolve **P007** or claim access to any database.
- It does **not** authorise a formal search. D023's screening-rate condition and P007's resolution
  both precede execution.
- It records **no** record count, and none is invented. Count fields are for entry at execution.
- It does **not** register anything under **D011**.
