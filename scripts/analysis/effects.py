"""Effect estimates on the log scale, with their provenance attached.

A ratio measure (OR, RR, HR) is pooled on the log scale, so every estimate must be converted and
given a standard error. Two routes are supported, and which one was used is recorded per estimate
because they are not equivalent in precision:

  * from a reported confidence interval — SE = (ln(upper) − ln(lower)) / (2 z)
  * from raw 2x2 counts — SE of ln(OR) = sqrt(1/a + 1/b + 1/c + 1/d)

Nothing is inferred. An estimate with no CI and no counts cannot be pooled and is rejected rather
than given a guessed variance.

Synthetic estimates must declare themselves. `synthetic=True` propagates through every
calculation, plot and report so that a test fixture can never be presented as a research finding.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from scripts.common.config import PipelineError

# Ratio measures are pooled on the log scale; a difference measure would not be.
RATIO_MEASURES = ("OR", "RR", "HR")
Z_95 = 1.959963984540054          # two-sided 95% normal quantile

# Relative gap between the reported estimate and the geometric mean of its CI, above which the
# inconsistency is recorded as a note. Mild asymmetry is normal when a source rounds its interval.
CI_ASYMMETRY_TOLERANCE = 0.10

FROM_CI = "SE from reported 95% CI"
FROM_COUNTS = "SE from 2x2 counts"
REPORTED_SE = "SE as reported"

# Adjustment status, mirroring config/extraction.yaml estimates.adjustment
CRUDE = "crude"
ADJUSTED = "adjusted"


@dataclass(frozen=True)
class Estimate:
    """One effect estimate from one study, ready for pooling.

    `source_location` is required: every number entering a synthesis must be traceable to a page,
    table or figure (provenance rule 4). `synthetic` marks a fixture that is not research data.
    Provenance and adjustment fields default to empty so that an estimate built directly in a test
    or from a 2x2 table is still valid. They are **required for any estimate entering a research
    synthesis**, and `provenance_problems()` reports what is missing rather than guessing.
    """
    study_id: str
    log_estimate: float
    se: float
    measure: str
    derivation: str
    source_location: str
    synthetic: bool = False
    notes: str = ""

    # --- adjustment (Part 2) -------------------------------------------------------------
    # `adjustment` mirrors the extraction enum: "crude" | "adjusted" | "" when unknown.
    # Adjusted and crude estimates answer different questions and are never pooled together
    # without an explicit, recorded justification.
    adjustment: str = ""
    adjusted_for: tuple[str, ...] = ()        # covariate list, verbatim, never harmonised here
    adjustment_set: str = ""                  # reviewer's label for this adjustment set
    is_primary_adjusted: bool = False         # the study's primary adjusted estimate?
    adjusted_alcohol: str = ""                # "yes" | "no" | "NR" — a subgroup and a key confounder

    # --- provenance ----------------------------------------------------------------------
    report_id: str = ""                       # which report of the study this came from (D004)
    estimate_id: str = ""

    # --- analysis context ----------------------------------------------------------------
    exposure_contrast: str = ""               # ever | current | former | dose_tier | other (P004)
    product_types: tuple[str, ...] = ()       # cigarette / bidi / cigar / pipe / mixed / NR (D009)
    outcome_site: str = ""                    # subsite this estimate refers to
    country: str = ""                         # as reported; region mapping is a pending decision
    design: str = ""                          # case_control | cohort
    risk_of_bias_level: str = ""              # populated only once P023 fixes an instrument

    @property
    def is_adjusted(self) -> bool:
        return self.adjustment == ADJUSTED

    @property
    def is_crude(self) -> bool:
        return self.adjustment == CRUDE

    def provenance_problems(self) -> list[str]:
        """What is missing before this estimate may enter a research synthesis.

        Reported rather than raised, so a caller can decide: a fixture legitimately lacks these,
        a research estimate must not.
        """
        problems = []
        if not self.source_location:
            problems.append("source_location is required (provenance rule 4)")
        if not self.report_id:
            problems.append("report_id is required: an estimate belongs to a report (D004)")
        if self.adjustment not in (CRUDE, ADJUSTED):
            problems.append(
                f"adjustment must be {CRUDE!r} or {ADJUSTED!r}, not {self.adjustment!r}; "
                "an estimate of unknown adjustment status cannot be placed in either analysis"
            )
        if self.adjustment == ADJUSTED and not self.adjusted_for:
            problems.append(
                "an adjusted estimate must record what it was adjusted for; "
                "'adjusted' without a covariate list is not interpretable"
            )
        return problems

    @property
    def variance(self) -> float:
        return self.se ** 2

    @property
    def estimate(self) -> float:
        return math.exp(self.log_estimate)

    def ci(self, z: float = Z_95) -> tuple[float, float]:
        return (math.exp(self.log_estimate - z * self.se),
                math.exp(self.log_estimate + z * self.se))


def _check_measure(measure: str) -> None:
    if measure not in RATIO_MEASURES:
        raise PipelineError(
            f"measure {measure!r} is not one of {RATIO_MEASURES}. Only ratio measures are pooled "
            "on the log scale here; a different measure needs its own, documented handling."
        )


def from_ci(study_id: str, estimate: float, ci_low: float, ci_high: float, measure: str,
            source_location: str, *, ci_level: float = 0.95, synthetic: bool = False,
            notes: str = "") -> Estimate:
    """Build an Estimate from a point estimate and its confidence interval."""
    _check_measure(measure)
    if not source_location:
        raise PipelineError(f"{study_id}: source_location is required for every extracted value")
    for name, value in (("estimate", estimate), ("ci_low", ci_low), ("ci_high", ci_high)):
        if not math.isfinite(value) or value <= 0:
            raise PipelineError(
                f"{study_id}: {name}={value} — a ratio measure must be finite and positive")
    if ci_low >= ci_high:
        raise PipelineError(f"{study_id}: ci_low ({ci_low}) must be below ci_high ({ci_high})")
    if not (ci_low <= estimate <= ci_high):
        raise PipelineError(
            f"{study_id}: the point estimate {estimate} lies outside its own confidence interval "
            f"({ci_low}, {ci_high}) — check the extraction against the source"
        )
    if ci_level != 0.95:
        raise PipelineError(
            f"{study_id}: ci_level={ci_level}; only 95% intervals are handled. Converting another "
            "level requires a documented decision, not a silent assumption."
        )
    se = (math.log(ci_high) - math.log(ci_low)) / (2 * Z_95)
    if se <= 0:
        raise PipelineError(f"{study_id}: derived SE is not positive ({se})")

    # The point estimate is kept as reported and the SE taken from the interval. If the two are
    # mutually inconsistent on the log scale the discrepancy is recorded, not reconciled: it may
    # be harmless rounding in the source, or it may signal a transcription error or an interval
    # built by a method other than the Wald approximation. Either way the reviewer should see it.
    implied = math.sqrt(ci_low * ci_high)
    relative_gap = abs(implied / estimate - 1.0)
    if relative_gap > CI_ASYMMETRY_TOLERANCE:
        notes = (f"{notes + '; ' if notes else ''}"
                 f"reported estimate {estimate:g} differs by {relative_gap:.1%} from the "
                 f"geometric mean of its CI ({implied:.4g}); the interval is not log-symmetric "
                 f"about the estimate. SE derived from the CI; estimate kept as reported. Check "
                 f"the source.")
    return Estimate(study_id, math.log(estimate), se, measure, FROM_CI, source_location,
                    synthetic, notes)


def from_counts(study_id: str, exposed_cases: int, exposed_noncases: int,
                unexposed_cases: int, unexposed_noncases: int, source_location: str, *,
                synthetic: bool = False, notes: str = "") -> Estimate:
    """Build an odds-ratio Estimate from a 2x2 table.

    No continuity correction is applied. A zero cell makes ln(OR) undefined, and silently adding
    0.5 would change the estimate without any record of it, so such a table is rejected and the
    decision left to the reviewer.
    """
    cells = {"exposed_cases": exposed_cases, "exposed_noncases": exposed_noncases,
             "unexposed_cases": unexposed_cases, "unexposed_noncases": unexposed_noncases}
    if not source_location:
        raise PipelineError(f"{study_id}: source_location is required for every extracted value")
    for name, n in cells.items():
        if not isinstance(n, int) or n < 0:
            raise PipelineError(f"{study_id}: {name}={n} — counts must be non-negative integers")
    zeros = [name for name, n in cells.items() if n == 0]
    if zeros:
        raise PipelineError(
            f"{study_id}: zero cell(s) {zeros} make ln(OR) undefined. No continuity correction is "
            "applied automatically; choose and record a method (e.g. a 0.5 correction, or the "
            "Mantel-Haenszel or Peto approach) as a documented decision."
        )
    log_or = (math.log(exposed_cases) + math.log(unexposed_noncases)
              - math.log(exposed_noncases) - math.log(unexposed_cases))
    se = math.sqrt(sum(1.0 / n for n in cells.values()))
    return Estimate(study_id, log_or, se, "OR", FROM_COUNTS, source_location, synthetic,
                    notes or f"2x2: {exposed_cases}/{exposed_noncases} vs "
                             f"{unexposed_cases}/{unexposed_noncases}")


def from_log_se(study_id: str, log_estimate: float, se: float, measure: str,
                source_location: str, *, synthetic: bool = False, notes: str = "") -> Estimate:
    """Build an Estimate where the study reported a log estimate and its SE directly."""
    _check_measure(measure)
    if not source_location:
        raise PipelineError(f"{study_id}: source_location is required for every extracted value")
    if not math.isfinite(log_estimate):
        raise PipelineError(f"{study_id}: log_estimate is not finite")
    if not math.isfinite(se) or se <= 0:
        raise PipelineError(f"{study_id}: se={se} must be finite and positive")
    return Estimate(study_id, log_estimate, se, measure, REPORTED_SE, source_location, synthetic,
                    notes)


def validate_set(estimates: list[Estimate], *, allow_mixed_adjustment: bool = False) -> None:
    """Checks that apply to a set of estimates about to be pooled.

    Refuses to mix synthetic and real estimates in the same analysis. That is the one failure mode
    that could put a test fixture inside a research result, so it is rejected outright rather than
    flagged.

    `allow_mixed_adjustment` exists so that pooling adjusted with crude estimates is possible only
    as a deliberate, recorded act. It defaults to False: the SAP lists mixing them without a
    defensible basis as a criterion for not pooling at all.
    """
    if not estimates:
        raise PipelineError("no estimates to pool")

    ids = [e.study_id for e in estimates]
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    if duplicates:
        raise PipelineError(
            f"a study appears more than once: {', '.join(duplicates)}. The unit of analysis is the "
            "study, and each may contribute at most one estimate per analysis (D004)."
        )

    kinds = {e.synthetic for e in estimates}
    if len(kinds) > 1:
        synthetic = sorted(e.study_id for e in estimates if e.synthetic)
        raise PipelineError(
            "refusing to pool synthetic and real estimates together. Synthetic: "
            f"{', '.join(synthetic)}. Fixtures exist to test the software and must never enter a "
            "research result."
        )

    measures = {e.measure for e in estimates}
    if len(measures) > 1:
        raise PipelineError(
            f"mixing effect measures {sorted(measures)} in one analysis. OR, RR and HR estimate "
            "different quantities; combining them needs a documented justification, so do it "
            "deliberately in separate analyses rather than implicitly here."
        )

    statuses = {e.adjustment for e in estimates}
    if CRUDE in statuses and ADJUSTED in statuses and not allow_mixed_adjustment:
        crude = sorted(e.study_id for e in estimates if e.is_crude)
        adjusted = sorted(e.study_id for e in estimates if e.is_adjusted)
        raise PipelineError(
            "refusing to pool adjusted and crude estimates together without an explicit "
            f"justification. Crude: {', '.join(crude)}. Adjusted: {', '.join(adjusted)}. "
            "They answer different questions, and the SAP lists this as a criterion for not "
            "pooling. Analyse them separately, or pass allow_mixed_adjustment=True having first "
            "recorded the methodological reason."
        )
