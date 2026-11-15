"""Backfilling the decision-provenance columns must add information and change nothing else.

Rows are structural stubs with no bibliographic content (D007).
"""
import csv
import hashlib

import pytest

from scripts.common.config import PipelineError
from scripts.screening import backfill_provenance as bf
from scripts.screening import worksheet
from scripts.screening.vocabulary import ADJUDICATED, ADOPTED, EXCLUDE, INCLUDE, TA, UNRESOLVED

OLD_FIELDS = ["report_id", "record_id", "source_id", "pmid", "doi", "pub_year", "first_author",
              "journal", "publication_types", "title", "abstract",
              "decision", "reason_code", "reviewer", "screened_date", "notes"]


def old_row(n, decision="", reason=""):
    r = {f: "" for f in OLD_FIELDS}
    r.update({"report_id": f"R{n:04d}", "record_id": f"rec-{n:04d}", "pmid": str(9000000 + n),
              "title": f"Title {n}", "abstract": f"Abstract {n}", "decision": decision,
              "reason_code": reason, "reviewer": "SSK" if decision else "",
              "screened_date": "2026-11-01" if decision else ""})
    return r


def sug(n, suggestion, reason=""):
    return {"report_id": f"R{n:04d}", "suggestion": suggestion,
            "suggested_reason_code": reason}


# --- the basis is derived from evidence, never assumed ---------------------------------

@pytest.mark.parametrize("decision,suggestion,reason,sug_reason,expected", [
    (INCLUDE, INCLUDE, "", "", ADOPTED),
    (EXCLUDE, EXCLUDE, "wrong_outcome", "wrong_outcome", ADOPTED),
    (INCLUDE, EXCLUDE, "", "wrong_outcome", ADJUDICATED),
    (UNRESOLVED, INCLUDE, "", "", ADJUDICATED),
    (INCLUDE, "", "", "", ADJUDICATED),
    ("", INCLUDE, "", "", ""),
    ("", "", "", "", ""),
])
def test_the_basis_follows_from_whether_the_decision_matches_the_suggestion(
        decision, suggestion, reason, sug_reason, expected):
    assert bf.basis_for(decision, suggestion, reason, sug_reason) == expected


def test_a_differing_decision_is_never_called_an_adoption():
    """The whole point: disagreeing with the tool must not be recorded as adopting it."""
    assert bf.basis_for(INCLUDE, EXCLUDE, "", "wrong_outcome") == ADJUDICATED


def test_keeping_the_decision_but_changing_the_reason_is_an_adjudication():
    """Same verdict, different reason, is a judgement about why - not an adoption."""
    assert bf.basis_for(EXCLUDE, EXCLUDE, "wrong_design", "wrong_outcome") == ADJUDICATED
    assert bf.basis_for(EXCLUDE, EXCLUDE, "wrong_outcome", "wrong_outcome") == ADOPTED


# --- the plan ----------------------------------------------------------------------------

def test_every_decided_row_gets_a_basis_and_every_row_gets_its_suggestion():
    rows = [old_row(1, INCLUDE), old_row(2, EXCLUDE, "wrong_outcome"), old_row(3)]
    plan = bf.plan(rows, [sug(1, INCLUDE), sug(2, EXCLUDE, "wrong_outcome"), sug(3, INCLUDE)])
    out = {r["report_id"]: r for r in plan["rows"]}
    assert out["R0002"]["suggestion_reason_code"] == "wrong_outcome"
    assert out["R0001"]["decision_basis"] == ADOPTED
    assert out["R0002"]["decision_basis"] == ADOPTED
    assert out["R0003"]["decision_basis"] == "", "an undecided row has no basis"
    assert out["R0003"]["suggestion"] == INCLUDE, "but its suggestion is still recorded"
    assert plan["counts"][ADOPTED] == 2


def test_a_report_absent_from_the_suggestion_file_is_refused():
    with pytest.raises(PipelineError, match="no entry in the suggestion file"):
        bf.plan([old_row(1, INCLUDE), old_row(2, INCLUDE)], [sug(1, INCLUDE)])


def test_a_suggestion_that_is_not_a_decision_value_is_refused():
    with pytest.raises(PipelineError, match="not decisions"):
        bf.plan([old_row(1, INCLUDE)], [sug(1, "probably")])


def test_an_already_migrated_worksheet_is_recognised():
    rows = [old_row(1, INCLUDE)]
    rows[0].update(suggestion=INCLUDE, suggestion_reason_code="", decision_basis=ADOPTED)
    assert bf.plan(rows, [sug(1, INCLUDE)])["migrated"] is True


def test_an_unmigrated_worksheet_is_not_reported_as_migrated():
    assert bf.plan([old_row(1, INCLUDE)], [sug(1, INCLUDE)])["migrated"] is False


# --- nothing else may change --------------------------------------------------------------

def test_verify_accepts_a_plan_that_only_adds_the_two_columns():
    rows = [old_row(1, EXCLUDE, "wrong_outcome")]
    bf.verify(rows, bf.plan(rows, [sug(1, EXCLUDE, "wrong_outcome")])["rows"])


@pytest.mark.parametrize("col,value", [
    ("decision", INCLUDE), ("reason_code", "wrong_design"), ("reviewer", "someone"),
    ("screened_date", "2030-01-01"), ("notes", "tampered"), ("title", "different"),
    ("pmid", "999"),
])
def test_verify_refuses_any_other_change(col, value):
    before = [old_row(1, EXCLUDE, "wrong_outcome")]
    after = [dict(before[0], suggestion=EXCLUDE, suggestion_reason_code="wrong_outcome",
                  decision_basis=ADOPTED)]
    after[0][col] = value
    with pytest.raises(PipelineError, match="must not alter any recorded value"):
        bf.verify(before, after)


def test_verify_refuses_a_changed_row_count():
    before = [old_row(1, INCLUDE), old_row(2, INCLUDE)]
    with pytest.raises(PipelineError, match="row count changed"):
        bf.verify(before, before[:1])


def test_verify_refuses_reordering():
    before = [old_row(1, INCLUDE), old_row(2, INCLUDE)]
    with pytest.raises(PipelineError, match="row order changed"):
        bf.verify(before, list(reversed(before)))


# --- the CLI ------------------------------------------------------------------------------

@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    screening = tmp_path / "data" / "screening"
    screening.mkdir(parents=True)
    monkeypatch.setattr(worksheet, "SCREENING_DIR", screening)
    ws = worksheet.worksheet_path(TA)
    rows = [old_row(1, INCLUDE), old_row(2, EXCLUDE, "wrong_outcome"), old_row(3)]
    with open(ws, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=OLD_FIELDS)
        w.writeheader()
        w.writerows(rows)
    sug_path = tmp_path / "suggestions.csv"
    with open(sug_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["report_id", "suggestion", "suggested_reason_code"])
        w.writeheader()
        w.writerows([sug(1, INCLUDE), sug(2, EXCLUDE, "wrong_outcome"), sug(3, INCLUDE)])
    return ws, sug_path


def test_a_dry_run_writes_nothing(sandbox, capsys):
    ws, sug_path = sandbox
    before = hashlib.sha256(ws.read_bytes()).hexdigest()
    assert bf.main(["--suggestions", str(sug_path)]) == 0
    assert hashlib.sha256(ws.read_bytes()).hexdigest() == before
    assert "DRY RUN" in capsys.readouterr().out


def test_apply_adds_the_columns_and_preserves_every_decision(sandbox, capsys):
    ws, sug_path = sandbox
    before = {r["report_id"]: dict(r) for r in bf.read_csv(ws)}
    assert bf.main(["--suggestions", str(sug_path), "--apply"]) == 0
    after = {r["report_id"]: r for r in bf.read_csv(ws)}

    assert list(after["R0001"]) == worksheet.FIELDS[TA], "schema is the full title/abstract set"
    for rid, b in before.items():
        for col in bf.PRESERVE:
            assert after[rid][col] == b[col], f"{rid}.{col} changed"
    assert after["R0001"]["decision_basis"] == ADOPTED
    assert after["R0003"]["decision_basis"] == "" and after["R0003"]["suggestion"] == INCLUDE
    capsys.readouterr()


def test_running_twice_is_idempotent(sandbox, capsys):
    ws, sug_path = sandbox
    bf.main(["--suggestions", str(sug_path), "--apply"])
    once = hashlib.sha256(ws.read_bytes()).hexdigest()
    assert bf.main(["--suggestions", str(sug_path), "--apply"]) == 0
    assert hashlib.sha256(ws.read_bytes()).hexdigest() == once
    assert "already migrated" in capsys.readouterr().out


def test_a_missing_suggestion_entry_fails_without_writing(sandbox, capsys):
    ws, sug_path = sandbox
    rows = list(csv.DictReader(open(sug_path, encoding="utf-8", newline="")))[:1]
    with open(sug_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["report_id", "suggestion", "suggested_reason_code"])
        w.writeheader()
        w.writerows(rows)
    before = hashlib.sha256(ws.read_bytes()).hexdigest()
    assert bf.main(["--suggestions", str(sug_path), "--apply"]) == 1
    assert hashlib.sha256(ws.read_bytes()).hexdigest() == before
    assert "no entry in the suggestion file" in capsys.readouterr().err
