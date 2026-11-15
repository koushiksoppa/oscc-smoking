# Risk of bias — instrument options and the decision required

**No risk-of-bias assessment has been started, and no instrument has been chosen.** This document
presents the options so the choice can be made deliberately. It adopts nothing.

The `risk_of_bias` table is already specified in
[`docs/data_dictionary/extraction_schema.md`](../data_dictionary/extraction_schema.md) and is
deliberately instrument-agnostic: `study_id`, `tool`, `tool_version`, `domain`, `judgement`,
`supporting_evidence`, `justification`, `information_missing`, `assessed_by`. Domain names come
from the chosen instrument and are not invented here, and no numeric score is computed unless the
instrument itself defines one. The structure can therefore be built the moment an instrument is
chosen; it cannot be built before, because the domains *are* the instrument.

## Why the choice cannot be made from the code

The eligible designs are **case–control and cohort** studies (eligibility criteria §1). Which
instrument suits them is a methodological judgement about this literature, not an engineering
question, and it has consequences that cannot be reversed cheaply: the domains determine what the
reviewer must look for in each paper, so changing instrument after assessment begins means
reassessing every study.

It also interacts with a decision that is still open. The statistical analysis plan lists
`risk-of-bias level` as a subgroup variable (§4) and a sensitivity analysis by risk of bias (§5).
Those are only executable if the instrument yields a study-level summary, which not all do.

## The options

### A. Newcastle–Ottawa Scale (NOS)

Separate forms for case–control and cohort studies; eight items in three groups (selection,
comparability, exposure/outcome), scored with stars to a maximum of nine.

**For.** By far the most widely used instrument for observational studies in this field, so a
reviewer and a reader will both recognise it. It has design-specific forms, which matches a review
admitting both designs. It yields a study-level total, so the SAP's risk-of-bias subgroup and
sensitivity analyses become executable directly.

**Against.** The star total is an unweighted sum, and the Cochrane Handbook advises against
collapsing risk of bias into a single score because it implies domains are interchangeable. Its
inter-rater reliability is documented as modest, and the comparability item requires the reviewer
to nominate the confounders that matter — which for this review means stating in advance that
alcohol, and arguably smokeless tobacco and betel quid (D009), are the ones that count. That is
itself a protocol decision.

### B. ROBINS-E (Risk Of Bias In Non-randomized Studies — of Exposures)

Seven domains assessed through signalling questions, each judged low / some concerns / high / very
high, with an overall judgement.

**For.** Purpose-built for exposure epidemiology, which is exactly this review's design: a
non-randomised exposure (smoked tobacco) and a disease outcome. It handles confounding explicitly
and demands a pre-specified confounder list, which forces the alcohol question into the open rather
than leaving it implicit. Domain-level judgements avoid the single-score objection, and it is the
current methodological recommendation for exposure reviews.

**Against.** Substantially more work per study — the signalling questions are extensive, which
under single-reviewer screening (D010) is a real cost. It is newer and less familiar to readers in
this field than NOS. Its "very high" category has no NOS equivalent, so results are not comparable
with the many existing OSCC meta-analyses that used NOS.

### C. Newcastle–Ottawa with domain-level reporting and no total score

NOS items, reported per domain, with the star total deliberately not computed.

**For.** Keeps the familiar, design-specific items while avoiding the composite-score objection.
Lighter than ROBINS-E.

**Against.** A non-standard use of a standard instrument, which must be declared as a deviation.
It also removes the study-level summary the SAP's subgroup and sensitivity analyses currently
assume, so either those analyses change or a separate rule for deriving a study-level judgement
from domains must be pre-specified — another decision.

## Recommendation — a recommendation only, not an adopted decision

**Option B, ROBINS-E**, if the reviewer can absorb the per-study workload; otherwise **Option C**.

The reasoning is that this review's central threat is confounding, not selection: the association
between smoking and oral cancer is heavily confounded by alcohol, and in much of the relevant
literature by smokeless tobacco and betel quid, which D009 classifies as confounders rather than
exposures. ROBINS-E is the only option that makes the confounder list an explicit, pre-specified
input to the assessment, which is precisely the discipline this review needs. Option C is the
fallback because it preserves domain-level honesty at a fraction of the effort, at the price of a
declared deviation.

Option A is not recommended, because its single total would be used in the SAP's subgroup analysis
and would then carry more weight than an unweighted star sum can bear.

## The exact decision required

> **P023.** Which risk-of-bias instrument applies to this review: Newcastle–Ottawa (A),
> ROBINS-E (B), or Newcastle–Ottawa reported per domain without a total score (C)? And, as part of
> the same decision, which confounders must a study address for the comparability or confounding
> domain to be judged adequately — alcohol alone, or alcohol together with smokeless tobacco and
> betel quid per D009?

Both halves must be settled before any study is assessed. The second cannot be deferred: an
instrument that asks whether confounding was handled adequately is unanswerable until "adequately"
is defined, and defining it after seeing the studies would be post-hoc.

## What happens once it is settled

1. A decision-log entry records the instrument, its version and the confounder list.
2. The `risk_of_bias` table is implemented with that instrument's domains and judgement scale, and
   a worksheet is generated with one row per `study_id` per domain and **every judgement empty**.
3. Two fields are added to the specified structure, which it currently lacks: an assessment date
   alongside `assessed_by`, and a disagreement-resolution field. The second is retained even under
   single-reviewer assessment (D010), because a reviewer who revises an earlier judgement should
   record why rather than overwrite it.
4. Validation refuses a judgement outside the instrument's own scale, a judgement with no
   supporting evidence, and `information_missing` treated as high risk — missing information is
   not evidence of bias.

None of this can begin yet for a more basic reason: **no study has been included.** Risk of bias
is assessed per included study, and the full-text stage has not run. The instrument decision can
nonetheless be taken now, and should be, because taking it after the included set is known invites
the choice to be shaped by the studies it will judge.
