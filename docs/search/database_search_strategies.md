# Database-specific search strategies

**Status: DRAFTED. None of these strategies has been executed as a formal search.**

Prepared 13 November 2026, translating the primary strategy adopted under **D023 (2026-11-13)** —
which carries **no study-design block** — into the syntax of each candidate database.

| Constraint | State |
|---|---|
| D023 | Adopted; no design block in any strategy below |
| Formal searches executed | **None.** PubMed's corrected query is adopted but unexecuted |
| 8,190 / 5,008 | Counts-only interrogation figures (2026-11-12), **not search yields** |
| P007 | **OPEN.** No database access beyond PubMed is verified |
| Registered under D011 | **Nothing.** No strategy here has an export, checksum or registry entry |
| Research question, eligibility criteria, D023 | Unchanged |

**Verification status of each translation.** Only the PubMed query has had its syntax checked
against a live interface, and that was a counts-only interrogation, not a search. **Every other
strategy below is an untested draft.** Controlled-vocabulary headings for Embase in particular are
marked **[VERIFY]** where the preferred term must be confirmed in the thesaurus browser before use —
they are written from general knowledge of the platform, which is not a substitute for checking.

---

## 1. The concepts being translated

Two blocks, joined with `AND`, exactly as adopted:

| Block | Concept | Source |
|---|---|---|
| **A — Outcome** | Oral-cavity cancer, including named subsites and SCC terminology | `docs/methods/recommended_search_strategy.md` §2 |
| **B — Exposure** | Smoked / combusted tobacco, including bidi, cheroot, waterpipe and reverse smoking | same |

**No third block.** The design block is omitted under D023 and is not reintroduced in any
translation below.

**Two deliberate properties carried into every translation**, so they are not mistaken for errors:

1. **Bare anatomical terms** (`buccal mucosa`, `floor of mouth`, `hard palate`, `oral tongue`,
   `retromolar`, `alveolar ridge`) carry no neoplasm qualifier and will retrieve non-neoplastic
   studies — buccal cytology and micronucleus work in smokers, for example. These are excluded at
   screening, not at retrieval.
2. **Generic tobacco terms** (`tobacco`, `tobacco use`, `tobacco habit`, `tobacco consumption`, and
   the product-class headings) will retrieve smokeless-tobacco and betel-quid studies. No
   smokeless-specific term appears in any exposure block. Smokeless tobacco is a confounder, not an
   eligible exposure, and such records are excluded at screening. **Retrieval is not eligibility.**

---

## 2. What does not translate cleanly

These are the differences that make a cross-platform query impossible to paste, and they must be
reported in the manuscript's search section rather than smoothed over.

| Issue | Consequence |
|---|---|
| **Field scope is not equivalent.** PubMed `[tiab]` = title + abstract. Embase `:ti,ab,kw` adds **author keywords**. Scopus `TITLE-ABS-KEY` adds **indexed and author keywords**. Web of Science `TS=` adds author keywords **and KeyWords Plus**, which are algorithmically generated from cited references | The same free-text term searches a **wider** field in Embase, Scopus and Web of Science than in PubMed. Retrieval differences between platforms are therefore partly an artefact of field scope, not of coverage |
| **Scopus and Web of Science have no controlled vocabulary at all** | The `"Mouth Neoplasms"[Mesh]` and `"Smoking"[Mesh]` arms have **no equivalent**. Those platforms rely entirely on free text, so a paper that an indexer tagged but whose title and abstract use unusual phrasing is reachable in PubMed and Embase and **unreachable** in Scopus and Web of Science. This is a real and unquantified sensitivity difference |
| **MeSH explosion has no exact Emtree counterpart** | `Mouth Neoplasms`[Mesh] explodes over lip, gingival, palatal, tongue and salivary-gland subtrees. Emtree's hierarchy under the corresponding heading is **not identical**, so `/exp` does not reproduce the same set. The subsite free-text terms partly compensate |
| **Truncation is unavailable in the PubMed strategy by design** | PubMed truncation disables automatic term mapping and is capped at 600 variants, so the adopted query **enumerates plurals** (`"oral cancer"` OR `"oral cancers"`). Scopus and Web of Science support `*` cleanly, so their translations use it and are consequently shorter. **The term sets are intended to be equivalent; the syntax is not** |
| **Hyphen and punctuation handling differs** | `water-pipe`, `hand-rolled`, `roll-your-own` are treated differently across platforms. Each translation states its assumption, and each must be checked in the interface |
| **IndMED's query language is not documented in this repository** | Its Boolean support, field tags and phrase behaviour are **unverified**. The strategy below is a simplified fallback, not a translation of equal power |
| **Conference abstracts** | Embase indexes them; PubMed largely does not. They are **retained for screening** and excluded under `conference_abstract` where detail is insufficient — not filtered at retrieval |

---

## 3. PubMed / MEDLINE — adopted

**Platform:** NCBI PubMed. **Vocabulary:** MeSH, auto-exploding. **Fields:** `[Mesh]`, `[tiab]`.
**Status:** adopted under D023; syntax checked by counts-only interrogation 2026-11-12; **not
executed as a formal search**.

### Copy-ready query

```
(
  "Mouth Neoplasms"[Mesh]
  OR "oral cancer"[tiab] OR "oral cancers"[tiab]
  OR "oral cavity cancer"[tiab] OR "oral cavity cancers"[tiab]
  OR "mouth cancer"[tiab] OR "mouth cancers"[tiab]
  OR "oral carcinoma"[tiab] OR "oral carcinomas"[tiab]
  OR "oral cavity carcinoma"[tiab]
  OR "oral neoplasm"[tiab] OR "oral neoplasms"[tiab]
  OR "mouth neoplasm"[tiab] OR "mouth neoplasms"[tiab]
  OR "oral cavity neoplasm"[tiab] OR "oral cavity neoplasms"[tiab]
  OR "oral malignancy"[tiab] OR "oral malignancies"[tiab]
  OR "oral squamous cell carcinoma"[tiab]
  OR "oral cavity squamous cell carcinoma"[tiab]
  OR "squamous cell carcinoma of the mouth"[tiab]
  OR OSCC[tiab]
  OR "oral epidermoid carcinoma"[tiab]
  OR "tongue cancer"[tiab] OR "tongue carcinoma"[tiab]
  OR "tongue neoplasm"[tiab] OR "tongue neoplasms"[tiab]
  OR "oral tongue"[tiab] OR "mobile tongue"[tiab]
  OR "buccal mucosa"[tiab] OR "buccal carcinoma"[tiab]
  OR "floor of mouth"[tiab]
  OR "gingival carcinoma"[tiab] OR "gingival cancer"[tiab] OR "gum cancer"[tiab]
  OR "hard palate"[tiab] OR "retromolar"[tiab] OR "alveolar ridge"[tiab]
)
AND
(
  "Smoking"[Mesh]
  OR "Tobacco Smoking"[Mesh]
  OR "Cigarette Smoking"[Mesh]
  OR "Tobacco Products"[Mesh]
  OR smoking[tiab] OR smoker[tiab] OR smokers[tiab] OR smoked[tiab]
  OR cigarette[tiab] OR cigarettes[tiab]
  OR tobacco[tiab] OR "tobacco smoke"[tiab] OR "tobacco use"[tiab]
  OR "tobacco habit"[tiab] OR "tobacco habits"[tiab]
  OR "smoking habit"[tiab] OR "smoking habits"[tiab]
  OR "tobacco consumption"[tiab]
  OR bidi[tiab] OR bidis[tiab] OR beedi[tiab] OR beedis[tiab]
  OR cigar[tiab] OR cigars[tiab] OR cheroot[tiab] OR cheroots[tiab]
  OR "pipe smoking"[tiab]
  OR waterpipe[tiab] OR "water pipe"[tiab] OR "water-pipe"[tiab]
  OR hookah[tiab] OR hukka[tiab] OR shisha[tiab] OR shishas[tiab]
  OR narghile[tiab] OR narghila[tiab] OR nargile[tiab] OR narguile[tiab] OR goza[tiab]
  OR kretek[tiab] OR "clove cigarette"[tiab]
  OR "reverse smoking"[tiab] OR chutta[tiab] OR dhumti[tiab] OR chillum[tiab]
  OR "hand-rolled"[tiab] OR "hand rolled"[tiab]
  OR "roll-your-own"[tiab] OR "roll your own"[tiab]
)
```

**Filters: none.** No language, species, date or publication-type restriction.

### Line-by-line

| Element | Function |
|---|---|
| `"Mouth Neoplasms"[Mesh]` | Indexed outcome arm. Auto-explodes over lip, gingival, palatal, tongue and salivary-gland subtrees. Reaches papers whose title and abstract use phrasing the free-text arm misses |
| `"oral cancer"` … `"oral malignancies"` | Generic outcome phrasing, with plurals enumerated because truncation would disable term mapping |
| `"oral squamous cell carcinoma"`, `OSCC`, epidermoid variants | Histology-specific phrasing. `OSCC` is the acronym the v1 query relied on; here it is one term among many rather than a requirement |
| `"tongue cancer"` … `"alveolar ridge"` | Named subsites, to reach papers that name the site in the title and the malignancy only in the abstract. Bare anatomical terms are deliberate — see §1 |
| `"Smoking"[Mesh]`, `"Tobacco Smoking"[Mesh]`, `"Cigarette Smoking"[Mesh]` | Indexed exposure arm, exploding over the smoking subtree |
| `"Tobacco Products"[Mesh]` | Reaches product-level indexing. Retrieves smokeless products too — excluded at screening |
| `smoking`, `smoker(s)`, `smoked`, `cigarette(s)`, `tobacco` | The primary free-text drivers. Most eligible studies say only "smoking" |
| `bidi` … `roll your own` | Product-specific safety net for records not yet MeSH-indexed — 21.6% of the existing export. **Not mandatory**: they sit in the same OR-group, never as a required term |
| `AND` between the blocks | The only conjunction. No third block |

---

## 4. Embase — DRAFT, requires Emtree verification

**Platform:** Elsevier embase.com. **Vocabulary:** **Emtree**, not MeSH. **Fields:** `:ti,ab,kw`.
**Status:** **untested draft. No Embase access is verified (P007 open).**

> **[VERIFY] Every Emtree heading below must be confirmed in the Emtree browser before use.**
> Emtree preferred terms and hierarchy differ from MeSH, and a heading that does not exist silently
> contributes nothing. Confirm the preferred term, check what `/exp` explodes over, and record what
> you confirmed.

### Copy-ready query

```
(
  'mouth tumor'/exp
  OR 'tongue tumor'/exp
  OR 'mouth cancer':ti,ab,kw OR 'oral cancer':ti,ab,kw OR 'oral cavity cancer':ti,ab,kw
  OR 'oral carcinoma':ti,ab,kw OR 'oral cavity carcinoma':ti,ab,kw
  OR 'oral neoplasm':ti,ab,kw OR 'mouth neoplasm':ti,ab,kw
  OR 'oral cavity neoplasm':ti,ab,kw
  OR 'oral malignancy':ti,ab,kw OR 'oral malignancies':ti,ab,kw
  OR 'oral squamous cell carcinoma':ti,ab,kw
  OR 'oral cavity squamous cell carcinoma':ti,ab,kw
  OR 'squamous cell carcinoma of the mouth':ti,ab,kw
  OR oscc:ti,ab,kw
  OR 'oral epidermoid carcinoma':ti,ab,kw
  OR 'epidermoid carcinoma of the mouth':ti,ab,kw
  OR 'tongue cancer':ti,ab,kw OR 'tongue carcinoma':ti,ab,kw OR 'tongue neoplasm':ti,ab,kw
  OR 'oral tongue':ti,ab,kw OR 'mobile tongue':ti,ab,kw
  OR 'buccal mucosa':ti,ab,kw OR 'buccal carcinoma':ti,ab,kw
  OR 'floor of mouth':ti,ab,kw
  OR 'gingival carcinoma':ti,ab,kw OR 'gingival cancer':ti,ab,kw OR 'gum cancer':ti,ab,kw
  OR 'hard palate':ti,ab,kw OR retromolar:ti,ab,kw OR 'alveolar ridge':ti,ab,kw
)
AND
(
  'smoking'/exp
  OR 'tobacco'/exp
  OR 'tobacco use'/exp
  OR smoking:ti,ab,kw OR smoker:ti,ab,kw OR smokers:ti,ab,kw OR smoked:ti,ab,kw
  OR cigarette:ti,ab,kw OR cigarettes:ti,ab,kw
  OR tobacco:ti,ab,kw OR 'tobacco smoke':ti,ab,kw OR 'tobacco use':ti,ab,kw
  OR 'tobacco habit':ti,ab,kw OR 'tobacco habits':ti,ab,kw
  OR 'smoking habit':ti,ab,kw OR 'smoking habits':ti,ab,kw
  OR 'tobacco consumption':ti,ab,kw
  OR bidi:ti,ab,kw OR bidis:ti,ab,kw OR beedi:ti,ab,kw OR beedis:ti,ab,kw
  OR cigar:ti,ab,kw OR cigars:ti,ab,kw OR cheroot:ti,ab,kw OR cheroots:ti,ab,kw
  OR 'pipe smoking':ti,ab,kw
  OR waterpipe:ti,ab,kw OR 'water pipe':ti,ab,kw
  OR hookah:ti,ab,kw OR hukka:ti,ab,kw OR shisha:ti,ab,kw OR shishas:ti,ab,kw
  OR narghile:ti,ab,kw OR narghila:ti,ab,kw OR nargile:ti,ab,kw OR narguile:ti,ab,kw
  OR goza:ti,ab,kw
  OR kretek:ti,ab,kw OR 'clove cigarette':ti,ab,kw
  OR 'reverse smoking':ti,ab,kw OR chutta:ti,ab,kw OR dhumti:ti,ab,kw OR chillum:ti,ab,kw
  OR 'hand rolled':ti,ab,kw
  OR 'roll your own':ti,ab,kw
)
```

**No filters.** Do **not** apply the `[embase]/lim` or `[article]/lim` limits: conference abstracts
are retained for screening.

### Notes and limitations

| Item | Note |
|---|---|
| `'mouth tumor'/exp`, `'tongue tumor'/exp` | **[VERIFY]** Candidate Emtree preferred terms for the outcome. Confirm the exact term and its explosion before running. If the preferred term differs, substitute it and record the substitution |
| `'smoking'/exp`, `'tobacco'/exp`, `'tobacco use'/exp` | **[VERIFY]** Candidate exposure headings. Emtree's smoking subtree does not map one-to-one onto MeSH's |
| `:ti,ab,kw` | **Wider than PubMed's `[tiab]`** — includes author keywords. A deliberate acceptance of wider retrieval, not an error |
| Hyphens | Embase generally treats `water-pipe` and `water pipe` alike, so the hyphenated variants are dropped and the spaced forms retained. **Verify in the interface**; if hyphens are significant, add `'water-pipe'`, `'hand-rolled'`, `'roll-your-own'` |
| `oscc` | Lower-cased; Embase search is case-insensitive |
| Quotation | Single quotes are the Embase phrase delimiter. Double quotes will not behave as expected |
| Conference abstracts | Indexed here and not in PubMed. Expect additional volume; retain and screen |
| Export | RIS. **Check the per-export record cap before running the full query** — this is the field most likely to constrain the workflow |

---

## 5. Scopus — DRAFT, requires interface verification

**Platform:** Elsevier Scopus. **Vocabulary:** **none — no thesaurus.** **Field:** `TITLE-ABS-KEY()`.
**Status:** **untested draft. Scopus access is publicly advertised but unverified (P007 open).**

> **No controlled vocabulary exists.** The MeSH and Emtree arms have no equivalent, so this
> translation is **entirely free text**. Truncation (`*`) is used to replace the enumerated plurals.

### Copy-ready query

```
TITLE-ABS-KEY(
  ( "oral cancer*" OR "oral cavity cancer*" OR "mouth cancer*"
    OR "oral carcinom*" OR "oral cavity carcinom*"
    OR "oral neoplas*" OR "mouth neoplas*" OR "oral cavity neoplas*"
    OR "oral malignan*"
    OR "oral squamous cell carcinom*" OR "oral cavity squamous cell carcinom*"
    OR "squamous cell carcinoma of the mouth"
    OR OSCC
    OR "oral epidermoid carcinom*" OR "epidermoid carcinoma of the mouth"
    OR "tongue cancer*" OR "tongue carcinom*" OR "tongue neoplas*"
    OR "oral tongue" OR "mobile tongue"
    OR "buccal mucosa" OR "buccal carcinom*"
    OR "floor of mouth"
    OR "gingival carcinom*" OR "gingival cancer*" OR "gum cancer*"
    OR "hard palate" OR retromolar OR "alveolar ridge" )
  AND
  ( smok* OR cigar* OR tobacco
    OR "tobacco smoke" OR "tobacco use" OR "tobacco habit*"
    OR "smoking habit*" OR "tobacco consumption"
    OR bidi OR bidis OR beedi OR beedis
    OR cheroot* OR "pipe smoking"
    OR waterpipe OR "water pipe" OR hookah OR hukka OR shisha* 
    OR narghile OR narghila OR nargile OR narguile OR goza
    OR kretek OR "clove cigarette*"
    OR "reverse smoking" OR chutta OR dhumti OR chillum
    OR "hand rolled" OR "roll your own" )
)
```

### Notes and limitations

| Item | Note |
|---|---|
| **No controlled vocabulary** | The single largest difference from PubMed and Embase. A paper reachable only through an indexer's tag is **unreachable here**. Report as a coverage limitation of this database, not of the review |
| `smok*` | Covers smoking, smoker, smokers, smoked, smoke. Replaces five enumerated terms |
| `cigar*` | Covers cigar, cigars, cigarette, cigarettes, cigarillo. **Deliberately broad**; the exposure block is permissive by design |
| `TITLE-ABS-KEY` | Searches title, abstract and keywords — **wider than PubMed's `[tiab]`** |
| Phrase quoting | Scopus `"..."` is a **loose** phrase: it ignores punctuation and permits wildcards. `{...}` is an exact string. Loose quoting is intended here. **Verify that `"oral cancer*"` behaves as expected** — wildcard-inside-quotes handling is the item most likely to differ from assumption |
| Hyphens | Scopus generally equates hyphenated and spaced forms; spaced forms retained. **Verify** |
| Proximity | `W/n` is available and **not used**. Adding proximity would narrow retrieval and is not part of the adopted strategy |
| Document-type limits | **None applied** |
| Export | CSV or RIS. **Check the export cap**, which is often 2,000 records per export |

---

## 6. Web of Science Core Collection — DRAFT, requires interface verification

**Platform:** Clarivate. **Vocabulary:** **none.** **Field:** `TS=()`.
**Status:** **untested draft. Access publicly advertised but unverified (P007 open).**

> **Editions and year ranges must be recorded** before or at execution. Web of Science coverage
> depends on which editions the subscription includes; without that record the search is **not
> reproducible**. The field is provided in
> `docs/methods/p007_access_verification_record.md` §5.3.

### Copy-ready query

```
TS=(
  ( "oral cancer*" OR "oral cavity cancer*" OR "mouth cancer*"
    OR "oral carcinom*" OR "oral cavity carcinom*"
    OR "oral neoplas*" OR "mouth neoplas*" OR "oral cavity neoplas*"
    OR "oral malignan*"
    OR "oral squamous cell carcinom*" OR "oral cavity squamous cell carcinom*"
    OR "squamous cell carcinoma of the mouth"
    OR OSCC
    OR "oral epidermoid carcinom*" OR "epidermoid carcinoma of the mouth"
    OR "tongue cancer*" OR "tongue carcinom*" OR "tongue neoplas*"
    OR "oral tongue" OR "mobile tongue"
    OR "buccal mucosa" OR "buccal carcinom*"
    OR "floor of mouth"
    OR "gingival carcinom*" OR "gingival cancer*" OR "gum cancer*"
    OR "hard palate" OR retromolar OR "alveolar ridge" )
  AND
  ( smok* OR cigar* OR tobacco
    OR "tobacco smoke" OR "tobacco use" OR "tobacco habit*"
    OR "smoking habit*" OR "tobacco consumption"
    OR bidi OR bidis OR beedi OR beedis
    OR cheroot* OR "pipe smoking"
    OR waterpipe OR "water pipe" OR hookah OR hukka OR shisha*
    OR narghile OR narghila OR nargile OR narguile OR goza
    OR kretek OR "clove cigarette*"
    OR "reverse smoking" OR chutta OR dhumti OR chillum
    OR "hand rolled" OR "roll your own" )
)
```

### Notes and limitations

| Item | Note |
|---|---|
| `TS=` | Topic field: title, abstract, author keywords **and KeyWords Plus**. KeyWords Plus is generated algorithmically from cited references, making `TS=` the **widest** field of the four platforms. Retrieval differences versus PubMed are partly attributable to this, not to coverage |
| **No controlled vocabulary** | As Scopus. The indexed arms have no equivalent |
| Truncation | `*` is supported. **Note the minimum-characters rule** before a wildcard; verify that `smok*` and `cigar*` are accepted |
| Phrase quoting | `"..."` is an exact phrase in Web of Science, **stricter than Scopus**. Wildcards inside quoted phrases may be rejected. **This is the most likely syntax failure in this query** — if `"oral cancer*"` is refused, expand to `"oral cancer" OR "oral cancers"` |
| Proximity | `NEAR/n` available and **not used** |
| Editions | Must be recorded. Not knowable without access |
| Export | Limited per-export batch, often 500 or 1,000 records. **Check before running** |
| Date range | **None applied.** Note that the *subscribed* year range may itself restrict coverage — record it |

---

## 7. IndMED — SIMPLIFIED FALLBACK, interface unverified

**Platform:** ICMR-NIC IndMED. **Vocabulary:** variable / undocumented here.
**Status:** **untested. Reachability unverified; the interface's query language is not documented in
this repository.** This is the weakest strategy of the five and is presented as such.

> **This is not a translation of equal power.** It is a simplified fallback for a platform whose
> Boolean support, field tags, phrase handling and truncation are unknown to this project. **Do not
> assume any operator works until it has been tested in the interface.**

### Staged approach

Because a single compound query may not be supported, run **short queries separately** and record
each as its own line. Start with the most specific and widen:

```
1.  oral cancer AND smoking
2.  oral cancer AND tobacco
3.  oral squamous cell carcinoma AND smoking
4.  oral squamous cell carcinoma AND tobacco
5.  mouth neoplasm AND tobacco
6.  oral cancer AND bidi
7.  oral cancer AND beedi
8.  oral cancer AND reverse smoking
9.  oral cancer AND chutta
10. tongue cancer AND tobacco
11. buccal mucosa AND tobacco
12. oral cancer AND cigarette
```

**If Boolean `AND` is unsupported**, run each concept term alone and intersect the results manually,
recording that this was necessary.

### Notes and limitations

| Item | Note |
|---|---|
| Rationale for inclusion | The exposure definition (D009) admits bidi, chutta and reverse smoking, and that literature is concentrated in Indian journals with incomplete MEDLINE coverage. This is the regional gap D022 and the P007 memorandum both address |
| Bidi spellings | Both `bidi` and `beedi` are searched separately — the spelling split is a real retrieval risk in regional indexing |
| Field tags | **Unknown.** Assume a single general search field unless the interface shows otherwise |
| Truncation | **Unknown.** Do not use `*` until confirmed |
| Phrase search | **Unknown.** Multi-word terms may be treated as `AND` of their words |
| Export | **Unknown, and the main risk.** Regional interfaces often lack a structured export carrying persistent identifiers, which degrades deduplication to title+author+year fingerprinting. Record the export format and whether identifiers are present |
| If unreachable | The regional gap does not disappear. D022 requires documented hand-searching of named journals over a stated date range, or an explicit coverage limitation with its likely direction of effect |

---

## 8. Cochrane CENTRAL — deliberately not translated

CENTRAL registers controlled trials. This review admits only case–control and cohort studies of an
exposure that cannot be ethically randomised, so CENTRAL's core content is a design mismatch. **It is
not searched**, and that omission is reported with this reason rather than left as a silent gap.

---

## 9. Status summary

| Database | Translation | Syntax verified? | Access verified? | Ready for manual testing? |
|---|---|---|---|---|
| **PubMed** | Adopted (D023) | **Yes** — counts-only interrogation 2026-11-12 | **Yes** (free) | **Yes — ready to execute once P007 settles the database set** |
| **Embase** | Drafted | **No** — Emtree headings marked [VERIFY] | **No** — not listed by the institution | Ready to test **if access is obtained** |
| **Scopus** | Drafted | **No** — wildcard-in-phrase behaviour unverified | **No** — advertised, unverified | Ready to test **on access** |
| **Web of Science** | Drafted | **No** — exact-phrase/wildcard conflict is the likely failure | **No** — advertised, unverified | Ready to test **on access**; editions must be recorded |
| **IndMED** | Simplified fallback | **No** — query language undocumented | **No** — reachability untested | Test the interface **before** relying on any syntax |
| Cochrane CENTRAL | Not translated | n/a | n/a | Not searched, by decision |

**No strategy here is empirically validated.** A strategy becomes validated only when it has been run
in the actual database interface and its behaviour recorded. The validation checklist for doing that
is `docs/search/database_search_validation_checklist.md`.

---

## 10. What this document does not do

- It does **not** resolve **P007**, which remains **open**. No database access is claimed.
- It does **not** execute any search, retrieve any record, or register anything under **D011**.
- It does **not** modify the decision register, the protocol, the 194-record dataset or any
  screening decision.
- It does **not** state a record count for any database. **No count is invented**, and the only
  figures cited anywhere in this project are the PubMed counts-only interrogations of 2026-11-12,
  which are not search yields.
- It does **not** reintroduce a study-design block, consistent with D023.
