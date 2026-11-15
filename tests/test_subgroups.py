"""Adjustment provenance, subgroup architecture and dependence handling.

Every Estimate constructed here is a SYNTHETIC SOFTWARE FIXTURE, built in-process and marked
`synthetic=True` where it could otherwise be mistaken for research data. None is written to disk,
and none enters `data/`. No real effect estimate exists in this project — `data/extraction/` does
not exist — so these fixtures test the machinery only.
"""
from __future__ import annotations

import math

import pytest

from scripts.analysis.effects import ADJUSTED, CRUDE, Estimate, validate_set
from scripts.analysis.meta import pool
from scripts.analysis.subgroups import (DEFAULT_MIN_STUDIES_PER_GROUP, MISSING, SUBGROUPS,
                                        available_subgroups, select_one_per_study,
                                        subgroup_analysis)
from scripts.common.config import PipelineError


def fixture(study_id, *, log=0.4, se=0.15, adjustment=ADJUSTED, adjusted_for=("alcohol",),
            alcohol="yes", products=("cigarette",), estimate_id="", primary=False,
            site="", country="", rob="") -> Estimate:
    """A SYNTHETIC estimate for software validation only."""
    return Estimate(
        study_id=study_id, log_estimate=log, se=se, measure="OR",
        derivation="SYNTHETIC FIXTURE — not research data", source_location="fixture",
        synthetic=True, adjustment=adjustment, adjusted_for=tuple(adjusted_for),
        adjustment_set="fixture set", is_primary_adjusted=primary, adjusted_alcohol=alcohol,
        report_id=f"R-{study_id}", estimate_id=estimate_id or f"E-{study_id}",
        product_types=tuple(products), outcome_site=site, country=country, risk_of_bias_level=rob)


def group(n, prefix="S", **kw):
    return [fixture(f"{prefix}{i}", **kw) for i in range(1, n + 1)]


# --- 1 & 2. adjusted vs crude survive, and remain distinguishable ---------------------

def test_adjusted_and_crude_are_distinguishable():
    a, c = fixture("A", adjustment=ADJUSTED), fixture("C", adjustment=CRUDE, adjusted_for=())
    assert a.is_adjusted and not a.is_crude
    assert c.is_crude and not c.is_adjusted


def test_adjustment_variables_survive_into_the_analysis_layer():
    e = fixture("S1", adjusted_for=("age", "sex", "alcohol", "betel quid"))
    assert e.adjusted_for == ("age", "sex", "alcohol", "betel quid")
    assert e.adjustment_set == "fixture set"
    assert e.report_id == "R-S1" and e.estimate_id == "E-S1"
    assert e.adjusted_alcohol == "yes"


def test_an_adjusted_estimate_without_a_covariate_list_is_reported_as_a_problem():
    e = fixture("S1", adjustment=ADJUSTED, adjusted_for=())
    assert any("adjusted for" in p for p in e.provenance_problems())


def test_unknown_adjustment_status_is_reported_as_a_problem():
    e = fixture("S1", adjustment="")
    assert any("adjustment must be" in p for p in e.provenance_problems())


def test_a_complete_estimate_has_no_provenance_problems():
    assert fixture("S1").provenance_problems() == []


# --- 3. adjustment sets cannot be conflated ------------------------------------------

def test_pooling_adjusted_with_crude_is_refused_by_default():
    mixed = [fixture("S1", adjustment=ADJUSTED), fixture("S2", adjustment=CRUDE, adjusted_for=())]
    with pytest.raises(PipelineError, match="adjusted and crude"):
        validate_set(mixed)


def test_pooling_adjusted_with_crude_is_possible_only_as_a_deliberate_act():
    mixed = [fixture("S1", adjustment=ADJUSTED), fixture("S2", adjustment=CRUDE, adjusted_for=())]
    validate_set(mixed, allow_mixed_adjustment=True)       # must not raise


def test_different_adjustment_sets_remain_visible_after_pooling():
    """Pooling must not erase which covariates each estimate controlled for."""
    a = fixture("S1", adjusted_for=("alcohol",))
    b = fixture("S2", adjusted_for=("alcohol", "betel quid"))
    sets = {e.study_id: e.adjusted_for for e in (a, b)}
    pool([a, b])
    assert sets["S1"] != sets["S2"], "distinct adjustment sets must not be conflated"


# --- 4 & 5. subgroup assignment and missing data --------------------------------------

def test_prespecified_subgroups_are_exactly_the_five_in_the_manuscript():
    assert set(SUBGROUPS) == {"product_type", "alcohol_adjustment", "subsite", "region",
                              "risk_of_bias"}


def test_blocked_subgroups_refuse_rather_than_inventing_categories():
    for key in ("subsite", "region", "risk_of_bias"):
        assert not available_subgroups()[key]
        with pytest.raises(PipelineError, match="cannot be run"):
            subgroup_analysis(group(8), key)


def test_subgroup_assignment_is_preserved():
    cig = group(4, prefix="C", products=("cigarette",))
    mix = group(4, prefix="M", products=("cigarette", "bidi"))
    res = subgroup_analysis(cig + mix, "product_type")
    assert res.counts["cigarette_only"] == 4
    assert res.counts["mixed_or_other"] == 4
    assert set(res.groups) == {"cigarette_only", "mixed_or_other"}


def test_missing_subgroup_data_is_reported_never_imputed():
    known = group(4, prefix="K", products=("cigarette",))
    other = group(4, prefix="O", products=("bidi",))
    unknown = group(2, prefix="U", products=("NR",))
    res = subgroup_analysis(known + other + unknown, "product_type")
    assert res.missing == 2
    assert sum(r.k for r in res.groups.values()) == 8, "unclassifiable rows must not be absorbed"
    assert any("never imputed" in n for n in res.notes)


def test_an_unexpected_category_is_refused():
    from scripts.analysis import subgroups as sg
    est = group(8, products=("cigarette",))
    original = sg._CLASSIFIERS["product_type"]
    sg._CLASSIFIERS["product_type"] = lambda e: "an_unplanned_category"
    try:
        with pytest.raises(PipelineError, match="unexpected categories"):
            subgroup_analysis(est, "product_type")
    finally:
        sg._CLASSIFIERS["product_type"] = original


# --- 6. adequate evidence required ----------------------------------------------------

def test_a_group_below_the_minimum_is_not_pooled():
    big = group(5, prefix="B", alcohol="yes")
    small = group(2, prefix="S", alcohol="no")
    res = subgroup_analysis(big + small, "alcohol_adjustment")
    assert "no" in res.excluded_small and res.excluded_small["no"] == 2
    assert "no" not in res.groups


def test_no_between_group_test_when_fewer_than_two_groups_qualify():
    big = group(5, prefix="B", alcohol="yes")
    small = group(2, prefix="S", alcohol="no")
    res = subgroup_analysis(big + small, "alcohol_adjustment")
    assert res.p_between is None and res.q_between is None
    assert any("between-group test needs at least" in n for n in res.notes)


def test_between_group_test_is_reported_when_both_groups_qualify():
    yes = group(4, prefix="Y", alcohol="yes", log=0.2)
    no = group(4, prefix="N", alcohol="no", log=0.9)
    res = subgroup_analysis(yes + no, "alcohol_adjustment")
    assert res.df_between == 1
    assert res.q_between > 0 and 0.0 <= res.p_between <= 1.0


def test_output_warns_against_the_common_misinterpretation():
    res = subgroup_analysis(group(4, prefix="Y", alcohol="yes")
                            + group(4, prefix="N", alcohol="no"), "alcohol_adjustment")
    assert "NOT evidence of a difference" in res.interpretation_warning
    assert "NOT evidence of a difference" in res.summary()


def test_subgroup_analysis_refuses_with_no_estimates():
    with pytest.raises(PipelineError, match="needs studies"):
        subgroup_analysis([], "product_type")


def test_post_hoc_subgroups_are_refused():
    with pytest.raises(PipelineError, match="not a prespecified subgroup"):
        subgroup_analysis(group(8), "smoking_intensity")


# --- 7. dependence: multiple estimates from one study ---------------------------------

def test_correlated_estimates_cannot_reach_a_subgroup_analysis():
    two = [fixture("S1", estimate_id="E1"), fixture("S1", estimate_id="E2")] + group(6)
    with pytest.raises(PipelineError, match="appears more than once"):
        subgroup_analysis(two, "product_type")


def test_selection_refuses_when_no_primary_is_marked():
    est = [fixture("S1", estimate_id="E1"), fixture("S1", estimate_id="E2")]
    with pytest.raises(PipelineError, match="none marked as the primary"):
        select_one_per_study(est)


def test_selection_refuses_when_several_are_marked_primary():
    est = [fixture("S1", estimate_id="E1", primary=True),
           fixture("S1", estimate_id="E2", primary=True)]
    with pytest.raises(PipelineError, match="are marked primary"):
        select_one_per_study(est)


def test_selection_error_names_every_candidate_so_nothing_is_discarded_silently():
    est = [fixture("S1", estimate_id="E1"), fixture("S1", estimate_id="E2"),
           fixture("S1", estimate_id="E3")]
    with pytest.raises(PipelineError) as exc:
        select_one_per_study(est)
    for eid in ("E1", "E2", "E3"):
        assert eid in str(exc.value)
    assert "none has been discarded" in str(exc.value)


def test_selection_uses_the_reviewers_recorded_choice():
    est = [fixture("S1", estimate_id="E1", log=0.1),
           fixture("S1", estimate_id="E2", log=0.9, primary=True),
           fixture("S2", estimate_id="E3")]
    chosen = select_one_per_study(est)
    assert [e.estimate_id for e in chosen] == ["E2", "E3"]


def test_a_single_estimate_per_study_needs_no_marker():
    chosen = select_one_per_study(group(3))
    assert len(chosen) == 3


# --- 8 & 9. existing behaviour and zero-study safeguards hold -------------------------

def test_existing_pooling_behaviour_is_unchanged():
    est = group(4)
    res = pool(est)
    assert res.k == 4
    assert math.isclose(res.log_estimate, 0.4, abs_tol=1e-9), "equal estimates pool to themselves"
    assert res.synthetic is True


def test_zero_study_safeguards_remain():
    with pytest.raises(PipelineError, match="no estimates"):
        validate_set([])
    with pytest.raises(PipelineError):
        pool([])


def test_duplicate_study_safeguard_remains():
    with pytest.raises(PipelineError, match="appears more than once"):
        validate_set([fixture("S1"), fixture("S1")])


def test_synthetic_and_real_still_cannot_be_mixed():
    real = Estimate("R1", 0.3, 0.1, "OR", "d", "Table 1", synthetic=False, adjustment=ADJUSTED,
                    adjusted_for=("alcohol",), report_id="R-R1")
    with pytest.raises(PipelineError, match="synthetic"):
        validate_set([real, fixture("S1")])


def test_fixtures_are_marked_synthetic():
    """Guards the rule that fixtures can never be mistaken for research data."""
    assert all(e.synthetic for e in group(3))
