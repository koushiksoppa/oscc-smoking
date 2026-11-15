# Submission package — completion checklist

**Built:** 13 November 2026 · **Repository:** `HEAD` `b5afaff`, 34 commits, nothing committed in
this sprint.

## Files

| Deliverable | Path | Size | State |
|---|---|---|---|
| Research project report (Word) | `Research_Project_Report.docx` | 580,989 B | **29 pages**, 24 tables, 4 figures |
| Research project report (PDF) | `Research_Project_Report.pdf` | 508,443 B | 29 pages |
| Presentation | `Research_Project_Presentation.pptx` | 573,939 B | **15 slides**, 4 embedded figures |
| Speaker notes (Word) | `Presentation_Speaker_Notes.docx` | 13,968 B | Per-slide notes, 11 anticipated questions |
| Speaker notes (PDF) | `Presentation_Speaker_Notes.pdf` | 162,053 B | 10 pages |
| Manuscript status note (Word) | `Manuscript_Status_Note.docx` | 6,331 B | What is and is not ready for publication |
| Manuscript status note (PDF) | `Manuscript_Status_Note.pdf` | 108,982 B | 3 pages |
| Architecture diagram | `figures/pipeline_architecture.png` | 191,109 B | 15 stages, status-coloured |
| Data-flow diagram | `figures/data_flow.png` | 182,258 B | 4 custody classes |
| Technology-stack diagram | `figures/tech_stack.png` | 124,518 B | 6 layers |
| Numerical results figure | `figures/record_status.png` | 85,349 B | Recomputed at build time |

The existing **systematic review manuscript** and **supplementary material** remain separate, in
`results/manuscript/`, unchanged by this sprint and still titled as a protocol and interim report.

## Generators — every deliverable is reproducible

```bash
.venv/Scripts/python -m scripts.reporting.build_report_figures
.venv/Scripts/python -m scripts.reporting.build_manuscript --source docs/reports/research_project_report.md --stem Research_Project_Report --outdir results/final_submission
.venv/Scripts/python -m scripts.reporting.build_manuscript --source docs/reports/presentation_speaker_notes.md --stem Presentation_Speaker_Notes --outdir results/final_submission
.venv/Scripts/python -m scripts.reporting.build_manuscript --source docs/reports/manuscript_status_note.md --stem Manuscript_Status_Note --outdir results/final_submission
.venv/Scripts/python -m scripts.reporting.build_presentation
```

## Validation performed

| Check | Result |
|---|---|
| Full test suite | **615 passed, 1 skipped** (616 collected) |
| New tests added this sprint | 16 (`tests/test_build_presentation.py`) |
| PPTX package validity | 43 parts, all XML well-formed, **0 dangling relationships**, every part has a content type |
| PPTX determinism | Two builds byte-identical |
| Figure determinism | Two builds byte-identical across all four |
| Report DOCX ↔ PDF | 64/64 headings in order, 719/719 table cells, 103/103 numeric tokens, 80/80 sentences |
| Speaker notes DOCX ↔ PDF | 19/19 headings, 26/26 cells, 26/26 numbers, 80/80 sentences (one split across a page break, both halves verified) |
| Status note DOCX ↔ PDF | 7/7 headings, 97/97 cells, 48/48 numbers, 34/34 sentences |
| Existing manuscript auditor | **0 failing checks** |
| Raw export checksum | **OK** |
| Seven screening/processed data files | **All OK** |
| Five verification-seed constants | Unchanged |

## Scientific-integrity checks

| Requirement | Status |
|---|---|
| Automated output labelled provisional, never as human decisions | **Enforced** — asserted by test |
| No claim of included studies while the formal count is zero | **Enforced** — asserted by test |
| No invented OR, CI, p-value, I², pooled estimate | **None present anywhere** |
| No forest plot generated without estimates | **None exists** |
| No claim that publication bias was assessed | **Explicitly stated as not assessed** |
| No unused technology claimed | **pandas explicitly declared unused** — asserted by test |
| No risk-of-bias instrument implied as chosen | **Asserted by test** in both workbook and deck |
| Counts-only interrogations not presented as search yields | **Asserted by test** |
| Raw data, screening records, protocol decisions unmodified | **Verified by checksum** |
| No human screening decision created | **None** — 0 of 194 still unadjudicated |

## What this package does not contain

No pooled estimate, forest plot, funnel plot, heterogeneity statistic or p-value — because no
eligible study estimate exists. No included studies. No extracted data. No risk-of-bias
assessments. These absences are the project's current state and are reported as such throughout.
