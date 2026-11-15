"""Subgroup analysis, and the estimate-selection rule that must precede it.

Two things live here, because they are the same problem seen from two sides:

- **Selection.** A study may report several estimates — different contrasts, different adjustment
  sets, different subsites. Only one may enter a given analysis (D004), and *which* one is a
  reviewer decision. `select_one_per_study` refuses to guess and reports the conflict instead.
- **Subgroups.** Pooling within strata, plus a formal test of whether the strata differ.

Only the five subgroups prespecified in the manuscript are implemented. The statistical analysis
plan lists nine candidates; the manuscript names five as planned. That discrepancy is a question for
the reviewer, recorded in `docs/methods/statistical_analysis_specification.md`, and this module
implements the narrower set rather than inventing a resolution.

**Nothing here decides whether a subgroup difference is real.** It reports a between-group test. The
common error — declaring a difference because one subgroup's interval excludes 1 and another's does
not — is not a valid inference, and `SubgroupResult.interpretation_warning` says so in the output.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from scipy import stats

from scripts.analysis.effects import Estimate
from scripts.analysis.meta import DL, MetaResult, RANDOM, pool
from scripts.common.config import PipelineError

# A stratum needs enough studies for its pooled estimate to mean anything. The SAP recommends at
# least 4 per group; the value is a reviewer decision and is passed in, not hard-coded as settled.
DEFAULT_MIN_STUDIES_PER_GROUP = 4

# The minimum number of groups a between-group test needs.
MIN_GROUPS_FOR_TEST = 2

MISSING = "__missing__"


@dataclass(frozen=True)
class Subgroup:
    """One prespecified subgroup analysis."""
    key: str
    label: str
    source_field: str
    categories: tuple[str, ...]          # empty when the category set is not yet settled
    blocked_by: str = ""                 # open decision preventing use, if any

    @property
    def is_ready(self) -> bool:
        return not self.blocked_by and bool(self.categories)


def _product_class(e: Estimate) -> str:
    """cigarette-only versus mixed or other products (D009)."""
    kinds = {p.strip().lower() for p in e.product_types if p.strip()}
    if not kinds or kinds == {"nr"}:
        return MISSING
    return "cigarette_only" if kinds == {"cigarette"} else "mixed_or_other"


def _alcohol_adjusted(e: Estimate) -> str:
    v = (e.adjusted_alcohol or "").strip().lower()
    return v if v in ("yes", "no") else MISSING


def _risk_of_bias(e: Estimate) -> str:
    return (e.risk_of_bias_level or "").strip().lower() or MISSING


def _subsite(e: Estimate) -> str:
    return (e.outcome_site or "").strip().lower() or MISSING


def _region(e: Estimate) -> str:
    # Deliberately NOT mapped: country -> region needs a stated scheme (UN, WHO, or other),
    # which is a methodological decision nobody has made. Returning the raw country keeps the
    # value honest and makes the missing decision visible.
    return (e.country or "").strip().lower() or MISSING


#: The five subgroups named as planned in the manuscript, and nothing else.
SUBGROUPS: dict[str, Subgroup] = {
    "product_type": Subgroup(
        "product_type", "Product type (cigarette-only vs mixed or other)",
        "estimates.product_types", ("cigarette_only", "mixed_or_other")),
    "alcohol_adjustment": Subgroup(
        "alcohol_adjustment", "Alcohol-adjusted vs not alcohol-adjusted",
        "estimates.adjusted_alcohol", ("yes", "no")),
    "subsite": Subgroup(
        "subsite", "Anatomical subsite", "estimates.outcome_site", (),
        blocked_by="P014-P022: the eligible subsite list is not settled, so no category set exists"),
    "region": Subgroup(
        "region", "Geographical region", "studies.country", (),
        blocked_by="no country-to-region scheme has been chosen (UN, WHO or other)"),
    "risk_of_bias": Subgroup(
        "risk_of_bias", "Risk-of-bias level", "risk_of_bias.judgement", (),
        blocked_by="P023: no appraisal instrument chosen, so no judgement categories exist"),
}

_CLASSIFIERS = {"product_type": _product_class, "alcohol_adjustment": _alcohol_adjusted,
                "subsite": _subsite, "region": _region, "risk_of_bias": _risk_of_bias}


# --------------------------------------------------------------------------- selection

@dataclass(frozen=True)
class SelectionConflict:
    study_id: str
    estimate_ids: tuple[str, ...]
    reason: str


def select_one_per_study(estimates: list[Estimate]) -> list[Estimate]:
    """Return one estimate per study, using the reviewer's recorded selection.

    A study contributing several estimates is the normal case, not an error: different exposure
    contrasts, adjustment sets and subsites all produce separate rows. They are **correlated**, so
    pooling them as independent studies would understate the standard error and overstate precision.

    This function does **not** choose. It requires that exactly one estimate per study carries the
    reviewer's `selected_for_analysis` marker — represented here by `is_primary_adjusted` — and
    refuses otherwise, listing the conflicts. **No estimate is ever discarded silently.**
    """
    if not estimates:
        raise PipelineError("no estimates to select from")

    by_study: dict[str, list[Estimate]] = {}
    for e in estimates:
        by_study.setdefault(e.study_id, []).append(e)

    chosen, conflicts = [], []
    for study_id, group in sorted(by_study.items()):
        if len(group) == 1:
            chosen.append(group[0])
            continue
        marked = [e for e in group if e.is_primary_adjusted]
        ids = tuple(e.estimate_id or "(unidentified)" for e in group)
        if len(marked) == 1:
            chosen.append(marked[0])
        elif not marked:
            conflicts.append(SelectionConflict(
                study_id, ids,
                f"{len(group)} estimates and none marked as the primary estimate for analysis"))
        else:
            conflicts.append(SelectionConflict(
                study_id, ids,
                f"{len(marked)} of {len(group)} estimates are marked primary; exactly one may be"))

    if conflicts:
        detail = "; ".join(f"{c.study_id}: {c.reason} [{', '.join(c.estimate_ids)}]"
                           for c in conflicts)
        raise PipelineError(
            "cannot select one estimate per study without the reviewer's decision. "
            f"{detail}. Correlated estimates from one study must never be pooled as independent "
            "studies (D004), and none has been discarded: record a selection for each conflict, "
            "with its rationale, and re-run."
        )
    return chosen


# --------------------------------------------------------------------------- subgroups

@dataclass(frozen=True)
class SubgroupResult:
    subgroup: Subgroup
    groups: dict[str, MetaResult]
    counts: dict[str, int]
    missing: int
    excluded_small: dict[str, int]
    q_between: float | None = None
    df_between: int | None = None
    p_between: float | None = None
    notes: list[str] = field(default_factory=list)

    @property
    def interpretation_warning(self) -> str:
        return (
            "A difference between subgroups is supported ONLY by the between-group test reported "
            "here. Comparing whether each subgroup's interval excludes the null is NOT evidence of "
            "a difference, and must not be reported as one."
        )

    def summary(self) -> str:
        head = f"Subgroup: {self.subgroup.label}  ({self.subgroup.source_field})"
        lines = [head, "-" * len(head)]
        for name, res in self.groups.items():
            lines.append(f"  {name:22} k={res.k:<3} {res.summary().splitlines()[0]}")
        if self.missing:
            lines.append(f"  {'missing/unclassifiable':22} n={self.missing} — excluded from the "
                         "test and reported, never imputed")
        for name, n in self.excluded_small.items():
            lines.append(f"  {name:22} k={n} — below the minimum, not pooled")
        if self.p_between is None:
            lines.append("  No between-group test: " + (self.notes[0] if self.notes else "n/a"))
        else:
            lines.append(f"  Between-group Q={self.q_between:.3f} (df={self.df_between}, "
                         f"p={self.p_between:.4f})")
        lines.append("  " + self.interpretation_warning)
        return "\n".join(lines)


def subgroup_analysis(estimates: list[Estimate], key: str, *,
                      min_studies: int = DEFAULT_MIN_STUDIES_PER_GROUP,
                      model: str = RANDOM, estimator: str = DL) -> SubgroupResult:
    """Pool within each stratum of a prespecified subgroup and test for a difference between them.

    One estimate per study must already have been selected; this function does not select.
    """
    if key not in SUBGROUPS:
        raise PipelineError(
            f"{key!r} is not a prespecified subgroup. Prespecified: {sorted(SUBGROUPS)}. "
            "Anything else is post-hoc and must be declared as such, not run here."
        )
    sub = SUBGROUPS[key]
    if sub.blocked_by:
        raise PipelineError(
            f"subgroup {key!r} cannot be run: {sub.blocked_by}. Running it would require inventing "
            "a category set that no decision supports."
        )
    if not estimates:
        raise PipelineError("no estimates: a subgroup analysis needs studies, and there are none")

    ids = [e.study_id for e in estimates]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        raise PipelineError(
            f"a study appears more than once: {', '.join(dupes)}. Select one estimate per study "
            "first (select_one_per_study); correlated estimates are not independent studies (D004)."
        )

    classify = _CLASSIFIERS[key]
    buckets: dict[str, list[Estimate]] = {}
    for e in estimates:
        buckets.setdefault(classify(e), []).append(e)

    missing = len(buckets.pop(MISSING, []))
    unknown = sorted(set(buckets) - set(sub.categories))
    if unknown:
        raise PipelineError(
            f"subgroup {key!r}: unexpected categories {unknown}. Permitted: "
            f"{list(sub.categories)}. An unplanned category is a data problem or a protocol "
            "change, not something to pool quietly."
        )

    groups, counts, too_small, notes = {}, {}, {}, []
    for name in sub.categories:
        group = buckets.get(name, [])
        counts[name] = len(group)
        if not group:
            continue
        if len(group) < min_studies:
            too_small[name] = len(group)
            notes.append(f"{name}: k={len(group)} below the minimum of {min_studies}; not pooled")
            continue
        groups[name] = pool(group, model=model, estimator=estimator)

    if missing:
        notes.append(f"{missing} estimate(s) could not be classified and are excluded from the "
                     "between-group test. They are reported, never imputed or reassigned.")

    q = df = p = None
    if len(groups) < MIN_GROUPS_FOR_TEST:
        notes.insert(0, f"only {len(groups)} group(s) met the minimum of {min_studies} studies; "
                        f"a between-group test needs at least {MIN_GROUPS_FOR_TEST}")
    else:
        # Between-group Q: the heterogeneity of the subgroup summaries about their common mean.
        weights = {n: 1.0 / (r.se ** 2) for n, r in groups.items()}
        total_w = sum(weights.values())
        mean = sum(weights[n] * groups[n].log_estimate for n in groups) / total_w
        q = sum(weights[n] * (groups[n].log_estimate - mean) ** 2 for n in groups)
        df = len(groups) - 1
        p = float(stats.chi2.sf(q, df))

    return SubgroupResult(sub, groups, counts, missing, too_small, q, df, p, notes)


def available_subgroups() -> dict[str, bool]:
    """Which prespecified subgroups can be run today, and which are blocked."""
    return {k: s.is_ready for k, s in SUBGROUPS.items()}
