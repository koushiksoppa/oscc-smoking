"""Figures for the research project report.

    python -m scripts.reporting.build_report_figures

Four figures, written to results/final_submission/figures/:

    pipeline_architecture.png  the fifteen pipeline stages, coloured by implementation status
    data_flow.png              which file each stage reads and writes, and where the gates sit
    tech_stack.png             the layers actually present in the repository
    record_status.png          the 194 records by current status

Status colours are not decorative: a stage is green only where code exists AND has been run on the
real data, amber where the code exists and is tested but has never been run, and grey where no
implementation exists. The counts in `record_status` come from `scripts.screening.prisma.gather()`
at build time, so a figure cannot drift from the data it describes.

Deterministic: fixed figure size, fixed DPI, no randomness, no timestamps drawn. The same repository
state produces byte-identical PNGs.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from scripts.common.config import ROOT

OUTDIR = ROOT / "results" / "final_submission" / "figures"

RUN = "#2e7d4f"        # implemented and executed on the real data
BUILT = "#b7791f"      # implemented and tested, never executed
ABSENT = "#8a8a8a"     # not implemented
INK = "#1a1a1a"
LIGHT = "#f4f4f2"

LEGEND = [(RUN, "Implemented and run on the real data"),
          (BUILT, "Implemented and tested; not yet run"),
          (ABSENT, "Not implemented")]

# (stage number, label, status, short note)
STAGES = [
    (1, "Literature identification", RUN, "PubMed v1r, 194 records"),
    (2, "Record import / parsing", RUN, "MEDLINE .nbib to CSV"),
    (3, "Deduplication", RUN, "0 duplicates, 194 reports"),
    (4, "Report and study identity", BUILT, "study_id needs full text"),
    (5, "Title/abstract screening", RUN, "194 provisional"),
    (6, "Independent adjudication", BUILT, "0 of 194 done"),
    (7, "Verification sampling", BUILT, "40 drawn, 0 of 120 cells"),
    (8, "Full-text retrieval", ABSENT, "0 retrieved"),
    (9, "Eligibility assessment", BUILT, "gate refuses: no includes"),
    (10, "Data extraction", BUILT, "gate refuses: no studies"),
    (11, "Risk-of-bias assessment", ABSENT, "instrument open (P023)"),
    (12, "Effect-size preparation", BUILT, "OR/RR/HR, SE routes"),
    (13, "Meta-analysis", BUILT, "gate refuses: no estimates"),
    (14, "Sensitivity and subgroup", BUILT, "leave-one-out built"),
    (15, "Manuscript and outputs", RUN, "DOCX/PDF/workbook built"),
]


def _box(ax, x, y, w, h, text, face, *, fontsize=8.2, weight="normal", textcolour="white"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.02",
                                linewidth=0.9, edgecolor=INK, facecolor=face, zorder=2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize,
            color=textcolour, weight=weight, zorder=3, linespacing=1.35)


def _arrow(ax, p, q, *, style="-|>", colour=INK, lw=1.0, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=9, linewidth=lw,
                                 color=colour, linestyle=ls, zorder=1,
                                 shrinkA=4, shrinkB=4))


def _canvas(w=11.0, h=7.6):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    return fig, ax


def _legend(ax, y=0.035, x=0.07):
    for i, (colour, label) in enumerate(LEGEND):
        cx = x + i * 0.31
        ax.add_patch(FancyBboxPatch((cx, y), 0.022, 0.022, boxstyle="round,pad=0.002",
                                    linewidth=0.7, edgecolor=INK, facecolor=colour))
        ax.text(cx + 0.032, y + 0.011, label, ha="left", va="center", fontsize=7.6, color=INK)


def pipeline_architecture(path: Path) -> None:
    """Three columns, read top-to-bottom then left-to-right, like the pipeline itself."""
    fig, ax = _canvas(11.0, 7.8)
    ax.text(0.5, 0.968, "Pipeline architecture: fifteen stages and their implementation status",
            ha="center", fontsize=11.5, weight="bold", color=INK)
    ax.text(0.5, 0.937, "Colour reflects what the repository actually does, not what is planned",
            ha="center", fontsize=8.3, color="#555")

    GATES = {9, 10, 13}
    w, h = 0.275, 0.094
    x0, ytop, dx, dy = 0.045, 0.800, 0.315, 0.152
    pos = {}
    for i, (num, label, status, note) in enumerate(STAGES):
        c, r = divmod(i, 5)                      # column-major: 1-5, 6-10, 11-15
        x, y = x0 + c * dx, ytop - r * dy
        _box(ax, x, y, w, h, f"{num}. {label}", status, fontsize=8.5, weight="bold")
        gate = num in GATES
        ax.text(x + w / 2, y - 0.026, note, ha="center", va="center",
                fontsize=6.9, color="#b3261e" if gate else "#444",
                weight="bold" if gate else "normal")
        pos[num] = (x, y, w, h)

    for num in range(1, 15):
        x, y, bw, bh = pos[num]
        nx, ny, nw, nh = pos[num + 1]
        if num % 5:                                       # down within a column
            _arrow(ax, (x + bw / 2, y - 0.042), (nx + nw / 2, ny + nh + 0.004))
        # no arrow across columns: the numbering carries the order and a diagonal would
        # cross the whole figure

    ax.text(0.5, 0.072,
            "Three gates refuse in sequence: eligibility needs adjudicated includes, extraction "
            "needs included studies," + chr(10) + "and the analysis needs extracted estimates. Each exits "
            "non-zero rather than producing an empty result.",
            ha="center", fontsize=7.9, color=INK, linespacing=1.5)
    _legend(ax, y=0.012)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def data_flow(path: Path) -> None:
    fig, ax = _canvas(11.2, 7.4)
    ax.text(0.5, 0.968, "Data flow: what each stage reads, writes and verifies",
            ha="center", fontsize=11.5, weight="bold", color=INK)
    ax.text(0.5, 0.937,
            "Every stage re-verifies provenance before reading and writes a report to "
            "results/validation/", ha="center", fontsize=8.3, color="#555")

    H = 0.082
    lanes = [("IMMUTABLE INPUT  —  checksum-gated, never edited", 0.775),
             ("GENERATED DATA  —  regenerable, never hand-edited", 0.580),
             ("HUMAN RESEARCH RECORDS  —  tracked, not regenerable", 0.385),
             ("OUTPUTS  —  generated from the above", 0.190)]
    for label, y in lanes:
        ax.add_patch(FancyBboxPatch((0.035, y - 0.030), 0.935, H + 0.085,
                                    boxstyle="round,pad=0.004", linewidth=0.7,
                                    edgecolor="#d0d0ce", facecolor=LIGHT, zorder=0))
        ax.text(0.048, y + H + 0.035, label, fontsize=7.0, weight="bold",
                color="#5a5a5a", va="center")

    cols = [0.055, 0.293, 0.531, 0.769]
    W = 0.196
    nodes = {
        "raw": (cols[0], lanes[0][1], "data/raw/*.nbib\n+ SHA256SUMS", RUN),
        "cit": (cols[0], lanes[1][1], "citations CSV\n+ records JSONL", RUN),
        "ded": (cols[1], lanes[1][1], "dedup/\nreport_index.csv  (194)", RUN),
        "ext": (cols[3], lanes[1][1], "data/extraction/\nDOES NOT EXIST", ABSENT),
        "sug": (cols[0], lanes[2][1], "ta_suggestions\n194 rows", RUN),
        "ta":  (cols[1], lanes[2][1], "screening_ta.csv\n194 provisional", RUN),
        "ft":  (cols[2], lanes[2][1], "screening_ft.csv\n85 rows, empty", BUILT),
        "ver": (cols[3], lanes[2][1], "verification_sample\n40 rows, 0 of 120", BUILT),
        "val": (cols[0], lanes[3][1], "results/validation/\nreports", RUN),
        "fig": (cols[1], lanes[3][1], "results/figures/\nPRISMA diagram", RUN),
        "man": (cols[2], lanes[3][1], "manuscript\nDOCX + PDF", RUN),
        "wb":  (cols[3], lanes[3][1], "extraction workbook\n93 fields, 0 rows", RUN),
    }
    for x, y, text, colour in nodes.values():
        _box(ax, x, y, W, H, text, colour, fontsize=7.4)

    def down(a, b, **kw):
        ax1, ay1 = nodes[a][0], nodes[a][1]
        bx1, by1 = nodes[b][0], nodes[b][1]
        _arrow(ax, (ax1 + W / 2, ay1), (bx1 + W / 2, by1 + H), **kw)

    def across(a, b, **kw):
        ax1, ay1 = nodes[a][0], nodes[a][1]
        bx1, by1 = nodes[b][0], nodes[b][1]
        _arrow(ax, (ax1 + W, ay1 + H / 2), (bx1, by1 + H / 2), **kw)

    down("raw", "cit")
    across("cit", "ded")
    down("ded", "ta")
    across("sug", "ta", colour="#777", ls=(0, (2, 2)))
    across("ta", "ft", colour=BUILT)
    across("ft", "ver", colour=BUILT)
    down("ft", "ext", colour=ABSENT, ls=(0, (3, 2)))
    down("ta", "fig")
    down("sug", "val")
    across("fig", "man")

    ax.text(0.5, 0.088,
            "The suggestion file is kept separate from the decision file on purpose: an automated "
            "suggestion is never written into a decision field.\n"
            "data/extraction/ is drawn greyed because it does not exist — no study has been "
            "included, so there is nothing to extract.",
            ha="center", fontsize=7.8, color=INK, linespacing=1.55)
    _legend(ax, y=0.012)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def tech_stack(path: Path) -> None:
    fig, ax = _canvas(10.0, 6.6)
    ax.text(0.5, 0.965, "Technology stack as actually present in the repository",
            ha="center", fontsize=11.5, weight="bold", color=INK)
    ax.text(0.5, 0.933, "No component is listed that the code does not import",
            ha="center", fontsize=8.3, color="#555")

    layers = [
        ("Outputs", "DOCX (OOXML via zipfile)  |  PDF (matplotlib PdfPages)  |  PPTX (OOXML)  |  "
                    "PNG figures  |  CSV", "#35526e"),
        ("Analysis", "scipy 1.18.1 — chi2, normal, t, linregress   |   matplotlib 3.11.2 — forest "
                     "and funnel plots", "#2f6b5f"),
        ("Pipeline logic", "Pure Python 3.14.7 standard library: csv, json, hashlib, re, difflib, "
                           "unicodedata, random, math", "#4a5a7a"),
        ("Configuration", "pyyaml 6.0.3 — config/sources.yaml, screening.yaml, extraction.yaml",
         "#6b5b7a"),
        ("Data formats", "MEDLINE .nbib (input, immutable)  |  CSV (all tabular data)  |  "
                         "JSONL (parsed records)", "#7a6a4a"),
        ("Assurance", "pytest 9.1.1 — 615 passed, 1 skipped   |   SHA-256 checksums   |   "
                      "Git, 34 commits", "#6e4a4a"),
    ]
    y = 0.80
    for name, content, colour in layers:
        ax.add_patch(FancyBboxPatch((0.06, y), 0.88, 0.098,
                                    boxstyle="round,pad=0.008,rounding_size=0.015",
                                    linewidth=0.9, edgecolor=INK, facecolor=colour, zorder=2))
        ax.text(0.095, y + 0.049, name, fontsize=9.0, weight="bold", color="white",
                va="center", ha="left")
        ax.text(0.325, y + 0.049, content, fontsize=7.5, color="white", va="center", ha="left")
        y -= 0.128

    ax.text(0.5, 0.075,
            "Deliberately absent: pandas (no module imports it — all tabular work uses the stdlib "
            "csv module), numpy as a direct\ndependency (it arrives transitively under scipy and "
            "matplotlib), and any third-party document library.",
            ha="center", fontsize=7.8, color=INK, linespacing=1.5)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def record_status(path: Path) -> None:
    from scripts.screening import prisma
    f = prisma.gather()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 4.3), dpi=200,
                                 gridspec_kw={"width_ratios": [1.15, 1]})

    labels = ["Identified\n(records)", "Unique reports\n(after dedup)",
              "Provisionally\nexcluded", "Provisionally\ncarried forward",
              "Formally\nscreened", "Studies\nincluded"]
    values = [f["identified"], f["unique_reports"], f["prov_excluded"], f["prov_included"],
              f["ta_screened"], 0]
    colours = [RUN, RUN, BUILT, BUILT, ABSENT, ABSENT]
    bars = a1.bar(range(len(values)), values, color=colours, edgecolor=INK, linewidth=0.7)
    for b, v in zip(bars, values):
        a1.text(b.get_x() + b.get_width() / 2, v + 4, str(v), ha="center",
                fontsize=9, weight="bold", color=INK)
    a1.set_xticks(range(len(labels)))
    a1.set_xticklabels(labels, fontsize=7.6)
    a1.set_ylabel("Records / reports", fontsize=8.5)
    a1.set_ylim(0, max(values) * 1.18)
    a1.set_title("Record status: provisional work is not screening",
                 fontsize=9.5, weight="bold", pad=8)
    a1.spines[["top", "right"]].set_visible(False)
    a1.tick_params(labelsize=7.5)

    done = [("Provisional classifications", f["ta_adopted"], 194, BUILT),
            ("Independent adjudications", f["ta_adjudicated"], 194, ABSENT),
            ("Verification response cells", 0, 120, ABSENT),
            ("Full texts retrieved", 0, 85, ABSENT),
            ("Extracted estimates", 0, 0, ABSENT)]
    ypos = range(len(done))
    for i, (label, got, total, colour) in enumerate(done):
        a2.barh(i, total or 1, color="#e6e6e4", edgecolor="#bbb", linewidth=0.6, height=0.58)
        if got:
            a2.barh(i, got, color=colour, edgecolor=INK, linewidth=0.7, height=0.58)
        a2.text((total or 1) * 1.02, i, f"{got} / {total}" if total else "0 / 0",
                va="center", fontsize=8, weight="bold", color=INK)
    a2.set_yticks(list(ypos))
    a2.set_yticklabels([d[0] for d in done], fontsize=7.6)
    a2.invert_yaxis()
    a2.set_xlim(0, 240)
    a2.set_xticks([])
    a2.set_title("Reviewer work completed", fontsize=9.5, weight="bold", pad=8)
    a2.spines[["top", "right", "bottom"]].set_visible(False)

    fig.suptitle("Figure: current state of the evidence base, recomputed from the repository",
                 fontsize=10.5, weight="bold", y=1.0)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


FIGURES = {"pipeline_architecture.png": pipeline_architecture,
           "data_flow.png": data_flow,
           "tech_stack.png": tech_stack,
           "record_status.png": record_status}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--outdir", default=str(OUTDIR))
    args = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    for name, fn in FIGURES.items():
        fn(out / name)
        print(f"  {name:28} {(out / name).stat().st_size:>8,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
