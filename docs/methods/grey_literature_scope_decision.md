# Grey literature — scope decision memorandum

**Status: APPROVED by the researcher (12 November 2026) and RECORDED in the decision register as
D022 (13 November 2026).**

Two things are deliberately held apart throughout and must not be conflated in any later report:

| | |
|---|---|
| **Approved** | The *methodology* — what will be searched, how it will be bounded, how records will be screened and linked. Section 1A. |
| **Not approved, because not yet known** | The *access* on which several sources depend. **No repository in section 2.1 has been verified as reachable.** Approving a method of searching a source is not evidence that the source can be searched. |

P007 is unchanged, `config/screening.yaml` and `config/extraction.yaml` are unchanged, no existing
decision was altered, and P013 is not begun. The register gained **one new entry, D022** (section
11), authorised separately on 2026-11-13; that insertion is purely additive. No search
was executed, no record retrieved, and **no repository, database or website was accessed in
preparing or revising this document**. No search date, yield, record count or accessibility status
is asserted for any source.

**Prepared:** 12 November 2026. **Revised twice and approved:** 12 November 2026.
**Repository state:** `HEAD` `b5afaff`; no commit made.

---

## 1A. Researcher approval — what was approved

Approved 12 November 2026. The ten choices below are the approved methodology; the detailed wording
that implements them is section 8.

| # | Approved choice | Implemented in |
|---|---|---|
| 1 | **Approach B** — bounded supplementary grey-literature searching | §1, §8 |
| 2 | **South Asian theses and dissertations prioritised** | §2.1, §2.2 |
| 3 | **Government and registry reports used primarily as discovery sources** | §5 |
| 4 | **Bounded supplementary Google Scholar searching** | §3 |
| 5 | **First-200-record and 50-consecutive-non-hit stopping rules**, explicitly described as **operational choices, not established standards** | §3.1, §3.2 |
| 6 | **Reference-list and forward-citation searching where accessible** | §8 |
| 7 | **Existing eligibility criteria applied consistently** to all potentially eligible records | §2.4 |
| 8 | **Thesis and article reports linked through one `study_id` with separate `report_id`s** | §6 |
| 9 | **No double-counting of participants or estimates** | §6.2 |
| 10 | **Existing extraction schema retained**, with the structured `src:` convention in `studies.notes` for study-level provenance (**Option A**) | §4 |

### Approved provenance safeguard

Option A is retained **provisionally**, with a mandatory stop:

> **If more than three included studies have conflicting reports for a study-level variable,
> extraction STOPS before it is finalised**, and a structured provenance-schema proposal is
> presented for researcher approval. **The schema extension is not implemented automatically**, and
> no change is made to `config/extraction.yaml` without explicit authorisation.

This converts the trigger from a recommendation into a hard stop. The condition is counted during
extraction and the count is recorded, so the trigger cannot pass unnoticed.

### Approved decision documentation

- This is recorded as a **separate methodological decision, not as part of P007**.
- **Recorded as D022**, not D021 — see section 11 for why `D021` must not be
  taken by default.
- **The register entry was authorised separately and written on 2026-11-13** (section 11).

---

## 1. Final approved approach

**Approach B: a bounded supplementary grey-literature search.** In summary:

| Element | Position |
|---|---|
| **South Asian theses and dissertations** | **The priority source.** Shodhganga, RGUHS, named institutional repositories, NDLTD — each conditional on an accessible interface |
| **Government and registry reports** | **Discovery sources only.** Consulted for their reference lists; prevalence-only and incidence-only reports are never included as evidence of the association |
| **Google Scholar** | **Bounded, supplementary, and explicitly not reproducible.** Operational stopping rule fixed in advance; does not replace a bibliographic database |
| **Citation searching** | Reference-list and forward-citation checking, already specified under P007, which reaches grey sources as well as published ones |
| **Eligibility** | **The existing criteria and the existing exclusion vocabulary, applied unchanged.** No new code; no latitude for being unpublished |
| **Thesis/article pairs** | Linked to **one underlying study** where they describe the same participants; all contributing reports preserved |
| **Double counting** | Prevented at the analysis boundary by `selected_for_analysis` and D004, not by discarding reports |

The case rests on one fact about this review rather than on general practice. D009 admits bidi,
chutta, cigars, pipes and reverse smoking, not cigarettes alone, and the studies that make D009
worth having are concentrated in South Asia — where hospital-based case–control studies of tobacco
habits and oral cancer frequently appear first, or only, in postgraduate dissertations. A search
confined to indexed journals is least sensitive exactly where this review is most distinctive.

Approach A leaves that unaddressed. Approach C is rejected: its marginal sources are
disproportionately those that will fail the English-language criterion (D013) or lack an effect
estimate, and an unbounded search is the one most likely to be begun and not finished under
single-reviewer screening (D010).

---

## 2. Theses and dissertations

### 2.1 Which sources are realistically searchable

**None of the following has been accessed, searched or tested by this project.** Each is listed on
the basis of its documented purpose and interface type; each carries an accessibility status of
**unverified**. The researcher must confirm reachability before any is relied upon, and record the
outcome either way.

| Source | What it holds | Realistically searchable? | Status |
|---|---|---|---|
| **Shodhganga** (INFLIBNET) | Indian doctoral theses deposited by participating universities | **Most promising single source.** Designed to be publicly searchable; coverage doctoral, dependent on university participation | Unverified |
| **RGUHS digital repository** | Karnataka health-science dissertations, including dentistry | **Potentially high value** for MDS dentistry dissertations, the design of interest; coverage state-level | Unverified |
| **University institutional repositories** (dental and health-science colleges) | Local MDS/MD dissertations, often not deposited nationally | **Variable**, and not systematically enumerable; useful where a specific institution is known to publish relevant work | Unverified |
| **NDLTD** | International aggregated thesis metadata | Moderate; metadata-level, full text depends on the holding repository | Unverified |
| **IndCat / union catalogues** | Bibliographic records of Indian theses | Low; catalogue records rarely carry the abstract needed to screen | Unverified |
| **ProQuest Dissertations & Theses** | International, strong North American coverage | **Not listed among the stated institution's subscriptions** (P007 memorandum) | **No evidence of access** |

**Priority if effort must be limited:** Shodhganga → RGUHS and named dental-college repositories →
NDLTD. ProQuest is excluded on access grounds unless that changes.

**A ceiling to report rather than work around.** MDS dissertations — the richest likely source of
eligible case–control studies — are **master's-level work, while Shodhganga is principally a
doctoral repository**. The most relevant body of work may therefore sit in institutional
repositories that cannot be enumerated systematically. This limits what any thesis search can
achieve and should be stated as a limitation, not concealed by listing more repositories than will
actually be searched.

### 2.2 How search terms are documented

Thesis repositories support neither the Boolean syntax, the field tags nor the controlled vocabulary
the PubMed strategy relies on. **The PubMed query cannot be transferred** and must not be presented
as though it were. For each repository the following is recorded at the time of searching:

repository name and URL; interface used (search box, browse-by-subject, browse-by-university); **the
exact character string entered, verbatim**; any field restriction (title, abstract, subject, full
text); any filter (year, department, degree, language); the date searched; the number of records
examined; the number carried forward; and whether the interface failed or was unreachable.

Because interfaces differ, a **simplified term set** is used rather than one query, combined as each
interface permits:

- Outcome: `oral cancer`, `oral squamous cell carcinoma`, `OSCC`, `mouth neoplasm`, `oral carcinoma`
- Exposure: `tobacco`, `smoking`, `bidi`, `beedi`, `smokeless`, `reverse smoking`, `chutta`
- Design, where supported: `case control`, `cohort`, `risk factor`

Both `bidi` and `beedi` spellings are searched. Where an interface permits one term at a time, each
run is recorded as its own line in the search record.

### 2.3 Language and accessibility

**Language.** Eligibility is English-language only (D013), applied at screening with a recorded
`not_english` reason rather than by an unreliable interface filter. Indian postgraduate
dissertations are predominantly in English, so the criterion binds less here than it would for Latin
American sources — part of why South Asian theses are the priority and Portuguese- and
Spanish-language repositories are not pursued. **Searching sources whose output will be excluded on
language is workload without yield.**

**Accessibility.** Three failure modes, each with a recorded response:

| Failure | Response |
|---|---|
| Repository unreachable or interface broken | Record the attempt, date and outcome; report it. **An unreachable source is a finding, not an omission** |
| Record found, full text restricted or embargoed | Record as identified. If eligibility cannot be determined, report it as **undetermined** — never as an exclusion on a criterion that was never assessed |
| Full text available but no extractable data | Screened normally; excluded as `no_usable_data` at full text |

### 2.4 Eligibility assessment

Grey-literature records are assessed against **the same criteria and the same controlled vocabulary
as database records**, by the same reviewer, with the same recorded decision basis. Being
unpublished earns no latitude, and no record is included on the grounds that it is hard to find.

The existing codes cover every case. **No new code is proposed and no change to
`config/screening.yaml` is requested** — the `editorial_or_commentary` suggestion in the first draft
is withdrawn, editorials and letters being handled by `wrong_design`.

| Situation | Existing code | Stage |
|---|---|---|
| Narrative, systematic or meta-analytic review | `review_or_meta` | ta, ft |
| Editorial, commentary, letter | `wrong_design` | ta, ft |
| Prevalence-only or incidence-only report | `no_usable_data` | ft |
| Thesis reporting an already-included population and adding nothing | `duplicate_publication`, linked to the retained `report_id` | ft |
| Abstract too thin to extract reliably | `conference_abstract` | ta, ft |
| Not in English | `not_english` | ta, ft |
| Oral cavity pooled with other head-and-neck sites | `outcome_not_separable` | ft |

---

## 3. Google Scholar — operational protocol

### 3.1 Four statements that must accompany any use of this source

1. **The thresholds are not established systematic-review standards.** The figures 200 and 50 are
   **arbitrary**. They are drawn from no guideline, are not a convention, and no evidence
   establishes them as optimal. Their sole justification is that they are **fixed in advance,
   applied uniformly and reported**, which converts an open-ended search into a bounded and
   declarable one. A different pair would be equally defensible. What would not be defensible is
   deciding when to stop while searching.
2. **Google Scholar relevance rankings are unstable.** Ordering varies with time and may vary
   between users; the service caps retrievable results at roughly the first thousand per query
   regardless of how many it claims to match.
3. **Search date, exact query, sorting, result count and stopping reason must be recorded** for
   every query — see the table below.
4. **Google Scholar is supplementary and does not replace a bibliographic database.** It contributes
   no controlled vocabulary, no reliable field searching and no stable result set. It is searched
   last, and no coverage claim rests on it.

**No claim of reproducibility is made for this source.** Even fully bounded and documented, a Google
Scholar search is **reportable but not repeatable**: a reader redoing it later will not obtain the
same ordered list. This is a limitation of the method and is reported as one. It is precisely why
the source is placed last and why nothing depends on it alone.

### 3.2 Exact specification

| Element | Specification |
|---|---|
| **Queries** | Five short phrase queries, run separately, each recorded on its own line. Scholar's query length is limited and its Boolean support weak — `OR` must be capitalised, nesting is unreliable, there is no truncation operator — so one compound string is not used: 1. `"oral cancer" tobacco case-control` 2. `"oral squamous cell carcinoma" smoking risk` 3. `"oral cancer" bidi` 4. `"oral cancer" "reverse smoking"` 5. `"oral squamous cell carcinoma" thesis tobacco` |
| **Sorting** | **Sort by relevance** (the default), not by date. Recorded explicitly, because the two give different sets under a first-200 bound |
| **Settings** | "Include patents" and "include citations" **disabled** — both return records that cannot be screened. 20 results per page, so the bound is a whole number of pages |
| **Date range** | **No date limit.** The literature spans decades; an arbitrary cut-off would lose older case–control studies |
| **Date searched** | Recorded for each query, to the day. Not asserted anywhere in advance |
| **Screening** | **Title first**, in displayed order. Any title that could plausibly describe an eligible study is opened and screened on abstract or full text. Clearly ineligible titles — wrong disease, wrong species, treatment or survival studies — are counted as examined and not opened |
| **Stopping procedure** | Per query, stop at whichever comes first: (a) **200 results examined**; (b) **50 consecutive results yielding nothing potentially eligible**, the counter resetting to zero whenever a record is carried forward; (c) the list ends |
| **Recorded per query** | Query string verbatim; sort order; settings; **date searched**; **number of results examined**; **which stopping condition triggered**; number carried forward |
| **Deduplication** | Carried-forward records enter the normal pipeline and are deduplicated against database records on the existing identifier hierarchy before screening |

---

## 4. Study-level provenance

### 4.1 What the schema already supports — inspected

Inspection of `config/extraction.yaml` as it currently stands (34 study fields, 47 estimate fields)
gives a more precise answer than the previous draft, and narrows the gap considerably.

| Scenario variable | Field | Table | Per-report provenance? |
|---|---|---|---|
| **Sample size** | `n_total`, `n_cases`, `n_controls`, `person_years` | studies | **No** — `notes` only |
| **Adjusted effect estimate** | `estimate`, `adjustment`, `adjusted_for`, and the seven `adjusted_*` flags | estimates | **Yes** — `report_id` + required `source_location` |
| **Exposure definition** | `exposure_definition`, `exposure_category`, `product_types`, `exposure_contrast` | **estimates** | **Yes** — already fully attributed |
| **Exposure ascertainment** (how smoking status was ascertained) | `exposure_ascertainment` | studies | **No** — `notes` only |

**The third scenario variable is not a study-level problem at all.** Exposure definitions live in the
**estimates** table, carry their own `report_id`, and require a `source_location`. Where a thesis and
its article define exposure differently, those are simply **two estimates with different
`exposure_definition` values and different `report_id`s** under one `study_id` — fully recorded
today, with no convention and no schema change. If only one may enter the analysis,
`selected_for_analysis` and `selection_rationale` record which and why.

**The real gap is narrower:** roughly twenty *descriptive* study-level fields — sample sizes,
recruitment period, age and sex summaries, outcome and exposure ascertainment, matching variables,
histology confirmation, anatomical sites, case definition, setting and design detail — have no
per-field source column. `primary_report_id` is singular ("The report used for extraction").

**What the gap actually costs.** These fields feed the **characteristics-of-included-studies table**,
the **risk-of-bias assessment** and **subgroup definitions**. They do **not** feed the pooled
estimate, whose every input is estimate-level and fully attributed. So the consequence of imperfect
study-level provenance is a characteristics table and a bias assessment whose sources cannot be
traced field by field — a transparency cost, not a numerical one.

**How often will it arise?** Only when a study has more than one contributing report **and** they
disagree on a descriptive variable. With no study yet included, the count is unknown and is not
estimated here. It may well be zero.

### 4.2 Option A — retain the schema, prescribe a convention in `notes`

A structured, prescribed convention rather than free prose:

```
src: n_total=R0042; n_cases=R0042; exposure_ascertainment=R0042
```

— each entry naming a study-level field and the `report_id` it was taken from, listed only where
that report is **not** `primary_report_id`. Silence means "from the primary report".

| | |
|---|---|
| **Cost** | None. No schema change, no regeneration of the workbook, no validator work, no test changes, no tracked config touched |
| **Reproducibility** | **Partial.** The information is present and human-readable, and an auditor reading `notes` can reconstruct provenance |
| **Weakness** | `notes` is documented as "Free text" and **nothing enforces the convention**. The validator cannot check it, the data dictionary cannot describe it as structured, and a query cannot reliably extract it. It depends entirely on reviewer discipline, and a single lapse is invisible |
| **Honest characterisation** | A documented habit, not a verified property. In a project whose discipline is "assert it, don't assume it", this is the uncomfortable part |

### 4.3 Option B — a minimal schema extension

One added field on `studies`:

```yaml
field_sources: {type: list, description: "Study-level fields taken from a report other than
  primary_report_id, as field=report_id pairs; empty when all come from the primary report"}
```

| | |
|---|---|
| **Cost** | Modest but real: `config/extraction.yaml` is a tracked config; the workbook regenerates (34 → 35 study fields, data dictionary 93 → 94); the auditor's expected counts change; tests change. All mechanical, and the generator is deterministic, so the change is verifiable |
| **Reproducibility** | **Materially better.** A declared column appears in the data dictionary, is visible in the template, and can later be validated. Provenance becomes a property of the record, not of the reviewer's habits |
| **Weakness** | Still free-text in content unless a validator is written. Adds a column that may hold nothing — the project's own discipline is not to build structure for evidence that does not exist |
| **Honest characterisation** | The right answer if thesis/article pairs turn out to be common; over-engineering if they turn out to be rare or absent |

### 4.4 Approved position on provenance

**APPROVED: Option A, provisionally, with a mandatory stop at the trigger.** The researcher's
safeguard is stricter than the recommendation below: on trigger, extraction **stops before it is
finalised** and a schema proposal is presented. The extension is **never implemented
automatically**, and `config/extraction.yaml` is not touched without explicit authorisation.

> **Operational consequence.** The number of included studies whose contributing reports disagree on
> a study-level variable is **counted and recorded during extraction**. At four, extraction halts
> pending a decision. Because the count is recorded rather than noticed, the trigger cannot pass
> unobserved — which is the point of fixing it in advance.

The reasoning that led here is retained below, including the argument against it, so that a later
reader can see what was weighed.

**Original recommendation: Option A now, with a stated trigger to revisit.**

The reasoning is proportionality, and it is finely balanced rather than obvious. The gap touches
descriptive fields only; the analysis inputs are already fully attributed; no study is yet included,
so the frequency is unknown and may be zero; and the whole extraction workbook currently ships as
empty templates precisely because the project declines to build structure ahead of evidence. Adding
a column for a case that may never occur runs against that discipline.

**The trigger, stated in advance so the choice is not deferred indefinitely:** if more than **three
included studies** turn out to have multiple contributing reports that disagree on a study-level
variable, Option B should be adopted at that point and the `notes` entries migrated. Fixing the
threshold now is what stops Option A becoming a permanent default by inertia.

**The argument against this recommendation, stated fairly:** Option B is cheap, mechanical and
verifiable, and adopting it before extraction begins avoids migrating anything later. A researcher
who expects a substantial thesis yield should choose B straight away, and that would be a sound
decision rather than a concession. **This is the researcher's call, and the memorandum does not
presume it.**

---

## 5. Government and registry reports

**Discovery sources, not evidence of the association.** National and state cancer-registry reports
and national tobacco surveys characterise incidence and exposure prevalence. They typically report
**neither an effect estimate nor the data from which one could be derived**, because they are not
designed to compare smokers with never-smokers.

| Treatment | Rule |
|---|---|
| Prevalence-only or incidence-only report | **Never included as evidence of the association.** If screened, excluded as `no_usable_data` |
| Report containing an eligible, extractable observational analysis — comparative, with a non-smoking reference group and a derivable estimate | Eligible on the same criteria as any other report; included only if it meets them in full |
| All such reports | **Primary value is their reference lists**, checked under the reference-list provision already in P007 |

Registry and survey reports may therefore be *consulted*, and their references followed, without any
being *included*. The search record states which were consulted; the PRISMA flow counts only those
formally screened. **The distinction between consulting a source for leads and screening it as a
record is preserved throughout** and must not be blurred in reporting.

---

## 6. Thesis and article linking

### 6.1 Consistency with D004 and the schema — checked

| Requirement | Schema support | Verdict |
|---|---|---|
| One `study_id` per population | D004; study is the unit of analysis | **Supported** |
| Separate `report_id`s preserved | `studies.report_ids` — all publications of this population | **Supported** |
| Both reports linked | `report_ids` + `primary_report_id` | **Supported** |
| Per-variable source, **estimates** | `estimates.report_id` + required `estimates.source_location` | **Fully supported** |
| Per-variable source, **study-level descriptive fields** | `primary_report_id` is singular; no per-field column | **Partial — section 4** |
| No double counting | `selected_for_analysis` — at most one per study per analysis — with `selection_rationale` | **Supported and enforced** |

### 6.2 Procedure

1. **Deduplication will not merge a thesis with its article, and must not be expected to.** The
   pipeline matches on normalised DOI, then PMID, then an exact title+author+year fingerprint;
   near-identical titles are flagged `needs_review` and **never merged automatically**. A thesis and
   its article share no identifier and differ in title, so both arrive at screening as separate
   reports. **This is correct behaviour, not a failure.**
2. **The reviewer identifies the shared population at full text**, by judgement — overlapping
   authors, institution, recruitment period, setting, sample size. A human decision under D010,
   recorded.
3. **One `study_id` is assigned.** Every contributing `report_id` is listed in `studies.report_ids`.
4. **`primary_report_id` names the fullest single account — not automatically the journal article.**
   Theses routinely carry detail that article length limits remove: fuller adjustment models, more
   exposure categories, complete counts.
5. **Each estimate is attributed to the report it came from**, via `estimates.report_id` and
   `source_location`. Where both reports give the same estimate, it is extracted **once**.
6. **The thesis is not discarded as a duplicate by default.** `duplicate_publication` applies only to
   a report contributing **nothing** beyond one already included. A thesis supplying additional
   estimates, fuller adjustment or omitted data is a **contributing report of an included study**,
   recorded in `report_ids` — not an exclusion.
7. **Double counting is prevented at the analysis boundary**, not by discarding reports:
   `selected_for_analysis` permits at most one estimate per study per analysis, with a recorded
   rationale, and D004 permits a `study_id` at most once in any analysis.
8. **Participants are never counted twice.** Where reports describe overlapping but non-identical
   samples — a thesis cohort later extended for publication — the overlap is recorded and **one**
   estimate is selected, with the reason stated.

---

## 7. Publication bias — rationale

**Grey-literature searching here is justified by search sensitivity**: reducing the risk that
eligible studies of non-cigarette smoked tobacco are missed because they were never published in an
indexed journal. That rationale holds whatever the final number of included studies, and it is the
whole justification.

**No small-study-effect analysis is promised.** `scripts/analysis/meta.py` refuses Egger's test
below ten studies (`MIN_STUDIES_EGGER = 10`), and the manuscript already reports publication bias as
*Not assessed*. If fewer than ten studies are included, **no such test will run**, and nothing here
commits to one. A funnel plot of a handful of studies establishes nothing.

What can honestly be said: if unpublished studies are systematically more likely to be null, a
review confined to published work inherits that bias whether or not any test is computed. Searching
grey literature addresses that substantively. It does not depend on, and does not promise, a
statistical assessment.

A **sensitivity analysis excluding grey-literature studies** may be informative if any are included
and the number permits. It is a **contingent option** (decision 7), **not a commitment**, and it is
a leave-out sensitivity analysis — **not** a test of publication bias.

---

## 8. Approved protocol wording

**APPROVED by the researcher on 12 November 2026** (section 1A, decision 2). This is the operative
wording. It is recorded here; it is **not** written to the decision register, and the entry
proposing to record it is section 11.

> **Grey literature.** A bounded supplementary search for grey literature will be undertaken
> alongside the bibliographic databases and supplementary methods specified under P007. Its purpose
> is **search sensitivity**: reducing the risk that eligible studies of non-cigarette smoked
> tobacco, which are concentrated in South Asia, are missed because they were never published in an
> indexed journal. No statistical assessment of small-study effects is promised, and none will be
> performed unless the number of included studies makes it meaningful.
>
> **Sources, in priority order.** (a) **Theses and dissertations** — Shodhganga, the Rajiv Gandhi
> University of Health Sciences repository, named institutional repositories of dental and
> health-science colleges, and NDLTD, each searched where an accessible interface is available;
> (b) **government and public-health reports**, including national and state cancer-registry and
> tobacco-survey series, **consulted as discovery sources** whose reference lists are checked;
> (c) **Google Scholar**, searched to the stopping rule below; (d) **reference-list and
> forward-citation checking** of included studies and relevant systematic reviews, already specified
> under P007, which reaches grey sources as well as published ones. ProQuest Dissertations & Theses
> is **not** searched, there being no confirmed access.
>
> **Limits.** Restricted to **English-language** records, consistent with D013, applied at
> screening. **No date limit.** Thesis repositories are searched with a simplified term set
> appropriate to each interface, since none supports the controlled vocabulary or Boolean syntax of
> the database strategies; the exact string entered is recorded for each.
>
> **Google Scholar stopping rule.** Five prespecified phrase queries are run separately, sorted by
> **relevance**, with patents and citations excluded and 20 results per page. For each query,
> screening proceeds by title in displayed order and stops at whichever occurs first: **200 results
> examined**, **50 consecutive results yielding nothing potentially eligible**, or the end of the
> list. **The thresholds 200 and 50 are an arbitrary operational bound fixed in advance to make the
> search bounded and reportable. They are not established systematic-review standards and are not
> presented as such.** Google Scholar orders results by an **unstable relevance algorithm**, so this
> search is **reportable but not repeatable**, and **no claim of reproducibility is made for it**.
> Google Scholar is **supplementary and does not replace a bibliographic database**; no coverage
> claim rests on it. For every query the **date searched, exact query string, sort order, number of
> results examined and the stopping condition that applied** are recorded.
>
> **Documentation.** Each grey-literature source is recorded as a separate search execution under
> D011, with its interface, the exact string entered, any field restriction or filter, the date
> searched, the number of records examined, the stopping condition where relevant, and the number
> carried forward. Where a source is unreachable or its interface fails, the attempt, date and
> outcome are recorded and reported: **an unreachable source is a finding, not an omission.** **No
> grey-literature source will be reported as searched unless the search was executed and its results
> preserved.**
>
> **Screening.** Grey-literature records are screened against the same eligibility criteria and the
> same controlled vocabulary of exclusion reasons as database records, by the same reviewer, with
> the same recorded decision basis. Narrative reviews are excluded as `review_or_meta`; editorials,
> commentaries and letters as `wrong_design`; prevalence-only and incidence-only reports, and any
> record lacking an effect estimate or data from which one can be derived, as `no_usable_data`.
> **No record is included on the grounds that it is unpublished.** Where full text is restricted so
> that eligibility cannot be determined, that is reported as **undetermined**, never recorded as an
> exclusion on a criterion never assessed.
>
> **Multiple reports of one study.** Where a thesis, report, abstract or article describe the same
> underlying participants, a **single `study_id`** is assigned (D004) and **all contributing
> `report_id`s are preserved** in `studies.report_ids`. `primary_report_id` names the most complete
> account, **not assumed to be the journal article**. Each estimate records the report it was taken
> from in `estimates.report_id` with its `source_location`, so estimates and exposure definitions
> drawn from different reports of one study remain separately attributed. **A thesis is not
> discarded as a duplicate publication merely because an article exists**; `duplicate_publication`
> applies only to a report contributing nothing beyond one already included. Study-level descriptive
> variables taken from a report other than the primary one are recorded in `studies.notes` using the
> convention `src: field=report_id`, entries being listed only where the source is not
> `primary_report_id`. Double counting is prevented at the analysis boundary:
> `selected_for_analysis` permits at most one estimate per study per analysis, with a recorded
> rationale, and a `study_id` appears at most once in any analysis. Where samples overlap without
> being identical, the overlap is recorded and one estimate selected, with the reason stated.
>
> **Unpublished or incomplete data.** Missing data are recorded as missing using the schema's
> missing codes (`NR`, `NA`, `UNCLEAR`) and are **never imputed or inferred**. A value taken from a
> different report of the same study is recorded as such. Where a record reports an eligible study
> but lacks the detail needed for extraction, it is recorded as identified and excluded as
> `no_usable_data` with the shortfall stated. Contacting authors is permitted at extraction, **not**
> as a search method; any datum so obtained is recorded with its source, the date, and the fact that
> it is author-supplied and unpublished.
>
> **If the grey-literature search is not performed**, or is performed and reaches nothing eligible,
> that is reported in the limitations with its likely direction of effect: a review confined to
> published studies is expected to over-represent positive findings.

---

## 9. Researcher decisions — outcome

**Seven of the eight were settled on 12 November 2026.** One remains open.

| # | Decision | Outcome |
|---|---|---|
| 1 | Approach | **APPROVED — Approach B** |
| 2 | Protocol wording (§8) | **APPROVED as drafted** |
| 3 | Source list and priority, ProQuest excluded | **APPROVED** |
| 4 | Google Scholar thresholds 200 / 50 | **APPROVED as operational choices, explicitly not standards** |
| 5 | Google Scholar queries | **APPROVED** (implied by approval of bounded Scholar searching and the §8 wording) |
| 6 | Study-level provenance | **APPROVED — Option A provisionally, with a mandatory stop at the trigger** (§4.4) |
| 7 | Sensitivity analysis excluding grey literature | **STILL OPEN.** Not addressed in the approval; remains contingent and deferred to the SAP, where the number of studies is known. It is a leave-out sensitivity analysis, **not** a test of publication bias |
| 8 | Where recorded | **APPROVED — a separate methodological decision, not part of P007.** No ID assigned; register not modified (§12) |

The full statement of each decision follows, retained as the record of what was weighed.

### Decision 1 — Approach

**Question.** Is a bounded supplementary grey-literature search (Approach B) adopted, rather than no
search (A) or an expanded search (C)?
**Recommended.** **Yes — Approach B.**
**If accepted.** The review gains a bounded, declarable attempt at the South Asian grey literature
its exposure definition makes material. Workload rises by a known, capped amount.
**If rejected in favour of A.** Defensible only if the omission is declared with its likely
direction of effect. The review becomes vulnerable to the objection that it searched only indexed
journals for an exposure concentrated where indexing is weakest.
**If rejected in favour of C.** Coverage rises; so does the risk of a search begun and not finished
under D010, which would be worse than a completed narrower one.

### Decision 2 — Protocol wording

**Question.** Is the wording in section 8 accepted as drafted, amended, or rejected?
**Recommended.** **Accept, subject to decisions 3–8**, each of which changes a specific clause.
**If accepted.** The wording is recorded in this memorandum as approved and carried into the
protocol and the manuscript's methods. P007 is unaffected.
**If rejected.** No grey-literature provision exists and section 8 remains a draft.

### Decision 3 — Source list and priority

**Question.** Are the sources and priority order in section 2.1 confirmed, including the exclusion
of ProQuest on access grounds?
**Recommended.** **Yes.** Shodhganga → RGUHS and named institutional repositories → NDLTD; ProQuest
excluded unless access is later confirmed.
**If accepted.** The search is bounded to an enumerable list, and each source's reachability becomes
a recorded finding.
**If rejected.** Either the list grows, raising workload with sources whose output is likely to fail
language or design criteria, or it shrinks, which must then be declared.
**Note.** Every source is **unverified**; accepting the list is not accepting that any is reachable.

### Decision 4 — Google Scholar thresholds

**Question.** Are the operational thresholds of 200 results examined and 50 consecutive non-hits
confirmed, or replaced with different prespecified values?
**Recommended.** **Confirm them**, on the explicit understanding that they are arbitrary, are not
standards, and are justified only by being fixed in advance and reported.
**If accepted.** The Scholar search is bounded, reportable, and honestly characterised.
**If rejected.** Any other prespecified pair is equally defensible. **What is not acceptable is
leaving the stopping point undefined**, which makes the search unreportable.

### Decision 5 — Google Scholar queries

**Question.** Are the five phrase queries in section 3.2 confirmed, or amended?
**Recommended.** **Confirm**, noting they are deliberately short because Scholar's Boolean support
is weak.
**If accepted.** Each is recorded verbatim with its date, count and stopping condition.
**If rejected.** Amended queries must still be prespecified and recorded; ad-hoc querying while
searching would make the search unreportable.

### Decision 6 — Study-level provenance

**Question.** Is study-level variable provenance handled by (A) a prescribed `src:` convention in
`studies.notes`, or (B) a minimal schema extension adding a `field_sources` column?
**Recommended.** **Option A now, with the stated trigger**: adopt B if more than three included
studies have contributing reports disagreeing on a study-level variable.
**If A is accepted.** Nothing changes today; no tracked config is touched. Provenance is
human-readable but **unenforced** — the validator cannot check it, and a lapse is invisible.
**If B is accepted.** `config/extraction.yaml` gains one field; the workbook regenerates (34 → 35
study fields, dictionary 93 → 94); the auditor's expected counts and the tests change. All
mechanical and verifiable, since generation is deterministic. Provenance becomes a property of the
record rather than of reviewer discipline. **Choosing B is a sound decision, not a concession**, and
is the better choice if a substantial thesis yield is expected.
**Either way.** The analysis inputs — estimates, adjustments and exposure definitions — are already
fully attributed and are unaffected by this decision.

### Decision 7 — Sensitivity analysis

**Question.** If grey-literature studies are included, is a sensitivity analysis excluding them
**required**, or performed only if the number of studies permits?
**Recommended.** **Contingent**, not required.
**If required.** The commitment may prove unmeetable: with few studies a leave-out analysis is
uninformative, and the protocol would promise something the evidence cannot support.
**If contingent.** The decision is deferred to the SAP, where the number of studies is known. **It
remains a leave-out sensitivity analysis, not a test of publication bias**, and must not be reported
as one.

### Decision 8 — Where the decision is recorded

**Question.** Does this become part of P007's resolution, or a separate decision-register entry?
**Recommended.** **A separate entry.** P007 concerns bibliographic database coverage and is already
conditional on unresolved access verification; grey literature is a distinct question with distinct
evidence, and binding them would mean neither can close until both are settled.
**If separate.** Grey literature can be settled now while P007 waits on access findings.
**If merged into P007.** P007's resolution grows larger and later, and the grey-literature provision
inherits P007's dependency on access checks it does not actually need.
**Either way.** Recording it in `docs/decisions/decision_log.md` is a **separate authorised act**
that this memorandum does not perform.

---

## 10. Limitations of the approved approach

1. **MDS dissertations may be largely unreachable** — the richest likely source is master's-level
   work, while the main national repository is principally doctoral, and institutional repositories
   cannot be enumerated systematically.
2. **Google Scholar is not reproducible.** Bounded and documented it is reportable; it is not
   repeatable, and no claim of reproducibility is made for it.
3. **No repository accessibility is verified.** Every source in section 2.1 is unverified; some may
   prove unreachable, and the search record must show which.
4. **English-only eligibility forecloses most Latin American grey literature** — a deliberate
   consequence of D013, not an oversight.
5. **Study-level per-variable provenance is unenforced under the recommended Option A** (section 4).
   Impact is confined to descriptive fields; analysis inputs are fully attributed.
6. **Workload is bounded but not zero**, and falls on a single reviewer whose screening capacity is
   already the binding constraint on the review.

---

## 11. Decision-register entry — RECORDED AS D022

**Authorised and written on 2026-11-13.** The entry below was recorded in
`docs/decisions/decision_log.md` as **D022**, in the `Decided` section after D020. The insertion is
purely additive: 15 lines added, none removed, and no existing entry altered.

The text as written in the register is the authoritative version; what follows is the proposal it
was built from, retained as the record of what was authorised.

### The decision ID must not default to D021

| Fact | Evidence |
|---|---|
| D001–D020 were the registered decisions when this was written | `docs/decisions/decision_log.md`; the highest heading was then `### D020 — Sampling-frame digest for verification draws` |
| **D021 is already spoken for** | Three documents already use D021 for the **blinded verification acceptance methodology** — "Drafted; not in the register" in `docs/project_completion_status.md`, discussed at `docs/reports/internal_audit_report.md:52`, and listed as "Drafted, not entered in the register" in `docs/reports/supplementary_material.md:251` |

Assigning D021 to grey literature would therefore **collide with three existing documents** and
silently renumber a decision that has been discussed under that label since before this phase. The
next genuinely unused identifier is **D022**.

**Proposed: D022**, leaving D021 free for the verification acceptance methodology it already names.
The researcher may instead prefer to register the verification methodology as D021 first, or to
renumber it; either is a separate decision, and this memorandum takes neither.

### Exact proposed entry

> ### D022 — Bounded supplementary grey-literature searching
>
> - **Status:** Adopted *(date of authorisation)*. Methodology approved 2026-11-12.
> - **Decision:** A bounded supplementary grey-literature search is undertaken alongside the
>   bibliographic databases and supplementary methods specified under P007, justified by **search
>   sensitivity** — reducing the risk that eligible studies of non-cigarette smoked tobacco, which
>   are concentrated in South Asia, are missed because they were never published in an indexed
>   journal. Sources, in priority order: **theses and dissertations** (Shodhganga, the RGUHS
>   repository, named institutional repositories, NDLTD), each conditional on an accessible
>   interface; **government and public-health reports**, used as **discovery sources** whose
>   reference lists are checked; **Google Scholar**, bounded by a prespecified stopping rule; and
>   **reference-list and forward-citation checking**. ProQuest is not searched, there being no
>   confirmed access. Records are restricted to **English** (D013), screened against the **existing
>   eligibility criteria and the existing exclusion vocabulary**, with no latitude for being
>   unpublished. Reports describing the same participants share **one `study_id`** with **separate
>   `report_id`s** preserved; a thesis is **not** discarded as a duplicate merely because an article
>   exists; double counting is prevented by `selected_for_analysis` and D004. Study-level provenance
>   uses the structured `src: field=report_id` convention in `studies.notes`; **the extraction
>   schema is unchanged**. The full operational specification is
>   `docs/methods/grey_literature_scope_decision.md` §8.
> - **Why:** The exposure definition (D009) admits bidi, chutta and reverse smoking, and the
>   studies that make it worth having are concentrated where journal indexing is weakest. A search
>   confined to indexed journals would be least sensitive exactly where this review is most
>   distinctive.
> - **Consequences:** Adds bounded screening work under single-reviewer screening (D010). Each
>   source is a separate registered execution under D011. **The Google Scholar thresholds (200
>   results examined; 50 consecutive non-hits) are operational choices fixed in advance, not
>   established systematic-review standards**, and that Scholar search is **reportable but not
>   repeatable**; no claim of reproducibility is made for it. **No source is reported as searched
>   unless the search was executed and its results preserved**, and an unreachable source is
>   recorded as a finding. **No repository accessibility has been verified.**
> - **Provenance safeguard:** Option A is provisional. **If more than three included studies have
>   conflicting reports for a study-level variable, extraction stops before it is finalised** and a
>   structured provenance-schema proposal is presented for approval. The extension is never
>   implemented automatically.
> - **Supersedes / relates to:** Independent of P007, which concerns bibliographic database
>   coverage and remains open pending access verification. Relies on D004, D009, D010, D011, D013.
> - **Open:** §9 decision 7 — whether a sensitivity analysis excluding grey-literature studies is
>   required if any are included, deferred to the SAP.

**Also requiring authorisation if the entry is written:** the open-questions table in the same file
currently lists no grey-literature question, so no `P0xx` needs closing — but if the researcher
prefers the matter tracked as a resolved open question rather than a standalone decision, that is a
different edit and is not proposed here.

---

## 12. What this document does not do

- It records the researcher's **approval of the methodology** (section 1A). The register entry was
  authorised separately and written as **D022** on 2026-11-13 (section 11); that insertion is the
  only change made to `docs/decisions/decision_log.md`.
- It does **not** modify P007, `config/screening.yaml` or `config/extraction.yaml`, and **alters no
  existing decision**. Its only change to `docs/decisions/decision_log.md` is the additive D022
  entry authorised on 2026-11-13.
- It does **not** begin P013.
- **No search was executed, and no repository, database or website was accessed** in preparing it.
- No search date, yield, record count or accessibility status is asserted for any source.
- No screening decision was created and no data changed.
- Every wording above awaits the researcher's approval.
