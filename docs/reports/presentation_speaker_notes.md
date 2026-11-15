# Presentation speaker notes

**Deck:** `Research_Project_Presentation.pptx` — 15 slides
**Project:** Is smoked tobacco use associated with an increased risk of squamous cell carcinoma of
the oral cavity?
**Date:** 13 November 2026

---

## How to frame the whole talk

The single most important thing to establish in your first thirty seconds, and to hold for the rest
of the talk, is this:

> **This project built and validated a research instrument and specified the protocol it enforces.
> It has not yet produced a synthesis. That is a stage of the work, not a failure of it.**

Say it early, plainly, once. If you say it apologetically it will sound like an excuse; if you state
it as a fact about where the work stands, it is simply accurate. Everything else follows from it.

The zeros in your results are not an embarrassment to be hurried past. They are the main evidence
that the system works. A pipeline that would happily print a pooled odds ratio from an unscreened
record set would be a worse piece of engineering, and you should be prepared to say so directly.

**Vocabulary discipline.** Three word choices will carry most of the credibility:

- Say **"provisional classification"**, never "screening decision", for the 194.
- Say **"counts-only interrogation"**, never "search", for the 8,190 and 5,008 figures.
- Say **"not yet done"**, never "not applicable", for the empty stages.

If you slip and say "we screened 194 records", correct yourself immediately. An examiner who catches
the distinction before you do will press hard on it; an examiner who hears you police it yourself
will usually stop probing.

---

## Slide 1 — Title and research question

**What is on it.** Title, the research question, your name, the date, and a status line.

**What to say.** "The question is whether smoked tobacco use is associated with an increased risk of
squamous cell carcinoma of the oral cavity. What I'm presenting is the pipeline and protocol built
to answer it rigorously. The review itself is not complete, and I'll be precise throughout about
what exists and what doesn't."

**Why the status line is on the title slide.** Because the honest framing should not arrive as a
concession on slide 14. Putting it first means every later slide is read correctly.

**Term to be ready for — "systematic review":** a review that uses a prespecified protocol and an
explicit, reproducible search to identify all studies meeting stated criteria, as distinct from a
narrative review where selection is at the author's discretion.

---

## Slide 2 — Background and motivation

**What is on it.** The disease and exposure background, and the methodological gap.

**What to say.** Spend about half your time on the second half of the slide. The clinical background
is necessary context; the methodological gap is your contribution.

**The key point, in your own words.** "If a screening worksheet records 194 decisions but not how
they were made, a reader cannot tell whether a human read 194 abstracts or accepted 194 machine
suggestions in one action. Those are completely different bodies of evidence and they look
identical in the file. That gap is what this project closes."

**Why oral cavity ≠ oropharynx matters.** Oropharyngeal cancer has a substantial HPV-associated
component with a different risk-factor profile. Pooling the two dilutes a tobacco association. This
is why the protocol treats subsite as a substantive eligibility question, and it explains the
`outcome_not_separable` exclusion code later.

**Terms.** *Bidi* — a small hand-rolled cigarette common in South Asia. *Reverse smoking* — holding
the lit end inside the mouth, practised in parts of South India, associated with palatal lesions.

---

## Slide 3 — Research objectives

**What is on it.** Eight infrastructure objectives in green; the scientific objective in red.

**What to say.** "Eight of nine objectives are met. The ninth — producing a pooled estimate — is
not, and it is blocked on two things: decisions only the reviewer can make, and reviewer work that
cannot be automated."

**Do not soften this slide.** The colour contrast is deliberate. An examiner who sees you present
the failure as plainly as the successes will trust the successes more.

**If asked "so is the project incomplete?"** — "The engineering objectives are complete and
validated. The scientific objective is not, and I can tell you exactly what remains and in what
order, which is slide 15."

---

## Slide 4 — Eligibility criteria (PECO)

**What is on it.** The PECO elements with settled/open status, and the controlled vocabulary.

**Term — PECO.** Population, Exposure, Comparator, Outcome. The observational analogue of PICO,
where "Intervention" becomes "Exposure" because nobody assigns smoking.

**What to say.** "The comparator is open, and I want to be clear why that matters rather than hide
it. Some studies compare against never-smokers and some against 'non-smokers', which may include
former smokers. Mixing those biases a pooled estimate toward the null. Until that's decided, the
protocol records the comparator verbatim rather than forcing a classification."

**The 90% threshold.** D008 requires SCC to be histologically confirmed or a stated majority of at
least 90% of cases. The reason for a threshold rather than "mostly SCC" is that a vague criterion
cannot be applied consistently by a single reviewer across 85 papers.

**Why four codes are full-text only.** `outcome_not_separable`, `no_reference_group`,
`no_usable_data` and `duplicate_publication` cannot be judged from an abstract without guessing.
Restricting them in the vocabulary itself means the tool prevents a premature judgement rather than
relying on the reviewer to remember.

**Likely question — "why are ten scope questions still open?"** "Because they are genuinely
difficult and deciding them casually would be worse than deciding them late. Whether the soft palate
counts as oral cavity differs between anatomical and staging conventions. One of these affects 14 of
the 85 reports I'd be assessing, so getting it wrong changes the evidence base materially."

---

## Slide 5 — Literature identification and search strategy

**What is on it.** The registered export, the lost export, two query defects, and the corrected
strategy.

**This is your most exposed slide. Present the weaknesses yourself.**

**What to say.** "One database has been searched, and the query used is narrower than the protocol
it is supposed to serve. I found this by auditing my own search rather than by assuming it was fine.
Two specific defects: 68 of the 194 records use the phrase 'oral cancer', which the query doesn't
require — they were retrieved only incidentally. And 98 of 194 matched the study-design part of the
query only through the single word 'cohort', which also catches prognostic studies of people who
already have the disease."

**On the lost export.** "The original 138-record export is lost. It's recorded as lost. I did not
substitute the re-run for it, because that would mean reporting a search I can't evidence. There's
also a residual discrepancy of about nine records between the documented 138 and what the re-run
implies, and it's recorded as unexplained rather than reconciled away."

**On the 8,190 / 5,008 figures — be careful.** "Those are counts-only interrogations to validate
query syntax and estimate volume. Nothing was retrieved, exported or screened, there's no registry
entry, and they are not search yields. They tell me roughly how much work the corrected search
implies, nothing more."

**Likely question — "why only PubMed?"** "Because that's the only access I can evidence. Embase
isn't listed among my institution's databases; Scopus and Web of Science are advertised but I
haven't verified I can actually run and export a search. Rather than list databases I might have, I
recorded what's verified and flagged the rest as a decision pending access checks."

---

## Slide 6 — Pipeline architecture

**What is on it.** Fifteen stages, colour-coded green (run on real data), amber (built and tested,
never run) and grey (not implemented).

**What to say.** "The colours are generated from the repository when the figure is built, not drawn
by hand, so the diagram can't drift from what the code does. Five stages are green, eight amber, two
grey."

**The three gates — your strongest engineering point.** "Three stages refuse to run. Extraction
refuses without an included study. Synthesis refuses without extracted estimates. The analysis CLI
refuses any row marked synthetic. Each exits with an error rather than producing an empty table. The
purpose is that 'we found no association' and 'we haven't looked' can never be confused in the
output."

**Likely question — "why is risk-of-bias grey rather than amber?"** "Because the instrument hasn't
been chosen. I deliberately didn't implement one. If I'd picked Newcastle–Ottawa or ROBINS-E to make
the diagram look complete, I'd have made a methodological decision by writing code instead of by
deciding it, which is exactly the failure mode the project is about."

---

## Slide 7 — Deduplication and record management

**What is on it.** The identifier hierarchy, the no-auto-merge rule, and the result.

**What to say.** "Matching goes normalised DOI, then PMID, then an exact title-author-year
fingerprint. Titles that are similar but not identical are flagged for review and never merged
automatically, because an automatic merge on a near-match can silently delete a distinct study."

**Get ahead of the obvious objection.** "The result was zero duplicates, which is exactly what you'd
expect from a single-database search. That's not evidence the stage works — the evidence is 63 tests
exercising the matching rules on constructed cases."

**Term — the D004 chain.** `record_id` is one database row; `report_id` is one unique publication
after deduplication; `study_id` is one unique study population, which a human assigns at full text
because several papers can report one population; `estimate_id` is one effect estimate. The unit of
analysis is the study, and a study may appear at most once in any analysis — that is what prevents
double-counting participants.

---

## Slide 8 — Screening and verification architecture

**This is the intellectual core of the project. Give it the most time.**

**What to say.** "Every decision carries a basis field: either adopted from an automated suggestion,
or independently adjudicated. These are never added together. A row counts as adjudicated only when
five fields are present, including a separate adjudicated date — so you can't convert a bulk-adopted
row into a formal one just by flipping a flag, because the new act has to be dated."

**The split PRISMA flow.** "A conventional flow diagram would say 194 screened and 85 sought. Those
numbers would imply human screening that hasn't happened. So the flow is split: the formal flow
counts only adjudicated decisions and currently reads zero; the 194 appear in a provisional section
explicitly outside the flow."

**The verification sample.** "Forty of the 194 reports, about 21%, drawn with a seeded, reproducible
procedure, with the recorded decision hidden. When I answer those 120 cells blind and compare, I get
an agreement rate against the automated suggestions. Thresholds were set in advance: 95% or above
adopt, 90 to 95 extend the sample, below 90 re-screen everything. Right now zero of 120 are done, so
there is no agreement rate and no kappa."

**Likely question — "isn't using automated screening a shortcut?"** "It would be if I reported the
output as screening. I don't. It's recorded as a suggestion, it's counted separately, the formal
flow reads zero, and the validator refuses to pass the stage as final while any row is
bulk-adopted. The tool proposes; the reviewer decides; the data records which happened."

**Likely question — "why not just adjudicate all 194 now?"** "It's roughly a day of careful work and
it has to be done properly, and several eligibility criteria it depends on are still open — notably
the subsite definition, which affects 14 of the 85. Adjudicating against criteria I'm about to
change would mean doing it twice."

---

## Slide 9 — Data flow and provenance

**What is on it.** Four custody classes and the files in each.

**What to say.** "Raw data is immutable and checksum-gated. Generated data can be deleted and
rebuilt. Human research records — the screening worksheets — are tracked precisely because they
can't be regenerated from anything. Outputs come from all three and are never hand-edited."

**Point at the separation.** "The suggestion file and the decision file are separate files on
purpose. An automated suggestion is never written into a decision field. That's a storage decision
enforcing a methodological one."

**Point at the grey box.** "`data/extraction/` doesn't exist. Not empty — absent. It gets created
when a study is included, and none has been."

---

## Slide 10 — Statistical analysis architecture

**What is on it.** What is implemented, and what is declared missing.

**What to say.** "Everything here is implemented and tested and none of it has been run on research
data, because there are no estimates to run it on."

**Explain inverse-variance weighting in one sentence.** "Each study contributes in proportion to its
precision — the reciprocal of its variance — so larger, more precise studies carry more weight."

**Fixed vs random effects.** "A fixed-effect model assumes one true effect common to all studies. A
random-effects model assumes the true effect varies between them and estimates that variance, τ².
For observational studies differing in population, design and adjustment, random effects is the
defensible default, and that's what's anticipated."

**I² in one sentence.** "The percentage of total variation across studies due to real heterogeneity
rather than chance. Roughly 25, 50 and 75% are conventionally called low, moderate and substantial —
but they're descriptive bands, not decision thresholds."

**The declared limitations are a strength, not a weakness.** "REML is implemented but has no
external validation — it's tested for self-consistency and limiting behaviour only. That proves it
solves the equation it encodes, not that the equation is right. Any REML estimate has to be
cross-checked against an established implementation before publication. There's also no
Hartung–Knapp interval, no Mantel–Haenszel, no meta-regression. I'd rather state those than have
someone find them."

**Likely question — "will you assess publication bias?"** "Egger's test and funnel plots are
implemented, and the code refuses to run Egger below ten studies because it's uninformative there.
If fewer than ten studies end up included, no test runs at all. So I'm not promising a publication
bias assessment — I'm promising that if one isn't meaningful, none will be reported."

---

## Slide 11 — Technology stack

**What is on it.** Six layers, and an explicit statement of what is absent.

**What to say.** "Python 3.14 with a deliberately small dependency set: PyYAML for configuration,
pytest for tests, SciPy for the distributions and regression, Matplotlib for figures and PDF
typesetting. That's it."

**The pandas point — make it, because it is unusual and defensible.** "Pandas is not used anywhere.
All tabular work uses the standard-library csv module. For a pipeline this size pandas would add
weight without adding capability, and csv preserves values exactly as written, which matters when
the whole project is about not silently transforming data. I'm mentioning it because claiming tools
you don't use is itself a reproducibility failure."

**On DOCX and PPTX.** "No document library was available and installing one wasn't authorised, so
the Word and PowerPoint files are written directly as OOXML through the zipfile module — those
formats are ZIP containers of XML. It's a constraint I worked within rather than around."

---

## Slide 12 — Numerical results

**What is on it.** The attrition chart, the completion chart, and the one-line chain.

**What to say.** "194 records identified, 194 unique after deduplication with zero duplicates, 109
provisionally classified for exclusion and 85 for retrieval, zero formally screened, zero included."

**Then the interpretation, which is the part that matters.** "The right-hand panel is the honest
summary of the project: one bar is complete, and it's the bar that records machine output. Every bar
representing human judgement is at zero."

**The exclusion reasons.** If asked: 63 wrong outcome, 33 wrong design, 10 reviews or meta-analyses,
2 not English, 1 wrong population. Add immediately: "Those are suggested reason codes, not reviewer
judgements. I would not put that table in a PRISMA diagram as it stands."

**Why not-English appears at all.** "Because the search was deliberately run unfiltered. The Humans
filter in PubMed works on an index term that 42 of these records don't have yet — they're the most
recent ones. Filtering would have silently dropped them. Excluding at screening with a recorded
reason is auditable; a database filter isn't."

---

## Slide 13 — Validation and reproducibility

**What is on it.** Tests, protected values, determinism, cross-format validation.

**What to say.** "599 tests pass and one is skipped by design — the skip is the raw-source test for
the lost export, and a test demanding a file I've recorded as missing would be a false failure."

**On determinism.** "Three generators were checked by rebuilding to a clean directory and comparing
bytes: the PRISMA figure, the extraction workbook and the report figures are all byte-identical on
rebuild. So anyone with the repository gets exactly these artefacts."

**On regression tests — a good, concrete story.** "Some tests exist because I found a specific
defect. The PRISMA banner once said '0 of 194 reports carry a decision, but 194 were adopted' — a
self-contradiction, because the code put the formal count into a sentence about recorded
classifications. It reached an embedded figure. Two tests now assert the corrected wording so it
can't come back."

**Likely question — "how do you know the DOCX and PDF match?"** "An independent harness opens the
produced files rather than trusting the build log — it parses the Word XML and decompresses the PDF
content streams. Nineteen of nineteen headings, 164 of 164 table cells, 109 of 109 numeric tokens
and 80 of 80 sampled sentences appear in both."

---

## Slide 14 — Limitations

**Do not rush this slide. Confidence here is what sells the whole project.**

**What to say.** "I'll state these plainly, because the value of the work depends on stating them.
One database. A query narrower than its own criteria. Zero of 194 independently adjudicated. Zero
full texts, zero studies included, zero estimates, zero risk-of-bias assessments, no pooled
analysis. The verification sample is drawn and unanswered."

**The sharpest point to make yourself, before anyone makes it for you.** "The automated suggestions
have never been validated on this corpus, and the error profile is probably asymmetric: a false
inclusion gets caught at full text, but a false exclusion removes a study permanently and
invisibly. That's exactly why the verification sample exists and why it has to be answered before
the suggestions are relied on."

---

## Slide 15 — Future work and conclusion

**What to say.** "The work splits into decisions and labour. The decisions are mine as researcher:
databases, the design block, ten scope questions, the appraisal instrument, the comparator and
contrast. The labour is the reviewer's and cannot be generated: 194 adjudications, 120 verification
cells, 85 full texts, extraction, appraisal. Only then does synthesis become legitimate."

**Closing line — say it as a claim, not a hope.** "The integrity properties usually asserted in a
methods section — that raw data wasn't altered, that a suggestion wasn't mistaken for a judgement,
that no result was computed before the evidence existed — have been made properties of a system
instead. The pipeline refuses to produce an estimate it can't justify. The clearest evidence it
works is the set of zeros I showed you."

---

# Anticipated questions and defensible answers

**"Isn't this just software? Where is the research?"**
The research output is a specified protocol and a validated instrument. Eighteen adopted
methodological decisions, each recorded with rationale, consequences and scope; an eligibility
framework; a prespecified analysis plan with its limitations declared. The synthesis is the next
stage, and the protocol work has to precede it or the synthesis isn't systematic.

**"Why haven't you just run the meta-analysis to show it works?"**
Because the analysis module refuses to run without extracted estimates, and that refusal is a
feature I'd have to disable. Any numbers produced that way would be fabricated. The module's
mathematics is verified against hand-worked arithmetic and published formulas in 48 tests — that is
how it is shown to work, without inventing data.

**"How do you know the automated suggestions are any good?"**
I don't yet, and the project says so. The instrument for finding out is the blinded verification
sample — 40 reports, 120 cells, thresholds fixed in advance. Until it's answered there is no
agreement rate and no kappa, and the formal flow correctly reads zero.

**"Why is PubMed alone not enough?"**
Because the exposure definition includes bidi and reverse smoking, and that literature is
concentrated in South Asian journals with incomplete MEDLINE coverage. A PubMed-only search is least
sensitive exactly where this review is most distinctive, so the loss is systematic rather than
random, which can bias an estimate rather than just widen it.

**"What's the single biggest threat to this review?"**
The executed query. It's narrower than the eligibility criteria it serves — it demands a literal
phrase that most aetiological papers don't use, omits the non-cigarette product terms, and uses no
controlled vocabulary. Any synthesis built on this record set alone would rest on a search that
doesn't match its own protocol. That's why the corrected strategy exists and why it has to be run
before any result is reported.

**"Could you have finished the review in the time available?"**
Not honestly. The reviewer work alone — 194 adjudications, 120 verification cells, 85 full texts,
then extraction and appraisal — is weeks, and several eligibility criteria it depends on are still
open. I'd rather present a complete instrument and an honest zero than an incomplete review with a
number attached to it.

**"What would you do differently?"**
Audit the search before screening rather than after. I built the screening architecture, ran the
provisional pass, and only then audited the query and found it narrower than the protocol. The
sequence meant provisional work was done against a record set I later found inadequate.

**"Is any of this reproducible by someone else?"**
Yes, and it's checked rather than claimed. Pinned dependencies, deterministic generation verified by
rebuilding to clean paths and comparing bytes, checksum-gated raw data, and 599 passing tests. The
one honest exception is the planned Google Scholar search, which is bounded and reportable but not
repeatable, because its relevance ranking is unstable — and the protocol says so.

**"Why record a decision log at all?"**
Because a methods section written at the end reconstructs reasoning from memory. A dated log records
what was decided, when, why, and explicitly what the decision does not cover. It also made the
PROSPERO deviation visible instead of invisible.

**"What is D022 and why isn't it D021?"**
D022 is the grey-literature decision. D021 was already used across three project documents for the
blinded-verification acceptance methodology, which is drafted but not registered. Taking D021 would
have silently renumbered an existing decision, so the next free identifier was used.

---

# Numbers you should be able to quote without notes

| Quantity | Value |
|---|---|
| Records identified / unique reports | 194 / 194 |
| Duplicates removed | 0 |
| Provisional exclusions / carried forward | 109 / 85 |
| **Independently adjudicated** | **0 of 194** |
| Verification sample / cells completed | 40 reports (20.6%) / **0 of 120** |
| Full texts retrieved / studies included | 0 / **0** |
| Extraction schema | 34 study + 47 estimate + 12 risk-of-bias = **93 fields**, 0 rows |
| Tests | **615 passed, 1 skipped** (616 collected) |
| Code / test lines | 7,292 / 5,957 |
| Adopted decisions / proposed / open questions | 18 / 4 / 22 |
| Corrected strategy counts (12 Nov 2026) | 8,190 without design block; 5,008 with |
| Exclusion reasons | 63 wrong outcome, 33 wrong design, 10 review, 2 not English, 1 population |

**If you are unsure of a number, say so and offer to check.** Everything here is recomputed from the
repository, and a wrong figure stated confidently does more damage than an admitted uncertainty.
