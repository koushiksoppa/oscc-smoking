"""Human review queues: what is derived, and what must never appear in them.

The queues exist to tell a reviewer what is outstanding. They must therefore contain no decision,
no suggestion, no reviewer and no date — a queue that carried an outcome would be a place where a
decision could be recorded without provenance, and the blinded queue in particular must not
disclose what was recorded, or the blinding it supports is destroyed.

Rows are structural stubs with no bibliographic content (D007).
"""
import csv

import pytest

from scripts.common.config import PipelineError
from scripts.screening import review_queue, worksheet
from scripts.screening.vocabulary import ADJUDICATED, ADOPTED, EXCLUDE, FT, INCLUDE, TA


def ta_row(n, **over):
    row = {c: "" for c in worksheet.FIELDS[TA]}
    row.update(report_id=f"R{n:04d}", record_id=f"rec-{n:04d}", pmid=f"{9000000 + n}",
               pub_year="2000", first_author=f"Author{n}", title=f"Title {n}")
    row.update(over)
    return row


def ft_row(n, **over):
    row = {c: "" for c in worksheet.FIELDS[FT]}
    row.update(report_id=f"R{n:04d}", pmid=f"{9000000 + n}", pub_year="2000",
               first_author=f"Author{n}", title=f"Title {n}")
    row.update(over)
    return row


def adopted(n):
    return ta_row(n, decision=EXCLUDE, reason_code="wrong_outcome", suggestion=EXCLUDE,
                  suggestion_reason_code="wrong_outcome", decision_basis=ADOPTED,
                  reviewer="R", screened_date="2026-11-01")


def judged(n):
    return ta_row(n, decision=EXCLUDE, reason_code="wrong_outcome", suggestion=EXCLUDE,
                  suggestion_reason_code="wrong_outcome", decision_basis=ADJUDICATED,
                  reviewer="R", screened_date="2026-11-01", adjudicated_date="2026-11-10")


# --- ta_adjudication ---------------------------------------------------------------------------

def test_an_adopted_decision_is_queued_for_adjudication():
    out = review_queue.ta_adjudication([adopted(1)])
    assert len(out) == 1
    assert out[0]["report_id"] == "R0001"
    assert out[0]["required_action"] == "adjudicate independently"


def test_an_independently_adjudicated_decision_is_not_queued():
    assert review_queue.ta_adjudication([judged(1)]) == []


def test_an_unscreened_report_is_queued():
    """No decision at all still needs a human; it must not fall through the gap."""
    out = review_queue.ta_adjudication([ta_row(1)])
    assert len(out) == 1 and out[0]["decision_basis"] == "(none)"


def test_a_basis_without_a_decision_is_queued():
    """A label with no verdict behind it is not an adjudication."""
    out = review_queue.ta_adjudication([ta_row(1, decision_basis=ADJUDICATED)])
    assert len(out) == 1


def test_the_adjudication_queue_shows_the_suggestion_beside_the_recorded_decision():
    """The reviewer may see what was proposed; the queue just must not decide for them."""
    out = review_queue.ta_adjudication([adopted(1)])[0]
    assert out["suggestion"] == EXCLUDE and out["recorded_decision"] == EXCLUDE
    assert out["suggestion_reason_code"] == "wrong_outcome"


def test_the_adjudication_queue_carries_no_reviewer_or_date_column():
    cols = review_queue.COLUMNS["ta_adjudication"]
    for forbidden in ("reviewer", "screened_date", "adjudicated_date"):
        assert forbidden not in cols, "an outcome must be recorded in the worksheet, not a queue"


# --- blinded_verification ----------------------------------------------------------------------

def test_only_unanswered_sample_rows_are_queued():
    rows = [{"report_id": "R0001", "your_decision": "", "title": "t"},
            {"report_id": "R0002", "your_decision": INCLUDE, "title": "t"}]
    out = review_queue.blinded_verification(rows)
    assert [r["report_id"] for r in out] == ["R0001"]


def test_a_whitespace_only_response_still_counts_as_unanswered():
    out = review_queue.blinded_verification([{"report_id": "R1", "your_decision": "   ",
                                              "title": "t"}])
    assert len(out) == 1


def test_the_blinded_queue_cannot_disclose_a_recorded_decision():
    """Its column list is the guarantee: there is nowhere for a decision to appear."""
    cols = review_queue.COLUMNS["blinded_verification"]
    for forbidden in ("decision", "recorded_decision", "suggestion", "reason_code",
                      "decision_basis", "your_decision"):
        assert forbidden not in cols
    # And nothing in a generated row holds one either, even if the input sheet did.
    out = review_queue.blinded_verification([
        {"report_id": "R1", "title": "t", "your_decision": "",
         "decision": INCLUDE, "suggestion": INCLUDE, "decision_basis": ADOPTED}])
    assert INCLUDE not in "".join(out[0].values())
    assert ADOPTED not in "".join(out[0].values())


# --- full text ---------------------------------------------------------------------------------

def test_a_report_with_no_retrieval_status_is_queued_for_retrieval():
    out = review_queue.ft_retrieval([ft_row(1)])
    assert len(out) == 1 and out[0]["full_text_status"] == "(none)"
    assert out[0]["required_action"] == "obtain full text"


def test_a_report_already_sought_is_not_queued_for_retrieval_again():
    assert review_queue.ft_retrieval([ft_row(1, full_text_status="sought")]) == []
    assert review_queue.ft_retrieval([ft_row(1, full_text_status="unavailable")]) == []


def test_only_retrieved_reports_are_queued_for_assessment():
    rows = [ft_row(1, full_text_status="retrieved"),
            ft_row(2, full_text_status="sought"),
            ft_row(3, full_text_status="unavailable")]
    out = review_queue.ft_assessment(rows)
    assert [r["report_id"] for r in out] == ["R0001"]


def test_an_assessed_report_leaves_the_assessment_queue():
    rows = [ft_row(1, full_text_status="retrieved", decision=EXCLUDE,
                   reason_code="no_usable_data", decision_basis=ADJUDICATED,
                   reviewer="R", screened_date="2026-11-11", adjudicated_date="2026-11-11")]
    assert review_queue.ft_assessment(rows) == []


def test_an_unavailable_full_text_never_enters_the_assessment_queue():
    """PRISMA reports it as not retrieved, which is not an eligibility decision."""
    assert review_queue.ft_assessment([ft_row(1, full_text_status="unavailable")]) == []


# --- build, write and summarise ----------------------------------------------------------------

@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    screening = tmp_path / "data" / "screening"
    screening.mkdir(parents=True)
    monkeypatch.setattr(worksheet, "SCREENING_DIR", screening)
    monkeypatch.setattr(review_queue, "QUEUE_DIR", tmp_path / "results" / "queues")

    def write(path, fields, rows):
        with open(path, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)

    write(worksheet.worksheet_path(TA), worksheet.FIELDS[TA], [adopted(1), judged(2)])
    write(worksheet.worksheet_path(FT), worksheet.FIELDS[FT],
          [ft_row(1), ft_row(2, full_text_status="retrieved")])
    write(screening / "verification_sample.csv",
          ["report_id", "pmid", "pub_year", "first_author", "title",
           "your_decision", "your_reason_code", "your_notes"],
          [{"report_id": "R0001", "pmid": "1", "pub_year": "2000", "first_author": "A",
            "title": "t", "your_decision": "", "your_reason_code": "", "your_notes": ""}])
    return tmp_path


def test_build_counts_each_queue_from_current_data(sandbox):
    q = review_queue.build()
    assert len(q["ta_adjudication"]) == 1, "only the adopted row, not the adjudicated one"
    assert len(q["blinded_verification"]) == 1
    assert len(q["ft_retrieval"]) == 1
    assert len(q["ft_assessment"]) == 1


def test_running_twice_produces_identical_queues(sandbox, capsys):
    assert review_queue.main([]) == 0
    first = {p.name: p.read_bytes() for p in review_queue.QUEUE_DIR.iterdir()}
    assert review_queue.main([]) == 0
    second = {p.name: p.read_bytes() for p in review_queue.QUEUE_DIR.iterdir()}
    assert first == second, "queues are regenerated, so they must be deterministic"
    capsys.readouterr()


def test_the_queues_never_write_to_a_worksheet(sandbox, capsys):
    import hashlib
    paths = [worksheet.worksheet_path(TA), worksheet.worksheet_path(FT),
             worksheet.SCREENING_DIR / "verification_sample.csv"]
    before = [hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]
    assert review_queue.main([]) == 0
    assert [hashlib.sha256(p.read_bytes()).hexdigest() for p in paths] == before
    capsys.readouterr()


def test_the_summary_names_every_queue_and_states_each_unit_separately(sandbox):
    """Replaces an assertion on an ambiguous single total.

    The old summary reported one number labelled "outstanding human actions", which conflated
    reports, task instances and response cells. The three are now reported separately and the
    text must say they are not added together.
    """
    q = review_queue.build()
    text = review_queue.render_summary(q, review_queue.verification_cells(
        [{"your_decision": "", "your_reason_code": "", "your_notes": ""}]))
    for name in q:
        assert f"`{name}.csv`" in text
    assert "Distinct reports across all queues" in text
    assert "Task instances" in text
    assert "Verification records" in text
    assert "Verification response cells" in text
    assert "**not** added together" in text
    assert "A response cell is not a task instance" in text
    assert "outstanding human actions" not in text, "the ambiguous total must be gone"
    assert "not** duplicate" in text, "the verification exercise must not be oversold"


def test_the_summary_reports_task_instances_and_distinct_reports_as_different_numbers():
    """The queues overlap, so the two totals genuinely differ and must not be conflated."""
    # One record in two queues: 2 task instances, 1 distinct report.
    q = {"ta_adjudication": [{"report_id": "R0001"}],
         "blinded_verification": [{"report_id": "R0001"}],
         "ft_retrieval": [], "ft_assessment": []}
    text = review_queue.render_summary(q, (0, 3))
    assert "| Task instances | **2** |" in text
    assert "| Distinct reports across all queues | **1** |" in text
    assert "1 + 1 + 0 + 0" in text, "the addends must be shown, in task-instance units"


def test_retrieval_tasks_are_never_described_as_response_cells():
    """85 retrieval tasks have no response cells; adding them to 120 would measure nothing."""
    q = {"ta_adjudication": [], "blinded_verification": [],
         "ft_retrieval": [{"report_id": f"R{i:04d}"} for i in range(85)], "ft_assessment": []}
    text = review_queue.render_summary(q, (0, 120))
    assert "have no response cells at all" in text
    assert "399" not in text, "task counts and cell counts must never be summed"


def test_verification_cells_are_counted_from_the_sheet_not_assumed():
    rows = [{"your_decision": "", "your_reason_code": "", "your_notes": ""} for _ in range(40)]
    assert review_queue.verification_cells(rows) == (0, 120)
    rows[0]["your_decision"] = "exclude"
    rows[1]["your_notes"] = "unclear abstract"
    assert review_queue.verification_cells(rows) == (2, 120)
    assert review_queue.verification_cells([]) == (0, 0)
    assert review_queue.verification_cells(
        [{"your_decision": "  ", "your_reason_code": "", "your_notes": ""}]) == (0, 3),         "whitespace is not an answer"


def test_a_missing_title_abstract_worksheet_is_refused_not_silently_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(worksheet, "SCREENING_DIR", tmp_path)
    with pytest.raises(PipelineError) as exc:
        review_queue.build()
    assert "no screening work to queue" in str(exc.value)


def test_absent_full_text_and_sample_files_give_empty_queues_not_errors(tmp_path, monkeypatch):
    """Those stages legitimately may not exist yet."""
    monkeypatch.setattr(worksheet, "SCREENING_DIR", tmp_path)
    with open(worksheet.worksheet_path(TA), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=worksheet.FIELDS[TA])
        w.writeheader()
        w.writerow(adopted(1))
    q = review_queue.build()
    assert len(q["ta_adjudication"]) == 1
    assert q["ft_retrieval"] == [] and q["ft_assessment"] == [] and q["blinded_verification"] == []


# --- the project's own queues: the published accounting must match the data --------------------

def project_queue(name):
    from scripts.common.config import ROOT
    path = ROOT / "results" / "queues" / f"{name}.csv"
    if not path.exists():
        pytest.skip("queues not generated in this checkout")
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def test_the_published_queue_counts_match_the_committed_data():
    from scripts.common.config import ROOT
    ta = project_queue("ta_adjudication")
    bv = project_queue("blinded_verification")
    fr = project_queue("ft_retrieval")
    fa = project_queue("ft_assessment")
    assert (len(ta), len(bv), len(fr), len(fa)) == (194, 40, 85, 0)
    assert len(ta) + len(bv) + len(fr) + len(fa) == 319, "task instances"

    union = {r["report_id"] for q in (ta, bv, fr, fa) for r in q}
    assert len(union) == 194, "distinct reports; the queues overlap"

    readme = (ROOT / "results" / "queues" / "README.md").read_text(encoding="utf-8")
    assert "| Distinct reports across all queues | **194** |" in readme
    assert "| Task instances | **319** |" in readme
    assert "| Verification records | **40** |" in readme
    assert "| Verification response cells | **120** |" in readme
    assert "399" not in readme


def test_the_published_overlap_claims_are_true_of_the_identifiers():
    from scripts.common.config import ROOT
    from scripts.screening.vocabulary import INCLUDE
    with open(ROOT / "data" / "screening" / "screening_ta.csv", encoding="utf-8",
              newline="") as fh:
        ta_rows = list(csv.DictReader(fh))
    ta_pop = {r["report_id"] for r in ta_rows}
    ta_inc = {r["report_id"] for r in ta_rows if (r["decision"] or "").strip() == INCLUDE}
    bv = {r["report_id"] for r in project_queue("blinded_verification")}
    fr = {r["report_id"] for r in project_queue("ft_retrieval")}

    assert bv <= ta_pop, "verification records are contained in the TA population"
    assert fr <= ta_inc, "retrieval records are contained in the TA include population"
    assert bv & fr, "some records occur in both queues, which is why the totals differ"
    assert (bv | fr) <= ta_pop


# --- the M-2 design document must list every deferred matter ----------------------------------
#
# A commit message once claimed four deferred questions while the document listed two. These
# assertions make the document the authority.

def architecture_doc():
    from scripts.common.config import ROOT
    path = ROOT / "docs" / "methods" / "verification_sample_architecture.md"
    if not path.exists():
        pytest.skip("architecture document not in this checkout")
    return path.read_text(encoding="utf-8")


def test_the_architecture_document_defers_exactly_four_matters():
    doc = architecture_doc()
    deferred = doc.split("## 7. Deferred")[1].split("## 8.")[0]
    assert deferred.count("UNRESOLVED / DEFERRED") == 4
    for heading in ("second EXTEND", "Extension sampling frame", "pooled",
                    "Maximum permitted number of extension samples"):
        assert heading in deferred, f"{heading!r} must be listed as deferred"
    assert "**Four** matters are deferred" in deferred


def test_each_deferred_matter_states_why_it_matters_and_what_must_be_decided():
    deferred = architecture_doc().split("## 7. Deferred")[1].split("## 8.")[0]
    for n in ("7.1", "7.2", "7.3", "7.4"):
        section = deferred.split(f"### {n}")[1].split("### ")[0]
        assert "UNRESOLVED / DEFERRED" in section
        assert "Why it matters" in section
        assert "What must be decided" in section


def test_no_decision_id_is_assigned_to_a_deferred_matter():
    deferred = architecture_doc().split("## 7. Deferred")[1].split("## 8.")[0]
    import re
    assert not re.search(r"\bD0\d\d\b", deferred), "a deferred matter must not carry a decision ID"
    assert "none is assigned a decision ID" in deferred


def test_the_deferrals_do_not_block_scoring_the_original_sample():
    doc = architecture_doc()
    section = doc.split("### What the deferrals do")[1].split("## 8.")[0]
    flat = " ".join(section.split())          # the document is wrapped; the claim is not
    assert "is not blocked by any of the above" in flat
    assert "120 response cells are complete" in flat
    assert "90–94.9% band" in flat, "the one band where an extension question blocks"
    assert "ADOPT or RE-SCREEN verdict requires none of them" in flat
