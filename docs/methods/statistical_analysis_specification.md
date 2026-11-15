# Statistical analysis — implementation specification

**Prepared 14 November 2026.** What the statistical software **actually does**, and what remains a
proposal awaiting the reviewer's approval.

> **This is an implementation specification, not the analysis plan.** The plan is
> `docs/methods/statistical_analysis_plan.md`, which is explicitly a skeleton — "NOT A PLAN YET" —
> and must be completed and approved before any pooled estimate is computed. **Where the two differ,
> the plan governs**, and the differences are listed in §12.
>
> **No analysis has been run.** `data/extraction/` does not exist; there are zero included studies
> and zero extracted estimates. Everything below is tested against synthetic fixtures only.

| Marker | Meaning |
|---|---|
| **IMPLEMENTED** | Working, tested, and enforced by the code |
| **PROPOSED** | Designed and coded, but rests on a choice the reviewer has not made |
| **BLOCKED** | Cannot be implemented until a named open question is resolved |

---

## 1. Estimand

**PROPOSED.** The association between smoked tobacco use and oral-cavity squamous cell carcinoma,
expressed as a ratio measure on the log scale, in the population of studies meeting the eligibility
criteria. **This is an association, not a causal effect**, and no causal language is used (standing
prohibition 7).

**The primary contrast is ever versus never** (**D026**). Current-versus-never and
former-versus-never are separate prespecified secondary analyses. Dose–response is narrative and
tabular only; **no pooled dose–response estimate is produced**, per D015 limitation (e). The data
model continues to record `exposure_contrast` verbatim.

## 2. Effect measures — IMPLEMENTED

Only ratio measures are pooled: **OR, RR, HR**, each on the log scale, exponentiated for
presentation. A non-ratio measure raises rather than being coerced.

**Mixing measures in one analysis is refused.** OR, RR and HR estimate different quantities; the
code requires separate analyses rather than an implicit combination.

### Standard errors — three routes, all IMPLEMENTED

| Route | Method | Recorded as |
|---|---|---|
| `from_ci` | SE from the reported 95% CI on the log scale | `SE from reported 95% CI` |
| `from_counts` | SE from the 2×2 table: `sqrt(1/a + 1/b + 1/c + 1/d)` | `SE from 2x2 counts` |
| `from_log_se` | SE as reported | `SE as reported` |

Every derivation is recorded in the `derivation` field. **Derived values are never typed by hand.**

**Consistency check:** the reported estimate is compared with the geometric mean of its interval;
a relative gap beyond 10% is recorded as a note, since mild asymmetry is normal when a source rounds.

## 3. Zero cells — IMPLEMENTED, and deliberately restrictive

A zero cell makes ln(OR) undefined. **No continuity correction is applied automatically.** The code
refuses the table and names the alternatives — a 0.5 correction, Mantel–Haenszel, or Peto — leaving
the choice to the reviewer as a recorded decision.

**Consequence, stated plainly:** a study with a zero cell **cannot currently contribute**. Neither
Mantel–Haenszel nor Peto is implemented, so rare-event data has no route. **This is a known
limitation, not an oversight** (§11).

## 4. Adjusted versus crude — IMPLEMENTED (model), PROPOSED (selection rule)

### What the model now carries

The analysis-layer `Estimate` previously held none of the extraction schema's adjustment
information — the Phase 2L audit's first gap. It now carries:

| Field | Purpose |
|---|---|
| `adjustment` | `crude` or `adjusted`, mirroring the extraction enum |
| `adjusted_for` | The covariate list, **verbatim**, never harmonised |
| `adjustment_set` | The reviewer's label for this adjustment set |
| `is_primary_adjusted` | Whether this is the study's primary adjusted estimate |
| `adjusted_alcohol` | `yes`/`no`/`NR` — both a subgroup variable and the key confounder under D009 |
| `report_id`, `estimate_id`, `source_location` | Provenance back to a report and a page |
| `exposure_contrast`, `product_types`, `outcome_site`, `country`, `design` | Analysis context |

`provenance_problems()` reports what is missing — absent `source_location` or `report_id`, unknown
adjustment status, or an "adjusted" estimate with no covariate list. It **reports** rather than
raises, so a fixture may legitimately lack them while a research estimate may not.

### Pooling adjusted with crude — IMPLEMENTED safeguard

`validate_set` **refuses** a set mixing adjusted and crude estimates, naming the studies on each
side. It can be overridden only by passing `allow_mixed_adjustment=True`, which exists so that doing
so is a deliberate, visible act. The SAP lists mixing them without a defensible basis among its
criteria for **not pooling at all**.

### Which adjusted estimate to use — PROPOSED, needs a decision

Where a study reports several adjusted models, **the code does not choose.** It requires exactly one
estimate per study to carry the reviewer's primary marker and refuses otherwise, listing every
candidate (§6).

**Open question for the reviewer:** the rule itself. Candidates — the study's own primary model; the
model adjusting for the largest confounder set; the model adjusting for a prespecified minimum set
(alcohol, and under D009 smokeless tobacco and betel quid). **No rule is adopted**, and the code
will refuse until one is recorded per study.

## 5. Models and heterogeneity — IMPLEMENTED

| Component | Status |
|---|---|
| Fixed-effect, inverse-variance | **IMPLEMENTED** |
| Random-effects, inverse-variance with τ² | **IMPLEMENTED** |
| τ² by DerSimonian–Laird | **IMPLEMENTED** |
| τ² by REML | **IMPLEMENTED — but see §11, no external validation** |
| Cochran's Q with χ² p-value | **IMPLEMENTED** |
| I² | **IMPLEMENTED** |
| Prediction interval | **IMPLEMENTED**, requires ≥3 studies |

**Model assumptions.** Fixed-effect assumes one common true effect; random-effects assumes effects
vary and estimates that variance. For observational studies differing in population, design and
adjustment, **random-effects is the defensible default**, and the SAP anticipates it. The estimator
is always named in output.

**I² interpretation.** The 25/50/75% bands are descriptive guidance, **not decision thresholds**,
and are reported as such.

## 6. Multiple estimates and dependence — IMPLEMENTED

A study reporting several estimates is normal, not an error: different contrasts, adjustment sets
and subsites all produce separate rows. **They are correlated.** Pooling them as independent studies
would understate the standard error and overstate precision.

Three safeguards:

1. **`validate_set` refuses** any set containing a repeated `study_id` (D004: the study is the unit
   of analysis, at most once per analysis).
2. **`select_one_per_study` refuses to guess.** It requires exactly one estimate per study to carry
   the reviewer's primary marker, and raises otherwise — naming **every** candidate estimate id.
3. **Nothing is discarded silently.** The refusal message states explicitly that no estimate has
   been dropped, and the unselected rows remain in the extraction data.

**Not implemented, and not needed yet:** multivariate or robust-variance methods that would allow
several correlated estimates from one study to contribute simultaneously. **The project's position
is selection, not modelling of dependence** — simpler, and defensible provided the selection rule is
prespecified (§4).

**Overlapping populations** — two studies sharing participants — are handled upstream, at `study_id`
assignment (D004): the reviewer assigns one `study_id` to one population, and the extraction schema
records every contributing `report_id`.

## 7. Subgroup analyses — PARTLY IMPLEMENTED

The manuscript names **five** planned subgroups. All five have machinery; **two can actually run**.

| Subgroup | Source field | Categories | Status |
|---|---|---|---|
| **Product type** | `estimates.product_types` | `cigarette_only`, `mixed_or_other` (D009) | **READY** |
| **Alcohol adjustment** | `estimates.adjusted_alcohol` | `yes`, `no` | **READY** |
| Anatomical subsite | `estimates.outcome_site` | — | **BLOCKED: P014–P022.** The eligible subsite list is unsettled, so no category set exists |
| Geographical region | `studies.country` | — | **BLOCKED.** No country-to-region scheme has been chosen (UN, WHO or other). This is a methodological decision, not a lookup |
| Risk-of-bias level | `risk_of_bias.judgement` | — | **BLOCKED: P023.** No instrument, so no judgement categories |

A blocked subgroup **raises** rather than returning an empty result, naming the blocking question.
A subgroup that is not one of the five raises as **post-hoc**.

### Minimum evidence — PROPOSED

Default **4 studies per group**, the SAP's recommendation, passed as a parameter rather than
hard-coded, because the threshold is the reviewer's decision. A group below it is **not pooled** and
is reported with its count.

### Missing subgroup data — IMPLEMENTED

Estimates that cannot be classified go to an explicit missing bucket, are **excluded from the
between-group test**, and are **reported with their count**. They are never imputed, never
reassigned, and never silently absorbed into a category.

### Testing for a subgroup difference — IMPLEMENTED

A between-group Cochran's Q on the subgroup summaries, with df = groups − 1 and a χ² p-value.
It is computed **only when at least two groups meet the minimum**; otherwise the result records why
not.

> **The misinterpretation this guards against.** A difference between subgroups is supported **only**
> by the between-group test. Observing that one subgroup's interval excludes the null while
> another's does not is **not evidence of a difference**. This warning is attached to every
> subgroup result and appears in its printed summary.

**Subgroup-specific pooled estimates and formal tests of difference are reported separately**, and
the former never implies the latter.

## 8. Sensitivity analyses

| Analysis | Status |
|---|---|
| Leave-one-out influence | **IMPLEMENTED** |
| Restriction by risk of bias | **BLOCKED: P023** |
| Adjusted estimates only | **IMPLEMENTED** via the adjustment field |
| Alcohol-adjusted only | **IMPLEMENTED** via `adjusted_alcohol` |
| Alternative heterogeneity estimator | **IMPLEMENTED** — DL versus REML |
| Alternative SE derivation where a CI was asymmetric | **PROPOSED** — the flag exists; the analysis is not automated |
| Excluding grey-literature studies | **PROPOSED, contingent** (D022). A leave-out analysis, **not** a publication-bias test |

## 9. Publication bias and small-study effects — IMPLEMENTED safeguards

Egger's regression and funnel plots exist. **Egger's test refuses below 10 studies**, and the SAP
sets the same threshold.

**Nothing is promised.** If fewer than ten studies are included, no test runs and the limitation is
stated instead. Funnel asymmetry has causes besides publication bias — true heterogeneity, poorer
methodology in smaller studies, chance — and must be reported with that caveat or not at all.

## 10. When meta-analysis will NOT be performed

From the SAP §7, enforced partly in code and otherwise by the reviewer. Pooling is **inappropriate**,
and a structured narrative synthesis is reported instead, if any of:

- fewer than 3 studies contribute to a contrast;
- the available estimates mix non-comparable exposure categories requiring harmonisation (rule 9);
- they mix adjusted and unadjusted without a defensible basis — **refused in code by default**;
- comparator definitions are irreconcilable across studies;
- heterogeneity is so extreme that a summary estimate would misrepresent the evidence.

Additional refusals enforced in code: **no estimates at all**; **a study appearing twice**;
**mixed effect measures**; **synthetic data mixed with real**; **any row marked synthetic** reaching
the analysis CLI.

**Deciding not to pool is a legitimate result and is reported as such.**

## 11. Known statistical limitations — unchanged by this phase

1. **REML has no external validation.** Tested for self-consistency — its τ² is a fixed point of its
   own update — and limiting behaviour. That establishes the implementation solves the equation it
   encodes, not that the equation is right. **Any REML τ² must be cross-checked against an
   established implementation before publication.**
2. **The pooled estimate, weights and τ² have no external reference check.**
3. **No Hartung–Knapp–Sidik–Jonkman interval**, which the Cochrane Handbook favours when *k* is
   small and τ² > 0 — the likely situation here.
4. **No Mantel–Haenszel or Peto method** — rare-event and zero-cell data have no route (§3).
5. **No meta-regression and no dose–response model.**
6. **No multivariate or robust-variance handling** of correlated estimates (§6).
7. **Single reviewer** (D010), reported under PRISMA items 8 and 9.

## 12. Unresolved choices requiring the reviewer's decision

| # | Question | Why it matters | Blocks |
|---|---|---|---|
| 1 | **The SAP lists nine candidate subgroups; the manuscript names five as planned.** Which set is prespecified? | Anything run beyond the prespecified set is post-hoc and must be declared so | Subgroup reporting |
| 2 | **The adjusted-estimate selection rule** (§4) | Without it the code refuses to select, and it must be prespecified to avoid choosing the most favourable model | Any pooled analysis |
| 3 | **Minimum studies per subgroup** — 4 recommended | Determines which subgroups run at all | Subgroup analyses |
| 4 | **Country-to-region scheme** | No scheme means no region subgroup | Region subgroup |
| 5 | **Zero-cell policy** | Otherwise such studies cannot contribute | Rare-event studies |
| 6 | **Primary effect measure**, and whether case–control and cohort estimates may be pooled at all | SAP marks this **(evidence)** — genuinely undecidable until the included studies are known | Primary analysis |
| 7 | **P023 instrument** | Blocks the risk-of-bias subgroup and sensitivity analysis | Appraisal |

## 13. What this phase changed

| Change | Effect |
|---|---|
| `Estimate` extended with 14 adjustment, provenance and context fields | Closes audit gap 1. Existing constructors unaffected — all fields default |
| `validate_set` refuses adjusted/crude mixing unless explicitly allowed | New safeguard |
| `scripts/analysis/subgroups.py` added | Closes audit gap 2 |
| `select_one_per_study` added | Makes dependence handling explicit and refusing |
| 30 regression tests added | Suite 639 → 669 |

**No statistical method was changed to make software pass tests.** No research data was created,
and every test fixture is constructed in-process and marked synthetic.
