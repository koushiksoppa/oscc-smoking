# Recommended search strategy (v3 candidate) — PROPOSAL, NOT EXECUTED

**Status: proposal for the reviewer's approval. No search has been executed from this document, no
records retrieved, no export created, and there is deliberately no entry in `config/sources.yaml`.**
A registry entry asserts that an export exists; one is added only after the reviewer runs the search
and exports the results.

This supersedes neither v1 nor v2 as a record. v1 is preserved verbatim as history; v2 remains the
drafted strategy. If approved, this becomes v3 with its own strategy file, execution date, count,
filters actually applied and export checksum.

---

## 1. Concept matrix

Controlled vocabulary verified against PubMed MeSH as cited in the existing strategy documents.
**Each heading must be re-verified against the live MeSH tree on the day of execution** and the
verification recorded, because MeSH is revised annually.

| Concept | Controlled vocabulary (PubMed MeSH) | Free-text terms (`[tiab]`) | Rationale |
|---|---|---|---|
| **Oral cavity cancer** | `Mouth Neoplasms`[Mesh] — explodes over Gingival, Lip, Palatal, Tongue and Salivary Gland Neoplasms | oral cancer · oral cavity cancer · mouth cancer · oral carcinoma · oral cavity carcinoma · oral neoplasm(s) · mouth neoplasm(s) · oral cavity neoplasm(s) · oral malignancy · tongue cancer · tongue carcinoma · oral tongue · mobile tongue · buccal mucosa · buccal carcinoma · floor of mouth · gingival carcinoma · gingival cancer · gum cancer · hard palate · retromolar · alveolar ridge | The adopted outcome is oral cavity cancer, not the literal phrase "oral squamous cell carcinoma". 68 of the 194 records in the existing export say "oral cancer"; 0 say "mouth cancer", a common British-usage and lay term that the existing strategy cannot reach. Exploding `Mouth Neoplasms` removes any need for separate subsite headings. |
| **Squamous cell carcinoma** | `Carcinoma, Squamous Cell`[Mesh] — **used only inside the outcome OR-group, never ANDed** | oral squamous cell carcinoma · oral cavity squamous cell carcinoma · OSCC · squamous cell carcinoma of the mouth · epidermoid carcinoma | Histology is confirmed at screening and extraction, not at the search stage. Requiring an explicit squamous term would exclude studies reporting "oral cancer" with histology stated only in the methods — exactly the studies the ≥90% criterion exists to admit. `epidermoid carcinoma` is the standard older synonym and is needed because no date limit is applied. |
| **Smoked tobacco** | `Smoking`[Mesh] — explodes over Cigarette Smoking, Tobacco Smoking, Water Pipe Smoking · `Tobacco Smoking`[Mesh] · `Cigarette Smoking`[Mesh] | smoking · smoker(s) · smoked · cigarette(s) · tobacco · tobacco smoke · tobacco use · tobacco habit · smoking habit · tobacco consumption | The exposure is any combusted tobacco. `smoking` does not match "smokers" or "smoked", which appear in 38 and 8 records respectively; PubMed's automatic expansion cannot be relied on in a documented strategy, so inflections are enumerated. |
| **Tobacco products (combusted)** | `Tobacco Products`[Mesh] | bidi(s) · beedi(s) · cigar(s) · cheroot · pipe smoking · waterpipe · water pipe · hookah · shisha · narghile · narghila · goza · kretek · clove cigarette · reverse smoking · chutta · dhumti · chillum · hand-rolled · roll-your-own | The exposure definition explicitly admits bidis, cigars, pipes and other combusted products. The South Asian and Indonesian product terms matter because the exposure burden is greatest in those populations. The waterpipe family is reachable through exploded MeSH only for indexed records, and **21.6% of the existing export (42 of 194) carries no MeSH at all**. |
| **Not exposure terms** | — | *smokeless · betel quid · gutkha · khaini · snuff · chewing tobacco* | Deliberately **absent from the exposure block**. These are confounders under the adopted exposure definition, not substitutes for it. Studies covering both remain reachable through their smoking terms. |
| **Aetiological design** *(optional block — see §3)* | `Epidemiologic Studies`[Mesh] — explodes over Case-Control, Cohort and Cross-Sectional Studies · `Risk Factors`[Mesh] · `Odds Ratio`[Mesh] | risk factor(s) · odds ratio(s) · relative risk · hazard ratio · case control · cohort · controls · matched controls · hospital-based · population-based · etiology · aetiology | If a design block is used at all it must require no literal design label, since eligible studies frequently describe their design only in the methods. |

### Terms deliberately not included

| Terms | Reason |
|---|---|
| Oropharynx, larynx, pharynx, hypopharynx, "head and neck" | Estimates pooling these subsites with the oral cavity are ineligible unless an oral-cavity-specific estimate is reported. Eligible papers of that kind remain reachable through the oral-cavity terms they also contain. Adding them as search terms would add large volume for little gain. |
| Smokeless tobacco, betel quid and chewing products | Confounders, not the exposure. |
| Leukoplakia, erythroplakia, oral submucous fibrosis, "potentially malignant" | **Contingent on an unresolved question** — whether populations restricted to premalignant lesions are in scope. Not added. See §6. |
| Lip-specific terms | **Contingent on unresolved lip-scope questions.** Note that `Mouth Neoplasms`[Mesh] already explodes over `Lip Neoplasms`, so indexed lip studies arrive regardless. Adding free-text lip terms is an option, not a recommendation. See §6. |
| Language, species, date and publication-type filters | None applied, per the adopted retrieval decision. |

---

## 2. Recommended PubMed query — copy-ready

**ADOPTED (D023, 2026-11-13): no design block.** This is the primary search strategy, not a
recommendation. Rationale in §3.

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

**Filters: none.** No language, species, date or publication-type restriction. Language and species
are handled at screening with a recorded exclusion reason, where each exclusion is auditable.

### Two properties of this query that are deliberate, not oversights

**1. Bare anatomical terms will retrieve non-neoplastic studies.** `buccal mucosa`, `floor of
mouth`, `hard palate`, `oral tongue`, `mobile tongue`, `retromolar` and `alveolar ridge` carry no
neoplasm qualifier. Combined with the exposure block they will retrieve, for example, buccal-mucosa
cytology and micronucleus studies in smokers, which are not cancer-incidence studies. These are
**expected and will be excluded at screening** under the recorded reason codes. They are retained
because the alternative — requiring a cancer word beside every subsite term — would lose studies
that name the subsite in the title and the malignancy only in the abstract. **No claim is made
about the precision of this query**; precision was not measured and no record has been examined.

**2. Generic tobacco terms will retrieve smokeless-only studies.** `Tobacco Products`[Mesh],
`tobacco`, `tobacco use`, `tobacco habit(s)` and `tobacco consumption` match studies of smokeless
tobacco, betel quid and chewing products. **No smokeless-specific term appears anywhere in the
exposure block**, and smokeless tobacco is not an eligible exposure: it is a confounder under the
adopted exposure definition. Such records are retrieved because the generic terms cannot
distinguish them at the search stage, and they are **excluded at screening as a wrong exposure**.
Retrieval is not eligibility.

**Product terms are not mandatory.** The broad smoking concept — the MeSH headings plus `smoking`,
`smoker(s)`, `smoked`, `cigarette(s)`, `tobacco` — is the primary driver of the exposure block.
The product-specific terms sit in the same OR-group as a free-text safety net for records that are
not yet MeSH-indexed, which is 21.6% of the existing export. Requiring a product-specific term
would be a severe loss of sensitivity, because most eligible studies say only "smoking".

### Optional design block

To be appended with `AND` **only if** the reviewer decides that volume requires it:

```
AND
(
  "Epidemiologic Studies"[Mesh]
  OR "Risk Factors"[Mesh]
  OR "Odds Ratio"[Mesh]
  OR "risk factor"[tiab] OR "risk factors"[tiab]
  OR "odds ratio"[tiab] OR "odds ratios"[tiab]
  OR "relative risk"[tiab] OR "hazard ratio"[tiab]
  OR controls[tiab] OR "matched controls"[tiab]
  OR "case control"[tiab] OR cohort[tiab]
  OR "hospital-based"[tiab] OR "population-based"[tiab]
  OR etiology[tiab] OR aetiology[tiab]
)
```

### Syntax validation of this query — 2026-11-12

**Tool-assisted syntax validation, not a researcher-executed search and not the search of record.**
Performed by automated tooling under the reviewer's direction.

| Item | Value |
|---|---|
| Date | **2026-11-12** (UTC) |
| Platform | NCBI E-utilities `esearch.fcgi`, database `pubmed` |
| Method | HTTP POST, `retmax=0` — **counts only; no record was retrieved, downloaded or exported** |
| Authentication | none; no API key, no sign-in, no account access |
| Query | exactly as printed above |
| Errors / warnings returned | **none**; HTTP 200 for every line |

| Line | Query | Count on 2026-11-12 |
|---|---|---|
| 1 | Outcome block alone | 116,283 |
| 2 | Exposure block alone | 495,031 |
| 3 | Design block alone | 6,526,293 |
| 4 | **1 AND 2 — the recommended primary query, no design block** | **8,190** |
| 5 | 1 AND 2 AND 3 — with the optional design block | **5,008** |

**PubMed's query translation was inspected.** Every `[tiab]` term resolved to `[Title/Abstract]`
and every `[Mesh]` term to `[MeSH Terms]`, with no unexpected automatic expansion. This matters
because the v1 strategy shows the opposite behaviour: five records in the existing export cannot be
explained by its literal wording. The query above is therefore reproducible as written.

**Limitations of this validation.** It establishes only that the syntax is accepted and what volume
to expect on the date shown. It is **not** a search yield: nothing was exported, no registry entry
exists, and the database grows daily, so the researcher's own execution will return a different
number on its own date. Precision was not assessed — no record was examined for eligibility.

#### What the C-1 correction changed, measured

| Version | Count on 2026-11-12 |
|---|---|
| Earlier draft including `"Carcinoma, Squamous Cell"[Mesh]` and a bare `"epidermoid carcinoma"[tiab]` | **14,390** |
| **Corrected query above** | **8,190** |
| Difference removed by the correction | **6,200 records (−43%)** |
| `"Carcinoma, Squamous Cell"[Mesh] AND` the exposure block, on its own | **8,731** |

The last line is the decisive one: that single site-unrestricted heading, combined with the exposure
block, retrieves about as many records as the entire corrected query — and none of them need
mention the oral cavity at all. Earlier figures quoted for the v2 draft (4,770 with a design block,
7,875 without, at 2026-10-29) describe **a different and narrower term set** and must not be cited
as counts for this query. The query here is broader, so its yield will be
higher by an amount that is unknown until it is run. **Any figure quoted before execution would be
invented.**

---

## 3. Why the design block is omitted from the primary search (adopted, D023)

| | Design block retained | No design block |
|---|---|---|
| Measured v2 yield at 2026-10-29 | 4,770 | 7,875 |
| Requires a design label | No — MeSH explosion and effect-measure terms avoid it | Not applicable |
| Removes | ~39% of the outcome-and-exposure set | — |
| Evidence that what it removes is ineligible | **None** | — |
| Methodological standing | Design filters for observational reviews are discouraged as unreliable | Preferred |

A design block is a filter, and a filter's cost is invisible: the records it removes never appear
for inspection. Retaining it buys a **measured** reduction in retrieval volume at the cost of an
**unmeasured risk** to sensitivity: whether the removed set contains any eligible study is
unknown, and the number lost may be zero. Removing it increases the number of records retrieved,
but the number of additional eligible studies recovered is unknown and may be zero, so the difference in
retrieval volume does **not** establish improved empirical sensitivity or recall. That is a
legitimate trade to make deliberately and report — it is not a trade to make silently, and it was
the reviewer's to make, not this document's.

**Adopted position (D023, 2026-11-13): the design block is omitted from the primary search.**
The operative comparison is the corrected query's **8,190 without the block against 5,008 with
it** — a retrieval-volume difference of **3,182 records**, both figures counts-only
interrogations of 2026-11-12 and **neither a search yield**. The 4,770-versus-7,875 pair belongs
to the superseded v2 draft and is not comparable. If a measured screening rate later shows 8,190
to be infeasible, D023 is revisited explicitly and the block reinstated as a recorded change;
the query is never narrowed mid-search.

---

## 4. Database-specific syntax

A PubMed query cannot be pasted into another platform. Each database needs its own strategy
document, with its own controlled vocabulary, field tags and date of execution. Full assessment in
`database_coverage_assessment.md`; the syntax requirements are:

| Database | Platform | Controlled vocabulary | Field tags | Translation notes |
|---|---|---|---|---|
| **PubMed/MEDLINE** | NCBI | MeSH, `[Mesh]`, auto-explodes | `[tiab]`, `[Mesh]` | As above. |
| **Embase** | Elsevier (embase.com) | **Emtree**, not MeSH. `'mouth cancer'/exp`, `'smoking'/exp` | `:ti,ab,kw` | Emtree headings differ in name and hierarchy; `/exp` must be explicit. `:kw` adds author keywords, absent from PubMed. Conference abstracts are indexed and should be retained for screening. |
| **Scopus** | Elsevier | None — no thesaurus | `TITLE-ABS-KEY( )` | Entirely free text. Supports `W/n` proximity and `*` truncation, both unavailable in PubMed. One long `TITLE-ABS-KEY` expression. |
| **Web of Science Core Collection** | Clarivate | None | `TS=( )` | Topic field covers title, abstract, author keywords and KeyWords Plus. `NEAR/n` proximity, `*` truncation. Edition coverage must be recorded. |
| **Cochrane CENTRAL** | Wiley | MeSH | `:ti,ab,kw`, `MeSH descriptor` | Trial-focused; low expected yield for observational aetiology. |
| **IndMED / regional** | ICMR-NIC and equivalents | Variable | Variable | Limited Boolean support; may require simplified queries and manual screening. Record the interface and date because coverage is less stable. |

For each database the search of record must report: query exactly as run, platform and interface,
date of execution, filters actually applied, records retrieved, export format, and the export's
checksum.

---

## 5. Reproducibility requirements before execution

1. **Re-verify every controlled-vocabulary heading** against the live thesaurus on the day of
   execution, and record the verification. MeSH and Emtree are revised annually.
2. **Record the execution date for every database.** The absence of a recorded date for v1 is
   unrecoverable and must not recur.
3. **Capture PubMed's "Search details"** output, which shows how automatic term mapping expanded
   the query. The existing strategy's phrase-handling behaviour is undocumented and five records in
   the current export cannot be explained by its literal wording.
4. **Export in a format that preserves identifiers** — PubMed/MEDLINE `.nbib` for PubMed, RIS for
   the others — and register each export's checksum before it is used.
5. **One registry entry per database per execution.** Never reuse a filename or an entry.
6. **Run the known-item test** in §6 and record the result whatever it is.
7. **Seek PRESS or equivalent peer review** of the final strategy. None has been performed on v1,
   v2 or this proposal.

---

## 6. Open questions this strategy does not resolve

| Question | Effect on the search | Position taken here |
|---|---|---|
| **Database set** | Determines how many strategy documents are needed | Recommendation only, in `database_coverage_assessment.md`; not adopted |
| **Volume versus single-reviewer capacity** | Determines whether the design block is retained | Both options costed; not adopted |
| **Premalignant-lesion populations** | Whether leukoplakia, erythroplakia and oral submucous fibrosis terms belong in the outcome block | **Terms not added.** Adding them would presume the answer |
| **Lip subsites** | Whether free-text lip terms belong in the outcome block | **Not added.** Exploded `Mouth Neoplasms` already reaches indexed lip studies; adding free-text lip terms is an option |
| **Comparator definition and primary contrast** | No effect on retrieval; both affect eligibility and extraction | No search term depends on either |
| **Known-item seed set** | Required before execution | Cannot be assembled from the repository; must come from the reviewer |

---

## 7. What must happen before this is executed

1. Reviewer approves or revises the term set in §1 and the query in §2.
2. Reviewer decides on the design block (§3).
3. Reviewer settles the database set, and a strategy document is written for each.
4. Reviewer supplies a seed set of known-eligible studies; the known-item test is run and recorded.
5. PRESS or equivalent peer review.
6. Only then is the search executed and exported, with a registry entry per database per execution.

Until all six are done, the 194-record set remains the only retrieved evidence base, and it should
not be treated as the evidence base of a systematic review.
