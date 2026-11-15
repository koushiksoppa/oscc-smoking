# Research decision log

Each entry records a decision, its rationale, its methodological basis, and its effect on the analysis.
**Type** distinguishes *protocol* decisions (made before seeing screening/extraction results) from *post-hoc* decisions (made after). Post-hoc decisions must be reported as such in the manuscript.

## Decided

### D001 — Preserve the original PubMed search as v1
- **Type:** protocol
- **Decision:** The executed PubMed query and its export are kept unchanged as search v1. Any refinement becomes a new, separately documented version; records from all versions are merged and deduplicated.
- **Rationale:** Reproducibility; PRISMA-S requires the exact strategy as run.
- **Impact:** None on results; enables an audit trail across search versions.

### D002 — Raw exports are read-only
- **Type:** protocol
- **Decision:** Files in `data/raw/` are never modified; every transformation is scripted and writes to `data/processed/`. Checksums are recorded.
- **Rationale:** Traceability from every number in the manuscript back to the source export.
- **Impact:** None on results.

### D003 — Adopt the evidence-provenance rules
- **Type:** protocol
- **Decision:** `docs/protocol/provenance_rules.md` governs all stages. It covers no fabrication, immutable raw inputs, the report/study distinction, a separate alcohol-adjustment field, no automatic harmonisation of exposure categories, outcome-site eligibility, and the analysis gate.
- **Rationale:** Set by the review lead before any data handling.
- **Impact:** Constrains extraction and analysis design. No pooled analysis is run before the gate conditions and the SAP are met.

### D004 — Separate identifiers for records, reports, studies and estimates
- **Type:** protocol
- **Decision:** `record_id` (database record) → `report_id` (unique publication, after deduplication) → `study_id` (unique population, by human judgement at full text) → `estimate_id`. The unit of analysis is `study_id`.
- **Rationale:** Prevents duplicate publications and overlapping cohorts from being counted as independent studies.
- **Impact:** Determines the number of studies (k) in every analysis.

### D005 — If the original v1 export is lost, it is not recreated
- **Type:** protocol
- **Decision:** A new PubMed retrieval, even with the identical query, is recorded as a new search version with its own date and count. It is never labelled v1.
- **Rationale:** PubMed content changes over time, so a re-run is a different search.
- **Impact:** The PRISMA flow would report the search that was actually used.

### D006 — Checksum registration semantics
- **Type:** protocol (engineering)
- **Decision:** The SHA-256 is registered once, on first verified import. Registration requires the record count to equal the count reported at search time. Later runs fail on any mismatch.
- **Rationale:** No checksum was recorded when v1 was downloaded, so registration establishes integrity only from import onward. Provenance of the file itself relies on its origin and the count check.
- **Impact:** None on results.

### D007 — Tests contain no bibliographic content
- **Type:** protocol (engineering)
- **Decision:** Unit tests use format fragments and structural stubs only. Tests on real data run against the registered raw exports and are skipped when the exports are absent.
- **Rationale:** No synthetic citations may exist in the repository (provenance rule 6).
- **Impact:** None on results.

### D008 — Outcome definition (resolves P001)
- **Type:** protocol
- **Decision:** Eligible outcome is cancer of the **oral cavity** where squamous cell carcinoma is histologically confirmed, or where SCC is a stated majority of **≥90%** of cases. Histological confirmation and the reported SCC proportion are extracted as fields. Estimates that pool the oral cavity with the oropharynx, larynx, pharynx or "head and neck" as a single outcome are **not eligible** unless an oral-cavity-specific estimate is reported separately.
- **Rationale:** Restricting to the literal phrase "oral squamous cell carcinoma" would capture a non-representative subset, because most aetiological case-control literature reports "oral cancer" or "oral cavity cancer" and states squamous histology in the methods. The ≥90% threshold keeps the synthesis aligned with the research question while admitting studies that report a small non-SCC minority. The exclusion of pooled head-and-neck outcomes follows provenance rule 12: anatomical subsites have different aetiology (notably HPV in the oropharynx).
- **Basis:** SCC accounts for the large majority of oral cavity malignancies; subsite-specific analysis is standard in head-and-neck epidemiology.
- **Impact:** Widens eligibility relative to search v1; makes the v1 outcome block (`"Oral Squamous Cell Carcinoma"[tiab] OR OSCC[tiab]`) demonstrably too narrow, which is the principal argument for a v2 search. Creates a planned sensitivity analysis restricted to 100%-SCC studies.

### D009 — Exposure definition (resolves P002)
- **Type:** protocol
- **Decision:** The exposure is **any smoked tobacco** — cigarettes, bidis, cigars, pipes and other combusted tobacco products. The product type(s) are extracted for every estimate, supporting a planned subgroup analysis of cigarette-only versus mixed or other products. **Smokeless tobacco and betel quid / areca nut are not exposures**; they are extracted as potential confounders, as is alcohol.
- **Rationale:** A cigarette-only review would exclude much of the most informative literature, particularly South Asian studies of bidi and reverse smoking, where the exposure burden is greatest. Combusted products share the relevant carcinogenic mechanism. Smokeless tobacco and betel quid have distinct dose–response relationships and are strongly associated with both smoking and oral cancer, so they are confounders rather than part of the exposure.
- **Impact:** Widens eligibility. Introduces exposure heterogeneity that the product-type subgroup analysis is designed to examine. Aligns the protocol with the README title ("Tobacco Smoking"); the narrower wording "cigarette smoking" in the original research question is superseded and the question is restated accordingly.

### D010 — Single-reviewer screening and extraction (resolves P005)
- **Type:** protocol
- **Decision:** Screening and data extraction are performed by one human reviewer. This is reported as a limitation under PRISMA 2020 items 8 and 9. Consequences carried through the pipeline: reviewer identity is recorded on every decision; any automated pre-sort is stored in a separate `suggestion` field that can never satisfy a `decision` field; and the review is never described as independently duplicated.
- **Rationale:** Resource constraint, declared openly rather than overstated.
- **Basis:** PRISMA 2020 requires reporting how many reviewers screened each record and whether they worked independently. Single-reviewer screening raises the risk of erroneous exclusion.
- **Impact:** A recognised limitation affecting the reliability of study selection and extraction. It does not alter effect estimates, but it must appear in the Limitations section. Automated tooling is not a reviewer and is not reported as one.

### D011 — Separate registry entries for separate search executions
- **Type:** protocol
- **Decision:** `config/sources.yaml` records one entry per database × **execution**, with an `execution` type (`historical` / `re_execution` / `new`), a `status` (`export_missing` / `awaiting_registration` / `registered`), the `filters_applied` **actually** used, and a `count_source` stating where `expected_records` came from. The historical v1 execution keeps the id `pubmed_v1` with `raw_file: null` and `status: export_missing`; the October 2026 re-run of the same query is a separate entry, `pubmed_v1r`. No entry is created for a merely drafted search, because an entry asserts that an export exists.
- **Rationale:** A 194-record export of the v1 query string arrived while the registry had a single `pubmed_v1` slot expecting 138 records. Registering it there would have misrepresented a later re-execution as the original search. The database's content changes over time and the filters actually applied may differ, so a re-run is a different search even with an identical query string.
- **Basis:** PRISMA-S requires the strategy, platform, filters and date **as run** for each search. D005.
- **Impact:** The PRISMA flow attributes records to the execution that actually produced them. `pubmed_v1` contributes no records unless its export is recovered. The 138 figure is retained as an unverified documented claim and is **not** changed to 194.

### D012 — Re-execution export renamed
- **Type:** protocol (engineering)
- **Decision:** The export was renamed from `pubmed-OralSquamo-set.nbib` to `pubmed-v1r-reexecution-194.nbib` before registration. File content was not touched; the SHA-256 is unchanged at `1d153fa8…27e4ca1e` (verified before and after).
- **Rationale:** A re-execution must not occupy the original export's filename. The original name is left free in case the original export is ever recovered.
- **Impact:** None on results.

### D013 — Retrieve unfiltered; apply language and species limits at screening (resolves P011)
- **Type:** protocol — **deviation from the v1 strategy, to be reported as such**
- **Decision:** Searches are run **without** the Humans and English database filters. The 194-record unfiltered set is retained. Non-English and non-human records are excluded at screening with a recorded reason code (`not_english`, `wrong_population`).
- **Rationale:** The Humans filter operates on the MeSH term `Humans`, so it discards every record PubMed has not yet indexed — 42 of the 194 records here, which are the most recent and therefore plausibly among the most relevant. A screening-level exclusion is auditable and appears in the PRISMA flow; a database filter removes records invisibly.
- **Basis:** Standard guidance against species filters in sensitive searches; PRISMA 2020 expects exclusions to be reported with reasons.
- **Impact:** Eligibility criteria are **unchanged** (English, human) — only the point of application moves. `not_english` and `wrong_population` will carry non-zero counts in the PRISMA flow. Screening volume rises by the number of records a filter would have removed.

### D014 — Identifier priority for deduplication, and the fallback for records lacking identifiers
- **Type:** protocol
- **Decision:** Records are matched in order of decreasing authority: **PMID**, then **DOI**, then an exact fingerprint of normalised title + first-author surname + year. Where several criteria match one pair, the strongest is the one reported as the merge reason. Records whose titles are merely *similar* (same year, sequence similarity ≥ 0.92) are flagged `needs_review` and **never merged automatically**; the stage exits non-zero while any remain unresolved. Normalisation is used only for comparison and never overwrites the citation dataset. Empty keys never match.
- **Rationale:** PMID is PubMed's own stable key for a citation, whereas DOI strings vary in form and are occasionally shared between records or recorded incorrectly, so PMID is the more reliable evidence when both are present. The fingerprint is the documented fallback for records carrying neither identifier; it requires all three components, so a record missing any of them matches nothing on that tier and can only be caught as a review candidate. A near-identical title may be a conference abstract, an erratum, a reanalysis or a different paper, which is a judgement only the reviewer can make (D010).
- **Impact on results:** **None on grouping.** Group membership is the transitive closure of all exact tiers and is therefore independent of their order; this was verified against both constructed cases and all 194 records of `pubmed_v1r`, which produced identical groups and identical `report_id` assignments under both orders. The priority changes only which criterion is *reported* as the reason for a merge.
- **Defect corrected:** before this decision the reported merge reason was decided by alphabetical sorting of the criterion strings, not by any priority. A pair that shared a PMID could therefore be recorded as an `identical title + first author + year (no shared identifier)` match — a false statement about the evidence, since the records did share an identifier. The criterion label no longer asserts the absence of identifiers, and the reason is now selected by priority. This affects only the audit trail's accuracy, not which records were grouped.

### D015 — Python + SciPy as the statistical implementation (resolves P008)
- **Type:** protocol (engineering with methodological consequences)
- **Decision:** The meta-analysis is implemented in **Python with SciPy** (`scripts/analysis/`). R and `metafor` are **not** used, and **no cross-validation against `metafor` is claimed**.
- **Rationale:** Approved by the reviewer. SciPy was already available, which avoided installing and learning a second toolchain under time pressure. The implementation is fully readable and sits inside the existing tested pipeline rather than beside it.
- **Basis / validation:** Cochran's Q p-value and the I² formula are checked against published values (Cochrane Handbook v6.5 §10.10.4.5); the fixed-effect and DerSimonian–Laird paths against arithmetic worked by hand in the tests. Full record: `docs/methods/analysis_validation.md`.
- **Limitations, explicitly accepted:** **(a)** REML has **no external validation** — it is tested only for self-consistency (its τ² is a fixed point of its own update) and limiting behaviour, so it establishes that the implementation solves the equation it encodes, not that the equation is correct. Every REML result carries this caveat in its own notes, and a REML estimate should be checked against `metafor::rma(method="REML")` before it appears in a manuscript. **(b)** The pooled estimate, weights and τ² have no external reference check, because no published worked example with per-study data was accessible. **(c)** No Hartung–Knapp–Sidik–Jonkman interval, which the Cochrane Handbook favours when k > 2 and τ² > 0 — the likely situation here. **(d)** No Mantel–Haenszel or Peto methods, so rare-event and zero-cell data have no route. **(e)** No meta-regression or dose–response model.
- **Impact:** All statistics are reproducible from the repository with pinned dependencies. The limitations above must appear in the manuscript's methods and limitations sections. `run_analysis.py` refuses to run until extracted study data exist, so no pooled estimate can be produced prematurely.

### D020 — Sampling-frame digest for verification draws (adopted; supersedes the file-byte rule for future draws)
- **Status:** ADOPTED 2026-11-10.
- **Type:** protocol (provenance)
- **Decision:** A verification sample's seed is derived from a **canonical digest of the sampling frame**, not from the worksheet file's bytes. The rule is named and versioned: `ordered_report_ids_v1`.

  The canonical form is specified exactly, so that it can be reproduced by hand:

  1. **Fields included:** `report_id`, and nothing else.
  2. **Record order:** worksheet file order, preserved, never sorted.
  3. **Encoding:** UTF-8.
  4. **Unicode normalisation:** NFC, applied to each identifier.
  5. **Null / empty values:** refused. An empty or whitespace-only `report_id` raises; it is never hashed as an empty string.
  6. **Serialisation:** the rule version, then LF, then each identifier followed by LF. The version sits inside the hashed payload, so two rules cannot produce the same digest for one frame.
  7. **Separator:** LF (0x0A) only, whatever the file on disk uses.
  8. **Hash:** SHA-256, lowercase hexadecimal, 64 characters.
  9. **Sampling frame:** every row of `data/screening/screening_ta.csv`, in file order. No filtering, subsetting or deduplication.
  10. **Versioning:** the rule label is recorded alongside every digest, and a change of rule requires a new version string and a new decision entry.

  **Why `report_id` alone faithfully identifies the frame.** The draw is positional: `random.Random(seed).sample(range(len(rows)), size)`, returning the rows at the chosen positions. The procedure therefore consumes only the *number* of sampling units and *which unit occupies each position*. `report_id` is the screening unit of analysis (D004) and is unique across the worksheet, so the ordered sequence of `report_id` values determines both exactly. Adding further columns would make the digest change when a title typo or an abstract re-import is corrected — events that alter no sampling unit and no position — and would thus report an unchanged frame as a different one. The chosen field set is sensitive to precisely what the draw depends on, and to nothing else.
- **Rationale:** The previous rule hashed the worksheet's bytes, so the seed depended on the file's line endings. The same worksheet seeds differently on a CRLF checkout and an LF checkout, which made independent recomputation platform-dependent. It also made the seed change when columns were added that the draw never reads. A frame digest removes both: it is invariant to line endings and to later columns, and it changes when the units or their order change.
- **Scope — future draws only.** This rule governs draws made after its adoption. It is **not** applied retroactively, and the existing sample is not redrawn. Measured: re-deriving a seed under any other rule selects a different sample (an LF-normalised digest overlaps the existing sample in 8 of 40 records; the canonical digest in 7 of 40). Applying a new rule retroactively would therefore describe a sample that was never drawn, so the historical rule and its outputs are preserved verbatim, as D005 requires of any superseded artefact.
- **Historical provenance, preserved unchanged.** The one sample that exists — `data/screening/verification_sample.csv`, 40 records — was drawn under the earlier rule, now labelled `file_bytes_crlf_v1`:

  | Item | Value |
  |---|---|
  | Worksheet | `data/screening/screening_ta.csv` as committed at `c704582` (16 columns, 194 rows) |
  | Seed derivation | `file_bytes_crlf_v1` — first 8 hex digits of the SHA-256 of the file's bytes, in the CRLF form it had on disk |
  | `DRAW_SHA` | `5938922a529a7f7318824f4216b4b9ab05b920a14def7c15e72c15ea2a6076eb` |
  | `DRAW_SEED` | `1496879658` |
  | Sampling-frame digest (recorded retrospectively, rule `ordered_report_ids_v1`) | `37cc07e64054ef938229fbecec5f7da70f4c9ae419aae9f79b04d642574209ad` |
  | Reproduces the committed 40 report IDs, in order | yes, from either the pre- or post-migration worksheet |
  | **Draw date** | **UNVERIFIED** |

  The frame digest is recorded for this sample so that its frame has a platform-independent identity. It is **not** used to re-derive its seed, which remains `1496879658` under the historical rule. Hashing the LF blob that Git stores for `c704582` gives `9ce12867b8f11222963719e7aae9193493f1524b21477a95c664f0cca8f8270a` (seed 2632001639); that value never drew this sample.
- **The original draw date is unverified and is not inferred.** No run log was captured and the sheet carries no date column. The draw necessarily preceded commit `c704582` (2026-11-01 17:48 +0530), but **a commit date is not evidence of when a draw was run**, and it is recorded as an upper bound only — exactly as `pubmed_v1`'s `search_date` remains unknown under P009. Every report states the date as UNVERIFIED.
- **Impact:** `--draw` seeds from the canonical frame digest and prints the rule in force with both digests. Positional row sampling is unchanged. The scoring report carries two labelled blocks: the draw's provenance under both rules, and the current worksheet's file and frame digests separately, so a current value can never be read as pre-specified draw provenance. Verified invariances: identical digest for CRLF and LF presentations; identical for the 16-column and 20-column schemas; unchanged by later columns and by corrections to non-identifying fields. Verified sensitivities: changes on row reorder, row addition, row removal and identifier change. 20 tests in `tests/test_draw_provenance.py`.
- **What this decision does not do.** It does not authorise an extension sample, does not alter the acceptance thresholds (≥95% ADOPT, 90–94.9% EXTEND, <90% RE-SCREEN), does not define the outcome of a second EXTEND, does not define the frame an extension sample would draw from, and does not bear on whether any screening decision has been adjudicated. Those remain open; the second-EXTEND outcome and the extension sampling frame are deferred.


### D022 — Bounded supplementary grey-literature searching
- **Status:** ADOPTED 2026-11-13. Methodology approved by the reviewer 2026-11-12.
- **Type:** protocol (search coverage)
- **Decision:** A **bounded supplementary grey-literature search** is undertaken alongside the bibliographic databases and supplementary methods specified under P007. Sources, in priority order: **theses and dissertations** — Shodhganga, the RGUHS repository, named institutional repositories of dental and health-science colleges, and NDLTD — each conditional on an accessible interface; **government and public-health reports**, including national and state cancer-registry and tobacco-survey series, used as **discovery sources** whose reference lists are checked rather than as evidence of the association; **Google Scholar**, bounded by the stopping rule below; and **reference-list and forward-citation checking** of included studies and relevant systematic reviews. **ProQuest Dissertations & Theses is not searched**, there being no confirmed access. Records are restricted to **English** (D013) and screened against the **existing eligibility criteria and the existing exclusion vocabulary** — `config/screening.yaml` is unchanged and no code is added. **No record is included on the grounds that it is unpublished.** The full operational specification is `docs/methods/grey_literature_scope_decision.md` §8.
- **Rationale:** The exposure definition (D009) admits bidi, chutta, cigars, pipes and reverse smoking rather than cigarettes alone, and the studies that make D009 worth having are concentrated in South Asia — where hospital-based case–control studies of tobacco habits and oral cancer frequently appear first, or only, in postgraduate dissertations. A search confined to indexed journals would therefore be least sensitive **exactly where this review is most distinctive**, and the resulting loss would be systematic rather than random. The justification is **search sensitivity**; it is not contingent on any statistical test being performable.
- **Reports and studies:** Where a thesis, report, abstract or article describe the same underlying participants, a **single `study_id`** is assigned (D004) and **all contributing `report_id`s are preserved** in `studies.report_ids`. `primary_report_id` names the most complete account, **which is not assumed to be the journal article** — theses routinely carry adjustment models, exposure categories and counts that article length limits remove. Each estimate records the report it came from in `estimates.report_id` with its required `source_location`, so estimates and exposure definitions drawn from different reports of one study remain separately attributed. **A thesis is not discarded as a duplicate publication merely because an article exists**: `duplicate_publication` applies only to a report contributing nothing beyond one already included. Double counting is prevented at the analysis boundary — `selected_for_analysis` permits at most one estimate per study per analysis, with a recorded rationale, and a `study_id` appears at most once in any analysis. Where samples overlap without being identical, the overlap is recorded and one estimate is selected with the reason stated.
- **Study-level provenance:** The **extraction schema is unchanged** (`config/extraction.yaml` untouched by this decision). Study-level descriptive variables taken from a report other than the primary one are recorded in `studies.notes` using the convention `src: field=report_id`, entries being listed only where the source is not `primary_report_id`. This is **Option A of `docs/methods/grey_literature_scope_decision.md` §4, adopted provisionally**, and its weakness is accepted explicitly: `notes` is a free-text field, so the convention is **human-readable but unenforced** — the validator cannot check it and a lapse is invisible. Estimate-level provenance, which carries the analysis, is unaffected and is fully attributed.
- **Provenance safeguard:** The number of included studies whose contributing reports **disagree on a study-level variable is counted and recorded during extraction**. **If it exceeds three, extraction stops before it is finalised** and a structured provenance-schema proposal is presented for the reviewer's approval. **The schema extension is never implemented automatically**, and `config/extraction.yaml` is not modified without explicit authorisation. The count is recorded rather than noticed, so the trigger cannot pass unobserved.
- **Google Scholar stopping rule:** Five prespecified phrase queries are run separately, sorted by **relevance**, with patents and citations excluded and 20 results per page. For each query, screening proceeds by title in displayed order and stops at whichever occurs first: **200 results examined**, **50 consecutive results yielding nothing potentially eligible**, or the end of the list. **The thresholds 200 and 50 are operational choices fixed in advance to make the search bounded and reportable. They are not established systematic-review standards and are not presented as such**; a different prespecified pair would be equally defensible, and what would not be defensible is deciding when to stop while searching. Google Scholar orders results by an **unstable relevance algorithm**, so this search is **reportable but not repeatable, and no claim of reproducibility is made for it**. It is **supplementary and does not replace a bibliographic database**; no coverage claim rests on it. For every query the date searched, exact query string, sort order, number of results examined and the stopping condition that applied are recorded.
- **Impact:** Each grey-literature source is a **separate registered search execution under D011**, with its interface, the exact string entered, any field restriction or filter, the date searched, the number of records examined, the stopping condition where relevant, and the number carried forward. Thesis repositories support neither the Boolean syntax nor the controlled vocabulary of the database strategies, so a simplified term set is used per interface and the exact string entered is recorded; the PubMed query is **not** transferable. Where a source is unreachable or its interface fails, the attempt, date and outcome are recorded and reported: **an unreachable source is a finding, not an omission**. **No source is reported as searched unless the search was executed and its results preserved.** Where full text is restricted so that eligibility cannot be determined, that is reported as **undetermined** and never recorded as an exclusion on a criterion never assessed. Adds bounded screening work under single-reviewer screening (D010).
- **No accessibility is established by this decision.** **No repository named above has been verified as reachable**; every one is recorded as unverified in `docs/methods/grey_literature_scope_decision.md` §2.1. Approving a method of searching a source is not evidence that the source can be searched, and the two are not to be conflated in any report.
- **What this decision does not do.** It does not resolve or alter **P007**, which concerns bibliographic database coverage and remains open pending access verification; this decision is independent of it and does not inherit its dependencies. It does not bear on **P013**. It does not promise **Egger's test or any small-study-effect analysis** — `scripts/analysis/meta.py` refuses Egger's test below ten studies, and the manuscript reports publication bias as *Not assessed*. It does not decide whether a **sensitivity analysis excluding grey-literature studies** is required if any are included; that remains open, is deferred to the SAP where the number of studies is known, and is a leave-out sensitivity analysis rather than a test of publication bias. It does not add an exclusion code: the `editorial_or_commentary` proposal was withdrawn, editorials and letters being handled by `wrong_design`. It does not authorise any search to be executed.
- **Relies on:** D004 (identifier hierarchy), D009 (exposure definition), D010 (single reviewer), D011 (one registry entry per execution), D013 (unfiltered retrieval, language at screening).


### D023 — No study-design block in the primary search (resolves P013)
- **Status:** ADOPTED 2026-11-13, on the reviewer's explicit authorisation.
- **Type:** protocol (search strategy)
- **Decision:** The primary search applies **no study-design block**. Retrieval is defined by the outcome and exposure blocks alone. On the corrected PubMed strategy this is **8,190 records** against **5,008** with the optional block, a difference of **3,182 records (38.9%)** — both figures from a **counts-only interrogation on 2026-11-12**, neither a search yield. The optional design block documented in `docs/methods/recommended_search_strategy.md` is **not appended** to the primary query. Full evaluation: `docs/methods/p013_design_block_decision.md`; the proposal adopted here: `docs/methods/p013_decision_proposal.md`.
- **Rationale.** A design block is a filter whose cost is invisible: the records it removes never appear for inspection. **Whether any eligible study is lost is unknown and may be zero**, but any loss that did occur would **not be random**: it would fall on studies that name their design only in the methods section, and on records without MeSH indexing, which are disproportionately the recent and regionally published South Asian studies that the exposure definition (D009) was written to capture. **42 of the 194 records already in hand carry no MeSH headings at all.** The block also fails to perform the function a design filter exists for: built on `Epidemiologic Studies`[Mesh], `Risk Factors`[Mesh], `Odds Ratio`[Mesh] and effect-measure free text, it admits cross-sectional studies, case series and reviews, none of which is eligible under the protocol, which admits case–control and cohort designs only. Its highest-yield free-text term, "cohort", is the principal source of prognostic studies of people who already have the disease: `wrong_outcome` accounts for **63 of the 109** provisional exclusions in the existing corpus, the largest single category.
- **Uncertainty, recorded as part of the decision.** *Removing the design block increases the number of records retrieved, but the number of additional eligible studies recovered is unknown. The decision prioritises search sensitivity over retrieval volume; it does not establish that the broader strategy has greater empirical sensitivity.* This statement is part of the decision and is reported with it wherever the strategy is described.
- **Terms accepted by the reviewer on authorisation, recorded verbatim.** **(1)** The empirical sensitivity improvement from removing the block is not established and may be zero. **(2)** The 3,182 additional records represent a known increase in retrieval workload, not a demonstrated increase in eligible studies. **(3)** The decision prioritises the opportunity to identify potentially eligible studies over reducing screening volume. **(4)** P007 remains open and database access must still be verified before finalising the complete search strategy.
- **Consequences.** Title/abstract screening volume increases by **3,182 records** for PubMed alone, before any additional database under P007 or any grey-literature source under D022. Under single-reviewer screening (D010) this is the binding constraint on the review. The increase is stated in **records**; it is **not** converted to hours, because **no screening rate has been observed** — the 194 existing classifications were adopted in bulk in a single action, so the repository holds no timing observation, and the 15-seconds-per-record figure in the superseded P013 wording is an assumption, not a measurement.
- **Preserving D010.** Screening-order aids and recorded batching are permitted. An automated suggestion **may order records** for presentation so that likely-eligible records are met first; it **may never satisfy a decision field**. Every eligibility decision remains independently human-adjudicated, recorded with `decision_basis = independently_adjudicated` and its own `adjudicated_date`, and the review is **not** described as independently duplicated. **This decision does not revise D010**; option (b) of the superseded P013 would have, and is not adopted.
- **Conditions.** Before the formal search is executed, the reviewer **measures** a screening rate on a prespecified sample of 200 records, drawn with the existing seeded procedure, recording start and end times. **No rate is assumed.** If the measured rate shows 8,190 to be infeasible, this decision is revisited **explicitly**, the block reinstated as a recorded change, and the 5,008-versus-8,190 comparison cited as its basis. **The query is never narrowed mid-search.**
- **Scope.** Concerns the design block only. It does **not** resolve **P007** (database coverage, which remains open with no database access verified beyond PubMed), does **not** revise **D010**, and does **not** bear on **D022**. It does not authorise any search to be executed.
- **Supersedes:** the registered P013 wording and its options (a)–(d), together with the 4,770 and 7,875 figures from the superseded v2 draft (2026-10-29), which are not comparable to the corrected query's 8,190 and 5,008 (2026-11-12).
- **Relies on:** D008, D009, D010, D011, D013.


### D024 — Removal of an ineffective quoted phrase from the PubMed strategy (PC-1)
- **Status:** ADOPTED 2026-11-14, on the reviewer's explicit approval of proposal PC-1.
- **Type:** protocol (search strategy — correction)
- **Decision:** The term `"epidermoid carcinoma of the mouth"[tiab]` is **removed** from the outcome block of the adopted PubMed strategy. `"oral epidermoid carcinoma"[tiab]`, which shares the same source line, is **retained**. The unquoted variant `epidermoid carcinoma of the mouth[tiab]` is **deliberately NOT adopted**. No other search term changes.
- **Why:** The quoted phrase is **not matched as a phrase by PubMed**. Submitted alone it returns **0 results**, and PubMed reports `QuotedPhraseNotFound` with `OutputMessage: No items found.` Sitting inside an `OR` group it contributed nothing while failing silently. Two independent observations established this: the reviewer in the PubMed web interface on 2026-11-14, and a per-line counts-only validation of all 88 lines of the adopted query on the same date, in which it was the **only** line of 88 returning zero and the only line carrying any warning.
- **Why the unquoted variant was not adopted.** Removing the quotation marks returned **28 results**, but that is **a different search, not a repair**: PubMed applies its own term handling to an unquoted string, which is not equivalent to exact-phrase matching. Adopting it would add a new, unvalidated term to an adopted strategy and change the retrieved set by an unknown amount. **No claim is made that those 28 records are relevant, let alone eligible**; none was examined, and retrieval is not eligibility.
- **Expected retrieval effect.** **Zero records lost.** The removed term matched nothing, so the retrieved set is identical before and after. **This is an empirical interface observation of 2026-11-14, not a guarantee of identical behaviour at a future execution**: PubMed's phrase index changes as records are added, and a phrase unmatched today could in principle be matched later. The claim is therefore about observed behaviour on a date, not about the query in perpetuity.
- **What is unchanged.** Sensitivity, precision, scope, the research question and the eligibility criteria are all unaffected. **No language, date, species or publication-type filter is introduced.** The outcome block drops from 44 to 43 terms; the exposure block is untouched.
- **Relationship to D023, which this does NOT amend.** **D023 concerns the omission of the study-design block and is untouched by this entry.** D024 concerns one ineffective quoted phrase in the outcome block. The two are deliberately kept distinct: D023's decision — that the primary search carries no design block — remains exactly as adopted, and no design term is introduced here.
- **Scope.** This is a correction to the **proposed** PubMed strategy. It is **not** authorisation to execute a formal search, does **not** register anything under D011, and does **not** resolve **P007**, which remains open with no database access beyond PubMed verified.
- **Applied in:** `docs/methods/recommended_search_strategy.md` §2 (the adopted query) and `docs/search/database_search_strategies.md` §3, which hold **byte-identical** copies and are tested for that; and `docs/reports/supplementary_material.md` S1.4, which reproduces the same term set in a **different line layout** for publication and is therefore tested for term equivalence rather than byte identity.
- **Deliberately NOT applied in:** the Embase, Scopus and Web of Science translations. Those carry platform-specific renderings of the phrase, **not** the exact PubMed term, and **the PubMed evidence does not transfer**: Scopus uses loose phrase matching and Web of Science exact matching, so the phrase may behave differently or correctly there. Removing it from those drafts on PubMed evidence would be unfounded. Each is an untested draft and is validated in its own interface (`docs/search/database_search_validation_checklist.md`).
- **Evidence:** `docs/search/phase_2k_manual_validation_log.md` §4.2 (reviewer's interface observation), §4.3 (per-line counts-only validation, 88/88 lines, 0 records retrieved), §12 (defect record) and §13 (proposal PC-1 as approved).
- **Relies on:** D011 (registration conventions), D023 (the strategy being corrected).


### D025 - Reference group: both definitions eligible, never-smoker primary (resolves P003)
- **Status:** ADOPTED 2026-11-14, on the reviewer's explicit authorisation.
- **Type:** protocol (eligibility / analysis)
- **Decision:** Both reference-group definitions are **eligible**. The comparator is recorded
  **verbatim** in `comparator_definition` and classified in `comparator_type` using the three
  existing enum values: `never_smoker`, `non_smoker_undefined`, `other`. The **primary analysis is
  restricted to studies with a `never_smoker` reference.** A **prespecified sensitivity analysis**
  adds studies with a `non_smoker_undefined` reference. Classification follows what the study
  states; a study that does not define its reference group is classified `non_smoker_undefined` and
  is **never promoted to `never_smoker` by inference**. A study whose reference group cannot be
  determined at all is excluded at full text under the existing reason code `no_reference_group`.
- **Fixed in advance to prevent a post-hoc primary analysis.** The never-smoker-reference analysis
  remains the primary analysis **irrespective of k**. If fewer than 3 studies contribute to it, the
  primary analysis is reported as **not estimable at k = n**; the mixed-reference analysis is
  reported as the prespecified sensitivity analysis, labelled as such, and is **never promoted to
  primary**. This rule is fixed before extraction and its entire value lies in having been fixed
  beforehand.
- **Rationale.** A reference group that may contain former smokers contains exposed people, so the
  contrast becomes exposed-versus-partly-exposed. Attenuation toward the null is the **plausible**
  consequence and is the reason the distinction is preserved and tested; it is **not guaranteed**,
  because its magnitude depends on the unreported proportion of former smokers in the reference
  group and on their time since quitting, neither of which is observable from the published data.
  Excluding such studies outright would discard information and select on reporting precision, which
  correlates with region - the dimension D009 was written to capture.
- **Interpretation.** The sensitivity analysis is a stability check, not a hypothesis test. The two
  estimates are compared descriptively; **no significance test is performed between them**, and
  non-overlapping intervals are not evidence of a reference-group effect.
- **Consequences.** Eligibility widens; no study is excluded for comparator wording alone.
  `comparator_type` is now a **settled** field: its `status: unresolved` and `depends_on: P003`
  markers are removed from `config/extraction.yaml`, so an off-list value is an error rather than a
  warning. One prespecified sensitivity analysis is added to the SAP. No new extraction field and no
  change to the enum values themselves.
- **Scope.** Does not alter D009, does not decide the contrast (D026), and does not decide the
  adjusted-model selection rule, which remains open.
- **Relies on:** D004, D008, D009, D010.


### D026 - Ever-versus-never as the primary contrast (resolves P004)
- **Status:** ADOPTED 2026-11-14, on the reviewer's explicit authorisation.
- **Type:** protocol (analysis)
- **Decision:** The **primary contrast is ever-smoker versus never-smoker.**
  **Current-versus-never** and **former-versus-never** are **prespecified secondary analyses**, each
  reported separately and neither designated co-primary. **One estimate per `study_id` per analysis**
  (D004); where a study reports several eligible contrasts, the contrast matching the analysis is
  selected, the selection is recorded in `selected_for_analysis` and `selection_rationale`, and
  estimates are **never averaged** across contrasts.
- **Dose-response.** Dose-response data are recorded at extraction as reported
  (`exposure_contrast = dose_tier`, with the existing `intensity_*`, `duration_*`, `pack_years` and
  `cumulative_*` fields) and are **presented narratively and in tabular form only.** **No pooled
  dose-response estimate is produced**, consistent with **D015 limitation (e)**, which records that
  no dose-response model is implemented. Any pooled dose-response analysis requires a **separately
  approved amendment to D015** and is **not** authorised by this decision.
- **No harmonisation.** Incompatible exposure categories are **never mapped onto a common category**.
  This restates **provenance rule 10** and **D003**; it is not a new rule. Where reported categories
  are not comparable across studies, the dose-response is described, not combined.
- **Rationale.** Ever-versus-never is the contrast most consistently reported, so it maximises
  contributing studies and minimises selection on reporting. Current-versus-never is biologically
  sharper but is vulnerable to reverse causation in case-control designs where diagnosis prompted
  quitting, which is a reason to report it separately rather than make it primary. Harmonising dose
  categories across studies would require assumptions about within-category exposure distributions
  that the published data do not support.
- **Consequences.** `exposure_contrast` is now a **settled** field: its `status: unresolved` and
  `depends_on: P004` markers are removed from `config/extraction.yaml`, so an off-list value is an
  error rather than a warning. All five enum values are already implemented, so the value list itself
  is unchanged. `select_one_per_study()` becomes executable instead of refusing. Two secondary
  analyses join the prespecified set.
- **Scope - what remains open.** This decision fixes the contrast only. It does **not** decide the
  **primary effect measure**, nor **whether case-control and cohort estimates may be pooled at all**.
  That question is marked *(evidence)* in the statistical analysis specification and is genuinely
  undecidable until the included studies are known; it **remains open** and SAP section 2 is **not**
  complete. It does not decide the adjusted-model selection rule.
- **Relies on:** D003, D004, D009, D015, D025. **Provenance rule:** 10.


### D027 - The original v1 search date is unrecoverable; the v1r date awaits the researcher (resolves P009)
- **Status:** ADOPTED 2026-11-14, on the reviewer's explicit authorisation.
- **Type:** reporting (search provenance)
- **Decision - `pubmed_v1`.** The execution date of the original v1 PubMed search is recorded as
  **unknown and not recoverable** unless primary evidence is obtained. It is reported under PRISMA-S
  as unknown. `config/sources.yaml` retains `search_date: null` for `pubmed_v1` alongside
  `status: export_missing`.
- **Decision - `pubmed_v1r`.** The re-execution's `search_date` **also remains `null`** and is **not
  populated until the reviewer personally verifies the actual execution date from their own record.**
  It is **not** inferred from the 2026-10-29 count interrogations documented in
  `search_v1r_pubmed_reexecution.md`, **not** from file timestamps, and **not** from the Entrez dates
  in the export, which bound the execution at >= 2026-10-25 but do not date it. Whether the export
  download and the 2026-10-29 count interrogations were one execution or two **is not established by
  anything in the repository**, and shall not be assumed.
- **Researcher verification required, recorded explicitly.** Populating `pubmed_v1r.search_date` is
  an outstanding action on the reviewer. Until it is done, the search date for the execution that
  produced **all 194 screened records** is unrecorded, and PRISMA-S reporting of that search is
  incomplete. This is a known, declared gap, not an oversight.
- **Rationale.** Every candidate source for the v1 date is a bound or a proxy on a different event:
  the export's Entrez dates bound the re-execution, file timestamps bound file operations, and the
  pause date bounds the project. A declared unknown is reportable under PRISMA-S; a reconstructed
  date is a fabricated provenance claim under provenance rule 5. The same reasoning is applied to the
  re-execution: its date is recoverable in principle, but only from the researcher, not by inference.
- **Consequences.** No eligibility, extraction or analysis consequence. Two declared gaps in the
  PRISMA-S search record: one permanent (v1), one pending the reviewer (v1r).
- **Recovery.** The only documented route for the v1 date is the researcher's own NCBI account search
  history (`docs/methods/obtaining_exports.md`). If either date is later obtained from a primary
  source, it is recorded as a **new dated amendment naming that source**, never by editing this entry.
- **Relies on:** D005, D011, D012, D013. **Provenance rule:** 5.


### D028 - Synthetic content: the absolute prohibition is retained and the demonstration is removed (resolves P010)
- **Status:** ADOPTED 2026-11-14, on the reviewer's explicit authorisation (Option B).
- **Type:** provenance rule (confirmation of rule 6 and D007)
- **Decision.** **Provenance rule 6 is retained in full and is NOT amended.** No placeholder data,
  synthetic study results or invented citations exist anywhere in the repository. No carve-out for
  labelled demonstration artefacts is created.
- **Test fixtures - the strict reading is confirmed.** Tests use MEDLINE-format fragments and
  structural stubs carrying **no bibliographic content**, created in pytest temporary directories
  only. No test writes a synthetic file under `data/`. This confirms existing practice and D007; no
  test fixture change is required.
- **The synthetic demonstration is removed.** Rule 6 as written stated that synthetic study results
  exist nowhere in the repository, while a synthetic pooled odds ratio and a synthetic forest plot in
  fact existed in `docs/` and `results/`. The conflict is resolved in favour of the rule: the
  demonstration is removed so that rule 6 is true as written, rather than the rule being weakened to
  accommodate the artefact. Removed: **Appendix H** of the official report; **section 14.8** of the
  research project report; the two speaker-note references to the demonstration; and
  `results/final_submission/figures/synthetic_forest_demo.png`. The affected DOCX, PDF and PPTX
  deliverables are rebuilt from the corrected sources.
- **What is deliberately NOT removed.** Every statement describing the software's *refusal* to handle
  synthetic data is genuine documentation of a safeguard and is retained: `validate_set` refusing to
  pool synthetic with real estimates; `run_analysis.py` refusing any row marked synthetic; the
  `synthetic` flag propagating into results; the watermarking mechanism itself; and the descriptions
  of these safeguards in `docs/methods/analysis_validation.md`, `docs/methods/extraction.md` and the
  statistical analysis specification. **No research finding is removed, because the reports contain
  none** - the removed values were invented and were labelled as such.
- **Historical records preserved.** `results/final_submission/COMBINED_REPORT_QA_SUMMARY.md` is left
  **unchanged**. It is a dated record of what was verified on 14 November 2026 against the build that
  existed then, and it is not rewritten to describe a build made later. This entry is the record that
  the build it describes was superseded.
- **Citation correction.** The register's P010 entry cited "rule 20". `docs/protocol/provenance_rules.md`
  contains **19** numbered rules; there is no rule 20. The operative rules are **5** (no fabrication)
  and **6** (no synthetic content). D007 cited rule 6 correctly.
- **Consequence accepted.** The deliverables lose their only demonstration that the implemented
  statistical machinery runs end to end. That evidence now rests on the test suite
  (`docs/methods/analysis_validation.md`), which is verified against hand-worked arithmetic and
  published formulas and contains no bibliographic or research content.
- **Relies on:** D003, D007, D015. **Provenance rules:** 5, 6.


### D029 - The v1 count residual is disclosed exactly and never reconciled (resolves P012)
- **Status:** ADOPTED 2026-11-14, on the reviewer's explicit authorisation.
- **Type:** reporting (search provenance)
- **Decision.** The three counts **138**, **194** and **150** are **preserved exactly as recorded**
  and none is altered. Specifically, **138 is not changed to 194, 150 or 147**, and 194 and 150 are
  not adjusted toward 138. Altering a recorded count to achieve reconciliation would falsify the
  history of the search.
- **The decomposition, stated exactly.** Against the re-execution of the identical query string on
  2026-10-29: **194 - 44 - 3 - 138 = 9.** That is, 194 records unfiltered; **44** attributable to the
  two filters absent from the re-execution (194 -> 150); **3** added to PubMed on or after the
  2026-09-20 pause (150 -> 147); leaving a residual of **exactly 9 records** against the documented
  138. **If the 3 post-pause records are not attributed, the residual is exactly 12** (150 - 138).
  The review reports the **9-record residual under the decomposition above** and names that
  decomposition wherever the figure appears.
- **Exact difference, unverified baseline.** The residual is an **exact arithmetic difference**, not
  an approximate one: 194 equals the export's record count exactly, and 150 equals the count
  predicted from the export's own language and MeSH tags. **138 is an unverified historical
  documented claim** - it is what was recorded at the time, and no export survives against which to
  check it. The residual therefore inherits the uncertainty of 138, not of the arithmetic.
- **Disclosed, not reconciled.** The residual is reported in the search-reporting section of the
  manuscript. The two candidate explanations - that records not MEDLINE-indexed at the time of the
  original search have since acquired the MeSH term `Humans` and thereby entered the filtered set, or
  that 138 was approximate - **cannot be distinguished** without the original export or the original
  search date (D027). **No explanation is adopted and no preference between them is recorded.**
- **Scope.** Affects only how the search history is reported. The screened corpus comes from
  `pubmed_v1r` (194 records, D013), so **no eligibility decision, extracted value or estimate depends
  on this residual.** If the lost export or the v1 date is ever obtained, the residual is revisited as
  a **new dated amendment**.
- **Relies on:** D005, D011, D013, D027. **Provenance rules:** 5, 7.


## Proposed — implemented, awaiting the reviewer's adoption

These three entries describe changes that are implemented and tested in the repository. They are
recorded here as **proposed**: the reviewer has approved the implementation, and adoption of the
wording below remains theirs. Nothing in this section is cited elsewhere as settled.

### D016 — Adopting a suggestion does not satisfy a decision field (operational enforcement of D010)
- **Status:** Proposed — awaiting the reviewer's adoption.
- **Type:** protocol
- **Decision:** `decision_basis` is required on every recorded screening decision and takes one of
  two values: `adopted_from_suggestion`, meaning the reviewer accepted an automated suggestion
  without judging the record individually, or `independently_adjudicated`, meaning the reviewer
  judged the record from its own evidence. A stage holding any `adopted_from_suggestion` row is
  **not** a screened stage: `validate_screening --final` refuses it, the PRISMA flow reports the
  two counts separately and carries a banner stating that the outcome is proposed rather than
  completed, and building the full-text worksheet from adopted includes warns by default and is
  refused under `--final`.
- **Rationale:** D010 states that an automated pre-sort "can never satisfy a `decision` field".
  Before this entry the repository recorded that distinction as a label and acted on it nowhere:
  the final gate certified a stage in which no record had been adjudicated, and the PRISMA flow
  reported 194 screened and 85 sought for retrieval without qualification. A label that nothing
  enforces documents a violation rather than preventing one.
- **Basis:** D010; PRISMA 2020 item 8, which requires automation tools used in the process to be
  reported.
- **Impact:** **This is forward-only enforcement and does not erase the historical provenance
  violation.** The 194 title/abstract decisions recorded on 2026-11-01 remain suggestion-derived
  and are now marked as such in the data. Under this entry the count of independently adjudicated
  records is **0 of 194**, the title/abstract stage cannot be declared final, and the full-text
  stage cannot be built under the final gate until records are adjudicated. The blinded
  verification sample is the mechanism by which that changes. Both facts must be reported in the
  manuscript's methods and limitations.

### D017 — The suggested reason code is preserved alongside the recorded one
- **Status:** Proposed — awaiting the reviewer's adoption.
- **Type:** protocol
- **Decision:** The title/abstract worksheet carries `suggestion_reason_code` beside `suggestion`.
  A decision counts as `adopted_from_suggestion` only when **both** the decision and its reason
  code match what was suggested; a reviewer who keeps the verdict but changes the reason has
  adjudicated, and the row records `independently_adjudicated`.
- **Rationale:** Without the column, a reviewer who kept `exclude` but changed the reason from
  `wrong_outcome` to `wrong_design` left no trace: the validator saw a decision matching its
  suggestion and passed. The reason code carries the methodological content of an exclusion and
  drives the PRISMA exclusion tally, so a change to it is a judgement that must be visible.
- **Basis:** D010; the reason-code vocabulary fixed in `docs/protocol/eligibility_criteria.md`.
- **Impact:** The 194 values were backfilled exactly from the committed audit artefact
  `data/screening/ta_suggestions_2026-11-01.csv`; 109 exclusions carry a suggested reason and 85
  includes correctly carry none, and all 194 match the recorded `reason_code`. No recorded value
  was altered. Nothing was inferred.

### D018 — Full-text decisions record their basis
- **Status:** Proposed — awaiting the reviewer's adoption.
- **Type:** protocol
- **Decision:** The full-text worksheet carries `decision_basis`, required whenever a full-text
  decision is recorded. It does **not** carry `suggestion` or `suggestion_reason_code`, because no
  suggestion mechanism exists at full text.
- **Rationale:** A column meaning "how was this decided" that exists at one stage and not the next
  invites the reading that full-text decisions need no such account. Adding it while the worksheet
  is empty costs nothing; adding it after decisions are recorded would mean migrating the
  reviewer's own work.
- **Impact:** The 85 full-text rows gained one column and nothing else; every reviewer field was
  empty before and remains empty. Full-text decisions will record
  `independently_adjudicated`, which is the positive evidence the review needs.

### D019 — The PRISMA flow reports adjudicated outcomes; provisional outcomes are reported separately
- **Status:** Proposed — awaiting the reviewer's adoption.
- **Type:** protocol (reporting)
- **Decision:** The formal PRISMA 2020 flow counts **independently adjudicated decisions only**.
  Records carrying a decision adopted from an automated suggestion are reported in a separate
  section headed "Provisional screening outcome — NOT part of the PRISMA flow", which states the
  provisional decision, exclusion, inclusion and unresolved counts and the provisional exclusion
  reasons. A record leaves the provisional section the moment it is independently adjudicated,
  and its original suggestion remains recorded in the worksheet. Acquisition and deduplication
  counts are unaffected: they describe files and records, not judgements. The diagram keeps its
  PRISMA 2020 structure and carries the provisional total as an annotation **outside** the flow.
- **Rationale:** The cells of a PRISMA flow mean completed screening outcomes. Reporting 109
  exclusions and 85 reports sought alongside a note saying none had been adjudicated left the
  numbers making a stronger claim than the prose, and a reader extracting the flow would have
  carried that claim forward. Separating the two makes the figure safe to quote.
- **Basis:** PRISMA 2020 flow diagram; D010; D016.
- **Impact:** **The formal flow currently reports 0 screened, 0 excluded and 0 sought for
  retrieval**, against 194 provisional decisions (109 provisionally excluded, 85 provisionally
  taken forward). That is the truthful position until records are adjudicated, and it will change
  only as adjudication proceeds. Five identities are enforced so the two views cannot drift:
  adjudicated + provisional + not screened equals the worksheet; formal screened equals
  adjudicated; provisional decisions sum to the provisional total; formal reports sought cannot
  exceed adjudicated includes; provisional full-text rows cannot exceed provisional includes.
- **Existing full-text worksheet:** `data/screening/screening_ft.csv` was built at `94f5e09` from
  85 title/abstract includes that are all provisional. It is retained unchanged apart from a
  derived column, `source_ta_decision_basis`, which records how each source title/abstract
  decision was made. All 85 rows carry `adopted_from_suggestion`. The column is recomputed on
  every refresh, so adjudicating a source record promotes its full-text row from the provisional
  count to the formal one without manual intervention. No full-text decision, reason code,
  reviewer or date was populated.

## Pending — require the review team's decision

**P014–P022 are the anatomical and histological decisions.** The evidence for them, with sources,
access dates and the distinction between verified facts and interpretation, is in
`docs/protocol/anatomical_histological_scope.md`. Recommendations are in
`docs/methods/protocol_decisions_for_researcher.md`. **None is adopted**; D008 remains the
operative outcome definition until the reviewer decides.

| ID | Question | Why it matters | Needed before |
|---|---|---|---|
| P003 | *Resolved by **D025*** — both reference definitions eligible; `never_smoker` is the primary analysis, `non_smoker_undefined` a prespecified sensitivity analysis, never promoted to primary. | — | — |
| P004 | *Resolved by **D026*** — ever-versus-never primary; current and former secondary; dose–response narrative and tabular only, never pooled (D015(e)). | — | — |
| P006 | Protocol registration (e.g., PROSPERO) before screening begins? | Registration after screening weakens the protocol/post-hoc distinction. | Screening |
| P007 | Additional databases (Embase, Scopus/Web of Science) and supplementary methods (reference lists, citation searching); constrained by institutional access. | Search sensitivity; PRISMA/MOOSE expectations. | Search v2 |
| P008 | *Resolved by **D015*** — Python + SciPy, with no claim of R/`metafor` cross-validation. | — | — |
| P009 | *Resolved by **D027*** — the v1 date is unknown and unrecoverable; `pubmed_v1r.search_date` stays `null` pending the reviewer's personal verification. | — | — |
| P010 | *Resolved by **D028*** — provenance rule 6 retained in full with no carve-out; the synthetic demonstration is removed from the repository. The former wording cited "rule 20"; there is no rule 20, and the operative rules are **5** and **6**. | — | — |
| P011 | *Resolved by **D013*** — retrieve unfiltered, apply language and species limits at screening. | — | — |
| P012 | *Resolved by **D029*** — 138, 194 and 150 preserved exactly; the residual is stated exactly as 194 − 44 − 3 − 138 = 9, or 12 if the 3 post-pause records are not attributed; 138 is an unverified historical documented claim; disclosed, never reconciled. | — | — |
| P014 | **Eligible oral-cavity subsites.** Adopt an explicit subsite list rather than a code range? `C02–C06` is unsafe: it admits C02.4 (lingual tonsil) and C05.1/C05.2 (soft palate, uvula). | Determines which studies are eligible at full text. | Full-text screening |
| P015 | **Lip (C00).** Part of the primary outcome, excluded on aetiological grounds, or included with separate and sensitivity analysis? Lip **is** anatomically oral cavity, so excluding it is a deliberate choice. The external/mucosal split is codeable for C00.0–C00.5 but not for C00.6/C00.8/C00.9. | Changes the evidence base and the primary estimate. | Full-text screening |
| P016 | **Soft palate and uvula (C05.1, C05.2).** Adopt the TNM convention (oropharynx) or NCIt's anatomical description (posterior oral cavity)? The sources genuinely conflict; the protocol must state which convention it adopts rather than assert a fact. | Determines eligibility for a whole subsite group. | Full-text screening |
| P017 | **Straddling unspecified/overlapping codes:** C02.8, C02.9, C05.8, C05.9, C06.80. Exclude, or include under a stated assumption? These cannot be assigned to a compartment from the code alone. | Affects borderline studies and the PRISMA exclusion counts. | Full-text screening |
| P018 | **Registry-grouped studies.** SEER's "Tongue" (C019–C029) and "Gum and Other Mouth" groups mix eligible and ineligible subsites. Exclude as non-separable, or include with contamination documented? | A strict rule may exclude good studies for reporting coarsely — selection on reporting quality. | Full-text screening |
| P019 | **Site-purity threshold.** D008 sets a ≥90% threshold for histology but none for anatomy. Adopt a parallel site threshold, or stratify a sensitivity analysis by reported purity? No threshold can be calibrated from available evidence. | Determines handling of mixed-site studies. | Extraction / SAP |
| P020 | **Definition of "separately reported"** in D008: does it require a site-specific **effect estimate**, or do site-specific **case counts** suffice? | Changes whether multi-site studies are eligible. | Full-text screening |
| P021 | **SCC variants.** Do verrucous (8051/3), basaloid (8083/3), papillary (8052/3) and spindle-cell squamous (8074/3) count as SCC for the ≥90% rule? | Determines histological eligibility. **Requires the WHO Blue Book, which was inaccessible.** | Extraction |
| P022 | **Non-SCC and borderline entities.** Adenosquamous (8560/3) and sarcomatoid NOS (8032/3, 8033/3) excluded but retained in the ≥90% denominator? Is primary SCC of a **minor** salivary gland eligible — C06.9 explicitly admits "minor salivary gland, unspecified site"? | Determines histological eligibility. **Requires the WHO Blue Book.** | Extraction |
| P013 | *Resolved by **D023*** — no study-design block in the primary search; the corrected PubMed strategy retrieves 8,190 records rather than 5,008, and the number of additional eligible studies recovered is unknown and may be zero. | — | — |
| P023 | **Risk-of-bias instrument.** Which instrument applies to case–control and cohort studies: **(a)** Newcastle–Ottawa Scale, **(b)** ROBINS-E, or **(c)** Newcastle–Ottawa reported per domain with no total score? And which confounders must a study address for the comparability/confounding domain to be judged adequate — alcohol alone, or alcohol together with smokeless tobacco and betel quid per D009? | Determines what the reviewer must look for in every included study, and whether the SAP's risk-of-bias subgroup (§4) and sensitivity (§5) analyses are executable at all. Changing instrument after assessment begins means reassessing every study. Options, trade-offs and a recommendation: `docs/methods/risk_of_bias_options.md`. | Before any study is appraised |
