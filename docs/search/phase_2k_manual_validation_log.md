# Phase 2K — manual validation log

**Created 14 November 2026.** A record to be completed **in each live database interface** by the
person performing validation.

> ## NO LIVE DATABASE WAS ACCESSED IN CREATING THIS LOG
>
> No query was executed, no interface opened, no account signed into, no export attempted, and no
> controlled-vocabulary heading looked up. Every per-database record below is **NOT TESTED** except
> where it records evidence that already exists in the repository.
>
> **The PubMed counts-only interrogation of 12 November 2026 is not evidence of a formal search and
> not evidence of a successful export.** It is recorded as what it was: a count read back from a
> query, with no record retrieved.

| Constraint | State at creation |
|---|---|
| Formal searches executed | **None** |
| Registered under D011 | **Nothing from any strategy in this log** |
| P007 | **OPEN** — no access beyond PubMed verified |
| D023 | Adopted; no design block in any query |
| Registered raw export | Untouched |

---

## 1. Permitted statuses

Use **only** these five. No other word is valid in a status field.

| Status | Meaning |
|---|---|
| `NOT TESTED` | No interaction attempted. The default |
| `ACCESS BLOCKED` | Interface unreachable, authentication failed, or no subscription. **Classify which** — see `p007_access_verification_record.md` §4 |
| `SYNTAX FAILED` | Query reached the database and was rejected, or a line demonstrably did not behave as intended |
| `SYNTAX VERIFIED` | Query executed and every line behaved as intended. **Does not imply an export was tested** |
| `EXPORT VERIFIED` | Syntax verified **and** at least one record exported successfully, with format and identifiers inspected |

`SYNTAX VERIFIED` and `EXPORT VERIFIED` are cumulative: a database is only ready for formal
searching at `EXPORT VERIFIED`, because the pipeline requires a preserved, checksummed export
(D011).

---

## 2. Static checks already completed — repository text only

These required no database. They were performed on 14 November 2026 against the repository's own
query text and are reproducible by anyone with the repository.

| # | Static check | Result |
|---|---|---|
| 1 | All five query blocks present in `database_search_strategies.md` | **PASS** — PubMed 47 lines, Embase 44, Scopus 27, Web of Science 27, IndMED 12 |
| 2 | PubMed block byte-identical to the adopted D023 query | **PASS** — SHA-256 of both blocks `c73bda8aa53de673be97ceee9e84096d…` |
| 3 | No study-design block in any query | **PASS** — 0 occurrences of design terms across all five blocks |
| 4 | Parenthesis balance | **PASS** — all five balanced |
| 5 | Quote pairing | **PASS** — double and single quotes paired in all five |
| 6 | Exactly one top-level `AND` joining two concept blocks | **PASS** — PubMed, Embase, Scopus, Web of Science each have exactly 1 |
| 7 | Term-set equivalence, PubMed vs Scopus and Web of Science | **PASS with 3 documented exceptions** — 80 of 83 PubMed free-text terms are matched verbatim or by a truncation stem. The 3 unmatched are `hand-rolled`, `roll-your-own`, `water-pipe`, all hyphen variants **deliberately dropped** with the spaced forms retained, as documented in §5 and §6 of the strategies file |
| 8 | v2 draft preserved as a historical record | **PASS** — supersession banner present, original 4,770 / 7,875 counts intact |

**What these static checks do not establish.** They test the query *as text*. They say nothing about
whether a heading exists, whether a field tag is accepted, whether a wildcard expands, or whether
any database can be reached. Every one of those requires the interface.

---

## 3. Unresolved `[VERIFY]` items and syntax assumptions

Carried forward from `database_search_strategies.md`. Each must be settled in the interface.

### Embase — controlled vocabulary, 5 headings

| Heading as drafted | Must confirm |
|---|---|
| `'mouth tumor'/exp` | Emtree **preferred term** and what `/exp` explodes over |
| `'tongue tumor'/exp` | As above |
| `'smoking'/exp` | As above |
| `'tobacco'/exp` | As above |
| `'tobacco use'/exp` | As above |

**A heading that does not exist returns zero and does not warn.** Run each `/exp` line alone and
record its count; a zero is the signal.

### Platform syntax assumptions

| # | Platform | Assumption | Risk if wrong |
|---|---|---|---|
| 1 | Embase | Single quotes delimit phrases; double quotes do not | Phrases silently split into `AND` of words |
| 2 | Embase | Hyphenated and spaced forms are equated, so `water-pipe`, `hand-rolled`, `roll-your-own` were dropped | Three terms lost |
| 3 | Embase | `:ti,ab,kw` accepted and includes author keywords | Field scope differs from assumption |
| 4 | Scopus | `"..."` is a **loose** phrase permitting wildcards; `{...}` is exact | — |
| 5 | **Scopus** | **A wildcard inside a quoted phrase works** — `"oral cancer*"` | **Most likely Scopus failure.** Fallback: expand to `"oral cancer" OR "oral cancers"` |
| 6 | Scopus | Hyphenated and spaced forms equated | Three terms lost |
| 7 | **Web of Science** | **A wildcard inside an exact phrase is accepted** | **Most likely WoS failure** — `TS=` phrase matching is stricter than Scopus. Same fallback |
| 8 | Web of Science | `smok*` and `cigar*` satisfy the minimum-characters-before-wildcard rule | Query rejected |
| 9 | Web of Science | `TS=` includes KeyWords Plus | Field scope differs |
| 10 | **IndMED** | **Boolean `AND` is supported at all** | Staged queries unusable; concepts must be run alone and intersected manually |
| 11 | IndMED | A single general search field exists | Field tags needed |
| 12 | IndMED | Truncation unknown — `*` **not used** | — |
| 13 | IndMED | Phrase search unknown; multi-word terms may split | Precision collapses |
| 14 | IndMED | A structured export exists | **Main risk.** Without persistent identifiers, deduplication degrades to title+author+year fingerprinting |

---

## 4. PubMed

| Field | Entry |
|---|---|
| Validation date | 2026-11-12 (counts-only, programmatic); 2026-11-14 (web interface, researcher, §4.1); 2026-11-14 (per-line counts-only, §4.3) |
| Person performing validation | 12 and 14 Nov per-line: automated tooling under the reviewer's direction. 14 Nov interface: the researcher |
| Access status | Accessible; free, no subscription required |
| Exact query tested | The adopted D023 query, `database_search_strategies.md` §3, verified byte-identical to `recommended_search_strategy.md` §2 |
| Query execution status | Accepted; HTTP 200; no errors or warnings *(counts-only interrogation, 2026-11-12)* |
| Database-reported result count | |
| Syntax warnings or errors | **One.** `"epidermoid carcinoma of the mouth"[tiab]` -> `QuotedPhraseNotFound`, 0 results. No warning on the other 87 lines (§4.2, §4.3) |
| Controlled-vocabulary heading verification | All five MeSH headings return a non-empty count (§4.3). **Explosion-tree contents NOT inspected and NOT verified** |
| Record export test | **NOT PERFORMED.** No record was retrieved or exported by the 2026-11-12 interrogation, the 2026-11-14 interface validation, or the 2026-11-14 per-line validation |
| Export format | |
| Persistent identifier availability | |
| Required correction | **One dead term identified** — see §12. **Not applied**: the adopted query is unchanged and a correction must be proposed separately for reviewer approval |
| **Final validation status** | **`SYNTAX VERIFIED`** — and no further. **Not** `EXPORT VERIFIED`, because no record has ever been exported from the adopted query |

> **Note on the 12 November 2026 interrogation.** It submitted the query and read back a count.
> **It retrieved no record, exported nothing, and produced no file.** It is therefore evidence of
> syntax acceptance only. The count it returned is recorded elsewhere as a counts-only
> interrogation figure and is **not** a search yield. PubMed cannot reach `EXPORT VERIFIED` until a
> record is actually exported and inspected.

**Separately** — the registered `pubmed_v1r` export (194 records, checksummed) proves that PubMed
export *works in general*. It does **not** validate the adopted D023 query, which has never been
executed as a formal search.

### 4.1 Exploratory interface validation — 14 November 2026, performed by the researcher

**Reported by the researcher. Not performed or witnessed by any automated tool, and recorded here as
reported.**

| Field | Entry |
|---|---|
| Date | 14 November 2026 |
| Person performing validation | The researcher |
| Interface | PubMed web interface |
| Query submitted | The adopted D023 query (`database_search_strategies.md` §3) |
| Filters | Cleared |
| **Interface-displayed result count** | **8,195** |
| Records displayed? | Yes — individual records were displayed in the results list |
| Export created? | **No** |
| Registered under D011? | **No** |
| Nature of the act | **Exploratory validation. Not a registered formal search** |

**What this establishes.** The adopted query is accepted by the PubMed web interface, executes
without error, and returns a non-empty result set whose records display. That is a meaningful
syntax confirmation in a second interface, independent of the 12 November programmatic run.

**What this does not establish.** It is **not** a formal search: no export was created, no checksum
exists, and there is no registry entry. The 8,195 figure is an **interface-displayed count on a
single date**, not a search yield, and it must never be reported as one. It says nothing about
sensitivity, precision or the eligibility of any displayed record. Records being *displayed* is not
records being *retrieved* in the sense D011 means.

**On 8,195 versus 8,190.** The 12 November counts-only interrogation returned 8,190; the 14 November
interface returned 8,195 — a difference of 5 records over two days. This is consistent with ordinary
database growth and requires no reconciliation. **Neither figure is a search yield**, and the pair
should not be presented as a measurement of change.

**Records observed on the first results page.** The researcher reports that the first displayed
records included oral-cavity and floor-of-mouth squamous cell carcinoma records.

> **This is an impression of a results page, and nothing follows from it.** It is recorded because
> it was observed, not because it demonstrates anything. Specifically, it is **not** evidence that
> the query is precise, that its top-ranked records are representative of the remaining ~8,190, or
> that any observed record is **eligible**. Eligibility is decided at full text against D008, D009
> and the open scope questions — never from a results list. PubMed's default ordering is not
> relevance to this review's criteria, so the first page is not a sample of anything.
>
> **No record was retrieved, recorded or carried forward**, and no screening decision arises from
> this observation.

### 4.2 Phrase-behaviour diagnostic — 14 November 2026, performed by the researcher

**Reported by the researcher.** A targeted test of one term in the adopted outcome block.

| Query line tested | Result | PubMed message |
|---|---|---|
| `"epidermoid carcinoma of the mouth"[tiab]` | **0 results** | PubMed reported that **the phrase was ignored** |
| `epidermoid carcinoma of the mouth[tiab]` | **28 results** | — |

**What this establishes.** The quoted form of this term is **not matched as a phrase by PubMed** and
contributes **nothing** to the adopted query. It is a dead term: it returns zero and, because it sits
inside an `OR` group, it fails silently without reducing the overall count. This is precisely the
failure mode the per-line validation exists to find, and it was found in the adopted query.

**What this does not establish.**

- The 28 results from the **unquoted** form are a **diagnostic observation only**. Removing the
  quotation marks changes what is being searched: PubMed then applies its own term handling to the
  unquoted string, which is **not** equivalent to exact-phrase matching. The 28 records are
  therefore **not** evidence that the phrase matches 28 articles.
- It is **not** evidence that any of those 28 records is eligible. Retrieval is not eligibility, and
  no record has been examined.
- It does **not** establish anything about the sensitivity or precision of the adopted query.

**Consequence, and what is NOT being done about it.** This is a defect in an **adopted** strategy
(D023). **The adopted query has not been modified, and must not be.** Any correction — removing the
dead term, replacing it with a form PubMed matches, or accepting it as inert — is a **change to an
adopted decision** and must be proposed separately for the reviewer's approval. It is recorded here
as a finding, not fixed. See §12.

### 4.3 Per-line counts-only validation — 14 November 2026

**Performed by automated tooling under the reviewer's direction**, via NCBI E-utilities `esearch.fcgi`, read-only, no sign-in, `retmax=0`.

| Item | Value |
|---|---|
| Date | 14 November 2026 |
| Method | HTTP POST to `esearch.fcgi`, `db=pubmed`, `retmax=0`, `retmode=xml` |
| Lines tested | **88 of 88** (every line of the adopted D023 query, tested individually) |
| **Records retrieved** | **0** |
| **Identifiers returned** | **0** across all 88 requests, verified by counting `<Id>` elements in every response |
| Export created | **None** |
| Registered under D011 | **No** |
| Transient failures | 3 requests returned HTTPError on the first pass (rate limiting) and **succeeded on retry**; all 88 lines have a recorded count |

**Result: exactly one line of 88 returns zero**, and it is the same line the researcher identified independently at §4.2:

| Line | Count | PubMed warning |
|---|---|---|
| `"epidermoid carcinoma of the mouth"[tiab]` | **0** | `QuotedPhraseNotFound`; `OutputMessage: No items found.` |

No other line carried any PubMed warning. **87 of 88 lines return a non-zero count.**

#### MeSH headings — counts only, NOT explosion verification

| Heading | Count returned |
|---|---|
| `"Mouth Neoplasms"[Mesh]` | 84,778 |
| `"Smoking"[Mesh]` | 171,066 |
| `"Tobacco Smoking"[Mesh]` | 7,970 |
| `"Cigarette Smoking"[Mesh]` | 5,136 |
| `"Tobacco Products"[Mesh]` | 15,710 |

> **A returned count is not verification of the explosion tree.** These five counts establish only that each heading is a recognised MeSH term that resolves to a non-empty set. **The contents of each heading's explosion tree have NOT been inspected**, and no claim is made about which descendant terms are included. Verifying that requires inspecting the MeSH tree itself in the MeSH Browser and documenting what it contains; that has not been done.

#### Ten lowest-count free-text lines

| Line | Count |
|---|---|
| `"epidermoid carcinoma of the mouth"[tiab]` | 0 |
| `narghila[tiab]` | 1 |
| `dhumti[tiab]` | 1 |
| `narguile[tiab]` | 6 |
| `chillum[tiab]` | 7 |
| `hukka[tiab]` | 10 |
| `shishas[tiab]` | 10 |
| `"gum cancer"[tiab]` | 14 |
| `nargile[tiab]` | 14 |
| `"clove cigarette"[tiab]` | 15 |

Low counts are **not** defects. The rare product terms (`narghila`, `dhumti`, `narguile`, `chillum`, `hukka`) are a deliberate free-text safety net sitting inside an `OR` group; a term contributing few records still contributes them. **No term is removed on the basis of a low count.**

#### What this validation does and does not establish

**Establishes.** Every line of the adopted query is syntactically accepted by PubMed; 87 of 88 resolve to a non-empty set; exactly one is a dead term, independently confirmed by two methods and two interfaces.

**Does not establish.** Nothing about **sensitivity**, **precision**, **recall** or the **eligibility** of any record. No record was retrieved or examined. A count is a property of a query on a date, not a measure of how well the query finds eligible studies. It does not verify MeSH explosion contents (above), and it is **not** a formal search: there is no export, no checksum and no registry entry.

---

## 5. Embase

| Field | Entry |
|---|---|
| Validation date | |
| Person performing validation | |
| Access status | Not listed among publicly advertised institutional databases; **availability unknown** |
| Exact query tested | |
| Query execution status | |
| Database-reported result count | |
| Syntax warnings or errors | |
| Controlled-vocabulary heading verification | *(record the confirmed preferred term and explosion for each of the five `/exp` headings in §3; note any substitution)* |
| Record export test | |
| Export format | |
| Persistent identifier availability | |
| Required correction | |
| **Final validation status** | **`NOT TESTED`** |

---

## 6. Scopus

| Field | Entry |
|---|---|
| Validation date | |
| Person performing validation | |
| Access status | Publicly advertised by the institution; **individual access unverified** |
| Exact query tested | |
| Query execution status | |
| Database-reported result count | |
| Syntax warnings or errors | *(record specifically whether `"oral cancer*"` — a wildcard inside a quoted phrase — was accepted)* |
| Controlled-vocabulary heading verification | **N/A — Scopus has no thesaurus.** Record this as a coverage limitation of the database |
| Record export test | |
| Export format | |
| Persistent identifier availability | *(DOI, PMID, Scopus EID)* |
| Required correction | |
| **Final validation status** | **`NOT TESTED`** |

---

## 7. Web of Science Core Collection

| Field | Entry |
|---|---|
| Validation date | |
| Person performing validation | |
| Access status | Publicly advertised by the institution; **individual access unverified** |
| Exact query tested | |
| Query execution status | |
| Database-reported result count | |
| Syntax warnings or errors | *(record specifically whether a wildcard inside an exact phrase was accepted, and whether `smok*` / `cigar*` met the minimum-characters rule)* |
| Controlled-vocabulary heading verification | **N/A — no thesaurus.** Record as a coverage limitation |
| **Editions subscribed** | *(required for reproducibility)* |
| **Year ranges covered** | *(required for reproducibility)* |
| Record export test | |
| Export format | |
| Persistent identifier availability | *(DOI, UT accession)* |
| Required correction | |
| **Final validation status** | **`NOT TESTED`** |

---

## 8. IndMED

| Field | Entry |
|---|---|
| Validation date | |
| Person performing validation | |
| Access status | **Reachability untested.** Free; the question is reachability, not subscription |
| Exact query tested | *(record which of the 12 staged queries were run, verbatim)* |
| Query execution status | |
| Database-reported result count | *(per staged query)* |
| Syntax warnings or errors | *(record first whether Boolean `AND` is supported at all)* |
| Controlled-vocabulary heading verification | *(record whether any controlled vocabulary exists)* |
| Record export test | |
| Export format | ☐ none ☐ structured ☐ copy-paste only |
| Persistent identifier availability | |
| Required correction | *(including whether manual intersection of concepts was necessary)* |
| **Final validation status** | **`NOT TESTED`** |

**If `ACCESS BLOCKED`:** the regional gap does not disappear. D022 requires documented
hand-searching of named journals over a stated date range, or an explicit coverage limitation with
its likely direction of effect.

---

## 9. Summary of validation status at creation

| Database | Status | Basis |
|---|---|---|
| **PubMed** | **`SYNTAX VERIFIED`** | 88/88 lines tested counts-only (2026-11-14) plus web-interface validation by the researcher (2026-11-14). **1 dead term found.** Export never tested against the adopted query |
| **Embase** | **`NOT TESTED`** | No access; 5 Emtree headings unconfirmed |
| **Scopus** | **`NOT TESTED`** | Access unverified |
| **Web of Science** | **`NOT TESTED`** | Access unverified |
| **IndMED** | **`NOT TESTED`** | Reachability untested |

**No database has reached `EXPORT VERIFIED`.** None is therefore ready for a formal search under
D011, PubMed included.

---

## 10. Order of work, and why

1. **~~PubMed export test~~ — WITHDRAWN as a distinct task (corrected 14 November 2026).**
   The earlier wording here invited a conflation and is corrected rather than deleted.

   **An export test is not the same act as executing the formal search, and for PubMed there is no
   useful export test left to run.** Two separate points:

   - **The export mechanism is already established.** The registered `pubmed_v1r` export — 194
     records, PubMed/MEDLINE `.nbib`, 958,710 bytes, PMID on 194/194, DOI on 185/194, title,
     abstract, journal and year on 194/194, checksum `1d153fa8…` — demonstrates that PubMed exports
     parse into the pipeline and carry persistent identifiers. **Nothing further needs testing about
     the mechanism.**
   - **What is unvalidated is the adopted D023 query, and running that query to export its results
     *is* the formal search of record** — not a test of it. Exporting only part of its results would
     be worse than not running it: it would produce an incomplete export against the query of
     record, which D011 cannot honestly register.

   The earlier phrase "exporting even a small result set" is therefore withdrawn. The formal PubMed
   search remains blocked on P007, on D023's screening-rate condition, and on separate authorisation
   to register a D011 entry.
2. **Embase access enquiry**, because it has the longest lead time and is the only one not
   publicly listed.
3. **Scopus and Web of Science**, both advertised, both likely quick confirmations.
4. **IndMED reachability**, which is a yes/no question before any syntax matters.

---

## 11. What this log does not do

- It does **not** record any live database interaction, because none occurred.
- It does **not** treat the 12 November counts-only interrogation as a formal search or a
  successful export.
- It does **not** invent a result count, a login, an export result, a MeSH or Emtree mapping, or
  any platform behaviour.
- It does **not** execute or register a formal search, retrieve or modify the registered raw export,
  or alter screening data, extraction data, decision-register entries or protocol decisions.
- It does **not** close **P007**, which remains open.

---

## 12. Proposed correction arising from validation — NOT APPLIED

**One defect was found in an adopted strategy. It is recorded, not fixed.**

| Item | Detail |
|---|---|
| Affected line | `"epidermoid carcinoma of the mouth"[tiab]` |
| Located in | The outcome block of the adopted D023 query |
| Behaviour | Returns **0 results**; PubMed reports `QuotedPhraseNotFound` |
| Effect on the query | **None on the total.** The line sits inside an `OR` group, so it contributes nothing and reduces nothing. It is **inert, not harmful** |
| Independently confirmed | Yes — by the researcher in the web interface (§4.2) and by per-line counts-only validation (§4.3) |
| Status | **NOT CORRECTED.** D023 is an adopted decision; the query is unchanged |

**Why no correction was made.** Changing the adopted query is a change to an adopted decision
(D023) and requires the reviewer's approval. Silently editing it — even to remove a term that
demonstrably does nothing — would be exactly the kind of unrecorded change the project's provenance
rules exist to prevent.

**Options, for a separate proposal.** None is recommended here; all three are defensible:

1. **Remove the line.** It contributes nothing. Minimal change, and the retrieved set is unaffected.
2. **Replace it with a form PubMed matches.** The unquoted variant returned 28 records, but **that
   is a diagnostic observation only** — removing the quotation marks changes what is searched, and
   is not equivalent to exact-phrase matching. Any replacement would need its own validation, and no
   claim is made that those 28 records are eligible or even relevant.
3. **Retain it as inert, and record why.** Documents that the term was considered and found
   unmatched, which has its own value in a search record.

**Until a decision is made, the adopted query stands as adopted**, with this defect documented.

---

## 13. PC-1 — correction to the adopted PubMed query — **APPROVED AND APPLIED**

> **APPROVED by the reviewer on 14 November 2026 and applied the same day, recorded in the
> decision register as D024.** The dead term `"epidermoid carcinoma of the mouth"[tiab]` has
> been removed from the operative PubMed strategy; `"oral epidermoid carcinoma"[tiab]` is
> retained; the unquoted variant was **not** adopted. **This is a correction to the proposed
> strategy, not authorisation to execute a formal search** — no search has been executed and
> the corrected query has never been run in full. The proposal text below is retained as the
> record of what was approved.

**PROPOSED, NOT APPLIED.** Requires the reviewer's explicit authorisation, because it amends a query
fixed by an adopted decision (D023).

### 13.1 Recommendation

**Remove the line `OR "oral epidermoid carcinoma"[tiab] OR "epidermoid carcinoma of the mouth"[tiab]`
in part — specifically, delete the dead term `"epidermoid carcinoma of the mouth"[tiab]` and retain
`"oral epidermoid carcinoma"[tiab]`.**

Option 1 of §12 (remove) is recommended over option 2 (replace) and option 3 (retain as inert).

### 13.2 Exact change

**Current line 24 of the outcome block (adopted):**

```
  OR "oral epidermoid carcinoma"[tiab] OR "epidermoid carcinoma of the mouth"[tiab]
```

**Proposed replacement:**

```
  OR "oral epidermoid carcinoma"[tiab]
```

Nothing else in the query changes. The outcome block drops from 44 to 43 terms; the exposure block
is untouched; no design block is introduced; no filter is added.

**`"oral epidermoid carcinoma"[tiab]` is retained and is not a dead term** — it returned a non-zero
count in the per-line validation (§4.3). Only the second phrase on that line is removed.

### 13.3 Why removal rather than replacement

| Option | Assessment |
|---|---|
| **1. Remove** *(recommended)* | The term returns 0 and contributes nothing. Removing it changes the retrieved set by **zero records** and removes a line that fails silently. The query becomes an accurate statement of what is actually searched |
| 2. Replace with the unquoted form | The unquoted variant returned 28 records, but **that is a different search**, not a repair. PubMed applies its own term handling to an unquoted string, so this would **add a new, unvalidated term** to an adopted query and change the retrieved set by an unknown amount. It would need its own validation, and **no claim exists that those 28 records are relevant or eligible** |
| 3. Retain as inert | Defensible, and it documents that the term was considered. But it leaves a line in the search of record that a reader would reasonably assume contributes something, and PRISMA-S expects the strategy as run to be reported accurately |

### 13.4 Effect of the change

| Property | Effect |
|---|---|
| Records retrieved | **None.** The term matches zero records, so the retrieved set is identical before and after |
| Sensitivity | **Unchanged.** Removing a term that matches nothing cannot reduce what is found |
| Precision | **Unchanged** |
| Scope, eligibility criteria, research question | **Unchanged** |
| D023's substance — no design block | **Unchanged** |
| Reproducibility | **Improved.** The reported strategy matches what the database actually executes |

**This correction is cosmetic in effect and substantive in provenance.** It alters no result; it
makes the recorded query honest.

### 13.5 What must accompany the change, if authorised

1. **A dated amendment note in the decision register under D023**, recording that the query was
   amended after adoption, why, and that the retrieved set is unaffected. D023 itself is **not**
   superseded — its decision (no design block) is untouched.
2. **The same edit in both places the query appears**, which must remain byte-identical:
   `docs/methods/recommended_search_strategy.md` §2 and
   `docs/search/database_search_strategies.md` §3.
3. **Corresponding removal from the Embase, Scopus and Web of Science translations**, where the
   same phrase appears. Those are untested drafts, so no validation is invalidated — but the term
   sets must stay aligned.
4. **Re-run the per-line counts-only validation** on the amended PubMed query to confirm 0 dead
   terms remain.
5. **A record in the manuscript's search section** that the strategy was amended before execution,
   with the date and reason. An amendment before any formal search is clean; the same amendment
   after execution would require re-running the search.

**Timing matters.** This should be decided **before** the formal search is executed. Amending an
executed query means the export no longer corresponds to the recorded strategy.

### 13.6 Decision required

| | |
|---|---|
| **Authorise PC-1** | Apply §13.2 in both locations plus the three translations, add the D023 amendment note, re-validate, and record the amendment |
| **Reject PC-1** | The adopted query stands unchanged with the defect documented at §12. Record the decision to retain |
| **Defer** | Permissible only until the formal search is executed |

