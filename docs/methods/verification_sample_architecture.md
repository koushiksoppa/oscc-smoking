# Verification-sample provenance architecture — DESIGN ONLY

**Status: design document. Nothing described here is implemented.**

This specifies how multiple blinded verification samples would be recorded, should an extension
sample ever be authorised. It is written now so that the structure is fixed before any agreement
figure is known, and therefore cannot be shaped by a result.

Two things must not be confused:

- **Technical capability** — code that can represent an extension sample.
- **Protocol authorisation** — a reviewer's decision that an extension sample should be drawn.

This document delivers only the first, as a design. It authorises nothing. No extension sample can
be authorised at present in any case: the one existing sample has **0 of 120 response cells
completed**, so no verdict exists, and `EXTEND` is reachable only from a scored result.

Architecture selected: **Architecture 2 — a central index referencing immutable per-sample files.**

---

## 1. Why Architecture 2

| | Architecture 1 — one manifest per sample | **Architecture 2 — central index + immutable files** |
|---|---|---|
| Discovery | by globbing filenames | by reading one registry |
| A misnamed or mislaid file | silently invisible | **detected** — index and disk must agree |
| "How many samples exist, in what order, and what triggered each?" | answerable only by reading every manifest | answerable in one place |
| Cross-sample invariants | no natural home | enforced in one validator |
| Repository precedent | none | **`config/sources.yaml`** — one entry per search execution (D011), paired with the append-only `data/raw/SHA256SUMS` (D005, D006) |
| Write path | simplest | must be transactional |
| Failure blast radius | one sample | the index, so it must be validated |

Architecture 2 is chosen because the repository already uses exactly this pattern for search
executions, and that pattern encodes rules this project has already paid for: an entry is never
repurposed, filenames are never reused, a figure always travels with its source, and a checksum is
authoritative only after the reviewer approves it. Reusing the pattern inherits those properties.

Architecture 1's failure mode is disqualifying for a provenance artefact: a sample that exists on
disk but is not discovered is indistinguishable from a sample that does not exist. Architecture 2
makes that state an error instead.

---

## 2. Proposed file structure — illustrative

```
config/verification_samples.yaml          # the index                              (new)
data/screening/
  verification_sample.csv                 # vs1 — EXISTING; never renamed or edited
  verification_sample_vs2.csv             # an extension sample, if ever authorised
  VERIFICATION_SHA256SUMS                 # append-only, mirrors data/raw/SHA256SUMS
results/validation/
  screening_verification_vs1.md           # one report per sample; never merged in place
  screening_verification_vs2.md
```

The existing `verification_sample.csv` **keeps its name**. It is a protected artefact with a
registered checksum, and filenames are never reused. The index records it at its current path as
`vs1`; new samples take new names.

---

## 3. Manifest schema — illustrative

```yaml
# config/verification_samples.yaml — ILLUSTRATIVE, NOT CREATED.
# One entry per DRAW. An entry is never repurposed, and never edited once answering has begun.
samples:
  - sample_id: vs1
    role: original                      # original | extension
    status: drawn_unanswered            # drawn_unanswered | drawn_answered | scored
    sheet_file: data/screening/verification_sample.csv
    sheet_sha256: 6b4f734375f94a513404a8275f0003c9ddbdffae92b82ede264f2450bc57e29a

    population_file: data/screening/screening_ta.csv
    population_n: 194
    sample_size: 40
    sampling_rule: simple_random_without_replacement
    sampling_rule_version: v1

    seed: 1496879658
    seed_derivation: file_bytes_crlf_v1                   # the historical rule
    source_digest: 5938922a529a7f7318824f4216b4b9ab05b920a14def7c15e72c15ea2a6076eb
    source_digest_rule: file_bytes_crlf_v1
    frame_digest: 37cc07e64054ef938229fbecec5f7da70f4c9ae419aae9f79b04d642574209ad
    frame_digest_rule: ordered_report_ids_v1              # D020, recorded retrospectively

    draw_date: null
    draw_date_source: >-
      UNVERIFIED. No run log was captured and the sheet carries no date column. The draw
      necessarily preceded commit c704582 (2026-11-01 17:48 +0530), which is an UPPER BOUND
      and not evidence of the draw date. Mirrors the count_source convention in
      config/sources.yaml and the unresolved search_date of pubmed_v1 (P009).

    report_ids: [ ... the 40 ordered report_ids, verbatim from the sheet ... ]

    triggered_by: null                  # vs1 is the original
    triggered_by_result: null
    triggered_by_verdict: null
    result_file: null                   # no scoring has occurred
    agreement: null                     # never pre-filled
```

An extension entry would differ only in its linkage and its provenance rule:

```yaml
  - sample_id: vs2
    role: extension
    status: drawn_unanswered
    seed_derivation: ordered_report_ids_v1        # D020 governs any later draw
    frame_digest_rule: ordered_report_ids_v1
    triggered_by: vs1
    triggered_by_result: results/validation/screening_verification_vs1.md
    triggered_by_verdict: EXTEND                  # the only verdict that permits an extension
    # ... all other fields as above, with vs2's own values
```

### Field rationale

`seed_derivation` and `frame_digest_rule` are stored **per sample**, not globally, because the two
rules coexist: `vs1` was drawn under the historical rule and any later sample under D020's. A
global setting would silently relabel history.

`report_ids` is stored in the index as well as the sheet so that a sheet which is edited, truncated
or re-sorted can be detected against an independent record of what was drawn.

`triggered_by_verdict` is stored so that the authorising result is named rather than assumed. Code
reads it; it does not write it on its own initiative.

---

## 4. Invariants the validator must enforce — fail-closed

1. `sample_id` unique; exactly one entry with `role: original`.
2. An entry is never edited once `status` has left `drawn_unanswered`. Corrections are new entries.
3. `sheet_sha256` must match the file on disk, or every command touching that sample refuses.
4. Every sheet on disk appears in the index, and every index entry has its sheet. Drift is an
   **error**, not a warning.
5. `report_ids` must equal the sheet's rows exactly, in order.
6. An `extension` entry requires `triggered_by` naming a sample whose `status` is `scored` and
   whose recorded verdict is `EXTEND`. **Code must never create an extension on any other basis,
   and never on its own initiative.**
7. `--draw` continues to refuse to overwrite an existing sheet, and additionally refuses to create
   an extension unless invariant 6 is satisfied.
8. `--score <sample_id>` scores that sample against **its own** recorded provenance. An unqualified
   `--score` refuses once more than one sample exists, rather than guessing.
9. Results are reported **per sample**, in per-sample files. No pooling occurs unless the protocol
   explicitly provides for it, and any combined figure is labelled a combined-set analysis — never
   presented as a third independent result.
10. The existing completeness gate is unchanged: any blank or whitespace-only response in a sample
    refuses scoring for that sample.

---

## 5. Migration and backward compatibility

A one-time **registration**, with no artefact changes:

- Create the index with a single `vs1` entry pointing at the existing path. Do not rename,
  redraw, re-hash or reorder anything.
- `draw_date` stays `null` with its `draw_date_source` note, exactly as `pubmed_v1`'s `search_date`
  remains unknown under P009.
- While `vs1` is the only entry, current single-sample behaviour continues to work unchanged.
  `--score` with no argument keeps scoring `vs1`, and begins refusing the moment a second entry
  exists.
- `DRAW_SHA`, `DRAW_SEED`, `DRAW_SEED_DERIVATION`, `DRAW_FRAME_DIGEST` and `FRAME_DIGEST_RULE`
  remain as committed. The index records the same values; it does not replace them.

---

## 6. Tests and failure cases required

| # | Case | Expected |
|---|---|---|
| 1 | duplicate `sample_id` | refuse |
| 2 | two entries with `role: original` | refuse |
| 3 | sheet on disk absent from the index | refuse |
| 4 | index entry with no sheet on disk | refuse |
| 5 | `sheet_sha256` mismatch | refuse every command touching that sample |
| 6 | `report_ids` disagree with the sheet | refuse |
| 7 | edit to an entry past `drawn_unanswered` | refuse |
| 8 | extension whose `triggered_by` is unscored, or scored with a verdict other than `EXTEND` | refuse |
| 9 | `--draw` over an existing sheet | refuse (existing behaviour preserved) |
| 10 | unqualified `--score` with two samples present | refuse |
| 11 | `--score vs2` | uses vs2's seed, digests and rule; never vs1's |
| 12 | each report | names its own `sample_id`, seed, digests and rule |
| 13 | two samples scored | two separate agreement figures; no implicit pooling |
| 14 | blank or partial responses in any sample | refuse scoring for that sample |
| 15 | a second `EXTEND` on a combined set | **halt with an explicit "protocol undefined" refusal** |
| 16 | `vs1`'s recorded provenance after migration | byte-identical to the committed constants |

Case 15 matters most: where the protocol is silent, the code must stop rather than improvise.

---

## 7. Deferred — not decided here, and not to be decided by code

**Four** matters are deferred. None has an answer here, and none is assigned a decision ID: they
are open questions, not decisions. All four are pre-specification questions — deciding any of them
after an agreement figure is known would make it post-hoc — so each must be closed **before an
extension sample is drawn or evaluated**, not before this design is implemented.

### 7.1 Outcome and handling after a second EXTEND

**Status: UNRESOLVED / DEFERRED.**

*Why it matters.* The acceptance rule states that 90–94.9% agreement draws one further sample of
the same size and re-applies the rule to the combined set. It does not say what follows if the
combined set **again** falls in 90–94.9%. Left open, the rule either recurses without limit or
stops at a point nobody chose.

*What must be decided.* Whether a second EXTEND outcome draws a further sample, terminates in
ADOPT, terminates in RE-SCREEN, or is resolved some other way — and whether that answer is the same
as the first EXTEND's or different. Until it exists, the design requires an explicit
"protocol undefined" refusal (case 15); it must not improvise.

### 7.2 Extension sampling frame

**Status: UNRESOLVED / DEFERRED.**

*Why it matters.* "A second sample of the same size" does not state whether it is drawn from the
unsampled remainder (154 of 194 at title/abstract) or from the full frame with the first sample
excluded. This materially changes what an extension means statistically, and therefore what a
combined-set agreement figure measures.

*What must be decided.* Which population an extension draws from, and whether the first sample's
records are excluded, eligible again, or re-used. The manifest records `population_file` and
`population_n` per sample so that whichever is decided is recorded explicitly rather than inferred.

### 7.3 Whether, when and under what conditions sample results may be pooled

**Status: UNRESOLVED / DEFERRED.**

*Why it matters.* The acceptance rule's phrase "the combined set" implies pooling on the EXTEND
path, but the conditions are unstated: whether pooling is permitted **only** on that path, whether
per-sample figures must also be reported alongside any pooled one, and whether a pooled figure may
be computed for any other purpose. Pooling two samples drawn under different rules, or from
different frames, would produce a figure whose meaning is unclear.

*What must be decided.* The exact circumstances in which per-sample agreement figures may be
combined, what must be reported alongside a combined figure, and whether pooling is forbidden
outside the EXTEND path. Until then, invariant 9 and case 13 require results to be reported **per
sample**, with no implicit pooling, and any combined figure to be labelled a combined-set analysis
rather than presented as an independent third result.

### 7.4 Maximum permitted number of extension samples

**Status: UNRESOLVED / DEFERRED.**

*Why it matters.* Nothing currently caps the number of extensions. Without a cap, repeated
extension is a form of optional stopping: each additional sample is another opportunity for the
agreement rate to cross a threshold, which inflates the chance of reaching ADOPT by sampling alone.

*What must be decided.* Whether a cap exists, what it is, and what happens when it is reached.
This is bound up with 7.1 and should be settled with it.

### What the deferrals do **not** block

**Scoring the original sample is not blocked by any of the above.** Once `vs1`'s own 120 response
cells are complete and the existing scoring requirements are satisfied — every sampled record
answered, the responses internally valid — `vs1` can be scored and its verdict reported on its own
terms. The four questions concern what happens *after* a verdict of EXTEND, so they bear on
whether and how an extension proceeds, not on whether the first sample may be evaluated.

Only one of the four becomes blocking at that point, and only in one case: if `vs1` scores in the
90–94.9% band, then 7.1, 7.2 and 7.4 must be settled before any extension is drawn. An ADOPT or
RE-SCREEN verdict requires none of them.

## 8. What this design does not touch

- Acceptance thresholds: ≥95% ADOPT, 90–94.9% EXTEND, <90% RE-SCREEN. Unchanged.
- The asymmetry rule (an exclude→include discrepancy sweeps that reason code). Unchanged.
- D001–D019. Unchanged; D016–D019 remain **Proposed**.
- The existing sample, its 40 report IDs, its seed, its digests, and its 0/120 response state.
- Whether any screening decision has been independently adjudicated. It has not: all 194
  title/abstract decisions remain `adopted_from_suggestion`.
- Whether verification has started. It has not.

Automated agreement is never independent adjudication. The blinded exercise compares one
reviewer's blinded judgement against an automated suggestion set; it is not duplicate screening,
and a high agreement figure would not convert adopted suggestions into adjudicated decisions.
