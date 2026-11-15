# Search strategy audit

**Status: audit and design only. No search was executed for this document, no record was
retrieved, and nothing in `data/` was altered.** The findings below come from inspecting the
protocol, the decision register, the existing strategy documents and the committed 194-record
export. Where a statement rests on analysis of that export it is marked as such; where it rests on
methodological argument rather than measurement, it says so.

## 1. What was inspected

| Source | What it established |
|---|---|
| `docs/protocol/eligibility_criteria.md` | Review question, PICO, inclusion and exclusion criteria |
| `docs/decisions/decision_log.md` | D001–D015, D020 and D022 adopted; D016–D019 proposed; D021 not in the register; P007, P013 and 16 further questions open |
| `docs/search/search_v1_pubmed.md` | The v1 query, its filters, and its own appraisal of five weaknesses |
| `docs/search/search_v1r_pubmed_reexecution.md` | The re-execution: 194 unfiltered, 150 filtered, against a documented 138 |
| `docs/search/search_v2_pubmed.md` | The drafted v2 strategy and its line-by-line counts |
| `config/sources.yaml` | Two registry entries; no entry for v2, correctly, because no export exists |
| `data/raw/pubmed/pubmed-v1r-reexecution-194.nbib` | 194 records, 152 with MeSH, 42 without |
| `data/screening/screening_ta.csv` | 194 provisional classifications; 85 forwarded, 109 excluded |
| `scripts/dedup/` | Identifier hierarchy and matching conventions, which any new search must satisfy |

Previous reports were not taken on trust. Every count in this document was re-derived.

## 2. The review question and eligibility criteria — preserved, not reopened

The scope is as adopted and is not widened here:

- **Outcome.** Oral cavity cancer with squamous cell carcinoma histologically confirmed, or SCC a
  stated majority of ≥90% of cases. Estimates pooled across head-and-neck subsites are ineligible
  unless an oral-cavity-specific estimate is reported separately.
- **Exposure.** Any smoked or combusted tobacco. **Smokeless tobacco and betel quid are
  confounders, not the exposure**, and are not substitutes for it.
- **Population.** Human adults.
- **Designs.** Case–control and cohort.

Two eligibility questions remain open and bear directly on search design: the comparator
definition and the primary exposure contrast. Ten questions of anatomical and histological scope
are also open, including whether lip subsites are in scope and whether populations restricted to
premalignant oral lesions are eligible. **This audit does not resolve any of them**, and no search
term is added or removed on the basis of an unsettled question without saying so.

## 3. Audit of the v1 strategy

```
("Oral Squamous Cell Carcinoma"[Title/Abstract] OR OSCC[Title/Abstract])
AND (smoking[Title/Abstract] OR cigarette[Title/Abstract])
AND ("case-control"[Title/Abstract] OR cohort[Title/Abstract])
Filters: Humans, English
```

### 3.1 Why it returned so few records

Three independent restrictions multiply. Measured against the committed export:

| Observation | Count | Source |
|---|---|---|
| Records in the export | 194 | export |
| Records whose title or abstract contains "oral squamous cell carcinoma" | 153 | export analysis |
| Records containing the abbreviation OSCC | 143 | export analysis |
| Records containing **only** OSCC, not the spelled-out phrase | 36 | export analysis |
| Records containing "oral cancer" | 68 | export analysis |
| Records containing "oral cavity cancer" | 6 | export analysis |
| Records containing "mouth cancer" | **0** | export analysis |
| Records matching the design block **only** through the word "cohort" | **98** | export analysis |
| Records with no MeSH indexing at all | **42 of 194 (21.6%)** | export analysis |

Two consequences follow.

**The outcome block selects on phrasing, not on topic.** 68 of the 194 records use the phrase "oral
cancer" — the dominant phrasing in aetiological epidemiology. Every one of them was retrieved only
because it *also* happened to contain "oral squamous cell carcinoma" or "OSCC". A study reporting
"oral cancer" with squamous histology stated in its methods — precisely the study the adopted
outcome definition is designed to include — contains neither v1 term and is invisible to this
query. The size of that missed set cannot be measured from inside the retrieved set, which is the
central limitation of this audit; it can only be measured by executing a broader query.

**Half the retrieved set arrived through one word.** 98 of 194 matched the design block only via
"cohort". That word does not identify an aetiological cohort study; it also matches prognostic
cohorts of patients who already have the disease. This is consistent with `wrong_outcome` being the
largest provisional exclusion reason (63 of 109). The design block is thus simultaneously
*insensitive* to eligible studies that never use a design label and *unspecific*, admitting a
large body of prognostic literature.

### 3.2 Itemised weaknesses

| # | Dimension | Finding |
|---|---|---|
| 1 | **MeSH coverage** | **None.** No controlled vocabulary at all. `Mouth Neoplasms`, `Carcinoma, Squamous Cell`, `Smoking`, `Tobacco Products`, `Case-Control Studies`, `Cohort Studies` and `Risk Factors` are all unused. Free text alone misses older records indexed under headings whose abstract wording differs. |
| 2 | **Free-text coverage** | Severely incomplete. The outcome block has two terms; the exposure block two; the design block two. No subsite terms, no product terms beyond "cigarette", no effect-measure terms. |
| 3 | **Boolean structure** | Three blocks ANDed is correct in principle. The fault is the content of each block, not the logic. |
| 4 | **Truncation and inflection** | No truncation. `smoking` does not match "smokers" or "smoked"; `cigarette` does not match "cigarettes" except through PubMed's automatic expansion, whose behaviour is not documented in the strategy. 38 records contain "smoker(s)" and 8 contain "smoked". |
| 5 | **Phrase searching** | `"Oral Squamous Cell Carcinoma"[Title/Abstract]` is a quoted phrase. **Five of the 194 records do not contain that phrase or the abbreviation in their stored title and abstract**, yet were retrieved — for example a record titled "Smokeless Tobacco Usage and Oral Cancer Risk" and one titled "Oral Tongue Squamous Cell Carcinoma". The most likely explanation is PubMed's automatic term mapping or phrase handling making the effective query broader than the written one. **This is a reproducibility concern that requires verification against PubMed's search-details output; it is not asserted as established here.** |
| 6 | **Filters** | Humans and English were applied in v1. D013 subsequently rejected this: the Humans filter operates on an index term absent from the 42 unindexed records, which are the most recent. The re-execution correctly applied no filters. |
| 7 | **Incorrect exclusions** | The design block functions as an unvalidated study-design filter. Methodological guidance discourages design filters for observational reviews precisely because they are unreliable. Here it removes 39% of the outcome-and-exposure set with no evidence that the removed records are ineligible. |
| 8 | **Platform and syntax** | PubMed (NCBI). Syntax is valid. The strategy is not portable: it cannot be pasted into Embase or Scopus, which use different field tags and controlled vocabularies. |
| 9 | **Reproducibility** | The query string is preserved verbatim, which is good practice. But **the v1 execution date is unrecorded and unrecoverable**, the export is lost, and the 138-record count cannot be verified. Re-execution of the same string returned 194 unfiltered and 150 filtered, leaving roughly nine records unexplained. |
| 10 | **Landmark-study retrieval** | **Cannot be assessed.** The repository contains no seed set, no reference list of known-relevant studies and no citation list against which recall could be tested. See §5. |
| 11 | **Peer review** | No PRESS or equivalent peer review of the strategy has been performed. |
| 12 | **Single database** | PubMed alone. Reporting guidance for reviews of observational studies expects multiple sources plus reference-list and citation checking. Open as P007. |

### 3.3 What the audit cannot establish

Retrieval analysis confined to a set produced by the query under audit is inherently circular: every
record in the export matched all three v1 blocks by construction. So the export can demonstrate
that the blocks are **narrow in their wording** and can quantify *how* records entered, but it
cannot measure what was missed. Three specific claims therefore remain unmeasured:

- how many eligible studies use "oral cancer" and never "OSCC";
- how many eligible studies never use a design label;
- how many bidi, cigar, pipe or waterpipe studies never use the words "smoking" or "cigarette".

On the third, the export offers weak and explicitly non-generalisable reassurance: of the 9 records
mentioning bidi, 2 mentioning pipe and 3 mentioning waterpipe, hookah or shisha, **all also
contained "smoking" or "cigarette"**. That is a property of the retrieved set, not of the
literature, and must not be read as evidence that the exposure block is adequate.

## 4. Audit of the drafted v2 strategy

The v2 draft is a substantial and largely sound redesign. It pairs controlled vocabulary with free
text in every block, correctly declines to require an explicit squamous-cell term — which would
exclude the studies the outcome definition exists to capture — correctly excludes smokeless tobacco
and betel quid from the exposure block, correctly applies no filters, and correctly refuses to
narrow itself for workload reasons.

### 4.1 On the 4,770 figure

The draft records a line-by-line count obtained by submitting the query to PubMed and NCBI
E-utilities on **2026-10-29 by automated tooling under the reviewer's direction** — read-only, no
sign-in, no account access — to confirm that the syntax parses and each block behaves as intended.
**This was tool-assisted syntax validation, not a researcher-executed search**, and the distinction
is preserved deliberately: the search of record is the one the researcher runs and exports, with its
own date, count and checksum.



| Line | Query | Count |
|---|---|---|
| 1 | Outcome block alone | 105,270 |
| 2 | Exposure block alone | 493,884 |
| 3 | Design block alone | 6,442,249 |
| 4 | **1 AND 2 AND 3** | **4,770** |
| 5 | 1 AND 2, design block removed | 7,875 |

**Characterisation.** This is a documented read-only syntax-validation execution with a date and
per-line counts — not an unverified estimate, and not the systematic search of record. No export
exists, no records were retrieved, and there is correctly no registry entry for v2. The count of
record will be whatever the researcher's own execution returns on its own date, which will differ
because the database grows. The figure should be cited as "approximately 4,770 at
2026-10-29 (syntax-validation run)", never as the search yield.

### 4.2 Remaining gaps in v2

| # | Gap | Evidence or reasoning |
|---|---|---|
| 1 | **The design block is retained** | It removes 39% of line 5 (7,875 → 4,770). Design filters for observational reviews are discouraged because they are unreliable; the 39% removed has not been shown to be ineligible. Keeping it buys feasibility at an unquantified cost in sensitivity. |
| 2 | **Waterpipe free text absent** | `"Smoking"[Mesh]` explodes over Water Pipe Smoking, so *indexed* records are covered; but 42 of 194 records carry no MeSH, and the free-text side lacks `waterpipe`, `water pipe`, `hookah`, `shisha`, `narghile`, `goza`. Unindexed waterpipe studies are reachable only if they also say "smoking". |
| 3 | **South Asian product terms incomplete** | `bidi`, `beedi` and `reverse smoking` are present; `chutta`, `dhumti`, `chillum` and `cheroot` are not. These denote combusted products central to the highest-incidence populations and therefore to D009. |
| 4 | **Historical histology terminology absent** | `epidermoid carcinoma` was the standard synonym for squamous cell carcinoma in older literature. It appears in 0 of the 194 records, which is unsurprising since v1 never searched it, and says nothing about its presence in the wider literature. Relevant if the search has no date limit. |
| 5 | **Outcome free text misses several forms** | `mouth neoplasm(s)`, `oral cavity neoplasm(s)`, `oral cavity carcinoma`, `oral cavity squamous cell carcinoma` (10 of 194 contain "oral cavity squamous"), `gingival cancer`, `gum cancer`, `hard palate`, `retromolar`, `alveolar ridge`, `oral tongue`, `mobile tongue`. "mouth cancer" appears in 0 of 194 yet is a common lay and British-usage term. |
| 6 | **Inflection coverage uneven** | `smoker`/`smokers`/`smoked` are enumerated, which is appropriate for PubMed, but `smoking habit`, `tobacco habit`, `tobacco consumption` and `tobacco use` are absent. |
| 7 | **No MeSH major-topic or subheading strategy** | Not a defect, but worth stating explicitly in the final strategy that no subheading restriction is used, since subheading restriction is a common and unreported source of lost records. |
| 8 | **No date limit stated** | v2 applies none. This should be stated affirmatively rather than left implicit, since "no date limit" is a reportable decision. |
| 9 | **Lip terms absent** | Consistent with lip scope being unresolved. Adding them is a sensitivity gain and a volume cost, and depends on an open question; it is presented as an option in the recommended strategy, not decided. |
| 10 | **No peer review** | PRESS review of v2 has not been performed. |

### 4.3 What v2 gets right and should not be changed

- No requirement for an explicit squamous-cell term. Requiring one would exclude studies reporting
  "oral cancer" with histology in the methods, which the outcome definition is written to include.
  Histology is verified at screening and extraction.
- Smokeless tobacco and betel quid excluded from the exposure block. They are confounders.
- Oropharynx, larynx, pharynx and "head and neck" terms excluded as *search* terms, while eligible
  papers of that kind remain reachable through the oral-cavity terms they also contain.
- No filters. Language and species are handled at screening with a recorded reason code.

## 5. Known-study retrieval validation — not possible as the repository stands

**The repository contains no set of known-relevant studies.** There is no seed list, no landmark
reference list, no citation export and no previously published review's included-study table against
which recall could be tested. No such list is invented here.

The only retrieval testing performed is the within-set analysis in §3.1, which is explicitly
circular and establishes nothing about recall.

**Recommended known-item test, to be performed before the search of record is executed.** The
reviewer assembles a seed set of 10–20 studies independently known to be eligible — from narrative
reviews, textbook citations, or earlier meta-analyses of smoking and oral cancer — and records them
with PMIDs in a tracked file. The candidate strategy is then run and recall against that seed set
measured. A strategy that fails to retrieve a known-eligible study must be revised before
execution, and the test must be documented whatever its result. **This is a verified-retrieval test
and is categorically different from the theoretical expectations in §4.2, which are reasoning about
terminology rather than measurement.**

## 6. Strategy comparison

| Dimension | Existing v1r | Drafted v2 | Recommended (this audit) |
|---|---|---|---|
| **Database coverage** | PubMed only | PubMed only | PubMed + Embase + one citation index, with a regional database for South Asian literature; reference-list and forward-citation checking |
| **Controlled vocabulary** | **None** | MeSH in all three blocks | MeSH in all blocks, with additional headings and an explicit statement that no subheading restriction is applied |
| **Outcome sensitivity** | **Very low** — two phrases; 68 of 194 say "oral cancer" and were caught only incidentally | Good — `Mouth Neoplasms`[Mesh] exploded plus 15 free-text forms | Better — adds `mouth neoplasm`, `oral cavity neoplasm/carcinoma`, subsite terms, `epidermoid carcinoma`, optional lip terms |
| **Exposure sensitivity** | **Low** — no inflections, no products beyond cigarette, no MeSH | Good — MeSH plus inflections, bidi, kretek, reverse smoking | Better — adds waterpipe family, chutta, dhumti, chillum, cheroot, tobacco use/habit forms |
| **Design handling** | Unvalidated two-word filter; 98 of 194 entered via "cohort" alone | `Epidemiologic Studies`[Mesh] exploded plus effect-measure free text; requires no design label | **Primary recommendation: no design block.** Secondary option: retain v2's block with the sensitivity cost declared |
| **Filters** | Humans + English | **None**, per D013 | **None**, with "no date limit" stated affirmatively |
| **Reproducibility** | Query preserved; **date unrecorded, export lost, 138 unverifiable, ~9 records unexplained**; phrase-handling behaviour undocumented | Query and syntax-check counts documented with a date; no export yet | Full PRISMA-S provenance per database: query as run, platform, interface, date, filters actually applied, count, export format and checksum |
| **Known-study retrieval** | **Untested** | **Untested** | **Known-item test required before execution** |
| **Volume** | 194 | 4,770 with design block / 7,875 without, at the 2026-10-29 syntax run | **8,190 without a design block / 5,008 with one, at the 2026-11-12 syntax validation** of the corrected query, PubMed alone. Both figures are tool-assisted syntax checks, **not search yields**. Additional databases will add an unknown quantity |
| **Main limitation** | Selects on phrasing, not topic; single database; unverifiable provenance | Single database; design block of unproven specificity; no known-item test | Volume versus single-reviewer capacity — the substance of P013 |

## 7. Conclusions

1. **The v1 strategy is not fit for the adopted protocol.** Its outcome block selects on phrasing
   rather than topic, it uses no controlled vocabulary, and its design block is both insensitive and
   unspecific. The 194-record set it produced should not be treated as the evidence base for a
   systematic review.
2. **The v2 draft is a sound redesign** and should form the basis of the search of record, with the
   additions in §4.2 and a decision on the design block.
3. **The methodologically preferable strategy removes the design block entirely**, at a measured
   cost of 7,875 records instead of 4,770 on PubMed alone. Whether that is feasible under
   single-reviewer screening is the substance of P013 and is not decided here.
4. **One database is not a systematic search.** P007 must be settled before execution.
5. **A known-item retrieval test must precede the search of record**, and cannot be performed until
   the reviewer supplies a seed set.
6. **A Boolean defect in this audit's own first recommendation was found on second review and
   corrected.** `"Carcinoma, Squamous Cell"[Mesh]` and a bare `"epidermoid carcinoma"[tiab]` had
   been placed in the outcome OR-group, where each was independently sufficient to satisfy the
   outcome block and so removed the oral-cavity concept from the query's logic. Measured on
   2026-11-12, the defect inflated retrieval by **6,200 records (14,390 against 8,190)**, and the
   `Carcinoma, Squamous Cell` heading combined with the exposure block retrieves **8,731** records
   on its own — about as many as the whole corrected query — none of which need mention the oral
   cavity. The corrected query is in `recommended_search_strategy.md`.
7. **No formal search was executed for this audit**, no record was retrieved or added, the
   194-record sampling frame is untouched, and no decision has been adopted or altered. The only
   external action was a read-only, counts-only syntax validation, recorded with its date and
   method.
