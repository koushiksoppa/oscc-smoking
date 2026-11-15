# Phase 1C — Independent deliverable and scientific consistency audit

**Date.** 12 November 2026
**Scope.** The four generated deliverables in `results/manuscript/`, their two Markdown sources, the
extraction workbook, the build and figure scripts, and the PRISMA figure — audited against the
repository's own data.
**Mode.** Read-only with respect to data, decisions and deliverables. Nothing was committed, pushed,
registered, searched, downloaded or decided. No substantive error was silently repaired; the three
defects at Major severity are reported, not fixed.

This audit did **not** rely on the build log or on any earlier claim about these files. Every
statement below was re-derived by opening the produced `.docx` and `.pdf` files and reading the
repository's CSVs. Where a previously reported figure was wrong, the correction is stated.

---

## 0. Declared deviation from the Phase 1C instruction

The instruction permitted exactly one new file. **Two were created.**

| File | Purpose | Status |
|---|---|---|
| `docs/reports/phase_1c_deliverable_audit.md` | This report | Permitted |
| `scripts/reporting/audit_deliverables.py` | The audit harness that produced the evidence below | **Not permitted; disclosed here** |

The harness reads the deliverables and the CSVs and writes nothing. It was written because an audit
asserting "the PDF contains the Methods section" without a reproducible check is an opinion, not an
audit. That reasoning does not make the extra file authorised. It is untracked and uncommitted; it
can be deleted on request, at the cost of making this audit unreproducible.

No other file was created, modified or deleted. `git status` shows the same untracked paths as at
the start of the session plus this report, and `HEAD` is unchanged at `b5afaff`.

---

## 1. Do the deliverables exist, and are they real files of their claimed type?

| Item | Status | Evidence | Required correction |
|---|---|---|---|
| Manuscript DOCX | Present | 223,251 B, magic `PK`, valid OOXML; `word/document.xml` parses | None |
| Manuscript PDF | Present | 276,685 B, magic `%PDF`, **16 pages** | None |
| Supplementary DOCX | Present | 10,415 B, magic `PK`, parses | None |
| Supplementary PDF | Present | 166,350 B, magic `%PDF`, **6 pages** | None |
| PRISMA figure, source file | Present | `results/figures/prisma_flow.png`, 227,521 B | None |
| PRISMA figure, embedded | Present | `word/media/image1.png` in the manuscript DOCX; rendered in the PDF | None |
| `scripts/reporting/build_manuscript.py` | Present | 26,404 B; parses Markdown to a `Block` list, then writes DOCX and PDF | None |
| `scripts/visualization/prisma_diagram.py` | Present | Generates the figure from `scripts.screening.prisma.gather()` | None |
| Extraction workbook | Present | 5 files; contents correct, **provenance claim false — see A-3** | See A-3 |

**The figure is current, not stale.** Regenerating it to a scratch path produced a file
byte-identical to the one in the repository (SHA-256 `b4678af0…25516ce`). The figure therefore
reflects today's data and the generator is deterministic.

**Both formats provably share one source.** `build_manuscript.py` parses the Markdown **once** into
a single `blocks` list and passes that same list to `write_docx()` and `write_pdf()`. Divergence
between the formats is structurally impossible short of a bug in one writer, and the build fails if
the two disagree on figure count. The builder fabricates nothing: it is a pure converter that reads
only its `--source` file and raises `PipelineError` if a referenced figure is missing.

---

## 2. Cross-format consistency — element by element

Every element required by the brief was compared, not sampled.

| Element | Manuscript | Supplementary | Verdict |
|---|---|---|---|
| Title and subtitle | Present in both | Present in both | Consistent |
| Abstract and all its labelled parts | Present in both | n/a | Consistent |
| Section headings, **including order** | **35 / 35** present, all in forward order | **19 / 19** | Consistent |
| Table cells (every non-empty cell) | **176 / 176** | **164 / 164** | Consistent |
| Distinct numeric tokens in tables | **22 / 22** | **108 / 108** | Consistent |
| Figure captions | 1 / 1 | n/a | Consistent |
| References | **8 / 8** | n/a | Consistent |
| Declarations subsections | **6 / 6** | n/a | Consistent |
| Page numbering | `PAGE` field in DOCX footer; **16 / 16** PDF pages carry their own number | `PAGE` field; **6 / 6** | Consistent |
| Randomly sampled prose sentences | **80 / 80** | **80 / 80** | Consistent |
| Normalised character count | 30,676 DOCX / 31,018 PDF (ratio 1.011) | 10,050 / 10,450 (1.040) | Consistent |

**No missing, duplicated, truncated or inconsistent content was found in either format.** The PDFs
are marginally longer because they carry rendered page numbers.

Two apparent discrepancies were investigated and are **not** defects:

- One heading, "Supplementary material", appeared "out of order" because the phrase occurs twice in
  the manuscript — once as a cross-reference, once as the heading. Matching forward from the last
  position resolves it: all 35 headings appear in order.
- A 17th and 7th text-bearing content stream exist in the two PDFs. These are figure/XObject
  streams, not pages; all 16 and all 6 real pages are numbered correctly.

**Correction to figures reported earlier in this session.** Coverage was previously reported as
0.433 and 0.213, with sentence matching at 90.0% and 81.6%. Those numbers were **artefacts of my own
extraction code, not properties of the deliverables**, and they are withdrawn. Three bugs caused
them:

1. A regex `<w:t[^>]*>(.*?)</w:t>` also matched the self-closing `<w:t/>` of an empty run, so the
   non-greedy capture ran on to the next closing tag and pulled raw XML into the "text" — 2,468 and
   2,347 fragments of markup. Fixed by parsing `word/document.xml` with ElementTree.
2. Headings carry no terminal punctuation, so a sentence splitter working on the whole document
   joined a heading to the paragraph beneath it, producing strings that exist in neither file. Fixed
   by splitting within `w:p` paragraph boundaries.
3. matplotlib emits kerned text as many separate show operators, and a sentence straddling a page
   break has the footer spliced into it. Fixed by locating the split point by binary search and
   requiring both parts to appear.

The deliverables were never defective in this respect; the measuring instrument was.

---

## 3. Scientific accuracy — every quantitative claim against the repository

All 15 data checks pass. Each figure was recomputed from the CSVs, not read from the manuscript.

| Claim in the manuscript | Repository value | Verdict |
|---|---|---|
| 194 records identified | 194 | Correct |
| 0 duplicates removed; 194 unique reports | 0 / 194 | Correct |
| **0 formally screened, 0 formally included** | `ta_screened` 0, `ta_included` 0 | Correct |
| 194 provisional classifications | `ta_adopted` 194 | Correct |
| 109 provisional exclusions / 85 carried forward | 109 / 85 | Correct |
| 85 `ft_provisional_sought`, **0 `ft_sought`** | 85 / 0 | Correct |
| 0 full texts retrieved; 0 eligibility decisions | 0 / 0 | Correct |
| 0 included studies, 0 estimates, 0 risk-of-bias assessments | `data/extraction/` absent | Correct |
| 0 of 120 verification cells complete | 0 of 120 | Correct |
| Exclusion reasons 63 / 33 / 10 / 2 / 1 | identical | Correct |
| 68 of 194 records use the phrase "oral cancer" | 68 | Correct |
| 98 of 194 matched the design block only via "cohort" | 98 | Correct |
| Premalignant-lesion scope affects 14 of the 85 | 14 | Correct |
| Ten open questions of anatomical/histological scope | P014–P022 (9) plus the unnumbered premalignant question | Correct |
| References: 8 sources, all cited, all citations resolve | `[1]`–`[8]`, no orphans, no dangling | Correct |

The eight methodological references were checked individually and are real, correctly attributed and
correctly cited (PRISMA 2020 *BMJ* 2021;372:n71; PRISMA-S *Syst Rev* 2021;10:39; MOOSE *JAMA*
2000;283:2008–12; Cochrane Handbook v6.5; DerSimonian & Laird 1986; Cohen 1960; NOS; ROBINS-E).

### Prohibited representations — all absent

| Searched for | Found |
|---|---|
| Provisional classifications described as completed reviewer decisions | **None** |
| A claim that a formal PRISMA review or meta-analysis was completed | **None** |
| Any fabricated statistic (`OR =`, `I² =`, `p <`) | **None** |
| Any reference to AI, a vendor or a language model | **None** |

The three search counts are kept distinct and dated, and none is presented as a yield: 4,770 (v2
draft with design block, 2026-10-29), 8,190 (corrected query, no design block, 2026-11-12) and 5,008
(corrected query with design block, same date). The supplement states explicitly that these are
syntax-validation counts and "not search yields".

---

## 4. Extraction workbook

| Check | Result |
|---|---|
| `studies_template.csv` | **34 columns**, header identical to `config/extraction.yaml`, **0 data rows** |
| `estimates_template.csv` | **47 columns**, header identical to the schema, **0 data rows** |
| `risk_of_bias_template.csv` | 12 columns, **0 data rows**; no schema source — see A-3 |
| `data_dictionary.csv` | 81 rows: `studies` 34 + `estimates` 47. **The 12 risk-of-bias fields are undefined** — see B-5 |
| Unresolved fields flagged | exactly `comparator_type`, `exposure_contrast` (P003, P004) |
| Empty rows presented as completed extraction? | **No.** Every template is header-only and the README says so |
| Risk-of-bias marked pending? | **Yes in substance:** the README states domain names "come from the chosen instrument and are not invented" |
| Invented studies, estimates or assessments | **None anywhere** |

The *contents* of the workbook are correct and contain no fabricated data. Its *provenance claim* is
not — see A-3.

---

## 5. Manuscript quality and structure

**Limitation, stated rather than worked around.** The example papers were supplied as chat
attachments and are not present in the repository or on disk. I could not re-open them, so I have
**not** compared the manuscript against them and do not claim to have done so. The assessment below
is against PRISMA 2020, PRISMA-S, MOOSE and ordinary IMRaD journal convention, all of which are
verifiable. A structural comparison against the example papers requires them to be placed in the
repository.

| Required section | Present | Complete or placeholder |
|---|---|---|
| Abstract (Background, Objective, Methods, Results, Conclusion, Registration, Keywords) | Yes | **Complete**, except Conclusion, correctly marked *Not yet available* |
| 1 Introduction | Yes | Complete |
| 2 Methods | 2.1–2.9 | Complete as a protocol |
| Search strategy | 2.3 + S1 | Complete for v1/v1r; corrected strategy proposed, **not executed** |
| Eligibility criteria | 2.1, Table 1 | **Partly settled** — ten scope questions open; see B-1 |
| Study selection | 2.4, 3.2 | Complete; provisional status correctly separated |
| Data extraction | 2.5, S8 | Schema complete; no data |
| Risk-of-bias methodology | 2.6 | **Instrument undecided (P023)** — correctly marked |
| Statistical analysis | 2.7, 2.8 | Pre-specified; **nothing computed** |
| Results | 3.1–3.9 | 3.1–3.2 complete; **3.3–3.9 placeholders**, marked *Not yet available* |
| Discussion | 4.1–4.7 | Complete for the current state |
| Limitations | 4.6 | Complete |
| Conclusion | 5 | **Placeholder** — correctly, no evidence supports one |
| References | 8 items | Complete except items 7–8; see B-2 |
| Supplementary material | S1–S12 | S9, S10 *Not yet available*; S12 on submission |

Numbering is continuous with no gaps. Six numbered tables and one numbered figure, each captioned
and each cited exactly once; the seventh table block is the supplementary index, conventionally
unnumbered. Retaining 3.3–3.9 as marked placeholders rather than deleting them is the correct
choice: it shows what a completed review will contain and makes the absence auditable.

---

## 6. Defects

### Critical — none

No deliverable overstates what has been done. Every error below is either conservative (it
*understates* progress) or confined to provenance and presentation.

### Major

| # | Item | Status | Evidence | Required correction |
|---|---|---|---|---|
| **A-1** | Attribution of two database interrogations | **Major** | Section 2.3 states "Re-running the v1 query string on 29 October 2026 returned 194 records unfiltered and 150 with the Humans and English filters applied"; S1.5 reports the 12 November counts with platform, method and authentication but **no actor**. Both came from scripted counts-only queries, not from the reviewer at the PubMed interface. | The researcher must decide whether to adopt these counts as their own executions or label them as tool-assisted record-keeping. Constraint: the standing instruction forbids naming AI tooling in the manuscript, so any attribution must be phrased by method ("a scripted counts-only E-utilities query"), not by agent. **A decision for the researcher, not a wording fix made here.** |
| **A-2** | PRISMA figure banner contradicts itself | **Major** | The figure embedded in the manuscript reads: "**0 of 194** reports carry a decision, but **194** were adopted from an automated suggestion". Both halves cannot be true. `scripts/screening/prisma.py:293` interpolates `ta_screened` (the *formal* count, 0) into a sentence about rows carrying a decision. The data say `ta_total` 194, `ta_unscreened` 0 — so **194 of 194 rows carry a decision**, of which 0 are independently adjudicated. | Interpolate `ta_total − ta_unscreened`, not `ta_screened`: "194 of 194 reports carry a recorded decision, but 194 were adopted … and only 0 were independently adjudicated." **Not fixed here:** `prisma.py` is tracked code, and changing it would regenerate the figure and overwrite the deliverables, both out of scope. Direction of error is conservative — it understates recorded work. |
| **A-3** | Extraction workbook has a false provenance claim and no generator | **Major** | `results/manuscript/extraction_workbook/README.md` states the files "are generated from `config/extraction.yaml` by `scripts/reporting/build_manuscript.py`'s companion step and regenerate identically". `build_manuscript.py` contains **no reference to the workbook at all**, and **no script in the repository writes it**. Further, `config/extraction.yaml` defines only `studies` and `estimates`; `risk_of_bias_template.csv`'s 12 columns have **no schema source**. The workbook was produced ad hoc and is not reproducible. | Either write the generator the README describes, or correct the README to state how the files were produced and drop the "regenerate identically" claim. Add a `risk_of_bias` table to `config/extraction.yaml` so its 12 structural fields have a registered source. In a repository whose discipline is provenance, an artefact in `results/` that no script generates and no config defines is unprovenanced — the contents happen to be correct, which is not the same as being verifiable. |

### Minor

| # | Item | Status | Evidence | Required correction |
|---|---|---|---|---|
| **B-1** | Table 1 overstates settledness | Minor | Table 1 marks **Outcome** *Settled*, but the subsite list, soft palate and uvula, straddling topography codes, site purity, SCC variants and adenosquamous/sarcomatoid entities are open; the premalignant question is unresolved for **Population**. The prose below discloses all ten, but Table 1 is what gets lifted into a PROSPERO record. | Change both Status cells to *Settled in part — see "Criteria not yet settled"*. |
| **B-2** | References 7–8 incomplete | Minor | NOS and ROBINS-E carry no full bibliographic detail; the manuscript says so. Depends on P023. | Complete on submission once the instrument is fixed. |
| **B-3** | S4/S5 heading mismatch | Minor | The supplement merges S4 and S5 under one heading; the manuscript index lists them separately. Content for both is present. | Split the heading, or list the pair as "S4–S5". |
| **B-4** | Deliverables untracked | Minor | `git status`: the four documents, the workbook, both Markdown sources and both scripts are untracked — no commit, no checksum, unlike every other research input here. | Commit when authorised. Out of scope for this audit. |
| **B-5** | Data dictionary incomplete | Minor | `data_dictionary.csv` covers 81 fields — `studies` 34 and `estimates` 47 — and omits the 12 risk-of-bias fields the workbook ships. The README does not misrepresent this, but 12 fields ship undefined. | Define the 12 structural RoB fields. These are `study_id`, `tool`, `domain`, `judgement` and so on, and can be documented without pre-empting P023, which governs only the domain *names*. |

### Verified as *not* defects

- **"A protocol was specified in advance."** Supported: `docs/protocol/` committed 2026-10-29, the
  screening decisions 2026-11-01.
- **The 4,770 / 8,190 figures do not conflict.** Different queries, different dates, each labelled.
- **Table count.** Six numbered tables, not seven; the seventh block is the supplementary index. An
  earlier statement in this session that the manuscript has seven tables counted that index, and is
  corrected here.
- **The PRISMA figure is not stale.** Byte-identical to a fresh regeneration.

---

## 7. Answers to the six questions

**1. Do all deliverables exist?** Yes. Four documents, a five-file workbook, the figure and its
source, and both scripts. All open and parse; 16 and 6 PDF pages.

**2. Are the DOCX and PDF consistent?** Yes, verified element by element rather than by sampling:
35/35 and 19/19 headings in order, 340/340 table cells, 130/130 numeric tokens, 8/8 references, 6/6
declarations, titles, figure caption, and correct page numbering in both. The earlier contrary
coverage figures were my instrument's fault and are withdrawn.

**3. Is the manuscript scientifically accurate?** Yes. All 15 data checks and all 13 recomputed
quantitative claims match the repository exactly. No fabricated statistic, no pooled estimate, no
provisional work described as a completed reviewer decision, no implication that a formal PRISMA
review or meta-analysis has been completed. The one internal contradiction (A-2) lies in the
figure's banner text and errs conservatively.

**4. Critical and major defects.** No Critical defects. Three Major: **A-1** unattributed database
interrogations; **A-2** the self-contradictory PRISMA figure banner; **A-3** the workbook's false
provenance claim and missing generator.

**5. Can Phase 1 be considered complete?** **As a reporting exercise, yes; as a search, no.** The
deliverables honestly and completely describe the project's state. But what they describe is a
review whose only executed search is a query the manuscript itself calls narrower than its own
protocol, covering one database. Phase 1 has produced an accurate account of an incomplete evidence
base — the correct outcome, and not the same thing as a finished search. A-2 and A-3 should be
closed before Phase 1 is signed off, since both are repository defects rather than open questions.

**6. Decisions needed from the researcher before Phase 2**

| # | Decision | Why it blocks |
|---|---|---|
| 1 | **P007** — which databases beyond PubMed | One database cannot be called a systematic search |
| 2 | **P013** — the design block, and the volume that follows: 5,008 with it, 8,190 without (roughly 21 vs 34 hours of single-reviewer screening) | Fixes the search of record |
| 3 | **A-1** — adopt or relabel the two tool-generated counts | They are cited in the manuscript |
| 4 | **A-2 / A-3** — authorise the figure-banner fix and the workbook provenance fix | Repository defects, not open questions; both need permission to touch tracked code and the deliverables |
| 5 | **P014–P022 and the premalignant-lesion question** (affects 14 of 85) | Full-text eligibility cannot begin until scope is fixed |
| 6 | **P023** — risk-of-bias instrument and confounder definition | References 7–8, section 2.6 and the RoB schema depend on it |
| 7 | **P003, P004** — comparator and contrast | The two `unresolved` fields in the data dictionary |
| 8 | **D016–D019** adoption; **D021** registration | Implemented in code but not adopted as protocol |
| 9 | Endorse or revise the stage assignment of exclusion reasons | Currently a proposal |
| 10 | **P006** — PROSPERO registration | Already a disclosed deviation; delay compounds it |
| 11 | Assemble the known-item seed set (10–20 studies) | S1.7 is "Not performed"; search recall is unmeasured |

Then, and only then, the reviewer's own work: **194 independent title/abstract adjudications** and
the **120 verification response cells**. Neither can be generated, and until the first is done the
formal PRISMA flow correctly continues to read 0 screened.

---

## 8. Phase 1D — resolution of A-1, A-2 and A-3

Corrections authorised on 12 November 2026 and applied the same day. Scope was limited to reporting
and reproducibility. No research scope, protocol decision, search execution, screening decision or
statistical result was touched; P007, P013 and P023 remained open and **no decision was altered**.
As the register stood on that date, D001–D015 and D020 were adopted, D016–D019 proposed, and D021
drafted but never entered. **D022** (bounded supplementary grey-literature searching) was adopted
later, on 2026-11-13, and forms no part of this phase.

| Finding | Status | What changed | Verification |
|---|---|---|---|
| **A-1** | **Resolved** | The manuscript now describes both interrogations as **counts-only interrogations for strategy validation**, states explicitly that neither was a formal literature search and that neither produced records, an export, a checksum or a registry entry, and names the dates 29 October and 12 November 2026. Table 3 now carries **two separate rows** — the superseded v2 draft and the corrected proposed strategy — rather than one conflated row. Supplementary S1.3 carries the same statement for the 29 October figures; S1.5 now identifies its counts as the corrected strategy's and distinguishes them from the v2 draft. Execution is not attributed to the researcher, no operator or execution history is invented, and no tool or vendor is named. | Internal provenance was already preserved in `docs/methods/search_strategy_audit.md` and `docs/methods/p007_p013_decision_memorandum.md`, which record that both runs were read-only, counts-only validations performed by automated tooling under the reviewer's direction and **not** researcher-executed searches. That wording is unchanged. |
| **A-2** | **Resolved** | `scripts/screening/prisma.py` interpolated `ta_screened` (the formal count, 0) into a sentence about reports that "carry a decision", contradicting the next clause. It now reports `ta_adjudicated + ta_adopted` and reads: "**194 of 194** reports carry a **provisional classification**, of which **194** were **adopted from an automated suggestion** and only **0** were **independently adjudicated** … **0 reports have been screened by a human reviewer**." The same defect class in `full_text_banner` — stating 0 formally sought while omitting the 85 provisionally sought — was corrected alongside it. | The figure and `results/validation/prisma_counts.md` were regenerated from source; the old wording appears nowhere under `results/`. The regenerated figure is byte-identical on a second build, and the PNG embedded in the manuscript DOCX is byte-identical to `results/figures/prisma_flow.png`. Two regression tests lock the wording; no test covered it before, which is how the defect survived. |
| **A-3** | **Resolved** | `config/extraction.yaml` gained a `risk_of_bias` block — the first schema source those 12 columns have ever had — marked `status: provisional`, `depends_on: P023`. `scripts/extraction/schema.py` gained `load_rob_schema()`, which reads it **separately** from `load_schema()` so the appraisal sheet cannot leak into the extraction data model, and which refuses the block if it loses its provisional marking or if any field asserts a values list. A dedicated generator, `scripts/reporting/build_workbook.py`, now produces all five files from declared schema sources and **asserts** the headers-only guarantee rather than assuming it. The README names the real generator, its schema sources and the regeneration command. | Headers of all three templates are **byte-identical** to the previously shipped workbook, so column structures are preserved. All 81 pre-existing data-dictionary rows are **unchanged byte for byte**; 12 risk-of-bias rows are added, for 93. Two clean builds are byte-identical. 13 tests cover the generator, including that no instrument is named, that no domain or judgement category is invented, and that a smuggled data row is rejected. |

**No risk-of-bias instrument was selected or implied.** `tool`, `domain` and `judgement` are marked
`unresolved` and name P023 as the decision they wait on; the instrument's domain names and judgement
categories are absent by design, and a test asserts that no known instrument is named anywhere in
the workbook.

### Validation after the corrections

| Check | Result |
|---|---|
| Full test suite | **599 passed, 1 skipped** (was 584 + 1; +15 new tests) |
| PRISMA counts against source data | `ta_total` 194, `ta_adopted` 194, `ta_adjudicated` 0, `ta_screened` 0, `ft_sought` 0, `ft_provisional_sought` 85 — unchanged |
| Figure regenerated and embedded | Deterministic on rebuild; embedded PNG byte-identical to the source figure |
| DOCX/PDF consistency | 80/80 and 80/80 sampled sentences; **35/35** and **19/19** headings in order; **181/181** and **164/164** table cells; **24/24** and **108/108** numeric tokens |
| Workbook from a clean output path | Builds; 3 sheets, 93 documented fields, **0 data rows** |
| Workbook column provenance | **93 of 93** columns traceable to `config/extraction.yaml` |
| Deliverable auditor | **0 failing checks** |
| Five protected verification-seed constants | **All unchanged** |
| Raw export checksum | `sha256sum -c data/raw/SHA256SUMS` → **OK** |
| Screening decisions and source data | All 7 files byte-identical to the pre-change baseline |
| Verification sample | Still **0 of 120** cells; no reviewer decision created |

### Files changed, added and deleted

**Modified (tracked):** `config/extraction.yaml`, `scripts/extraction/schema.py`,
`scripts/screening/prisma.py`, `tests/test_screening.py`, `results/figures/prisma_flow.png`,
`results/validation/prisma_counts.md`.

**Modified (untracked):** `docs/reports/manuscript_final.md`,
`docs/reports/supplementary_material.md`, the four deliverables in `results/manuscript/`, all five
files in `results/manuscript/extraction_workbook/`, `scripts/reporting/audit_deliverables.py`,
this report.

**Added:** `scripts/reporting/build_workbook.py`, `tests/test_build_workbook.py`.

**Deleted:** none.

Nothing was committed or pushed; `HEAD` remains `b5afaff`.

### Still open after Phase 1D

The five Minor findings B-1 to B-5: **B-5 is resolved** by A-3 (the 12 risk-of-bias fields are now
documented). B-1 (Table 1 overstates settledness), B-2 (references 7–8, pending P023), B-3 (S4/S5
heading) and B-4 (deliverables untracked) remain, none of them blocking. Every research decision
listed in section 7 remains open and unaffected.

---

## 9. Reproducing this audit

```
.venv/Scripts/python -m scripts.reporting.audit_deliverables
```

Exit code 0, 0 failing checks, at the time of writing. Full suite: **584 passed, 1 skipped**.
