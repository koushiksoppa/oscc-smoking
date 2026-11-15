"""Draw provenance: historical immutability and the canonical sampling-frame digest (D020).

Two rules coexist and must stay distinguishable:

* `file_bytes_crlf_v1` — the historical rule, which produced the committed 40-record sample. It
  hashes the worksheet's bytes, so it is platform-dependent. It is preserved, never re-derived.
* `ordered_report_ids_v1` — the canonical rule (D020), which governs later draws. It hashes the
  sampling frame the draw procedure actually consumes, so it is platform-independent.

Fixture rows are structural stubs with no bibliographic content (D007). Where these tests read
the project's own files they read them only; nothing here writes to a worksheet or to the sample.
"""
import csv
import hashlib
import io
import subprocess
import unicodedata
import unittest.mock

import pytest

from scripts.common.config import ROOT, PipelineError
from scripts.screening import verify_sample
from scripts.screening.verify_sample import canonical_frame, draw, frame_digest, seed_from

# The provenance of the one sample that exists. Written out here so that a change to the module
# constants fails loudly rather than being silently ratified by a test that imports them.
HISTORICAL_SHA = "5938922a529a7f7318824f4216b4b9ab05b920a14def7c15e72c15ea2a6076eb"
HISTORICAL_SEED = 1496879658
HISTORICAL_SHEET_SHA = "6b4f734375f94a513404a8275f0003c9ddbdffae92b82ede264f2450bc57e29a"
HISTORICAL_FRAME_DIGEST = "37cc07e64054ef938229fbecec5f7da70f4c9ae419aae9f79b04d642574209ad"

WORKSHEET = ROOT / "data" / "screening" / "screening_ta.csv"
SAMPLE = ROOT / "data" / "screening" / "verification_sample.csv"


# The development commit that holds the pre-migration worksheet and the sample as first drawn.
HISTORICAL_COMMIT = "c704582"


def historical_commit_available() -> bool:
    """Is the development commit present in this repository?

    The standalone submission snapshot is published without the development repository's commit
    history, so the tests that read the pre-migration worksheet from `HISTORICAL_COMMIT` have no
    input here. They are skipped rather than failed: the precondition is absent, and the
    assertions themselves are unchanged and still enforced wherever the history is present.
    """
    return subprocess.run(["git", "cat-file", "-e", f"{HISTORICAL_COMMIT}^{{commit}}"],
                          capture_output=True, cwd=ROOT).returncode == 0


requires_development_history = pytest.mark.skipif(
    not historical_commit_available(),
    reason=("Requires historical development commit c704582, which is not included in the "
            "standalone submission snapshot."))


def git_show(path):
    return subprocess.run(["git", "show", f"{HISTORICAL_COMMIT}:{path}"],
                          capture_output=True, cwd=ROOT).stdout


def committed_worksheet():
    """The worksheet exactly as committed at c704582, before the provenance migration."""
    blob = git_show("data/screening/screening_ta.csv")
    return blob, list(csv.DictReader(io.StringIO(blob.decode("utf-8"))))


def current_worksheet():
    return list(csv.DictReader(open(WORKSHEET, encoding="utf-8", newline="")))


def sample_ids():
    return [r["report_id"] for r in csv.DictReader(open(SAMPLE, encoding="utf-8", newline=""))]


def stub_frame(n=10):
    """A structural sampling frame: identifiers and nothing that identifies a real report."""
    return [{"report_id": f"R{i:04d}", "title": f"Title {i}"} for i in range(1, n + 1)]


# --- historical preservation -------------------------------------------------------------------

def test_historical_draw_sha_is_exactly_unchanged():
    assert verify_sample.DRAW_SHA == HISTORICAL_SHA
    assert len(verify_sample.DRAW_SHA) == 64, "a SHA-256 is 64 hex characters"
    int(verify_sample.DRAW_SHA, 16)


def test_historical_draw_seed_is_exactly_unchanged():
    assert verify_sample.DRAW_SEED == HISTORICAL_SEED
    assert seed_from(verify_sample.DRAW_SHA) == verify_sample.DRAW_SEED
    assert verify_sample.DRAW_SEED_DERIVATION == "file_bytes_crlf_v1"


@requires_development_history
def test_the_historical_sha_is_the_digest_of_the_committed_worksheet_in_crlf_form():
    blob, _ = committed_worksheet()
    assert hashlib.sha256(blob.replace(b"\n", b"\r\n")).hexdigest() == HISTORICAL_SHA
    # The LF blob hashes differently. That asymmetry is the defect D020 exists to remove.
    assert hashlib.sha256(blob).hexdigest() != HISTORICAL_SHA


@requires_development_history
def test_the_historical_forty_report_ids_and_their_order_are_unchanged():
    committed = git_show("data/screening/verification_sample.csv").decode("utf-8")
    ids = sample_ids()
    assert ids == [r["report_id"] for r in csv.DictReader(io.StringIO(committed))]
    assert len(ids) == 40 and len(set(ids)) == 40


def test_the_historical_sample_file_is_byte_for_byte_unchanged():
    assert hashlib.sha256(SAMPLE.read_bytes()).hexdigest() == HISTORICAL_SHEET_SHA
    rc = subprocess.run(["git", "diff", "--quiet", "HEAD", "--",
                         "data/screening/verification_sample.csv"], cwd=ROOT).returncode
    assert rc == 0, "the committed sample must not differ from HEAD"


@requires_development_history
def test_historical_reconstruction_still_reproduces_the_original_sample():
    _, old = committed_worksheet()
    ids = sample_ids()
    assert [r["report_id"] for r in draw(old, 40, verify_sample.DRAW_SEED)] == ids
    # And from the migrated worksheet, because the frame itself did not change.
    assert [r["report_id"] for r in draw(current_worksheet(), 40, verify_sample.DRAW_SEED)] == ids


def test_the_two_rules_can_never_stand_in_for_one_another():
    assert seed_from(frame_digest(current_worksheet())) != verify_sample.DRAW_SEED
    assert verify_sample.DRAW_FRAME_DIGEST != verify_sample.DRAW_SHA
    assert verify_sample.FRAME_DIGEST_RULE != verify_sample.DRAW_SEED_DERIVATION


@requires_development_history
def test_the_recorded_frame_digest_is_the_digest_of_the_frame_the_sample_came_from():
    _, old = committed_worksheet()
    assert frame_digest(old) == verify_sample.DRAW_FRAME_DIGEST == HISTORICAL_FRAME_DIGEST


# --- canonical digest: required invariances ----------------------------------------------------

@requires_development_history
def test_crlf_and_lf_presentations_give_identical_canonical_digests():
    blob, lf_rows = committed_worksheet()
    crlf_rows = list(csv.DictReader(io.StringIO(blob.decode("utf-8").replace("\n", "\r\n"))))
    assert len(crlf_rows) == len(lf_rows) == 194
    assert frame_digest(crlf_rows) == frame_digest(lf_rows)


@requires_development_history
def test_pre_and_post_migration_worksheets_give_identical_canonical_digests():
    """Four columns were added; the sampling frame was not touched."""
    _, old = committed_worksheet()
    cur = current_worksheet()
    assert len(list(old[0])) == 16 and len(list(cur[0])) == 20, "the schemas must differ"
    assert [r["report_id"] for r in old] == [r["report_id"] for r in cur]
    assert frame_digest(old) == frame_digest(cur)


def test_irrelevant_later_columns_do_not_change_the_canonical_digest():
    base = stub_frame()
    widened = [dict(r, risk_of_bias="high", extracted_on="2027-01-01") for r in base]
    assert frame_digest(widened) == frame_digest(base)


def test_rewriting_a_non_identifying_field_does_not_change_the_digest():
    """A corrected title changes no sampling unit and no position, so the frame is the same."""
    base = stub_frame()
    corrected = [dict(r, title=r["title"] + " (corrected)") for r in base]
    assert frame_digest(corrected) == frame_digest(base)


# --- canonical digest: required sensitivities ---------------------------------------------------

def test_reordering_sampling_frame_rows_changes_the_digest():
    base = stub_frame()
    assert frame_digest([base[1], base[0]] + base[2:]) != frame_digest(base)
    assert frame_digest(list(reversed(base))) != frame_digest(base)


def test_adding_or_removing_a_sampling_frame_row_changes_the_digest():
    base = stub_frame()
    assert frame_digest(base[:-1]) != frame_digest(base)
    assert frame_digest(base + [{"report_id": "R0099"}]) != frame_digest(base)


def test_changing_a_sampling_unit_identifier_changes_the_digest():
    base = stub_frame()
    mutated = [dict(r) for r in base]
    mutated[3]["report_id"] = "R9999"
    assert frame_digest(mutated) != frame_digest(base)


# --- canonical digest: serialisation specification ----------------------------------------------

def test_the_serialisation_is_deterministic_and_explicitly_versioned():
    base = stub_frame()
    assert canonical_frame(base) == canonical_frame(base)
    assert frame_digest(base) == frame_digest(base)

    payload = canonical_frame(base)
    assert payload.startswith(verify_sample.FRAME_DIGEST_RULE.encode("utf-8") + b"\n")
    assert payload.endswith(b"\n")
    assert b"\r" not in payload, "LF only, whatever the file on disk uses"
    assert payload.decode("utf-8").splitlines()[1:] == [r["report_id"] for r in base]
    assert len(frame_digest(base)) == 64
    assert frame_digest(base) == frame_digest(base).lower()


def test_a_different_rule_version_gives_a_different_digest_for_the_same_frame():
    """The version is inside the hashed payload, so two rules cannot collide on one frame."""
    base = stub_frame()
    before = frame_digest(base)
    with unittest.mock.patch.object(verify_sample, "FRAME_DIGEST_RULE", "ordered_report_ids_v2"):
        assert canonical_frame(base).startswith(b"ordered_report_ids_v2\n")
        assert frame_digest(base) != before


def test_the_canonical_digest_is_nfc_normalised():
    decomposed = [{"report_id": "R0001" + unicodedata.normalize("NFD", "é")}]
    composed = [{"report_id": "R0001" + unicodedata.normalize("NFC", "é")}]
    assert decomposed[0]["report_id"] != composed[0]["report_id"], "inputs must differ as bytes"
    assert frame_digest(decomposed) == frame_digest(composed)


def test_a_frame_row_with_no_identifier_is_refused_rather_than_hashed_as_empty():
    for bad in ("", "   ", None):
        with pytest.raises(PipelineError) as exc:
            frame_digest([{"report_id": "R0001"}, {"report_id": bad}])
        assert "report_id" in str(exc.value)


# --- the report keeps the two provenances apart and claims no draw date -------------------------

def test_the_scoring_report_labels_both_rules_and_never_claims_a_draw_date():
    rows = stub_frame(100)
    for r in rows:
        r.update(decision="exclude", reason_code="wrong_outcome")
    sample = draw(rows, 40, HISTORICAL_SEED)
    sheet = [{"report_id": r["report_id"], "your_decision": "exclude",
              "your_reason_code": "wrong_outcome", "your_notes": ""} for r in sample]
    result = verify_sample.score(sheet, rows)
    report = verify_sample.render(result, "x" * 64, current_frame=frame_digest(rows))

    pre = report.split("## Pre-specified before the sample was drawn")[1].split("\n## ")[0]
    assert verify_sample.DRAW_SEED_DERIVATION in pre
    assert verify_sample.FRAME_DIGEST_RULE in pre
    assert verify_sample.DRAW_SHA in pre and verify_sample.DRAW_FRAME_DIGEST in pre
    assert "UNVERIFIED" in pre, "the draw date must not be asserted"
    assert "commit date is not evidence" in pre

    run = report.split("## This scoring run")[1].split("\n## ")[0]
    assert frame_digest(rows) in run
    assert verify_sample.DRAW_FRAME_DIGEST not in run, "draw provenance must not leak into this block"
