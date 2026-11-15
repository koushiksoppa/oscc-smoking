"""Stage 3 screening: vocabulary, worksheet generation, validation and PRISMA accounting.

Rows are structural stubs with no bibliographic content (D007). No test records a screening
decision that is presented as a reviewer's; decisions here are synthetic inputs used to prove the
validator's rules, and they never touch the project's own screening files.
"""
import csv

import pytest
import yaml

from scripts.common import config
from scripts.common.config import PipelineError
from scripts.screening import prisma, validate_screening, vocabulary, worksheet
from scripts.screening.vocabulary import EXCLUDE, FT, INCLUDE, TA, UNRESOLVED


# --- vocabulary ----------------------------------------------------------------------

def test_project_vocabulary_loads():
    vocab = vocabulary.load_vocabulary()
    assert {INCLUDE, EXCLUDE, UNRESOLVED} <= set(vocab.decisions)
    assert "unavailable" in vocab.retrieval_statuses
    assert len(vocab.reasons) >= 10


def test_vocabulary_matches_the_protocol_document():
    """The config and docs/protocol/eligibility_criteria.md must not drift apart."""
    doc = (config.ROOT / "docs" / "protocol" / "eligibility_criteria.md").read_text(encoding="utf-8")
    documented = set()
    for line in doc.splitlines():
        if line.startswith("| `") and "`" in line[3:]:
            documented.add(line.split("`")[1])
    coded = set(vocabulary.load_vocabulary().codes())

    # full_text_unavailable is documented as a retrieval status, not an exclusion reason.
    assert documented - {"full_text_unavailable"} == coded, (
        f"documented-only: {sorted(documented - {'full_text_unavailable'} - coded)}; "
        f"config-only: {sorted(coded - documented)}"
    )


def test_full_text_unavailable_is_a_retrieval_status_not_a_reason():
    vocab = vocabulary.load_vocabulary()
    assert "full_text_unavailable" not in vocab.codes()


def test_stage_restrictions_are_asymmetric():
    vocab = vocabulary.load_vocabulary()
    ta, ft = set(vocab.codes(TA)), set(vocab.codes(FT))
    assert ta < ft, "every title/abstract reason must also be valid at full text"
    assert {"no_reference_group", "no_usable_data", "outcome_not_separable",
            "duplicate_publication"} <= (ft - ta), \
        "reasons needing the methods section must not be available at title/abstract"


@pytest.mark.parametrize("bad", [
    {"reasons": [{"code": "a", "description": "d", "stages": []}]},
    {"reasons": [{"code": "a", "description": "d", "stages": ["nowhere"]}]},
    {"reasons": [{"code": "a", "description": "d", "stages": ["ta"]},
                 {"code": "a", "description": "d2", "stages": ["ft"]}]},
])
def test_malformed_vocabulary_is_rejected(tmp_path, monkeypatch, bad):
    path = tmp_path / "screening.yaml"
    path.write_text(yaml.safe_dump({
        "decisions": ["include", "exclude", "unresolved"],
        "retrieval_statuses": ["sought", "retrieved", "unavailable"], **bad}), encoding="utf-8")
    monkeypatch.setattr(vocabulary, "SCREENING_CONFIG", path)
    with pytest.raises(PipelineError):
        vocabulary.load_vocabulary()


def test_vocabulary_requires_the_three_decisions(tmp_path, monkeypatch):
    path = tmp_path / "screening.yaml"
    path.write_text(yaml.safe_dump({
        "decisions": ["include", "exclude"],          # 'unresolved' missing
        "retrieval_statuses": ["sought"],
        "reasons": [{"code": "a", "description": "d", "stages": ["ta"]}]}), encoding="utf-8")
    monkeypatch.setattr(vocabulary, "SCREENING_CONFIG", path)
    with pytest.raises(PipelineError, match="unresolved"):
        vocabulary.load_vocabulary()


# --- validation rules ----------------------------------------------------------------

def src_row(report_id, pmid="1", title="t"):
    return {"report_id": report_id, "pmid": pmid, "title": title}


def ws_row(report_id, pmid="1", title="t", decision="", reason="", reviewer="", notes="",
           status="", screened_date=None):
    """A worksheet row. A recorded decision carries a date, as the schema requires."""
    return {"report_id": report_id, "pmid": pmid, "title": title, "decision": decision,
            "reason_code": reason, "reviewer": reviewer, "notes": notes,
            "full_text_status": status,
            "screened_date": screened_date if screened_date is not None
            else ("2026-11-01" if decision else "")}


def check(rows, source=None, stage=TA):
    return validate_screening.check(rows, source or [src_row(r["report_id"]) for r in rows], stage)


def test_unscreened_worksheet_passes_with_a_progress_warning():
    f = check([ws_row("R0001"), ws_row("R0002")])
    assert f.errors == []
    assert any("not yet screened" in w for w in f.warnings)


def test_valid_decisions_are_accepted():
    f = check([
        ws_row("R0001", decision=INCLUDE, reviewer="SSK"),
        ws_row("R0002", decision=EXCLUDE, reason="review_or_meta", reviewer="SSK"),
        ws_row("R0003", decision=UNRESOLVED, reviewer="SSK"),
    ])
    assert f.errors == []


def test_unknown_decision_is_an_error():
    f = check([ws_row("R0001", decision="maybe", reviewer="SSK")])
    assert any("unknown decision" in e for e in f.errors)


def test_exclusion_without_a_reason_is_an_error():
    f = check([ws_row("R0001", decision=EXCLUDE, reviewer="SSK")])
    assert any("no reason_code" in e for e in f.errors)


def test_unknown_reason_code_is_an_error():
    f = check([ws_row("R0001", decision=EXCLUDE, reason="not_a_code", reviewer="SSK")])
    assert any("unknown reason_code" in e for e in f.errors)


def test_full_text_reason_is_refused_at_title_abstract():
    f = check([ws_row("R0001", decision=EXCLUDE, reason="no_reference_group", reviewer="SSK")], stage=TA)
    assert any("not permitted at title/abstract" in e for e in f.errors)


def test_same_reason_is_accepted_at_full_text():
    f = validate_screening.check(
        [ws_row("R0001", decision=EXCLUDE, reason="no_reference_group", reviewer="SSK",
                status="retrieved")],
        [src_row("R0001")], FT)
    assert f.errors == []


def test_reason_on_an_inclusion_is_an_error():
    f = check([ws_row("R0001", decision=INCLUDE, reason="wrong_design", reviewer="SSK")])
    assert any("belong only to exclusions" in e for e in f.errors)


def test_decision_without_a_reviewer_is_an_error():
    f = check([ws_row("R0001", decision=INCLUDE)])
    assert any("no reviewer" in e for e in f.errors)


def test_other_requires_a_written_justification():
    f = check([ws_row("R0001", decision=EXCLUDE, reason="other", reviewer="SSK")])
    assert any("requires a written justification" in e for e in f.errors)
    ok = check([ws_row("R0001", decision=EXCLUDE, reason="other", reviewer="SSK", notes="why")])
    assert ok.errors == []


def test_retrieval_status_cannot_be_used_as_an_exclusion_reason():
    f = validate_screening.check(
        [ws_row("R0001", decision=EXCLUDE, reason="full_text_unavailable", reviewer="SSK")],
        [src_row("R0001")], FT)
    assert any("not an exclusion reason" in e for e in f.errors)


def test_unavailable_full_text_cannot_carry_a_decision():
    f = validate_screening.check(
        [ws_row("R0001", decision=EXCLUDE, reason="wrong_design", reviewer="SSK",
                status="unavailable")],
        [src_row("R0001")], FT)
    assert any("no eligibility decision can be made" in e for e in f.errors)


def test_unknown_full_text_status_is_an_error():
    f = validate_screening.check([ws_row("R0001", status="maybe")], [src_row("R0001")], FT)
    assert any("unknown full_text_status" in e for e in f.errors)


def test_unresolved_records_are_warned_about():
    f = check([ws_row("R0001", decision=UNRESOLVED, reviewer="SSK")])
    assert any("unresolved" in w for w in f.warnings)


# --- identifier integrity ------------------------------------------------------------

def test_duplicate_report_id_is_an_error():
    f = check([ws_row("R0001"), ws_row("R0001")])
    assert any("duplicate report_id" in e for e in f.errors)


def test_deleted_rows_are_detected():
    f = validate_screening.check([ws_row("R0001")], [src_row("R0001"), src_row("R0002")], TA)
    assert any("missing from the worksheet" in e for e in f.errors)


def test_added_rows_are_detected():
    f = validate_screening.check([ws_row("R0001"), ws_row("R9999")], [src_row("R0001")], TA)
    assert any("not in the source set" in e for e in f.errors)


def test_edited_derived_column_is_detected():
    """Guards against spreadsheet re-import mangling identifiers or titles."""
    f = validate_screening.check([ws_row("R0001", pmid="999")], [src_row("R0001", pmid="1")], TA)
    assert any("derived column 'pmid' differs" in e for e in f.errors)


def test_empty_worksheet_is_handled():
    f = validate_screening.check([], [], TA)
    assert f.errors == []
    assert any("reports in worksheet: 0" in i for i in f.info)


# --- worksheet generation, end to end ------------------------------------------------

@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    """A processed-data tree with two unique reports, one of them a duplicate group."""
    processed = tmp_path / "data" / "processed"
    (processed / "citations").mkdir(parents=True)
    (processed / "dedup").mkdir(parents=True)
    monkeypatch.setattr(worksheet, "PROCESSED_DIR", processed)
    monkeypatch.setattr(worksheet, "SCREENING_DIR", tmp_path / "data" / "screening")
    monkeypatch.setattr(prisma, "PROCESSED_DIR", processed)
    monkeypatch.setattr(prisma, "VALIDATION_DIR", tmp_path / "results" / "validation")
    monkeypatch.setattr(validate_screening, "VALIDATION_DIR", tmp_path / "results" / "validation")
    # Provenance is verified by the dedup stage; bypassing it here would not be a screening test.
    monkeypatch.setattr(worksheet, "verify_provenance", lambda source_id: "0" * 64)

    def write(name, rows, fields=None):
        path = processed / name
        with open(path, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields or list(rows[0]))
            w.writeheader()
            w.writerows(rows)

    write("citations/src_citations.csv", [
        {"record_id": "src:1", "journal": "J1", "publication_types": "Journal Article",
         "abstract": "abstract one"},
        {"record_id": "src:2", "journal": "J2", "publication_types": "Review",
         "abstract": "abstract two"},
    ])
    write("dedup/report_index.csv", [
        {"record_id": "src:1", "source_id": "src", "report_id": "R0001", "is_primary": "yes",
         "pmid": "11", "doi": "10.1/a", "pub_year": "2001", "first_author": "A, B", "title": "t1"},
        {"record_id": "src:2", "source_id": "src", "report_id": "R0002", "is_primary": "yes",
         "pmid": "22", "doi": "", "pub_year": "2002", "first_author": "C, D", "title": "t2"},
    ])
    return tmp_path


def test_worksheet_is_generated_with_no_decisions(sandbox):
    result = worksheet.build(TA)
    rows = worksheet.read_csv(worksheet.worksheet_path(TA))

    assert result["rows"] == 2 and result["added"] == 2
    assert [r["report_id"] for r in rows] == ["R0001", "R0002"]
    for r in rows:
        assert r["decision"] == "" and r["reason_code"] == "" and r["reviewer"] == "", \
            "the generator must never record a decision (D010)"


def test_worksheet_preserves_citation_information(sandbox):
    worksheet.build(TA)
    rows = {r["report_id"]: r for r in worksheet.read_csv(worksheet.worksheet_path(TA))}
    assert rows["R0001"]["pmid"] == "11" and rows["R0001"]["title"] == "t1"
    assert rows["R0001"]["abstract"] == "abstract one"
    assert rows["R0002"]["publication_types"] == "Review"
    assert rows["R0002"]["doi"] == ""


def test_generation_refuses_to_overwrite_an_existing_worksheet(sandbox):
    worksheet.build(TA)
    with pytest.raises(PipelineError, match="not overwritten"):
        worksheet.build(TA)


def test_refresh_preserves_recorded_decisions(sandbox):
    worksheet.build(TA)
    path = worksheet.worksheet_path(TA)
    rows = worksheet.read_csv(path)
    rows[0].update(decision=EXCLUDE, reason_code="review_or_meta", reviewer="SSK",
                   screened_date="2026-11-01", notes="n")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    result = worksheet.build(TA, refresh=True)
    after = {r["report_id"]: r for r in worksheet.read_csv(path)}

    assert result["decisions_carried"] == 1
    assert after["R0001"]["decision"] == EXCLUDE
    assert after["R0001"]["reason_code"] == "review_or_meta"
    assert after["R0001"]["reviewer"] == "SSK" and after["R0001"]["notes"] == "n"
    assert after["R0002"]["decision"] == ""


def test_refresh_adds_new_reports_without_disturbing_old_ones(sandbox):
    worksheet.build(TA)
    index = worksheet.PROCESSED_DIR / "dedup" / "report_index.csv"
    rows = worksheet.read_csv(index)
    rows.append({**rows[0], "record_id": "src:3", "report_id": "R0003", "pmid": "33",
                 "title": "t3"})
    with open(index, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    result = worksheet.build(TA, refresh=True)
    assert result["rows"] == 3 and result["added"] == 1


def test_refresh_refuses_to_discard_a_decision_for_a_vanished_report(sandbox):
    worksheet.build(TA)
    path = worksheet.worksheet_path(TA)
    rows = worksheet.read_csv(path)
    rows[1].update(decision=INCLUDE, reviewer="SSK")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    index = worksheet.PROCESSED_DIR / "dedup" / "report_index.csv"
    kept = [r for r in worksheet.read_csv(index) if r["report_id"] != "R0002"]
    with open(index, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(kept[0]))
        w.writeheader()
        w.writerows(kept)

    with pytest.raises(PipelineError, match="would discard recorded work"):
        worksheet.build(TA, refresh=True)


def test_worksheet_generation_does_not_modify_source_data(sandbox):
    index = worksheet.PROCESSED_DIR / "dedup" / "report_index.csv"
    citations = worksheet.PROCESSED_DIR / "citations" / "src_citations.csv"
    before = (index.read_bytes(), citations.read_bytes())
    worksheet.build(TA)
    assert (index.read_bytes(), citations.read_bytes()) == before


def test_full_text_worksheet_contains_only_title_abstract_includes(sandbox):
    worksheet.build(TA)
    path = worksheet.worksheet_path(TA)
    rows = worksheet.read_csv(path)
    rows[0].update(decision=INCLUDE, reviewer="SSK")
    rows[1].update(decision=EXCLUDE, reason_code="review_or_meta", reviewer="SSK")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    worksheet.build(FT)
    ft = worksheet.read_csv(worksheet.worksheet_path(FT))
    assert [r["report_id"] for r in ft] == ["R0001"]
    assert ft[0]["full_text_status"] == "" and ft[0]["decision"] == ""


def test_full_text_worksheet_requires_the_title_abstract_stage_first(sandbox):
    with pytest.raises(PipelineError, match="no includes to carry forward"):
        worksheet.build(FT)


def test_missing_report_index_is_refused(sandbox):
    (worksheet.PROCESSED_DIR / "dedup" / "report_index.csv").unlink()
    with pytest.raises(PipelineError, match="Run scripts.dedup.deduplicate first"):
        worksheet.build(TA)


def test_missing_citations_file_is_refused(sandbox):
    (worksheet.PROCESSED_DIR / "citations" / "src_citations.csv").unlink()
    with pytest.raises(PipelineError, match="not found"):
        worksheet.build(TA)


# --- PRISMA accounting ---------------------------------------------------------------

def test_prisma_marks_unrun_stages_pending_not_zero(sandbox, monkeypatch):
    monkeypatch.setattr(prisma, "load_sources", lambda: [])
    monkeypatch.setattr(prisma.worksheet, "worksheet_path",
                        lambda stage: sandbox / "data" / "screening" / f"screening_{stage}.csv")
    flow = prisma.gather()

    assert flow["duplicates_removed"] == 0 and flow["unique_reports"] == 2
    assert flow["ta_screened"] == prisma.PENDING, "an unrun stage is pending, not zero"
    assert flow["included_studies"] == prisma.PENDING
    assert prisma.consistency(flow) == []


def test_prisma_counts_awaiting_screening_separately(sandbox, monkeypatch):
    monkeypatch.setattr(prisma, "load_sources", lambda: [])
    monkeypatch.setattr(prisma.worksheet, "worksheet_path",
                        lambda stage: sandbox / "data" / "screening" / f"screening_{stage}.csv")
    worksheet.build(TA)
    path = worksheet.worksheet_path(TA)
    rows = worksheet.read_csv(path)
    rows[0].update(decision=EXCLUDE, reason_code="review_or_meta", reviewer="SSK",
                   decision_basis=vocabulary.ADJUDICATED, screened_date="2026-11-01",
                   adjudicated_date="2026-11-10")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    flow = prisma.gather()
    assert flow["ta_total"] == 2 and flow["ta_screened"] == 1
    assert flow["ta_unscreened"] == 1 and flow["ta_excluded"] == 1 and flow["ta_included"] == 0
    assert prisma.consistency(flow) == []


def test_prisma_detects_an_unreconcilable_flow():
    flow = {"identified": 100, "duplicates_removed": 5, "unique_reports": 90,
            "ta_reasons": {}, "ft_reasons": {}, "ft_exists": False}
    assert any("does not equal unique reports" in p for p in prisma.consistency(flow))


def test_prisma_detects_reasons_not_matching_exclusions():
    flow = {"ft_excluded": 3, "ft_reasons": {"wrong_design": 1}, "ta_reasons": {},
            "ft_exists": True}
    assert any("every exclusion needs exactly one reason" in p for p in prisma.consistency(flow))


@pytest.mark.parametrize("total,screened,expect", [
    (None, None, "NOT STARTED"),
    (194, 0, "NOT SCREENED"),
    (194, 50, "IN PROGRESS"),
    (194, 194, "TITLE/ABSTRACT COMPLETE"),
])
def test_prisma_banner_cannot_be_mistaken_for_a_finding(total, screened, expect):
    banner = prisma.screening_banner({"ta_total": total, "ta_screened": screened})
    assert expect in banner
    if expect == "NOT SCREENED":
        assert "not** because nothing was eligible" in banner


def test_prisma_rejects_more_sought_than_included():
    flow = {"ta_included": 2, "ft_sought": 5, "ta_reasons": {}, "ft_reasons": {},
            "ft_exists": True}
    assert any("exceeds independently adjudicated" in p for p in prisma.consistency(flow))


# --- PRISMA: the full-text stage must not report "not done" as a zero -----------------

def _write(path, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def _ta_include_both(sandbox, monkeypatch):
    """Build a title/abstract sheet with both reports included, then the full-text sheet."""
    monkeypatch.setattr(prisma, "load_sources", lambda: [])
    worksheet.build(TA)
    path = worksheet.worksheet_path(TA)
    rows = worksheet.read_csv(path)
    for r in rows:
        r.update(decision=INCLUDE, reviewer="SSK",
                 decision_basis=vocabulary.ADJUDICATED,
                 screened_date="2026-11-01", adjudicated_date="2026-11-10")
    _write(path, rows)
    worksheet.build(FT)
    return worksheet.worksheet_path(FT)


def test_full_text_counts_are_pending_until_a_decision_is_recorded(sandbox, monkeypatch):
    """Creating the worksheet makes rows exist; it does not make them assessed."""
    _ta_include_both(sandbox, monkeypatch)
    flow = prisma.gather()

    assert flow["ft_sought"] == 2, "the worksheet is the set sought, so this is a real count"
    assert flow["ft_unscreened"] == 2 and flow["ft_screened"] == 0
    for key in ("ft_assessed", "ft_not_retrieved", "ft_included", "ft_excluded",
                "ft_unresolved"):
        assert flow[key] == prisma.PENDING, f"{key} must be pending, not zero"
    assert prisma.consistency(flow) == []


def test_full_text_retrieval_is_reported_separately_from_eligibility(sandbox, monkeypatch):
    """A retrieved report is not an assessed one; recording a status settles only retrieval."""
    path = _ta_include_both(sandbox, monkeypatch)
    rows = worksheet.read_csv(path)
    rows[0]["full_text_status"] = "retrieved"
    rows[1]["full_text_status"] = "unavailable"
    _write(path, rows)

    flow = prisma.gather()
    assert flow["ft_not_retrieved"] == 1 and flow["ft_assessed"] == 1
    assert flow["ft_included"] == prisma.PENDING, "no decision recorded yet"
    assert prisma.consistency(flow) == []


def test_partially_assessed_full_text_stage_reports_both_numbers(sandbox, monkeypatch):
    path = _ta_include_both(sandbox, monkeypatch)
    rows = worksheet.read_csv(path)
    rows[0].update(full_text_status="retrieved", decision=EXCLUDE,
                   reason_code="no_usable_data", reviewer="SSK")
    rows[1]["full_text_status"] = "retrieved"
    _write(path, rows)

    flow = prisma.gather()
    assert flow["ft_screened"] == 1 and flow["ft_unscreened"] == 1
    assert flow["ft_excluded"] == 1 and flow["ft_included"] == 0
    assert "IN PROGRESS" in prisma.full_text_banner(flow)


def test_full_text_reason_rows_stay_pending_until_a_decision_exists(sandbox, monkeypatch):
    _ta_include_both(sandbox, monkeypatch)
    flow = prisma.gather()
    body = prisma.render(flow, [])
    assert "| `no_usable_data` | <pending> |" in body
    assert "| `no_usable_data` | 0 |" not in body


def test_banner_warns_that_an_unassessed_full_text_stage_is_not_a_finding(sandbox, monkeypatch):
    _ta_include_both(sandbox, monkeypatch)
    banner = prisma.screening_banner(prisma.gather())
    assert "FULL TEXT: NOT ASSESSED" in banner
    assert "not** a finding that nothing was eligible" in banner


def test_banner_says_nothing_about_full_text_when_no_worksheet_exists():
    """Guards the contract the title/abstract banner tests rely on."""
    assert prisma.full_text_banner({"ta_total": 194, "ta_screened": 194}) == ""
    assert prisma.full_text_banner({"ft_sought": prisma.PENDING}) == ""
    assert "FULL TEXT" not in prisma.screening_banner({"ta_total": 194, "ta_screened": 194})


def test_a_fully_assessed_full_text_stage_reports_real_zeros(sandbox, monkeypatch):
    """Once every report is decided, a zero is a genuine zero and must show as one."""
    path = _ta_include_both(sandbox, monkeypatch)
    rows = worksheet.read_csv(path)
    for r in rows:
        r.update(full_text_status="retrieved", decision=INCLUDE, reviewer="SSK")
    _write(path, rows)

    flow = prisma.gather()
    assert flow["ft_included"] == 2 and flow["ft_excluded"] == 0
    assert "FULL TEXT: COMPLETE" in prisma.full_text_banner(flow)
    assert "| `no_usable_data` | 0 |" in prisma.render(flow, [])


# --- decision provenance: a suggestion must never pass as an adjudicated decision -------

def prov_row(report_id, suggestion="", decision="", basis="", reason="", reviewer="SSK",
             adjudicated_date=None):
    """A title/abstract row carrying the provenance columns, complete by default.

    An adjudication is a dated act, so one is supplied unless a test overrides it.
    """
    if adjudicated_date is None:
        adjudicated_date = "2026-11-10" if basis == vocabulary.ADJUDICATED else ""
    return {"report_id": report_id, "pmid": "1", "title": "t", "suggestion": suggestion,
            "decision": decision, "decision_basis": basis, "reason_code": reason,
            "reviewer": reviewer if decision else "", "notes": "",
            "screened_date": "2026-11-01" if decision else "",
            "adjudicated_date": adjudicated_date}


def test_the_vocabulary_defines_the_two_decision_bases():
    vocab = vocabulary.load_vocabulary()
    assert vocabulary.ADOPTED in vocab.basis_codes()
    assert vocabulary.ADJUDICATED in vocab.basis_codes()
    for b in vocab.decision_bases:
        assert b.description.strip(), f"{b.code} has no description"


def test_a_config_without_the_required_bases_is_refused(tmp_path, monkeypatch):
    cfg = yaml.safe_load(open(vocabulary.SCREENING_CONFIG, encoding="utf-8"))
    cfg["decision_bases"] = [{"code": "something_else", "description": "d"}]
    path = tmp_path / "screening.yaml"
    path.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    monkeypatch.setattr(vocabulary, "SCREENING_CONFIG", path)
    with pytest.raises(PipelineError, match="decision_bases must include"):
        vocabulary.load_vocabulary()


def test_duplicate_decision_bases_are_refused(tmp_path, monkeypatch):
    cfg = yaml.safe_load(open(vocabulary.SCREENING_CONFIG, encoding="utf-8"))
    cfg["decision_bases"] = cfg["decision_bases"] + [cfg["decision_bases"][0]]
    path = tmp_path / "screening.yaml"
    path.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    monkeypatch.setattr(vocabulary, "SCREENING_CONFIG", path)
    with pytest.raises(PipelineError, match="Duplicate decision_basis"):
        vocabulary.load_vocabulary()


def test_the_title_abstract_schema_carries_both_provenance_columns():
    fields = worksheet.FIELDS[TA]
    assert "suggestion" in fields and "decision_basis" in fields
    assert fields.index("suggestion") < fields.index("decision"), \
        "the suggestion is what was proposed before the decision; order should read that way"
    assert fields.index("decision") < fields.index("decision_basis")


def test_the_full_text_schema_carries_a_basis_but_no_suggestion_columns():
    """Full text has no suggestion mechanism, but every decision must still say how it was made.

    This replaces an earlier assertion that full text carried neither column. The basis was
    added there by decision; the suggestion columns deliberately were not.
    """
    fields = worksheet.FIELDS[FT]
    assert "decision_basis" in fields
    assert fields.index("decision") < fields.index("decision_basis")
    assert "suggestion" not in fields and "suggestion_reason_code" not in fields


def test_a_decision_without_a_basis_is_an_error():
    f = check([prov_row("R0001", suggestion=INCLUDE, decision=INCLUDE)])
    assert any("no decision_basis" in e for e in f.errors)


def test_an_unknown_basis_is_an_error():
    f = check([prov_row("R0001", suggestion=INCLUDE, decision=INCLUDE, basis="rubber_stamped")])
    assert any("unknown decision_basis" in e for e in f.errors)


def test_a_basis_without_a_decision_is_an_error():
    f = check([prov_row("R0001", basis=vocabulary.ADOPTED)])
    assert any("recorded with no decision" in e for e in f.errors)


def test_adopting_nothing_is_an_error():
    """`adopted_from_suggestion` with no suggestion claims an adoption that never happened."""
    f = check([prov_row("R0001", decision=INCLUDE, basis=vocabulary.ADOPTED)])
    assert any("nothing that was adopted" in e for e in f.errors)


def test_a_decision_that_differs_from_the_suggestion_is_not_an_adoption():
    f = check([prov_row("R0001", suggestion=EXCLUDE, decision=INCLUDE,
                        basis=vocabulary.ADOPTED)])
    assert any("is not an adoption" in e for e in f.errors)


def test_adopting_a_matching_suggestion_is_valid():
    f = check([prov_row("R0001", suggestion=INCLUDE, decision=INCLUDE,
                        basis=vocabulary.ADOPTED)])
    assert f.errors == []


def test_an_adjudicated_decision_may_differ_from_the_suggestion():
    """This is the whole point: a reviewer who overrules the tool must be able to record it."""
    f = check([prov_row("R0001", suggestion=EXCLUDE, decision=INCLUDE,
                        basis=vocabulary.ADJUDICATED)])
    assert f.errors == []


def test_an_unknown_suggestion_value_is_an_error():
    f = check([prov_row("R0001", suggestion="probably", decision=INCLUDE,
                        basis=vocabulary.ADJUDICATED)])
    assert any("unknown suggestion" in e for e in f.errors)


def test_the_report_counts_decisions_by_basis():
    f = check([prov_row("R0001", suggestion=INCLUDE, decision=INCLUDE, basis=vocabulary.ADOPTED),
               prov_row("R0002", suggestion=EXCLUDE, decision=INCLUDE,
                        basis=vocabulary.ADJUDICATED)])
    assert any(f"basis — {vocabulary.ADOPTED}: 1" in i for i in f.info)
    assert any(f"basis — {vocabulary.ADJUDICATED}: 1" in i for i in f.info)


# --- C1: warnings by default, hard gate at the final stage -------------------------------

def test_an_unfinished_stage_warns_by_default():
    f = check([ws_row("R0001")])
    assert f.errors == [] and any("not yet screened" in w for w in f.warnings)


def test_an_unfinished_stage_is_an_error_when_declared_final():
    rows = [ws_row("R0001")]
    f = validate_screening.check(rows, [src_row("R0001")], TA, final=True)
    assert any("not yet screened" in e and "cannot be declared final" in e for e in f.errors)
    assert f.warnings == []


def test_unresolved_records_block_a_final_stage():
    rows = [ws_row("R0001", decision=UNRESOLVED, reviewer="SSK")]
    f = validate_screening.check(rows, [src_row("R0001")], TA, final=True)
    assert any("unresolved" in e for e in f.errors)


def test_a_complete_stage_passes_the_final_gate():
    rows = [ws_row("R0001", decision=EXCLUDE, reason="review_or_meta", reviewer="SSK")]
    f = validate_screening.check(rows, [src_row("R0001")], TA, final=True)
    assert f.errors == [] and f.warnings == []


# --- D010 enforcement: an adopted suggestion does not satisfy a decision field -----------

def test_adoption_requires_the_reason_to_match_too():
    """Same verdict, different reason, is a judgement about why - it must not read as adoption."""
    row = prov_row("R0001", suggestion=EXCLUDE, decision=EXCLUDE,
                   basis=vocabulary.ADOPTED, reason="wrong_design")
    row["suggestion_reason_code"] = "wrong_outcome"
    f = check([row])
    assert any("changing the reason is an adjudication" in e for e in f.errors)


def test_adoption_with_a_matching_reason_is_valid():
    row = prov_row("R0001", suggestion=EXCLUDE, decision=EXCLUDE,
                   basis=vocabulary.ADOPTED, reason="wrong_outcome")
    row["suggestion_reason_code"] = "wrong_outcome"
    assert check([row]).errors == []


def test_adopted_decisions_warn_by_default():
    f = check([prov_row("R0001", suggestion=INCLUDE, decision=INCLUDE,
                        basis=vocabulary.ADOPTED)])
    assert f.errors == []
    assert any("cannot satisfy a decision field" in w for w in f.warnings)


def test_adopted_decisions_block_the_final_gate():
    """The substance of D010: a stage of adopted suggestions is not a screened stage."""
    rows = [prov_row("R0001", suggestion=INCLUDE, decision=INCLUDE, basis=vocabulary.ADOPTED)]
    f = validate_screening.check(rows, [src_row("R0001")], TA, final=True)
    assert any("cannot satisfy a decision field" in e and "cannot be declared final" in e
               for e in f.errors)


def test_an_independently_adjudicated_stage_passes_the_final_gate():
    rows = [prov_row("R0001", suggestion=EXCLUDE, decision=EXCLUDE,
                     basis=vocabulary.ADJUDICATED, reason="wrong_outcome")]
    f = validate_screening.check(rows, [src_row("R0001")], TA, final=True)
    assert f.errors == [] and f.warnings == []


def test_a_full_text_decision_also_needs_a_basis():
    row = {"report_id": "R0001", "pmid": "1", "title": "t", "decision": INCLUDE,
           "decision_basis": "", "reason_code": "", "reviewer": "SSK", "notes": "",
           "full_text_status": "retrieved"}
    f = check([row], stage=FT)
    assert any("no decision_basis" in e for e in f.errors)


# --- full-text carry-forward is gated on the basis of the includes ----------------------

def test_adopted_includes_are_identified():
    rows = [prov_row("R0001", suggestion=INCLUDE, decision=INCLUDE, basis=vocabulary.ADOPTED),
            prov_row("R0002", suggestion=INCLUDE, decision=INCLUDE, basis=vocabulary.ADJUDICATED),
            prov_row("R0003", suggestion=EXCLUDE, decision=EXCLUDE, basis=vocabulary.ADOPTED,
                     reason="wrong_outcome")]
    assert worksheet.adopted_includes(rows) == ["R0001"], "only includes, only adopted ones"


def test_building_full_text_from_adopted_includes_warns(sandbox, capsys):
    worksheet.build(TA)
    path = worksheet.worksheet_path(TA)
    rows = worksheet.read_csv(path)
    for r in rows:
        r.update(decision=INCLUDE, decision_basis=vocabulary.ADOPTED, suggestion=INCLUDE,
                 reviewer="SSK")
    _write(path, rows)
    worksheet.build(FT)
    assert "adopted from an automated suggestion" in capsys.readouterr().err


def test_building_full_text_from_adopted_includes_is_refused_under_the_final_gate(sandbox):
    worksheet.build(TA)
    path = worksheet.worksheet_path(TA)
    rows = worksheet.read_csv(path)
    for r in rows:
        r.update(decision=INCLUDE, decision_basis=vocabulary.ADOPTED, suggestion=INCLUDE,
                 reviewer="SSK")
    _write(path, rows)
    with pytest.raises(PipelineError, match="would be built on automated output"):
        worksheet.build(FT, strict=True)


def test_adjudicated_includes_carry_forward_without_complaint(sandbox, capsys):
    worksheet.build(TA)
    path = worksheet.worksheet_path(TA)
    rows = worksheet.read_csv(path)
    for r in rows:
        r.update(decision=INCLUDE, decision_basis=vocabulary.ADJUDICATED, reviewer="SSK")
    _write(path, rows)
    worksheet.build(FT, strict=True)
    assert "adopted" not in capsys.readouterr().err


# --- PRISMA distinguishes the two, and matches the real worksheet -----------------------

def test_prisma_counts_adopted_and_adjudicated_separately(sandbox, monkeypatch):
    monkeypatch.setattr(prisma, "load_sources", lambda: [])
    worksheet.build(TA)
    path = worksheet.worksheet_path(TA)
    rows = worksheet.read_csv(path)
    rows[0].update(decision=INCLUDE, decision_basis=vocabulary.ADOPTED, suggestion=INCLUDE,
                   reviewer="SSK", screened_date="2026-11-01")
    rows[1].update(decision=EXCLUDE, decision_basis=vocabulary.ADJUDICATED,
                   reason_code="wrong_outcome", reviewer="SSK",
                   screened_date="2026-11-01", adjudicated_date="2026-11-10")
    _write(path, rows)

    flow = prisma.gather()
    assert flow["ta_adopted"] == 1 and flow["ta_adjudicated"] == 1
    banner = prisma.screening_banner(flow)
    assert "NOT INDEPENDENTLY ADJUDICATED" in banner
    assert "proposed** screening outcome" in banner
    body = prisma.render(flow, [])
    assert "| … provisional, awaiting adjudication (not counted above) | 1 |" in body
    assert "| … independently adjudicated (counted above) | 1 |" in body


def test_banner_counts_recorded_classifications_not_formal_decisions():
    """The banner must not report the formal count as the number carrying a classification.

    Regression for audit finding A-2. The banner interpolated `ta_screened` — which counts
    independently adjudicated decisions only, and is 0 — into a sentence about reports that
    "carry a decision", while the next clause said 194 were adopted. Both cannot be true, and the
    contradiction reached the PRISMA figure embedded in the manuscript.
    """
    flow = {"ta_total": 194, "ta_screened": 0, "ta_adopted": 194, "ta_adjudicated": 0}
    banner = prisma.screening_banner(flow)

    assert "194 of 194 reports carry a **provisional classification**" in banner
    assert "0 of 194" not in banner
    # the three facts the figure has to keep apart
    assert "194 were **adopted from an automated suggestion**" in banner
    assert "0 were **independently adjudicated**" in banner
    # and it must be unreadable as completed human screening
    assert "**0 reports have been screened by a human reviewer**" in banner
    assert "proposed** screening outcome, not a completed one" in banner


def test_full_text_banner_reports_provisionally_sought_reports():
    """0 formally sought must not be stated without the 85 that are provisionally sought."""
    flow = {"ft_sought": 0, "ft_screened": 0, "ft_provisional_sought": 85}
    banner = prisma.full_text_banner(flow)

    assert "0 report(s) are formally sought" in banner
    assert "A further 85 report(s) are **provisionally** sought" in banner
    assert prisma.full_text_banner({"ft_sought": 0, "ft_screened": 0}).endswith("eligible.")


def test_prisma_marks_adopted_counts_pending_without_a_worksheet(sandbox, monkeypatch):
    monkeypatch.setattr(prisma, "load_sources", lambda: [])
    flow = prisma.gather()
    assert flow["ta_adopted"] == prisma.PENDING


def test_prisma_counts_match_the_projects_own_worksheet():
    """Every reported count must be traceable to the actual rows."""
    path = worksheet.worksheet_path(TA)
    if not path.exists():
        pytest.skip("no title/abstract worksheet in this checkout")
    rows = worksheet.read_csv(path)
    flow = prisma.gather()
    decided = [r for r in rows if (r.get("decision") or "").strip()]
    adj = [r for r in decided if r["decision_basis"] == vocabulary.ADJUDICATED]
    adopted = [r for r in decided if r["decision_basis"] == vocabulary.ADOPTED]

    assert flow["ta_total"] == len(rows)
    # Formal cells count independently adjudicated decisions and nothing else.
    assert flow["ta_screened"] == len(adj) == flow["ta_adjudicated"]
    assert flow["ta_included"] == sum(1 for r in adj if r["decision"] == INCLUDE)
    assert flow["ta_excluded"] == sum(1 for r in adj if r["decision"] == EXCLUDE)
    assert flow["ta_unresolved"] == sum(1 for r in adj if r["decision"] == UNRESOLVED)
    # Provisional outcomes are counted, but outside the flow.
    assert flow["ta_adopted"] == flow["prov_total"] == len(adopted)
    assert flow["prov_included"] == sum(1 for r in adopted if r["decision"] == INCLUDE)
    assert flow["prov_excluded"] == sum(1 for r in adopted if r["decision"] == EXCLUDE)
    assert flow["ta_excluded"] + flow["ta_included"] + flow["ta_unresolved"] == flow["ta_screened"]
    assert flow["ta_adjudicated"] + flow["ta_adopted"] + flow["ta_unscreened"] == flow["ta_total"]
    assert prisma.consistency(flow) == []


# --- the formal flow counts adjudicated outcomes; provisional ones sit outside it ---------

def ta_sheet(sandbox, spec):
    """Build a title/abstract worksheet from (decision, basis, reason) triples."""
    worksheet.build(TA)
    path = worksheet.worksheet_path(TA)
    rows = worksheet.read_csv(path)
    for row, (decision, basis, reason) in zip(rows, spec):
        row.update(decision=decision, decision_basis=basis, reason_code=reason,
                   suggestion=decision if basis == vocabulary.ADOPTED else "",
                   suggestion_reason_code=reason if basis == vocabulary.ADOPTED else "",
                   reviewer="SSK" if decision else "",
                   screened_date="2026-11-01" if decision else "",
                   adjudicated_date=("2026-11-10"
                                     if basis == vocabulary.ADJUDICATED else ""))
    _write(path, rows)
    return path


def test_a_wholly_provisional_stage_reports_zero_in_the_formal_flow(sandbox, monkeypatch):
    monkeypatch.setattr(prisma, "load_sources", lambda: [])
    ta_sheet(sandbox, [(EXCLUDE, vocabulary.ADOPTED, "wrong_outcome"),
                       (INCLUDE, vocabulary.ADOPTED, "")])
    flow = prisma.gather()
    assert flow["ta_screened"] == 0 and flow["ta_excluded"] == 0 and flow["ta_included"] == 0
    assert flow["prov_total"] == 2 and flow["prov_excluded"] == 1 and flow["prov_included"] == 1
    assert flow["ta_reasons"] == {}, "a provisional reason is not a formal exclusion reason"
    assert flow["prov_reasons"]["wrong_outcome"] == 1
    assert prisma.consistency(flow) == []


def test_partial_adjudication_moves_a_record_from_provisional_to_formal(sandbox, monkeypatch):
    monkeypatch.setattr(prisma, "load_sources", lambda: [])
    ta_sheet(sandbox, [(EXCLUDE, vocabulary.ADJUDICATED, "wrong_outcome"),
                       (INCLUDE, vocabulary.ADOPTED, "")])
    flow = prisma.gather()
    assert flow["ta_screened"] == 1 and flow["ta_excluded"] == 1 and flow["ta_included"] == 0
    assert flow["prov_total"] == 1 and flow["prov_included"] == 1
    assert flow["ta_reasons"]["wrong_outcome"] == 1
    assert prisma.consistency(flow) == []


def test_an_adjudicated_record_differing_from_its_suggestion_counts_formally(sandbox, monkeypatch):
    """The reviewer overrules the tool: the decision is formal, the suggestion stays on record."""
    monkeypatch.setattr(prisma, "load_sources", lambda: [])
    path = ta_sheet(sandbox, [(INCLUDE, vocabulary.ADJUDICATED, ""),
                              (EXCLUDE, vocabulary.ADOPTED, "wrong_outcome")])
    rows = worksheet.read_csv(path)
    rows[0]["suggestion"] = EXCLUDE          # the tool had proposed the opposite
    rows[0]["suggestion_reason_code"] = "wrong_design"
    _write(path, rows)

    flow = prisma.gather()
    assert flow["ta_included"] == 1, "an adjudicated include is a formal include"
    assert flow["prov_included"] == 0
    assert worksheet.read_csv(path)[0]["suggestion"] == EXCLUDE, "the suggestion is preserved"
    assert prisma.consistency(flow) == []


def test_a_retained_suggestion_stops_being_provisional_once_adjudicated(sandbox, monkeypatch):
    """Agreeing with the tool after judging it is adjudication, not adoption."""
    monkeypatch.setattr(prisma, "load_sources", lambda: [])
    path = ta_sheet(sandbox, [(EXCLUDE, vocabulary.ADOPTED, "wrong_outcome"),
                              (INCLUDE, vocabulary.ADOPTED, "")])
    assert prisma.gather()["prov_total"] == 2

    rows = worksheet.read_csv(path)
    rows[0].update(decision_basis=vocabulary.ADJUDICATED,    # same verdict, now judged
                   adjudicated_date="2026-11-10")
    _write(path, rows)

    flow = prisma.gather()
    assert flow["prov_total"] == 1 and flow["ta_screened"] == 1 and flow["ta_excluded"] == 1
    assert worksheet.read_csv(path)[0]["suggestion"] == EXCLUDE, "suggestion still on record"
    assert prisma.consistency(flow) == []


# --- the five identities ------------------------------------------------------------------

def test_the_four_way_split_must_account_for_every_report():
    """Adjudicated, provisional, invalid and unscreened must exhaust the worksheet."""
    flow = {"ta_adjudicated": 5, "ta_adopted": 3, "ta_invalid": 0, "ta_unscreened": 1,
            "ta_total": 10, "ta_reasons": {}, "ft_reasons": {}, "ft_exists": False}
    assert any("does not equal the worksheet" in p for p in prisma.consistency(flow))


def test_a_provisional_outcome_leaking_into_the_formal_flow_is_detected():
    flow = {"ta_screened": 194, "ta_adjudicated": 0, "ta_reasons": {}, "ft_reasons": {},
            "ft_exists": False}
    assert any("provisional outcome has leaked" in p for p in prisma.consistency(flow))


def test_provisional_decisions_must_sum_to_the_provisional_total():
    flow = {"prov_excluded": 2, "prov_included": 1, "prov_unresolved": 0, "ta_adopted": 5,
            "ta_reasons": {}, "ft_reasons": {}, "ft_exists": False}
    assert any("provisional decisions do not sum" in p for p in prisma.consistency(flow))


def test_formal_reports_sought_cannot_exceed_adjudicated_includes():
    flow = {"ta_included": 1, "ft_sought": 4, "ta_reasons": {}, "ft_reasons": {},
            "ft_exists": True}
    assert any("exceeds independently adjudicated" in p for p in prisma.consistency(flow))


def test_provisional_full_text_rows_cannot_exceed_provisional_includes():
    flow = {"ft_provisional_sought": 9, "prov_included": 2, "ta_reasons": {}, "ft_reasons": {},
            "ft_exists": True}
    assert any("provisional full-text rows" in p for p in prisma.consistency(flow))


# --- full-text provenance -------------------------------------------------------------------

def test_the_full_text_worksheet_records_the_basis_of_its_source_decision(sandbox, capsys):
    ta_sheet(sandbox, [(INCLUDE, vocabulary.ADOPTED, ""),
                       (INCLUDE, vocabulary.ADJUDICATED, "")])
    worksheet.build(FT)
    ft = worksheet.read_csv(worksheet.worksheet_path(FT))
    assert "source_ta_decision_basis" in ft[0]
    assert sorted(r["source_ta_decision_basis"] for r in ft) == sorted([
        vocabulary.ADOPTED, vocabulary.ADJUDICATED])
    capsys.readouterr()


def test_adjudicating_a_source_record_promotes_its_full_text_row(sandbox, capsys):
    """The provenance column is derived, so a refresh updates it without manual intervention."""
    path = ta_sheet(sandbox, [(INCLUDE, vocabulary.ADOPTED, ""),
                              (INCLUDE, vocabulary.ADOPTED, "")])
    worksheet.build(FT)
    ft = worksheet.read_csv(worksheet.worksheet_path(FT))
    assert all(r["source_ta_decision_basis"] == vocabulary.ADOPTED for r in ft)

    rows = worksheet.read_csv(path)
    rows[0].update(decision_basis=vocabulary.ADJUDICATED, adjudicated_date="2026-11-10")
    _write(path, rows)
    worksheet.build(FT, refresh=True)

    ft = {r["report_id"]: r for r in worksheet.read_csv(worksheet.worksheet_path(FT))}
    assert ft[rows[0]["report_id"]]["source_ta_decision_basis"] == vocabulary.ADJUDICATED
    assert ft[rows[1]["report_id"]]["source_ta_decision_basis"] == vocabulary.ADOPTED
    capsys.readouterr()


def test_full_text_rows_are_split_by_the_provenance_of_their_source(sandbox, monkeypatch, capsys):
    monkeypatch.setattr(prisma, "load_sources", lambda: [])
    ta_sheet(sandbox, [(INCLUDE, vocabulary.ADOPTED, ""),
                       (INCLUDE, vocabulary.ADJUDICATED, "")])
    worksheet.build(FT)
    flow = prisma.gather()
    assert flow["ft_sought"] == 1, "only the adjudicated source counts formally"
    assert flow["ft_provisional_sought"] == 1
    assert flow["ft_rows"] == 2
    assert prisma.consistency(flow) == []
    capsys.readouterr()


# --- adversarial: the one-field basis flip, and the rules that now stop it ---------------

def test_flipping_only_the_basis_on_an_adopted_row_is_rejected():
    """The defect this guards: a find-and-replace over one column would otherwise convert
    194 provisional records into formal ones, carrying the bulk-adoption reviewer and date."""
    row = prov_row("R0001", suggestion=INCLUDE, decision=INCLUDE,
                   basis=vocabulary.ADJUDICATED, adjudicated_date="")
    f = check([row])
    assert any("no adjudicated_date" in e for e in f.errors)


def test_an_adjudication_without_its_own_date_is_rejected():
    row = prov_row("R0001", suggestion=EXCLUDE, decision=EXCLUDE, reason="wrong_outcome",
                   basis=vocabulary.ADJUDICATED, adjudicated_date="")
    assert any("adjudication must record when it was made" in e for e in check([row]).errors)


def test_an_adjudicated_date_on_an_adopted_row_is_rejected():
    row = prov_row("R0001", suggestion=INCLUDE, decision=INCLUDE, basis=vocabulary.ADOPTED,
                   adjudicated_date="2026-11-10")
    assert any("only an independent adjudication has one" in e for e in check([row]).errors)


def test_an_adjudicated_date_without_a_decision_is_rejected():
    row = prov_row("R0001", adjudicated_date="2026-11-10")
    assert any("only an independent adjudication has one" in e for e in check([row]).errors)


def test_a_decision_without_a_screened_date_is_rejected():
    assert any("no screened_date" in e
               for e in check([ws_row("R0001", decision=INCLUDE, reviewer="SSK",
                                      screened_date="")]).errors)


def test_a_full_text_decision_without_a_screened_date_is_rejected():
    row = {"report_id": "R0001", "pmid": "1", "title": "t", "decision": INCLUDE,
           "decision_basis": vocabulary.ADJUDICATED, "reason_code": "", "reviewer": "SSK",
           "screened_date": "", "adjudicated_date": "2026-11-10", "notes": "",
           "full_text_status": "retrieved"}
    assert any("no screened_date" in e for e in check([row], stage=FT).errors)


def test_a_complete_adjudication_is_accepted():
    row = prov_row("R0001", suggestion=EXCLUDE, decision=EXCLUDE, reason="wrong_outcome",
                   basis=vocabulary.ADJUDICATED)
    assert check([row]).errors == []


def test_an_adjudication_differing_from_its_suggestion_keeps_the_suggestion():
    row = prov_row("R0001", suggestion=EXCLUDE, decision=INCLUDE,
                   basis=vocabulary.ADJUDICATED)
    row["suggestion_reason_code"] = "wrong_outcome"
    assert check([row]).errors == []
    assert row["suggestion"] == EXCLUDE and row["suggestion_reason_code"] == "wrong_outcome"


def test_an_invalid_adjudication_does_not_promote_full_text_provenance(sandbox, capsys):
    """An incomplete title/abstract row must not push its report into the formal flow."""
    path = ta_sheet(sandbox, [(INCLUDE, vocabulary.ADOPTED, ""),
                              (INCLUDE, vocabulary.ADOPTED, "")])
    rows = worksheet.read_csv(path)
    rows[0]["decision_basis"] = vocabulary.ADJUDICATED      # no adjudicated_date: invalid
    _write(path, rows)
    worksheet.build(FT, refresh=True)

    ft = {r["report_id"]: r for r in worksheet.read_csv(worksheet.worksheet_path(FT))}
    assert ft[rows[0]["report_id"]]["source_ta_decision_basis"] == "", \
        "an invalid row asserts no provenance"
    assert "do not pass row validation" in capsys.readouterr().err


def test_an_invalid_adjudication_enters_no_formal_count(sandbox, monkeypatch, capsys):
    monkeypatch.setattr(prisma, "load_sources", lambda: [])
    path = ta_sheet(sandbox, [(INCLUDE, vocabulary.ADOPTED, ""),
                              (INCLUDE, vocabulary.ADOPTED, "")])
    rows = worksheet.read_csv(path)
    rows[0]["decision_basis"] = vocabulary.ADJUDICATED
    _write(path, rows)
    worksheet.build(FT, refresh=True)

    flow = prisma.gather()
    assert flow["ft_sought"] == 0, "an invalid adjudication buys no formal retrieval"
    assert flow["ft_provisional_sought"] == 1
    capsys.readouterr()


def test_a_decided_row_with_an_empty_basis_is_caught_twice(sandbox, monkeypatch):
    """Rejected by the row validator, and counted as invalid rather than as a formal outcome."""
    monkeypatch.setattr(prisma, "load_sources", lambda: [])
    path = ta_sheet(sandbox, [(EXCLUDE, vocabulary.ADOPTED, "wrong_outcome"),
                              (INCLUDE, vocabulary.ADOPTED, "")])
    rows = worksheet.read_csv(path)
    rows[0]["decision_basis"] = ""
    _write(path, rows)

    src = [src_row(r["report_id"]) for r in rows]
    assert any("no decision_basis" in e
               for e in validate_screening.check(rows, src, TA).errors)
    flow = prisma.gather()
    assert flow["ta_invalid"] == 1, "counted, not silently dropped"
    assert flow["ta_adjudicated"] == 0 and flow["ta_adopted"] == 1
    assert prisma.consistency(flow) == [], "the four-way identity still balances"
