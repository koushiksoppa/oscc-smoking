"""Generate the human review queues from the worksheets as they stand.

    python -m scripts.screening.review_queue

Writes to `results/queues/`. Everything here is **derived** from the worksheets and the blinded
sample; nothing is a decision, a suggestion or a judgement. Each queue answers one question: which
records still need a human, and what exactly is the human being asked to do?

Four queues, because four different kinds of work are outstanding and conflating them is how a
provisional outcome gets mistaken for a finished one:

* **ta_adjudication** — reports carrying a decision adopted from an automated suggestion. Under
  D010 a suggestion cannot satisfy a decision field, so each of these needs the reviewer's own
  judgement before it counts. The recorded decision and its suggestion are shown side by side so
  the reviewer can see what was proposed, but the adjudication is theirs.
* **blinded_verification** — the drawn sample's unanswered rows. Deliberately carries no recorded
  decision: the sheet is blinded and this queue must not unblind it.
* **ft_retrieval** — reports taken forward whose full text has not been sought or recorded.
* **ft_assessment** — reports whose full text is retrieved but which carry no eligibility decision.

The queues are regenerated from current data on every run, so they are never stale and are never
hand-edited. They record no reviewer, no date and no decision: those belong in the worksheets.
"""
from __future__ import annotations

import argparse
import csv
import sys

from scripts.common.config import PipelineError, ROOT
from scripts.screening import vocabulary, worksheet
from scripts.screening.vocabulary import ADJUDICATED, ADOPTED, FT, INCLUDE, TA

QUEUE_DIR = ROOT / "results" / "queues"

# What the reviewer is being asked to supply, per queue. Written into each file so the queue is
# self-describing and a reviewer need not consult the methods guide to use it.
ACTIONS = {
    "ta_adjudication": (
        "Read the title and abstract. Record your own decision, independent of the suggestion "
        "shown. Then fill decision, decision_basis=independently_adjudicated, reason_code (if "
        "excluding), reviewer, screened_date and adjudicated_date in "
        "data/screening/screening_ta.csv."),
    "blinded_verification": (
        "Read the title and abstract. Record your judgement in your_decision, your_reason_code "
        "and your_notes in data/screening/verification_sample.csv. Do NOT look up the recorded "
        "decision first: the sheet is blinded on purpose, and consulting it destroys the check."),
    "ft_retrieval": (
        "Obtain the full text. Record full_text_status (sought / retrieved / unavailable) and "
        "full_text_source in data/screening/screening_ft.csv. 'unavailable' is reported by PRISMA "
        "as not retrieved, which is not an exclusion."),
    "ft_assessment": (
        "Assess the retrieved full text against the eligibility criteria. Record decision, "
        "decision_basis, reason_code (if excluding), reviewer, screened_date and "
        "adjudicated_date in data/screening/screening_ft.csv."),
}

COLUMNS = {
    "ta_adjudication": ["report_id", "pmid", "pub_year", "first_author", "title",
                        "recorded_decision", "recorded_reason_code", "suggestion",
                        "suggestion_reason_code", "decision_basis", "required_action"],
    "blinded_verification": ["report_id", "pmid", "pub_year", "first_author", "title",
                             "required_action"],
    "ft_retrieval": ["report_id", "pmid", "doi", "pub_year", "first_author", "title",
                     "source_ta_decision_basis", "full_text_status", "required_action"],
    "ft_assessment": ["report_id", "pmid", "doi", "pub_year", "first_author", "title",
                      "full_text_status", "full_text_source", "required_action"],
}


def read(path) -> list[dict[str, str]]:
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def ta_adjudication(ta_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Reports whose recorded decision rests on an adopted suggestion, or on nothing."""
    out = []
    for r in ta_rows:
        basis = (r.get("decision_basis") or "").strip()
        decision = (r.get("decision") or "").strip()
        if basis == ADJUDICATED and decision:
            continue                      # already the reviewer's own judgement
        out.append({
            "report_id": r["report_id"], "pmid": r.get("pmid", ""),
            "pub_year": r.get("pub_year", ""), "first_author": r.get("first_author", ""),
            "title": r.get("title", ""),
            "recorded_decision": decision, "recorded_reason_code": r.get("reason_code", ""),
            "suggestion": r.get("suggestion", ""),
            "suggestion_reason_code": r.get("suggestion_reason_code", ""),
            "decision_basis": basis or "(none)",
            "required_action": "adjudicate independently",
        })
    return out


def blinded_verification(sample_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Unanswered rows of the drawn sample. Carries no recorded decision, by design."""
    return [{
        "report_id": r["report_id"], "pmid": r.get("pmid", ""),
        "pub_year": r.get("pub_year", ""), "first_author": r.get("first_author", ""),
        "title": r.get("title", ""),
        "required_action": "judge blind",
    } for r in sample_rows if not (r.get("your_decision") or "").strip()]


def ft_retrieval(ft_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Reports with no retrieval status recorded yet."""
    return [{
        "report_id": r["report_id"], "pmid": r.get("pmid", ""), "doi": r.get("doi", ""),
        "pub_year": r.get("pub_year", ""), "first_author": r.get("first_author", ""),
        "title": r.get("title", ""),
        "source_ta_decision_basis": r.get("source_ta_decision_basis", ""),
        "full_text_status": (r.get("full_text_status") or "").strip() or "(none)",
        "required_action": "obtain full text",
    } for r in ft_rows if not (r.get("full_text_status") or "").strip()]


def ft_assessment(ft_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Retrieved full texts carrying no eligibility decision."""
    return [{
        "report_id": r["report_id"], "pmid": r.get("pmid", ""), "doi": r.get("doi", ""),
        "pub_year": r.get("pub_year", ""), "first_author": r.get("first_author", ""),
        "title": r.get("title", ""),
        "full_text_status": r.get("full_text_status", ""),
        "full_text_source": r.get("full_text_source", ""),
        "required_action": "assess eligibility",
    } for r in ft_rows
        if (r.get("full_text_status") or "").strip() == "retrieved"
        and not (r.get("decision") or "").strip()]


def build() -> dict[str, list[dict[str, str]]]:
    ta_path = worksheet.worksheet_path(TA)
    if not ta_path.exists():
        raise PipelineError(
            f"{ta_path.name} not found; there is no screening work to queue. Create it first.")
    ta_rows = read(ta_path)

    ft_path = worksheet.worksheet_path(FT)
    ft_rows = read(ft_path) if ft_path.exists() else []

    sample_path = worksheet.SCREENING_DIR / "verification_sample.csv"
    sample_rows = read(sample_path) if sample_path.exists() else []

    return {
        "ta_adjudication": ta_adjudication(ta_rows),
        "blinded_verification": blinded_verification(sample_rows),
        "ft_retrieval": ft_retrieval(ft_rows),
        "ft_assessment": ft_assessment(ft_rows),
    }


# One sampled record carries three response cells. Counted from the sheet rather than assumed, so
# the figure cannot drift from the instrument if the sample size or the response fields change.
RESPONSE_FIELDS = ("your_decision", "your_reason_code", "your_notes")


def verification_cells(sample_rows: list[dict[str, str]]) -> tuple[int, int]:
    """(completed, total) response cells across the drawn sample."""
    total = len(sample_rows) * len(RESPONSE_FIELDS)
    done = sum(1 for r in sample_rows for f in RESPONSE_FIELDS if (r.get(f) or "").strip())
    return done, total


def read_sample() -> list[dict[str, str]]:
    path = worksheet.SCREENING_DIR / "verification_sample.csv"
    return read(path) if path.exists() else []


def write_queues(queues: dict[str, list[dict[str, str]]]) -> list[str]:
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for name, rows in queues.items():
        path = QUEUE_DIR / f"{name}.csv"
        with open(path, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=COLUMNS[name])
            w.writeheader()
            for r in rows:
                w.writerow({c: r.get(c, "") for c in COLUMNS[name]})
        written.append(path.name)
    return written


def render_summary(queues: dict[str, list[dict[str, str]]],
                   verification_cells: tuple[int, int] = (0, 0)) -> str:
    """Summarise the queues in units that are stated, never mixed.

    Three quantities are easy to conflate and are therefore reported separately: a **distinct
    report** (a record, which may appear in more than one queue), a **task instance** (one
    queue's work on one record), and a **verification response cell** (one of three answers per
    sampled record). Adding a response-cell count to a task count would give a number that
    measures nothing, so the totals are never summed across units.
    """
    done_cells, total_cells = verification_cells
    rows_by = {name: len(rows) for name, rows in queues.items()}
    task_instances = sum(rows_by.values())
    distinct = len({r["report_id"] for rows in queues.values() for r in rows})

    lines = [
        "# Human review queues \u2014 generated", "",
        "Regenerated by `scripts/screening/review_queue.py` from the worksheets as they stand. "
        "Every row is derived; **nothing here is a decision, a suggestion or a judgement**, and "
        "no queue records a reviewer, a date or an outcome. Those belong in the worksheets.", "",
        "## How much work is outstanding", "",
        "Three quantities, in three different units. They are **not** added together.", "",
        "| Quantity | Count | Unit |", "|---|---|---|",
        f"| Distinct reports across all queues | **{distinct}** | reports (the union; the queues "
        "overlap) |",
        f"| Task instances | **{task_instances}** | one queue's work on one record "
        f"({' + '.join(str(rows_by[n]) for n in queues)}) |",
        f"| Verification records | **{rows_by['blinded_verification']}** | reports sampled |",
        f"| Verification response cells | **{total_cells}** | 3 per sampled record "
        "(`your_decision`, `your_reason_code`, `your_notes`) |", "",
        f"**Completed: {done_cells} of {total_cells} verification response cells, and 0 of "
        f"{task_instances} task instances. Every task below is outstanding.**", "",
        "A response cell is not a task instance, and the two are never summed. The "
        f"{rows_by['ft_retrieval']} retrieval tasks have no response cells at all: retrieval is "
        "recorded as a status in the full-text worksheet, not as answers on a form.", "",
        "## The queues", "",
        "| Queue | Task instances | What the reviewer must do |", "|---|---|---|",
    ]
    for name, rows in queues.items():
        lines.append(f"| `{name}.csv` | **{len(rows)}** | {ACTIONS[name]} |")
    lines += [
        "", "## How the queues overlap", "",
        "The queues are different **tasks**, some of them on the same **records**, which is why "
        "the task-instance total exceeds the number of distinct reports.", "",
        "- Every verification record is drawn from the title/abstract population, so the "
        "verification queue is contained in it.",
        "- Every full-text retrieval record is a title/abstract **include**, so the retrieval "
        "queue is contained in that subset.",
        "- A record can therefore appear in both the verification and the retrieval queue, and "
        "some do.",
        f"- The union of all queues is **{distinct} distinct reports**.", "",
        "## Dependencies between the queues", "",
        "`ta_adjudication` gates everything downstream: until a report's title/abstract decision "
        "is the reviewer's own, the full-text row it produced is provisional and the formal "
        "PRISMA flow counts it nowhere. `blinded_verification` is independent of the others and "
        "can be done at any time; it measures one reviewer's blinded judgement against the "
        "automated suggestion set, and is **not** duplicate screening. `ft_assessment` cannot "
        "begin for a report until its full text is recorded as retrieved.", "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        queues = build()
    except PipelineError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    written = write_queues(queues)
    summary = QUEUE_DIR / "README.md"
    summary.write_text(render_summary(queues, verification_cells(read_sample())),
                       encoding="utf-8")
    for name, rows in queues.items():
        print(f"  {name:22s} {len(rows):4d} record(s)")
    print(f"-> results/queues/ ({', '.join(written)}, README.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
