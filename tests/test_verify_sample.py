"""Blinded verification of a sample of recorded title/abstract decisions.

Rows are structural stubs with no bibliographic content (D007). Decisions here are synthetic
inputs used to exercise the agreement arithmetic and the pre-specified acceptance rule; none is
presented as a reviewer's judgement, and no test writes to the project's own worksheet.
"""
import csv
import hashlib

import pytest

from scripts.common.config import PipelineError
from scripts.screening import verify_sample, worksheet
from scripts.screening.verify_sample import (ADOPT_AT, EXTEND_AT, RESPONSE, SHEET_FIELDS, build_sheet,
                                             draw, kappa, score, seed_from, verdict)
from scripts.screening.vocabulary import EXCLUDE, INCLUDE, TA, UNRESOLVED

FIELDS = worksheet.FIELDS[TA]


def ta_row(n, decision="", reason=""):
    r = {f: "" for f in FIELDS}
    r.update({"report_id": f"R{n:04d}", "record_id": f"rec-{n:04d}", "source_id": "stub_v1",
              "pmid": f"{9000000 + n}", "pub_year": "2000", "first_author": f"Author{n}",
              "journal": "Journal", "publication_types": "Journal Article",
              "title": f"Title {n}", "abstract": f"Abstract {n}",
              "decision": decision, "reason_code": reason,
              "reviewer": "SSK" if decision else "", "screened_date": "2026-11-01" if decision else ""})
    return r


def population(n_exclude=60, n_include=40, reason="wrong_outcome"):
    rows = [ta_row(i, EXCLUDE, reason) for i in range(1, n_exclude + 1)]
    rows += [ta_row(i, INCLUDE) for i in range(n_exclude + 1, n_exclude + n_include + 1)]
    return rows


def sheet_from(ta_rows, reviewer_decisions):
    """A completed sheet: reviewer_decisions maps report_id -> (decision, reason)."""
    out = []
    for r in ta_rows:
        d, reason = reviewer_decisions[r["report_id"]]
        entry = {f: "" for f in SHEET_FIELDS}
        entry.update({"report_id": r["report_id"], "title": r["title"],
                      "your_decision": d, "your_reason_code": reason})
        out.append(entry)
    return out


def as_recorded(ta_rows, flip=0, direction="exclude_to_include"):
    """Reviewer agrees with every record except `flip` of them, in the stated direction."""
    out, flipped = {}, 0
    for r in ta_rows:
        d, reason = r["decision"], r["reason_code"]
        if flipped < flip:
            if direction == "exclude_to_include" and d == EXCLUDE:
                d, reason, flipped = INCLUDE, "", flipped + 1
            elif direction == "include_to_exclude" and d == INCLUDE:
                d, reason, flipped = EXCLUDE, "wrong_design", flipped + 1
        out[r["report_id"]] = (d, reason)
    assert flipped == flip, "fixture could not flip the requested number"
    return out


# --- the draw is reproducible and unchosen ---------------------------------------------

def test_the_seed_is_derived_from_the_worksheet_not_chosen():
    assert seed_from("5938922a529a7f73") == 0x5938922a == 1496879658
    assert seed_from("00000001ffff") == 1


def test_the_same_worksheet_always_draws_the_same_sample():
    rows = population()
    a = [r["report_id"] for r in draw(rows, 40, 1496879658)]
    b = [r["report_id"] for r in draw(rows, 40, 1496879658)]
    assert a == b and len(a) == 40


def test_a_different_seed_draws_a_different_sample():
    rows = population()
    a = {r["report_id"] for r in draw(rows, 40, 1)}
    b = {r["report_id"] for r in draw(rows, 40, 2)}
    assert a != b


def test_the_sample_is_returned_in_worksheet_order_and_without_repeats():
    ids = [r["report_id"] for r in draw(population(), 40, 7)]
    assert ids == sorted(ids) and len(set(ids)) == 40


@pytest.mark.parametrize("size", [0, -1, 101])
def test_an_impossible_sample_size_is_refused(size):
    with pytest.raises(PipelineError):
        draw(population(), size, 1)


# --- the instrument is genuinely blinded ------------------------------------------------

def test_the_sheet_carries_no_recorded_decision():
    """If the reviewer can see the recorded decision, this confirms rather than verifies."""
    sample = draw(population(), 40, 1496879658)
    sheet = build_sheet(sample, {})
    for leak in ("decision", "reason_code", "reviewer", "screened_date", "notes"):
        assert leak not in sheet[0], f"{leak} must not appear in the blinded sheet"
    joined = " ".join(v for row in sheet for v in row.values())
    assert EXCLUDE not in joined and INCLUDE not in joined
    assert all(row[f] == "" for row in sheet for f in RESPONSE)


def test_the_sheet_shows_what_the_reviewer_needs_to_judge():
    sheet = build_sheet([ta_row(1, EXCLUDE, "wrong_outcome")], {"rec-0001": "eng"})
    assert sheet[0]["title"] == "Title 1" and sheet[0]["abstract"] == "Abstract 1"
    assert sheet[0]["publication_types"] == "Journal Article"
    assert sheet[0]["language"] == "eng", "language is needed to judge not_english"


# --- agreement arithmetic ----------------------------------------------------------------

def test_kappa_matches_a_hand_worked_value():
    """5 (exc,exc) + 1 (exc,inc) + 4 (inc,inc): po=0.9, pe=0.5, kappa=0.8."""
    pairs = [(EXCLUDE, EXCLUDE)] * 5 + [(EXCLUDE, INCLUDE)] + [(INCLUDE, INCLUDE)] * 4
    assert kappa(pairs) == pytest.approx(0.8)


def test_kappa_is_undefined_rather_than_zero_without_variation():
    """Both raters excluding everything gives 0/0; reporting 0.0 would read as chance agreement."""
    assert kappa([(EXCLUDE, EXCLUDE)] * 40) is None
    assert kappa([]) is None


@pytest.mark.parametrize("rate,expected", [
    (1.0, "ADOPT"), (ADOPT_AT, "ADOPT"), (0.949, "EXTEND"),
    (EXTEND_AT, "EXTEND"), (0.899, "RE-SCREEN"), (0.0, "RE-SCREEN"),
])
def test_the_acceptance_rule_is_applied_as_pre_specified(rate, expected):
    assert verdict(rate) == expected


def test_full_agreement_adopts_the_remainder():
    rows = population()
    sample = draw(rows, 40, 1496879658)
    result = score(sheet_from(sample, as_recorded(sample)), rows)
    assert result["agreed"] == 40 and result["rate"] == 1.0
    assert result["verdict"] == "ADOPT" and result["discrepancies"] == []


def test_two_discrepancies_in_forty_still_adopts():
    rows = population()
    sample = draw(rows, 40, 1496879658)
    result = score(sheet_from(sample, as_recorded(sample, flip=2)), rows)
    assert result["rate"] == pytest.approx(0.95) and result["verdict"] == "ADOPT"


def test_three_discrepancies_extends_the_sample():
    rows = population()
    sample = draw(rows, 40, 1496879658)
    result = score(sheet_from(sample, as_recorded(sample, flip=3)), rows)
    assert result["rate"] == pytest.approx(0.925) and result["verdict"] == "EXTEND"


def test_five_discrepancies_forces_a_full_re_screen():
    rows = population()
    sample = draw(rows, 40, 1496879658)
    result = score(sheet_from(sample, as_recorded(sample, flip=5)), rows)
    assert result["rate"] == pytest.approx(0.875) and result["verdict"] == "RE-SCREEN"


# --- the asymmetry rule -------------------------------------------------------------------

def test_an_erroneous_exclusion_triggers_a_sweep_of_that_reason_code():
    rows = population(reason="wrong_outcome")
    sample = draw(rows, 40, 1496879658)
    result = score(sheet_from(sample, as_recorded(sample, flip=1)), rows)
    assert result["sweeps"] == ["wrong_outcome"]
    assert result["sweep_sizes"]["wrong_outcome"] == 60, "every record with that reason"
    assert "evidence lost" in verify_sample.render(result, "x" * 64)


def test_the_opposite_direction_triggers_no_sweep():
    """Including something the reviewer would exclude costs retrieval effort, not evidence."""
    rows = population()
    sample = draw(rows, 40, 1496879658)
    result = score(sheet_from(sample, as_recorded(sample, flip=1,
                                                  direction="include_to_exclude")), rows)
    assert result["discrepancies"] and result["sweeps"] == []
    assert "Not triggered" in verify_sample.render(result, "x" * 64)


def test_reason_code_disagreement_is_reported_without_changing_the_decision_rate():
    rows = population()
    sample = draw(rows, 40, 1496879658)
    responses = as_recorded(sample)
    rid = next(r["report_id"] for r in sample if r["decision"] == EXCLUDE)
    responses[rid] = (EXCLUDE, "wrong_design")
    result = score(sheet_from(sample, responses), rows)
    assert result["rate"] == 1.0, "the decision still agrees"
    assert result["reason_discrepancies"] == [(rid, "wrong_outcome", "wrong_design")]


# --- the completed sheet must be valid before it is scored ---------------------------------

def test_an_unanswered_row_is_refused():
    rows = population()
    sample = draw(rows, 40, 1496879658)
    sheet = sheet_from(sample, as_recorded(sample))
    sheet[0]["your_decision"] = ""
    with pytest.raises(PipelineError, match="no your_decision"):
        score(sheet, rows)


@pytest.mark.parametrize("decision,reason,match", [
    ("maybe", "", "not a decision value"),
    (EXCLUDE, "", "no reason code"),
    (EXCLUDE, "no_usable_data", "not permitted at title/abstract"),
    (INCLUDE, "wrong_outcome", "reason code recorded on a non-exclusion"),
])
def test_an_invalid_judgement_is_refused(decision, reason, match):
    rows = population()
    sample = draw(rows, 40, 1496879658)
    sheet = sheet_from(sample, as_recorded(sample))
    sheet[0].update(your_decision=decision, your_reason_code=reason)
    with pytest.raises(PipelineError, match=match):
        score(sheet, rows)


def test_unresolved_is_an_acceptable_judgement():
    rows = population()
    sample = draw(rows, 40, 1496879658)
    responses = as_recorded(sample)
    rid = sample[0]["report_id"]
    responses[rid] = (UNRESOLVED, "")
    result = score(sheet_from(sample, responses), rows)
    assert result["agreed"] == 39 and result["sweeps"] == []


def test_a_report_outside_the_worksheet_is_refused():
    rows = population()
    sample = draw(rows, 40, 1496879658)
    sheet = sheet_from(sample, as_recorded(sample))
    sheet[0]["report_id"] = "R9999"
    with pytest.raises(PipelineError, match="not in the title/abstract worksheet"):
        score(sheet, rows)


# --- the CLI never touches the recorded decisions -------------------------------------------

@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    screening = tmp_path / "data" / "screening"
    screening.mkdir(parents=True)
    monkeypatch.setattr(worksheet, "SCREENING_DIR", screening)
    monkeypatch.setattr(verify_sample, "VALIDATION_DIR", tmp_path / "results" / "validation")
    path = worksheet.worksheet_path(TA)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(population())
    return path


def test_drawing_does_not_alter_the_worksheet(sandbox, capsys):
    before = hashlib.sha256(sandbox.read_bytes()).hexdigest()
    assert verify_sample.main(["--draw"]) == 0
    assert hashlib.sha256(sandbox.read_bytes()).hexdigest() == before
    sheet = list(csv.DictReader(open(verify_sample.sheet_path(), encoding="utf-8", newline="")))
    assert len(sheet) == 40 and "decision" not in sheet[0]
    capsys.readouterr()


def test_drawing_refuses_to_overwrite_a_sheet_that_may_hold_judgements(sandbox, capsys):
    assert verify_sample.main(["--draw"]) == 0
    assert verify_sample.main(["--draw"]) == 1
    assert "not overwritten" in capsys.readouterr().err


def test_scoring_before_drawing_fails(sandbox, capsys):
    assert verify_sample.main(["--score"]) == 1
    assert "Run --draw first" in capsys.readouterr().err


def test_scoring_writes_a_report_and_leaves_the_worksheet_alone(sandbox, capsys):
    before = hashlib.sha256(sandbox.read_bytes()).hexdigest()
    verify_sample.main(["--draw"])
    path = verify_sample.sheet_path()
    rows = list(csv.DictReader(open(path, encoding="utf-8", newline="")))
    ta = {r["report_id"]: r for r in population()}
    for r in rows:
        rec = ta[r["report_id"]]
        r["your_decision"], r["your_reason_code"] = rec["decision"], rec["reason_code"]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=SHEET_FIELDS)
        w.writeheader()
        w.writerows(rows)

    assert verify_sample.main(["--score"]) == 0
    assert hashlib.sha256(sandbox.read_bytes()).hexdigest() == before
    report = (verify_sample.VALIDATION_DIR / "screening_verification.md").read_text(encoding="utf-8")
    assert "**Verdict: ADOPT**" in report
    assert "not** independent duplicate screening" in report
    capsys.readouterr()


def test_the_report_distinguishes_suggestions_decisions_sample_and_agreement():
    """The reader must not be able to mistake this for inter-reviewer agreement."""
    rows = population()
    sample = draw(rows, 40, 1496879658)
    report = verify_sample.render(score(sheet_from(sample, as_recorded(sample)), rows), "x" * 64)
    for term in ("**Automated suggestion**", "**Human reviewer decision**",
                 "**Blinded verification sample**", "**Agreement**"):
        assert term in report
    assert "not a reference standard" in report
    assert "not** inter-reviewer agreement" in report
    assert "not** treat the suggestions as ground truth" in report


# --- The reported draw provenance is recorded, not re-derived -----------------------------------
#
# The seed is a function of the worksheet, so once the worksheet changes a re-derived seed names a
# draw that never happened. These tests pin the distinction between the draw's provenance and the
# state of the file a scoring run happens to read.

def complete_sheet(path, ta_rows):
    """Fill a drawn sheet with the recorded decisions, i.e. perfect agreement."""
    rows = list(csv.DictReader(open(path, encoding="utf-8", newline="")))
    recorded = {r["report_id"]: r for r in ta_rows}
    for r in rows:
        rec = recorded[r["report_id"]]
        r["your_decision"], r["your_reason_code"] = rec["decision"], rec["reason_code"]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=SHEET_FIELDS)
        w.writeheader()
        w.writerows(rows)
    return rows


def test_the_recorded_draw_seed_is_the_seed_of_the_recorded_digest():
    # A typo in either constant would make the pair describe no draw at all.
    assert seed_from(verify_sample.DRAW_SHA) == verify_sample.DRAW_SEED
    assert verify_sample.DRAW_SEED == 1496879658
    assert len(verify_sample.DRAW_SHA) == 64
    assert int(verify_sample.DRAW_SHA, 16) >= 0          # a real hex digest


def test_scoring_reports_the_recorded_draw_seed_not_one_derived_from_the_worksheet(sandbox, capsys):
    verify_sample.main(["--draw"])
    complete_sheet(verify_sample.sheet_path(), population())
    assert verify_sample.main(["--score"]) == 0
    report = (verify_sample.VALIDATION_DIR / "screening_verification.md").read_text(encoding="utf-8")

    live = hashlib.sha256(sandbox.read_bytes()).hexdigest()
    assert str(verify_sample.DRAW_SEED) in report
    assert verify_sample.DRAW_SHA in report
    # The sandbox worksheet is not the committed one, so its own seed must not be reported as
    # the draw seed.
    assert live != verify_sample.DRAW_SHA
    assert f"`{seed_from(live)}`" not in report
    capsys.readouterr()


def test_scoring_reports_the_current_worksheet_digest_separately(sandbox, capsys):
    verify_sample.main(["--draw"])
    complete_sheet(verify_sample.sheet_path(), population())
    verify_sample.main(["--score"])
    report = (verify_sample.VALIDATION_DIR / "screening_verification.md").read_text(encoding="utf-8")

    live = hashlib.sha256(sandbox.read_bytes()).hexdigest()
    assert "Worksheet SHA-256 at the draw | `" + verify_sample.DRAW_SHA in report
    assert "Current worksheet SHA-256 | `" + live in report
    assert "## This scoring run" in report
    capsys.readouterr()


def test_no_report_labels_a_current_digest_as_pre_specified_draw_provenance(sandbox, capsys):
    verify_sample.main(["--draw"])
    complete_sheet(verify_sample.sheet_path(), population())
    verify_sample.main(["--score"])
    report = (verify_sample.VALIDATION_DIR / "screening_verification.md").read_text(encoding="utf-8")

    live = hashlib.sha256(sandbox.read_bytes()).hexdigest()
    prespecified = report.split("## Pre-specified before the sample was drawn")[1].split("##")[0]
    this_run = report.split("## This scoring run")[1].split("##")[0]
    assert verify_sample.DRAW_SHA in prespecified and live not in prespecified
    assert live in this_run and verify_sample.DRAW_SHA not in this_run
    capsys.readouterr()


def test_a_changed_worksheet_warns_but_scoring_continues(sandbox, capsys):
    verify_sample.main(["--draw"])
    complete_sheet(verify_sample.sheet_path(), population())
    assert verify_sample.main(["--score"]) == 0          # exit 0: not blocked

    err = capsys.readouterr().err
    assert "worksheet has changed since the sample was drawn" in err
    assert verify_sample.DRAW_SHA in err
    assert "Scoring continues" in err
    report = (verify_sample.VALIDATION_DIR / "screening_verification.md").read_text(encoding="utf-8")
    assert "The worksheet has changed since the sample was drawn" in report
    assert "Same file as the draw | no" in report
    assert "**Verdict: ADOPT**" in report      # the verdict is still computed and reported


def test_an_unchanged_worksheet_neither_warns_nor_claims_a_mismatch(monkeypatch, sandbox, capsys):
    verify_sample.main(["--draw"])
    complete_sheet(verify_sample.sheet_path(), population())
    live = hashlib.sha256(sandbox.read_bytes()).hexdigest()
    monkeypatch.setattr(verify_sample, "DRAW_SHA", live)
    monkeypatch.setattr(verify_sample, "DRAW_SEED", seed_from(live))

    assert verify_sample.main(["--score"]) == 0
    assert "worksheet has changed" not in capsys.readouterr().err
    report = (verify_sample.VALIDATION_DIR / "screening_verification.md").read_text(encoding="utf-8")
    assert "Same file as the draw | yes" in report
    assert "The worksheet has changed" not in report


def test_scoring_calculations_are_unchanged_by_the_provenance_fix(sandbox, capsys):
    # The seed never fed the agreement computation; confirm the numbers still come from score()
    # alone, for both perfect and imperfect agreement.
    rows = population()
    perfect = score(sheet_from(rows, as_recorded(rows)), rows)
    assert perfect["agreed"] == perfect["n"] == 100
    assert perfect["rate"] == 1.0 and perfect["verdict"] == "ADOPT"

    two_off = score(sheet_from(rows, as_recorded(rows, flip=2)), rows)
    assert two_off["agreed"] == 98 and two_off["rate"] == 0.98
    assert two_off["verdict"] == "ADOPT" and two_off["sweeps"]

    # And the rendered report carries those same numbers whatever digest it is handed.
    for sha in ("x" * 64, verify_sample.DRAW_SHA):
        assert "98 / 100" in verify_sample.render(two_off, sha)


def test_drawing_derives_its_seed_from_the_live_sampling_frame(sandbox, capsys):
    """D020: a new draw seeds from the canonical frame digest, not from the file's bytes.

    Replaces the pre-D020 expectation that the seed came from the file bytes. The assertion is
    strengthened, not relaxed: it pins the new source *and* that the superseded one is not used.
    """
    rows = population()
    frame_seed = seed_from(verify_sample.frame_digest(rows))
    file_seed = seed_from(hashlib.sha256(sandbox.read_bytes()).hexdigest())
    assert frame_seed != file_seed, "the two rules must be distinguishable for this test to bite"

    assert verify_sample.main(["--draw"]) == 0
    out = capsys.readouterr().out
    assert f"with seed {frame_seed}" in out
    assert str(file_seed) not in out                    # the superseded rule is not used
    assert str(verify_sample.DRAW_SEED) not in out      # nor the recorded historical constant
    assert verify_sample.FRAME_DIGEST_RULE in out       # the rule in force is named
    assert verify_sample.frame_digest(rows) in out      # and its digest is reported

    drawn = [r["report_id"] for r in
             csv.DictReader(open(verify_sample.sheet_path(), encoding="utf-8", newline=""))]
    assert drawn == [r["report_id"] for r in draw(rows, 40, frame_seed)]
    assert drawn != [r["report_id"] for r in draw(rows, 40, file_seed)]
