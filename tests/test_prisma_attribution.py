"""PRISMA attribution: a claim of adjudication is not evidence of one.

Rows are structural stubs with no bibliographic content (D007). The four source categories a
full-text row can have — valid formal, valid provisional, invalid, and missing — must each land
in exactly one bucket, and the buckets must exhaust the worksheet.
"""
import csv

import pytest

from scripts.screening import prisma, validate_screening, vocabulary, worksheet
from scripts.screening.vocabulary import ADJUDICATED, ADOPTED, EXCLUDE, FT, INCLUDE, TA


def ta_full(rid, basis, adjudicated_date="", decision=INCLUDE, reason=""):
    r = {f: "" for f in worksheet.FIELDS[TA]}
    r.update(report_id=rid, record_id=f"rec-{rid}", pmid=f"90{rid[-2:]}", title=f"T {rid}",
             abstract="a", decision=decision, decision_basis=basis, reason_code=reason,
             suggestion=decision if basis == ADOPTED else "",
             suggestion_reason_code=reason if basis == ADOPTED else "",
             reviewer="SSK", screened_date="2026-11-01", adjudicated_date=adjudicated_date)
    return r


def ta_blank(rid):
    r = {f: "" for f in worksheet.FIELDS[TA]}
    r.update(report_id=rid, record_id=f"rec-{rid}", pmid=f"90{rid[-2:]}", title=f"T {rid}")
    return r


def ft_full(rid, claimed_basis):
    r = {f: "" for f in worksheet.FIELDS[FT]}
    r.update(report_id=rid, record_id=f"rec-{rid}", pmid=f"90{rid[-2:]}", title=f"T {rid}",
             source_ta_decision_basis=claimed_basis)
    return r


@pytest.fixture
def sheets(tmp_path, monkeypatch):
    screening = tmp_path / "data" / "screening"
    screening.mkdir(parents=True)
    monkeypatch.setattr(worksheet, "SCREENING_DIR", screening)
    monkeypatch.setattr(prisma, "load_sources", lambda: [])
    monkeypatch.setattr(prisma, "PROCESSED_DIR", tmp_path / "absent")

    def write(stage, rows):
        with open(worksheet.worksheet_path(stage), "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=worksheet.FIELDS[stage])
            w.writeheader()
            w.writerows(rows)
    return write


@pytest.fixture
def four_rows(sheets):
    """One valid formal, one valid provisional, one invalid, one with no source record."""
    sheets(TA, [ta_full("R0001", ADJUDICATED, "2026-11-10"),
                ta_full("R0002", ADOPTED),
                ta_full("R0003", ADJUDICATED)])            # invalid: no adjudicated_date
    sheets(FT, [ft_full("R0001", ADJUDICATED),
                ft_full("R0002", ADOPTED),
                ft_full("R0003", ""),
                ft_full("R0099", ADJUDICATED)])            # source record does not exist
    return prisma.gather()


# --- title/abstract classification ------------------------------------------------------

def test_the_four_source_categories_are_classified_correctly(four_rows):
    f = four_rows
    assert f["ta_adjudicated"] == 1, "only the valid adjudication is formal"
    assert f["ta_adopted"] == 1
    assert f["ta_invalid"] == 1, "an undated adjudication is invalid, not formal"
    assert f["ta_unscreened"] == 0


def test_an_invalid_adjudication_inflates_no_formal_count(four_rows):
    """The defect this guards: flipping decision_basis used to buy a formal screening count."""
    f = four_rows
    assert f["ta_screened"] == 1 and f["ta_included"] == 1
    assert f["ta_excluded"] == 0 and f["ta_unresolved"] == 0


def test_an_invalid_row_is_not_counted_as_provisional_either(four_rows):
    assert four_rows["ta_adopted"] == 1, "the invalid row must not fall back to provisional"


# --- full-text attribution ----------------------------------------------------------------

def test_a_missing_source_record_does_not_inflate_formal_retrieval(four_rows):
    """The four states are distinguished, not merged into one residual."""
    f = four_rows
    assert f["ft_rows"] == 4
    assert f["ft_sought"] == 1
    assert f["ft_provisional_sought"] == 1
    assert f["ft_invalid_source"] == 1, "R0003: source exists but fails validation"
    assert f["ft_unattributed"] == 1, "R0099: no source record at all"
    assert f["ft_ineligible_source"] == 0


def test_a_claimed_basis_in_the_full_text_file_is_not_trusted(four_rows):
    """R0099 carries 'independently_adjudicated' in its own row and is still not counted."""
    assert four_rows["ft_sought"] == 1


def test_a_valid_formal_source_does_reach_formal_retrieval(sheets):
    sheets(TA, [ta_full("R0001", ADJUDICATED, "2026-11-10")])
    sheets(FT, [ft_full("R0001", "")])          # claims nothing; the source decides
    f = prisma.gather()
    assert f["ft_sought"] == 1 and f["ft_unattributed"] == 0


def test_a_valid_provisional_source_reaches_provisional_retrieval(sheets):
    sheets(TA, [ta_full("R0001", ADOPTED)])
    sheets(FT, [ft_full("R0001", ADJUDICATED)])   # lies about its source
    f = prisma.gather()
    assert f["ft_sought"] == 0 and f["ft_provisional_sought"] == 1


# --- identities ----------------------------------------------------------------------------

def test_both_accounting_identities_hold_for_the_four_rows(four_rows):
    f = four_rows
    assert (f["ta_adjudicated"] + f["ta_adopted"] + f["ta_invalid"] + f["ta_unscreened"]
            == f["ta_total"])
    assert (f["ft_sought"] + f["ft_provisional_sought"] + f["ft_invalid_source"]
            + f["ft_ineligible_source"] + f["ft_unattributed"] == f["ft_rows"])
    assert prisma.consistency(f) == []


def test_a_broken_title_abstract_identity_is_reported():
    flow = {"ta_adjudicated": 1, "ta_adopted": 1, "ta_invalid": 1, "ta_unscreened": 0,
            "ta_total": 10, "ta_reasons": {}, "ft_reasons": {}, "ft_exists": False}
    assert any("plus invalid (1) plus not screened" in p for p in prisma.consistency(flow))


def test_a_broken_full_text_identity_is_reported():
    flow = {"ft_sought": 1, "ft_provisional_sought": 1, "ft_invalid_source": 0,
            "ft_ineligible_source": 0, "ft_unattributed": 0, "ft_rows": 9,
            "ta_reasons": {}, "ft_reasons": {}, "ft_exists": True}
    problems = prisma.consistency(flow)
    assert any("does not equal the full-text worksheet" in p for p in problems)
    assert any("ineligible source" in p for p in problems), "every state is named"


# --- reporting -------------------------------------------------------------------------------

def test_invalid_and_unattributed_rows_are_reported_not_omitted(four_rows):
    body = prisma.render(four_rows, [])
    assert "**invalid**" in body and "| Full-text rows in the worksheet | 4 |" in body
    assert "| Full-text rows whose source record fails validation | 1 |" in body
    assert "| Full-text rows with no source record at all | 1 |" in body
    assert "| Full-text rows whose source is valid but no longer an include | 0 |" in body


def test_the_diagram_annotates_them_outside_the_flow(four_rows):
    from scripts.visualization.prisma_diagram import MAIN, SIDE, build_boxes
    diagram = build_boxes(four_rows)
    assert "fail validation" in diagram.footnote
    assert "source record that fails validation" in diagram.footnote
    assert "no source record at all" in diagram.footnote
    assert sum(1 for b in diagram.boxes if b.column == MAIN) == 5
    assert sum(1 for b in diagram.boxes if b.column == SIDE) == 4
    body = "\n".join(b.text for b in diagram.boxes)
    assert "invalid" not in body, "no box may carry an invalid count"


# --- a mixed population with every category present --------------------------------------------

def test_a_mixed_population_with_every_category(sheets):
    sheets(TA, [
        ta_full("R0001", ADJUDICATED, "2026-11-10"),
        ta_full("R0002", ADJUDICATED, "2026-11-10", decision=EXCLUDE, reason="wrong_outcome"),
        ta_full("R0003", ADOPTED),
        ta_full("R0004", ADOPTED, decision=EXCLUDE, reason="wrong_design"),
        ta_full("R0005", ADJUDICATED),                 # invalid
        ta_blank("R0006"),                             # unscreened
    ])
    f = prisma.gather()
    assert (f["ta_adjudicated"], f["ta_adopted"], f["ta_invalid"], f["ta_unscreened"]) == \
        (2, 2, 1, 1)
    assert f["ta_total"] == 6
    assert (f["ta_included"], f["ta_excluded"]) == (1, 1), "formal counts exclude the rest"
    assert (f["prov_included"], f["prov_excluded"]) == (1, 1)
    assert prisma.consistency(f) == []


def test_the_validator_and_the_flow_agree_on_what_is_invalid(sheets):
    """All three layers use the same check, so they cannot disagree."""
    rows = [ta_full("R0001", ADJUDICATED), ta_full("R0002", ADJUDICATED, "2026-11-10")]
    sheets(TA, rows)
    vocab = vocabulary.load_vocabulary()
    rejected = {r["report_id"] for r in rows if worksheet.adjudication_problems(r, vocab)}
    src = [{"report_id": r["report_id"], "pmid": r["pmid"], "title": r["title"]} for r in rows]
    errors = validate_screening.check(rows, src, TA).errors
    assert rejected == {"R0001"}
    assert any("R0001" in e for e in errors)
    assert prisma.gather()["ta_invalid"] == 1


# --- a valid source that is no longer an include ------------------------------------------

def test_a_valid_but_ineligible_source_is_counted_separately(sheets):
    """A reviewer changes a title/abstract decision to exclude after the full-text worksheet
    was built. The row is stale: its source is valid, but it is no longer an include."""
    sheets(TA, [ta_full("R0001", ADJUDICATED, "2026-11-10", decision=EXCLUDE,
                        reason="wrong_outcome")])
    sheets(FT, [ft_full("R0001", ADJUDICATED)])
    f = prisma.gather()
    assert f["ft_ineligible_source"] == 1
    assert f["ft_sought"] == 0, "a stale row must not count as a formal retrieval"
    assert f["ft_invalid_source"] == 0, "its source is valid; the problem is eligibility"
    assert f["ft_unattributed"] == 0, "the source record does exist"
    assert prisma.consistency(f) == []


def test_an_ineligible_source_is_not_confused_with_an_invalid_one(sheets):
    sheets(TA, [ta_full("R0001", ADJUDICATED, "2026-11-10", decision=EXCLUDE,
                        reason="wrong_outcome"),      # valid, ineligible
                ta_full("R0002", ADJUDICATED)])        # invalid: no adjudicated_date
    sheets(FT, [ft_full("R0001", ADJUDICATED), ft_full("R0002", ADJUDICATED)])
    f = prisma.gather()
    assert (f["ft_ineligible_source"], f["ft_invalid_source"]) == (1, 1)
    assert f["ft_sought"] == 0 and f["ft_provisional_sought"] == 0


def test_an_unscreened_source_is_ineligible_not_invalid(sheets):
    """A row with no decision at all is valid; it simply is not an include."""
    sheets(TA, [ta_blank("R0001")])
    sheets(FT, [ft_full("R0001", ADJUDICATED)])
    f = prisma.gather()
    assert f["ft_ineligible_source"] == 1 and f["ft_invalid_source"] == 0


def test_every_full_text_state_in_one_population(sheets):
    sheets(TA, [
        ta_full("R0001", ADJUDICATED, "2026-11-10"),                       # formal include
        ta_full("R0002", ADOPTED),                                         # provisional include
        ta_full("R0003", ADJUDICATED),                                     # invalid
        ta_full("R0004", ADJUDICATED, "2026-11-10", decision=EXCLUDE,
                reason="wrong_outcome"),                                   # valid, ineligible
    ])
    sheets(FT, [ft_full("R0001", ADJUDICATED), ft_full("R0002", ADOPTED),
                ft_full("R0003", ADJUDICATED), ft_full("R0004", ADJUDICATED),
                ft_full("R0099", ADJUDICATED)])                            # no source
    f = prisma.gather()
    assert (f["ft_sought"], f["ft_provisional_sought"], f["ft_invalid_source"],
            f["ft_ineligible_source"], f["ft_unattributed"]) == (1, 1, 1, 1, 1)
    assert f["ft_rows"] == 5
    assert f["ta_included"] == 1 and f["prov_included"] == 1, "formal counts untouched"
    assert prisma.consistency(f) == []


def test_off_flow_states_never_inflate_formal_counts(sheets):
    """Three rows that must contribute nothing to screening, exclusion, inclusion or retrieval."""
    sheets(TA, [ta_full("R0003", ADJUDICATED),
                ta_full("R0004", ADJUDICATED, "2026-11-10", decision=EXCLUDE,
                        reason="wrong_outcome")])
    sheets(FT, [ft_full("R0003", ADJUDICATED), ft_full("R0004", ADJUDICATED),
                ft_full("R0099", ADJUDICATED)])
    f = prisma.gather()
    assert f["ft_sought"] == 0
    assert f["ta_included"] == 0
    assert f["ta_screened"] == 1, "only the valid adjudicated exclude is formally screened"
    assert f["ta_excluded"] == 1
    assert prisma.consistency(f) == []


def test_the_diagram_names_each_off_flow_state_separately(sheets):
    from scripts.visualization.prisma_diagram import MAIN, SIDE, build_boxes
    sheets(TA, [ta_full("R0003", ADJUDICATED),
                ta_full("R0004", ADJUDICATED, "2026-11-10", decision=EXCLUDE,
                        reason="wrong_outcome")])
    sheets(FT, [ft_full("R0003", ADJUDICATED), ft_full("R0004", ADJUDICATED),
                ft_full("R0099", ADJUDICATED)])
    diagram = build_boxes(prisma.gather())
    assert "source record that fails validation" in diagram.footnote
    assert "no longer an include" in diagram.footnote
    assert "no source record at all" in diagram.footnote
    assert sum(1 for b in diagram.boxes if b.column == MAIN) == 5
    assert sum(1 for b in diagram.boxes if b.column == SIDE) == 4
