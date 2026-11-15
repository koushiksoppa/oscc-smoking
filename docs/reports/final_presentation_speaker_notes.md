# Final presentation — speaker notes

**Deck:** `Final_Research_Project_Presentation.pptx` — 15 slides
**Project:** Is smoked tobacco use associated with an increased risk of squamous cell carcinoma of
the oral cavity?
**Date:** 14 November 2026

---

## Framing the whole talk

Establish this in your first thirty seconds and hold it for the rest:

> **This reporting period built and validated a research instrument and specified the protocol it
> enforces. It has not yet produced a synthesis. That is a stage of the work, not a failure of it.**

Say it once, plainly, early. Said apologetically it sounds like an excuse; said as a fact about where
the work stands, it is simply accurate — and it frames every later slide correctly.

**The zeros are your argument, not your embarrassment.** A pipeline that would happily print a pooled
odds ratio from an unscreened record set would be worse engineering. Be ready to say that directly.

**Three words carry most of your credibility:**

- Say **"provisional classification"**, never "screening decision", for the 194.
- Say **"counts-only interrogation"**, never "search", for 8,190 / 5,008 / 8,195.
- Say **"not yet done"**, never "not applicable", for the empty stages.

If you slip, correct yourself immediately. An examiner who catches the distinction before you do will
press hard; one who hears you police it yourself usually stops probing.

---

## Slide 1 — Title and research question

**Say:** "The question is whether smoked tobacco use is associated with increased risk of squamous
cell carcinoma of the oral cavity. What I'm presenting is an interim project: the pipeline and
protocol built to answer it rigorously, plus preliminary record-processing results. The review itself
is not complete, and I'll be precise throughout about what exists and what doesn't."

**Why the status line sits on the title slide.** So the honest framing arrives first rather than as a
concession on slide 13.

**Term to have ready — "systematic review":** a review using a prespecified protocol and an explicit,
reproducible search to identify all studies meeting stated criteria, as distinct from a narrative
review where selection is at the author's discretion.

---

## Slide 2 — Background and rationale

Spend about half your time on the second half of the slide. The clinical background is context; the
methodological gap is your contribution.

**The key sentence, in your own words:** "If a screening worksheet records 194 decisions but not how
they were made, a reader cannot tell whether a human read 194 abstracts or accepted 194 machine
suggestions in one action. Those are completely different bodies of evidence and they look identical
in the file. That gap is what this project closes."

**Why oral cavity ≠ oropharynx.** Oropharyngeal cancer has a substantial HPV-associated component
with a different risk-factor profile, so pooling the two dilutes a tobacco association. This is why
subsite is treated as a substantive eligibility question and why `outcome_not_separable` exists as an
exclusion code.

**Terms.** *Bidi* — a small hand-rolled cigarette common in South Asia. *Reverse smoking* — holding
the lit end inside the mouth, practised in parts of South India, associated with palatal lesions.

---

## Slide 3 — Research objectives

**Say:** "Eight of nine objectives are met. The ninth — producing a pooled estimate — is not, and
it's blocked on two things: decisions only the reviewer can make, and reviewer work that cannot be
automated."

**Do not soften this slide.** The colour contrast is deliberate. An examiner who sees you present the
failure as plainly as the successes will trust the successes more.

**If asked "so the project is incomplete?"** — "The engineering objectives are complete and
validated. The scientific objective is not, and I can tell you exactly what remains and in what
order."

---

## Slide 4 — Systematic review methodology

**Say:** "Four reporting standards: PRISMA 2020 for the review, PRISMA-S for the search, MOOSE for
observational specifics, and the Cochrane Handbook for synthesis. The protocol was committed on 29
October and the screening records on 1 November, so it was genuinely specified in advance — that's
checkable in the Git history, not just asserted."

**On the register.** "Nineteen adopted decisions, each recorded with its rationale, its consequences
and — unusually — an explicit statement of what it does *not* cover. That last part is what stops a
decision quietly expanding later."

**Volunteer the deviation.** "We are not prospectively registered, and the provisional pass preceded
registration. That's a protocol deviation and it's reported as one rather than omitted."

**Likely question — "why are 22 questions still open?"** "Because deciding them casually would be
worse than deciding them late. Whether the soft palate counts as oral cavity differs between
anatomical and staging conventions. One of these affects 14 of the 85 reports I'd be assessing."

---

## Slide 5 — Search strategy development

**This is your most exposed slide. Present the weaknesses yourself.**

**Say:** "One database has been searched, and the query used is narrower than the protocol it's
supposed to serve. I found that by auditing my own search, not by assuming it was fine. Two specific
defects: 68 of the 194 records use the phrase 'oral cancer', which the query doesn't require — they
were retrieved only incidentally. And 98 of 194 matched the study-design part only through the single
word 'cohort', which also catches prognostic studies of people who already have the disease."

**On the corrected strategy.** "Two decisions fixed it. D023 removes the study-design block
entirely — a design filter's cost is invisible, because the records it removes never appear for
inspection. D024 removes one dead phrase: per-line validation of all 88 lines found exactly one
returning zero, with PubMed reporting QuotedPhraseNotFound. Removing it changes retrieval by zero
records, because it matched nothing."

**On the big numbers — be careful.** "8,190, 5,008 and 8,195 are counts read back from a query.
Nothing was retrieved, exported or screened; there's no registry entry. They tell me roughly how much
work the corrected search implies, and nothing more. They are not search yields."

**Likely question — "why only PubMed?"** "Because that's the only access I can evidence. Embase isn't
listed among my institution's databases; Scopus and Web of Science are advertised but I haven't
verified I can actually run and export a search. I recorded what's verified and flagged the rest."

---

## Slide 6 — Literature acquisition

**Say:** "One registered execution: 194 records, with a SHA-256 checksum recorded at registration. Any
later alteration of that file is detectable, and the pipeline re-verifies before every stage that
reads it."

**On the unfiltered retrieval.** "We deliberately didn't apply PubMed's Humans and English filters.
The Humans filter works on an index term that 42 of these 194 records don't have yet — they're the
most recent ones. Filtering would have silently dropped them. Excluding at screening with a recorded
reason code is auditable; a database filter isn't."

**On the lost export.** "The original 138-record export is lost. It's recorded as lost. I did not
substitute the re-run for it, because that would mean reporting a search I can't evidence."

---

## Slide 7 — Deduplication and screening results

**Say:** "Matching goes normalised DOI, then PMID, then an exact title-author-year fingerprint.
Titles that are similar but not identical are flagged for review and never merged automatically,
because an automatic merge on a near-match can silently delete a distinct study."

**Get ahead of the obvious objection.** "The result was zero duplicates, which is exactly what you'd
expect from a single-database search. That isn't evidence the stage works — the evidence is 63 tests
exercising the matching rules on constructed cases."

**On the 109/85 split — the crucial qualification.** "Those are the output of an automated procedure.
The reason codes are *suggested* codes, not reviewer judgements. I would not put that table in a
PRISMA diagram as it stands."

---

## Slide 8 — PRISMA progress

**Say:** "A conventional flow diagram would say 194 screened and 85 sought. Those numbers would imply
human screening that hasn't happened. So the flow is split: the formal flow counts only
independently adjudicated decisions and currently reads zero; the 194 appear in a provisional section
explicitly outside the flow."

**Point at the right-hand panel.** "This is the honest summary of the project. One bar is complete,
and it's the bar recording machine output. Every bar representing human judgement is at zero."

**On the verification sample.** "Forty of the 194 reports, about 21%, drawn with a seeded reproducible
procedure, with the recorded decision hidden. When those 120 cells are answered blind and compared, I
get an agreement rate against the automated suggestions. Thresholds were set in advance: 95% or above
adopt, 90–95 extend, below 90 re-screen. Right now zero of 120 are done, so there is no agreement
rate and no kappa."

---

## Slide 9 — Research pipeline architecture

**Say:** "Fifteen stages. The colours are generated from the repository when the figure is built, not
drawn by hand, so the diagram can't drift from what the code does."

**The three gates — your strongest engineering point.** "Three stages refuse to run. Extraction
refuses without an included study. Synthesis refuses without extracted estimates. The analysis CLI
refuses any row marked synthetic. Each exits with an error rather than producing an empty table. The
purpose is that 'we found no association' and 'we haven't looked' can never be confused in the
output."

**Likely question — "why is risk-of-bias grey rather than amber?"** "Because the instrument hasn't
been chosen. I deliberately didn't implement one. Picking Newcastle–Ottawa or ROBINS-E to make the
diagram look complete would be making a methodological decision by writing code instead of by
deciding it — exactly the failure mode this project is about."

---

## Slide 10 — Data extraction framework

**Say:** "Ninety-three documented fields — 34 study-level, 47 estimate-level, 12 structural
risk-of-bias fields — each traceable to a line of configuration. The workbook regenerates
deterministically: rebuild it to a clean directory and you get byte-identical files."

**On the zeros.** "`data/extraction/` doesn't exist. Not empty — absent. The directory is created when
a study is included, and none has been."

**On the risk-of-bias fields.** "Twelve structural columns — who assessed what, when, on what
evidence. The instrument's domain names and judgement categories are deliberately absent, because
they come from whichever instrument P023 settles on. There's a test asserting that no known
instrument is named anywhere in the workbook."

---

## Slide 11 — Meta-analysis methodology

**Say first:** "Everything here is implemented and tested, and none of it has been run on research
data, because there are no estimates to run it on."

**Explain inverse-variance weighting in one sentence.** "Each study contributes in proportion to its
precision — the reciprocal of its variance — so larger, more precise studies carry more weight."

**Fixed vs random effects.** "Fixed-effect assumes one true effect common to all studies.
Random-effects assumes the true effect varies and estimates that variance, τ². For observational
studies differing in population, design and adjustment, random effects is the defensible default."

**I² in one sentence.** "The percentage of total variation across studies due to real heterogeneity
rather than chance. The 25, 50 and 75% bands are descriptive, not decision thresholds."

**Zero cells — a good concrete example of the project's philosophy.** "A zero cell makes the log odds
ratio undefined. Most software quietly adds 0.5. We refuse the table and name the alternatives,
because a silent correction changes an estimate without any record of it."

**Multiple estimates from one study.** "A study reporting several estimates is normal — different
contrasts, different adjustment sets. They're correlated, so pooling them as independent studies
would understate the standard error. The code requires the reviewer to mark one per study and refuses
to guess, naming every candidate so nothing is dropped silently."

**Likely question — "will you assess publication bias?"** "Egger's test and funnel plots are
implemented, and the code refuses to run Egger below ten studies because it's uninformative there. If
fewer than ten studies are included, no test runs at all. So I'm not promising a publication-bias
assessment — I'm promising that if one isn't meaningful, none will be reported."

---

## Slide 12 — Software validation and technical results

**Say:** "670 tests pass and one is skipped by design — it's the raw-source test for the lost export,
and a test demanding a file I've recorded as missing would be a false failure."

**On determinism.** "Three generators were checked by rebuilding to a clean directory and comparing
bytes: the PRISMA figure, the extraction workbook and the report figures are byte-identical on
rebuild. Anyone with the repository gets exactly these artefacts."

**On regression tests — a good concrete story.** "Some tests exist because I found a specific defect.
A PRISMA banner once read '0 of 194 reports carry a decision, but 194 were adopted' — a
self-contradiction, because the code put the formal count into a sentence about recorded
classifications. It reached an embedded figure. Two tests now lock the corrected wording."

**The pandas point — make it, it's unusual and defensible.** "Pandas is not used anywhere. All tabular
work uses the standard-library csv module. For a pipeline this size pandas would add weight without
capability, and csv preserves values exactly as written, which matters when the whole project is
about not silently transforming data. I mention it because claiming tools you don't use is itself a
reproducibility failure."

---

## Slide 13 — Limitations and unresolved decisions

**Do not rush this slide. Confidence here sells the whole project.**

**Say:** "I'll state these plainly, because the value of the work depends on stating them. One
database. A query narrower than its own criteria. Zero of 194 adjudicated. Zero full texts, studies,
estimates, appraisals, pooled analyses. The verification sample is drawn and unanswered."

**The sharpest point — make it before anyone makes it for you.** "The automated suggestions have
never been validated on this corpus, and the error profile is probably asymmetric: a false inclusion
gets caught at full text, but a false exclusion removes a study permanently and invisibly. That's
exactly why the verification sample exists and why it must be answered before the suggestions are
relied on."

---

## Slide 14 — Current scientific contribution

**Say:** "This is what the period actually delivered." Walk the five green bullets briskly, then land
on the last one.

**The closing line of this slide, delivered slowly:** "A worksheet containing 194 completed rows
yields a formal screening count of zero. That number is uncomfortable and it is correct. A pipeline
that reported 194 screened on this data would be a worse instrument."

---

## Slide 15 — Conclusion and future work

**Say:** "The work splits into decisions and labour. The decisions are mine as researcher: databases,
scope, instrument, comparator and contrast, registration. The labour is the reviewer's and cannot be
generated: adjudication, 120 verification cells, 85 full texts, extraction, appraisal. Only then does
synthesis become legitimate."

**Flag the ordering point — it shows judgement.** "One recommendation I'd highlight: don't adjudicate
the current 194 yet. They come from the superseded query. Once the adopted strategy runs, the record
set changes substantially. Adjudicating now would mean doing that work twice."

**Closing line — say it as a claim, not a hope.** "The integrity properties usually asserted in a
methods section — that raw data wasn't altered, that a suggestion wasn't mistaken for a judgement,
that no result was computed before the evidence existed — have been made properties of a system
instead. The pipeline refuses to produce an estimate it can't justify. The clearest evidence it works
is the set of zeros I showed you."

---

# Anticipated questions and defensible answers

**"Isn't this just software? Where is the research?"**
The research output is a specified protocol and a validated instrument: nineteen adopted
methodological decisions each with rationale and scope, an eligibility framework, and a prespecified
analysis plan with its limitations declared. The synthesis is the next stage, and protocol work has
to precede it or the synthesis isn't systematic.

**"Why haven't you just run the meta-analysis to show it works?"**
Because the analysis module refuses without extracted estimates, and that refusal is a feature I'd
have to disable. Any numbers produced that way would be fabricated. The mathematics is verified
against hand-worked arithmetic and published formulas in 48 tests. That is how the machinery is
shown to work without inventing data.

**"How do you know the automated suggestions are any good?"**
I don't yet, and the project says so. The instrument for finding out is the blinded verification
sample — 40 reports, 120 cells, thresholds fixed in advance. Until it's answered there is no
agreement rate and no kappa, and the formal flow correctly reads zero.

**"Why is PubMed alone not enough?"**
Because the exposure definition includes bidi and reverse smoking, and that literature is
concentrated in South Asian journals with incomplete MEDLINE coverage. A PubMed-only search is least
sensitive exactly where this review is most distinctive, so the loss is systematic rather than
random — which can bias an estimate, not just widen it.

**"What's the single biggest threat to this review?"**
The executed query. It demands a literal phrase most aetiological papers don't use, omits the
non-cigarette product terms, and uses no controlled vocabulary. Any synthesis built on this record
set alone would rest on a search that doesn't match its own protocol. That's why the corrected
strategy exists and must be run before any result is reported.

**"Could you have finished the review in the time available?"**
Not honestly. The reviewer work alone — adjudication, 120 verification cells, 85 full texts, then
extraction and appraisal — is weeks, and several eligibility criteria it depends on are still open.
I'd rather present a complete instrument and an honest zero than an incomplete review with a number
attached.

**"What would you do differently?"**
Audit the search before screening rather than after. I built the screening architecture, ran the
provisional pass, and only then audited the query and found it narrower than the protocol. That
sequence meant provisional work was done against a record set I later found inadequate.

**"Is any of this reproducible by someone else?"**
Yes, and it's checked rather than claimed: pinned dependencies, deterministic generation verified by
rebuilding to clean paths and comparing bytes, checksum-gated raw data, and 669 passing tests. The
one honest exception is a planned Google Scholar search, which is bounded and reportable but not
repeatable because its relevance ranking is unstable — and the protocol says so.

**"Why keep a decision log at all?"**
Because a methods section written at the end reconstructs reasoning from memory. A dated log records
what was decided, when, why, and explicitly what the decision does not cover. It also made the
registration deviation visible instead of invisible.

---

# Numbers to quote without notes

| Quantity | Value |
|---|---|
| Records identified / unique reports | 194 / 194 |
| Duplicates removed | 0 |
| Provisional exclusions / carried forward | 109 / 85 |
| **Independently adjudicated** | **0 of 194** |
| Verification sample / cells completed | 40 reports (20.6%) / **0 of 120** |
| Full texts retrieved / studies included | 0 / **0** |
| Extraction schema | 34 + 47 + 12 = **93 fields**, 0 rows |
| Exclusion reasons | 63 wrong outcome, 33 wrong design, 10 review, 2 not English, 1 population |
| Records without MeSH indexing | 42 of 194 (21.6%) |
| Tests | **670 passed, 1 skipped, from 671 collected** |
| Adopted decisions / proposed / open | 19 / 4 / 22 |
| Corrected strategy counts (12 Nov 2026) | 8,190 without design block; 5,008 with — **not yields** |

**If you're unsure of a number, say so and offer to check.** Everything here is recomputed from the
repository, and a wrong figure stated confidently does more damage than an admitted uncertainty.
