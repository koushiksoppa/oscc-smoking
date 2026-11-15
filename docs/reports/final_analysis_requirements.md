# Final analysis — exact numerical output requirements

**Prepared 14 November 2026.** The complete list of numerical outputs the final research paper must
contain, each with its source dataset, calculation method and validation requirement.

> ## Every value in this document is a SPECIFICATION, not a result
>
> **No placeholder number appears anywhere below.** Where a value does not yet exist, the cell reads
> `NOT AVAILABLE` and states what must happen first. A reader must never be able to mistake a
> specification for a finding.
>
> **Currently available: the identification and deduplication figures for one superseded search, and
> nothing else.** No study is included, no estimate extracted, no pooled result computed.

---

## 1. Availability at a glance

| Category | Items | Available now | Blocked |
|---|---|---|---|
| Identification and selection | 8 | 2 (for `pubmed_v1r` only) | 6 |
| Study and participant characteristics | 5 | 0 | 5 |
| Effect estimates | 4 | 0 | 4 |
| Synthesis | 6 | 0 | 6 |
| Risk of bias | 2 | 0 | 2 |
| Publication bias | 2 | 0, and **may remain unavailable by design** | 2 |

---

## 2. Identification and study selection (PRISMA 2020 flow)

| # | Output | Source dataset | Calculation | Validation requirement | Status |
|---|---|---|---|---|---|
| 2.1 | **Records identified per database** | `config/sources.yaml` + each registered export | Count of records in each export, verified against the database-reported count at execution | Export checksum must match `data/raw/SHA256SUMS`; the count recorded at execution must equal the parsed count, and a disagreement is reported, never reconciled by editing | **PARTIAL** — `pubmed_v1r` = 194 from the **superseded v1 query**. The adopted D023 strategy has never been executed, in any database |
| 2.2 | **Records identified from other sources** (grey literature, citation searching) | Per-source search records under D022 | Count per source | Each source a separate execution under D011 | `NOT AVAILABLE` — no grey-literature search performed |
| 2.3 | **Duplicate records removed** | `data/processed/dedup/dedup_audit.csv` | Pairs merged on normalised DOI → PMID → exact title+author+year fingerprint. Near-matches flagged `needs_review`, never auto-merged | The 11 PRISMA identities must hold. Cross-database rules must be reviewed before first multi-source use | **AVAILABLE for `pubmed_v1r`: 0 duplicates, 194 unique reports.** Will change entirely on re-search |
| 2.4 | **Records screened** | `data/screening/screening_ta.csv` | Count of rows with `decision_basis = independently_adjudicated` | `validate_screening --stage ta --final` must pass; it currently fails by design | **`0`** — and this is the true value, not a missing one. 194 provisional classifications exist and **are not screening** |
| 2.5 | **Records excluded at title/abstract, with reasons** | same | Count per `reason_code`, adjudicated rows only | Exclusions must sum to the adjudicated excluded total | **`0`.** The 109/63/33/10/2/1 provisional figures are **suggestion outputs and must not appear in a PRISMA exclusion table** |
| 2.6 | **Full texts sought** | `data/screening/screening_ft.csv` | Count of `ft_sought` (valid, adjudicated include) | Five attribution states must sum to the row count | **`0`.** 85 rows are `ft_provisional_sought` |
| 2.7 | **Full texts retrieved / not retrieved** | same, `full_text_status` | Count by status | Every row accounted for | `NOT AVAILABLE` — 0 retrieved |
| 2.8 | **Full texts excluded, with reasons** | same | Count per `reason_code` among full-text decisions | Each exclusion carries exactly one code; `duplicate_publication` links to the retained `report_id` | `NOT AVAILABLE` |

## 3. Included studies and reports

| # | Output | Source dataset | Calculation | Validation requirement | Status |
|---|---|---|---|---|---|
| 3.1 | **Studies included** | `data/extraction/studies.csv` | Count of distinct `study_id` | A `study_id` is a population, assigned by human judgement at full text (D004) | **`0`.** `data/extraction/` does not exist |
| 3.2 | **Reports per included study** | `studies.report_ids` | Count of `report_id` values per `study_id` | Every contributing report preserved; the fullest source named in `primary_report_id`; redundant reports excluded as `duplicate_publication` and linked (D022) | `NOT AVAILABLE` |
| 3.3 | **Participants per study** | `studies.n_total` | As reported — never derived | Recorded as reported; missing recorded as `NR`/`NA`/`UNCLEAR`, never zero or blank | `NOT AVAILABLE` |
| 3.4 | **Cases and controls per study** | `n_cases`, `n_controls`, `person_years` | As reported | `n_controls` is `NA` for cohorts; `person_years` `NA` for case–control | `NOT AVAILABLE` |
| 3.5 | **Total participants and total cases across included studies** | sum of 3.3, 3.4 | Arithmetic sum, reported with the number of studies contributing | **Must state how many studies contributed**, since missing values make a bare total misleading | `NOT AVAILABLE` |

## 4. Exposure and comparator characteristics

| # | Output | Source dataset | Calculation | Validation requirement | Status |
|---|---|---|---|---|---|
| 4.1 | **Exposure categories per estimate** | `estimates.exposure_definition`, `exposure_category` | Recorded **verbatim**; never auto-mapped | Rule 9: verbatim labels, no harmonisation at extraction | `NOT AVAILABLE` |
| 4.2 | **Exposure contrast** | `estimates.exposure_contrast` | As reported | **Field is `unresolved` pending P004.** Values recorded but not protocol-conformant until P004 is decided | `NOT AVAILABLE`, and **blocked on P004** |
| 4.3 | **Comparator definition and type** | `comparator_definition`, `comparator_type` | Verbatim definition; typed classification | **Field is `unresolved` pending P003.** Mixing never-smoker and undefined non-smoker references biases toward the null | `NOT AVAILABLE`, and **blocked on P003** |
| 4.4 | **Product types** | `estimates.product_types` | cigarette / bidi / cigar / pipe / mixed / NR (D009) | Required for the cigarette-only versus mixed subgroup analysis | `NOT AVAILABLE` |
| 4.5 | **Dose/intensity/duration measures** | `intensity_*`, `duration_*`, `pack_years`, `cumulative_*` | As reported; **never derived here** | `pack_years` recorded exactly as reported, never computed | `NOT AVAILABLE` |

## 5. Effect estimates — per study

| # | Output | Source dataset | Calculation | Validation requirement | Status |
|---|---|---|---|---|---|
| 5.1 | **Effect estimate and 95% CI, as reported** | `estimates.estimate`, `ci_low`, `ci_high`, `measure` | Transcribed, not computed. `source_location` **required** — page, table, row | `verified = yes` required before synthesis; CI asymmetry beyond 10% of the geometric mean reported as an inconsistency | `NOT AVAILABLE` |
| 5.2 | **log effect size and standard error** | derived from 5.1 | `from_ci` (SE from the 95% CI), `from_counts` (SE from the 2×2 table), or `from_log_se` (as reported). Computed on the **log scale** | `log_estimate_calc` and `se_calc` are **DERIVED — never typed by hand**; the formula and inputs recorded in `derivation` | `NOT AVAILABLE` |
| 5.3 | **Adjusted and unadjusted estimates, kept distinct** | `estimates.adjustment`, `adjusted_for`, seven `adjusted_*` flags | Reported separately; **never pooled together without a stated justification** | **⚠ Requires the E-gap fix** — the analysis `Estimate` object currently carries **no adjustment field**, so the code cannot distinguish them (see §8) | `NOT AVAILABLE`, and **blocked on a code change** |
| 5.4 | **2×2 cell counts where reported** | `n_exposed_cases` … `n_unexposed_controls` | As reported | A zero cell makes ln(OR) undefined; the code **refuses** rather than applying a silent continuity correction | `NOT AVAILABLE` |

## 6. Synthesis

| # | Output | Source dataset | Calculation | Validation requirement | Status |
|---|---|---|---|---|---|
| 6.1 | **Pooled effect estimate and 95% CI** | selected estimates, one per study | Inverse-variance weighting on the log scale; random-effects anticipated | **One estimate per study per analysis** (D004), enforced by `validate_set`. Must not run with synthetic rows. **Pooling may be inappropriate even when estimates exist** — see the pre-specified non-pooling criteria | `NOT AVAILABLE` |
| 6.2 | **Number of studies and estimates contributing** | same | Count | Must accompany every pooled figure. A pooled estimate without *k* is uninterpretable | `NOT AVAILABLE` |
| 6.3 | **Between-study heterogeneity: Q, df, p** | same | Cochran's Q with χ² p-value | Q and I² checked against published worked values (Cochrane Handbook §10.10.4.5) | `NOT AVAILABLE` |
| 6.4 | **I²** | same | Derived from Q and df | Reported with the interpretive caveat that the 25/50/75% bands are descriptive, not thresholds | `NOT AVAILABLE` |
| 6.5 | **τ²** | same | DerSimonian–Laird **or** REML — the estimator **must be named** | **⚠ REML has no external validation.** Any REML τ² must be cross-checked against an established implementation before publication | `NOT AVAILABLE` |
| 6.6 | **Prediction interval** | same | Implemented; requires ≥3 studies | **Methodologically justified only with enough studies and a non-zero τ².** Note that no Hartung–Knapp interval is implemented, which the Cochrane Handbook favours when *k* is small and τ² > 0 | `NOT AVAILABLE` |

## 7. Subgroup, sensitivity, risk of bias and publication bias

| # | Output | Source dataset | Calculation | Validation requirement | Status |
|---|---|---|---|---|---|
| 7.1 | **Subgroup analyses** — product type, region, anatomical subsite, risk-of-bias level, adjusted vs unadjusted | `studies.country`, `estimates.product_types`, `outcome_site`, risk-of-bias table, `adjustment` | Stratified pooling with a between-subgroup test | **⚠ NOT IMPLEMENTABLE TODAY.** No subgroup machinery exists in `scripts/analysis/`, and no subgroup field reaches `Estimate` (§8) | `NOT AVAILABLE`, **blocked on a code change** |
| 7.2 | **Leave-one-out sensitivity analysis** | pooled set | Implemented (`leave_one_out`) | Report the range of pooled estimates across omissions | `NOT AVAILABLE` |
| 7.3 | **Sensitivity analysis by risk of bias** | risk-of-bias table | Restriction to low-risk studies | **Blocked on P023** — no instrument chosen | `NOT AVAILABLE` |
| 7.4 | **Sensitivity analysis excluding grey literature** | `studies.source_database` | Leave-out analysis | **Contingent, not promised** (D022, open decision 7). It is a leave-out analysis, **not** a test of publication bias | `NOT AVAILABLE` |
| 7.5 | **Risk-of-bias judgements per study per domain** | `data/extraction/risk_of_bias.csv` | Human appraisal using the chosen instrument | 12 structural fields exist; **domain names and judgement categories deliberately absent pending P023** | `NOT AVAILABLE` |
| 7.6 | **Risk-of-bias summary across studies** | same | Counts per domain per judgement | Requires 7.5 | `NOT AVAILABLE` |
| 7.7 | **Egger's test** | pooled set | Regression of effect on precision | **Refused below 10 studies** (`MIN_STUDIES_EGGER = 10`). If fewer are included, **no test runs and none is reported** | `NOT AVAILABLE`, **and may remain so by design** |
| 7.8 | **Funnel plot** | same | Implemented | Asymmetry has causes besides publication bias — true heterogeneity, methodological quality, chance. Must be reported with that caveat, or not at all | `NOT AVAILABLE` |

## 8. Code changes required before these outputs are possible

Two are not data problems but implementation gaps, and both are **cheapest to fix now**, while
`data/extraction/` is still empty.

| # | Gap | Blocks | Fix |
|---|---|---|---|
| 8.1 | `scripts.analysis.effects.Estimate` carries **none** of the 14 adjustment/subgroup fields the extraction schema records | 5.3, 7.1 | Carry `adjustment`, the `adjusted_*` flags, `product_types`, `outcome_site`, `comparator_type`, `exposure_contrast` into `Estimate` |
| 8.2 | **No subgroup pooling function exists** anywhere in `scripts/analysis/` | 7.1 — all five pre-specified subgroup analyses | Implement stratified pooling with a between-subgroup heterogeneity test |

Neither requires a methodological decision. Both require authorisation to change code.

## 9. Declared statistical limitations that must appear in the paper

Carried from the repository's own records; a reader entitled to the numbers is entitled to these:

1. **REML has no external validation** — tested for self-consistency and limiting behaviour only.
2. **The pooled estimate, weights and τ² have no external reference check.**
3. **No Hartung–Knapp–Sidik–Jonkman interval**, favoured when *k* is small and τ² > 0.
4. **No Mantel–Haenszel or Peto method** — rare-event and zero-cell data have no route.
5. **No meta-regression and no dose–response model.**
6. **Single reviewer** (D010) — reported under PRISMA items 8 and 9.
7. **Zero cells are refused, not corrected** — a deliberate choice, but it means such studies cannot
   contribute without a separately recorded decision.

## 10. Rules governing this document

- **No placeholder results.** Unavailable values read `NOT AVAILABLE` with the reason.
- **Provisional figures are never promoted.** The 194 / 109 / 85 provisional classifications are
  suggestion outputs. They may be reported as such and **never** as PRISMA screening counts.
- **Counts-only interrogation figures (8,190 / 5,008 / 8,195) are not search yields** and may not
  appear as records identified.
- **Every pooled figure is reported with its *k*.**
- **The τ² estimator is always named.**
- **No analysis is run with zero included studies.**
