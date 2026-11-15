"""Deduplication: one authoritative matching computation, reused downstream.

Matching must be computed once and its result passed on, not recomputed by each consumer.
Recomputation is not merely wasteful: `find_duplicates` is the only place the matching rules
live, so a second, independent computation is a second opportunity for the grouping used to
assign `report_id`s to diverge from the grouping reported in the audit trail. These tests pin
the single-computation invariant so it cannot be reintroduced, and pin that repeated execution
produces identical output.

Rows are structural stubs (field values like 't1', 'Last, First'), not citations — D007.
"""
import inspect

import pytest

from scripts.dedup import match

ORDER = ["src_a", "src_b"]


def row(rid, pmid="", doi="", title="", author="", year="", source="src_a"):
    return {"record_id": rid, "source_id": source, "pmid": pmid, "doi": doi,
            "title": title, "first_author": author, "pub_year": year}


def population():
    """A frame exercising every merge criterion plus a chain and a singleton."""
    return [
        row("a:1", pmid="1", doi="10.1/x", title="t1", author="L, F", year="2000"),
        row("a:2", pmid="1", title="t1 variant", author="L, F", year="2000"),   # PMID match
        row("a:3", doi="10.1/x", title="t1 other", author="L, F", year="2000"),  # DOI -> chain
        row("a:4", title="t9", author="M, G", year="1999"),                      # singleton
        row("b:5", title="t9", author="M, G", year="1999", source="src_b"),      # fingerprint
    ]


@pytest.fixture
def counting(monkeypatch):
    """Count calls to the matching primitives without altering their behaviour."""
    calls = {"find_duplicates": 0, "assign_report_ids": 0}
    real_fd, real_ar = match.find_duplicates, match.assign_report_ids

    def fd(rows):
        calls["find_duplicates"] += 1
        return real_fd(rows)

    def ar(*args, **kwargs):
        calls["assign_report_ids"] += 1
        return real_ar(*args, **kwargs)

    monkeypatch.setattr(match, "find_duplicates", fd)
    monkeypatch.setattr(match, "assign_report_ids", ar)
    return calls


# --- the single-computation invariant ----------------------------------------------------------

def test_resolve_computes_matching_exactly_once(counting):
    match.resolve(population(), ORDER)
    assert counting["find_duplicates"] == 1, "matching must be computed once per resolve()"
    assert counting["assign_report_ids"] == 1


def test_assign_report_ids_consumes_precomputed_groups_and_pairs():
    """Its signature must require the matching result, so it cannot recompute it."""
    params = inspect.signature(match.assign_report_ids).parameters
    assert "groups" in params and "pairs" in params
    body = inspect.getsource(match.assign_report_ids)
    assert "find_duplicates" not in body, "assign_report_ids must not rerun matching"


def test_the_reported_pairs_are_the_same_objects_that_produced_the_assignment():
    """A second computation could silently disagree with the one used for assignment."""
    rows = population()
    groups, pairs = match.find_duplicates(rows)
    assignment = match.assign_report_ids(rows, groups, pairs, ORDER)
    result = match.resolve(rows, ORDER)

    assert result.assignment == assignment
    assert [(p.record_a, p.record_b, p.criterion, p.resolution) for p in result.pairs] == \
           [(p.record_a, p.record_b, p.criterion, p.resolution) for p in pairs]
    # Every merged pair's two records must share the report_id the assignment gave them.
    for p in result.pairs:
        if p.resolution == match.MERGED:
            assert result.assignment[p.record_a]["report_id"] == \
                   result.assignment[p.record_b]["report_id"], \
                   "a merged pair whose records land in different reports means the grouping " \
                   "used for assignment diverged from the grouping reported"


def test_every_merged_pair_is_reflected_in_the_grouping_and_vice_versa():
    """The audit trail and the assignment must describe the same partition."""
    rows = population()
    result = match.resolve(rows, ORDER)
    by_report = {}
    for rid, info in result.assignment.items():
        by_report.setdefault(info["report_id"], set()).add(rid)

    merged = {frozenset((p.record_a, p.record_b)) for p in result.pairs
              if p.resolution == match.MERGED}
    for pair in merged:
        a, b = tuple(pair)
        assert result.assignment[a]["report_id"] == result.assignment[b]["report_id"]
    # No multi-record group may exist without at least one merged pair inside it.
    for report_id, members in by_report.items():
        if len(members) > 1:
            assert any(p <= members for p in merged), \
                f"{report_id} groups {sorted(members)} with no merged pair to justify it"


# --- repeated execution ------------------------------------------------------------------------

def test_repeated_execution_produces_identical_output():
    rows = population()
    first, second = match.resolve(rows, ORDER), match.resolve(rows, ORDER)
    assert first.assignment == second.assignment
    assert first.report_ids == second.report_ids
    assert [(p.record_a, p.record_b, p.criterion, p.matched_value, p.resolution) for p in first.pairs] == \
           [(p.record_a, p.record_b, p.criterion, p.matched_value, p.resolution) for p in second.pairs]


def test_repeated_execution_is_unaffected_by_input_order():
    rows = population()
    forward = match.resolve(rows, ORDER)
    backward = match.resolve(list(reversed(rows)), ORDER)
    assert forward.assignment == backward.assignment, \
        "report_id assignment must not depend on the order rows arrive in"


def test_matching_does_not_mutate_its_input():
    """A consumer that reused mutated rows would match against different data."""
    rows = population()
    before = [dict(r) for r in rows]
    match.resolve(rows, ORDER)
    assert rows == before


# --- record conservation -----------------------------------------------------------------------

def test_no_record_is_lost_or_assigned_twice():
    rows = population()
    result = match.resolve(rows, ORDER)
    assert set(result.assignment) == {r["record_id"] for r in rows}
    assert len(result.assignment) == len(rows)
    primaries = [rid for rid, i in result.assignment.items() if i["is_primary"] == "yes"]
    assert len(primaries) == len(result.report_ids), "exactly one primary per report"


def test_each_report_has_exactly_one_primary():
    rows = population()
    result = match.resolve(rows, ORDER)
    counts = {}
    for info in result.assignment.values():
        if info["is_primary"] == "yes":
            counts[info["report_id"]] = counts.get(info["report_id"], 0) + 1
    assert all(n == 1 for n in counts.values())
    assert set(counts) == result.report_ids


def test_every_duplicate_is_traceable_to_its_primary_and_its_evidence():
    rows = population()
    result = match.resolve(rows, ORDER)
    for rid, info in result.assignment.items():
        if info["is_primary"] == "yes":
            assert info["duplicate_of"] == "" and info["merge_criterion"] == ""
        else:
            assert info["duplicate_of"] in result.assignment, "must name a real record"
            assert info["merge_criterion"], "a duplicate must carry its evidence"
            assert result.assignment[info["duplicate_of"]]["is_primary"] == "yes"


def test_pairs_needing_review_are_never_silently_merged():
    """Record matching is not a study-level judgement; ambiguity stays visible."""
    rows = [row("a:1", title="a comparative study of oral lesions", author="L, F", year="2001"),
            row("a:2", title="a comparative study of oral lesion", author="L, F", year="2001")]
    result = match.resolve(rows, ORDER)
    assert result.unresolved_pairs, "near-identical titles must be flagged, not merged"
    ids = {i["report_id"] for i in result.assignment.values()}
    assert len(ids) == 2, "a pair awaiting review must not be grouped"
