"""The controlled screening vocabulary, loaded from config/screening.yaml.

The vocabulary is fixed by protocol: a screener chooses from these codes and may not substitute
free text (docs/protocol/eligibility_criteria.md). Adding or removing a code is a protocol change
requiring a decision-log entry, and tests/test_screening.py fails if the config and the protocol
document disagree.
"""
from __future__ import annotations

from dataclasses import dataclass

import yaml

from scripts.common.config import ROOT, PipelineError

SCREENING_CONFIG = ROOT / "config" / "screening.yaml"

INCLUDE = "include"
EXCLUDE = "exclude"
UNRESOLVED = "unresolved"

# How a decision came about. ADOPTED records that the reviewer took an automated suggestion
# without judging the record individually; it is not independent adjudication (D010).
ADOPTED = "adopted_from_suggestion"
ADJUDICATED = "independently_adjudicated"
TA = "ta"
FT = "ft"
STAGES = (TA, FT)
STAGE_LABEL = {TA: "title/abstract", FT: "full text"}


@dataclass(frozen=True)
class Reason:
    code: str
    description: str
    stages: tuple[str, ...]
    requires_note: bool = False

    def permitted_at(self, stage: str) -> bool:
        return stage in self.stages


@dataclass(frozen=True)
class DecisionBasis:
    code: str
    description: str


@dataclass(frozen=True)
class Vocabulary:
    decisions: tuple[str, ...]
    retrieval_statuses: tuple[str, ...]
    reasons: tuple[Reason, ...]
    decision_bases: tuple[DecisionBasis, ...] = ()

    def basis_codes(self) -> tuple[str, ...]:
        return tuple(b.code for b in self.decision_bases)

    def reason(self, code: str) -> Reason | None:
        return next((r for r in self.reasons if r.code == code), None)

    def codes(self, stage: str | None = None) -> tuple[str, ...]:
        return tuple(r.code for r in self.reasons if stage is None or r.permitted_at(stage))


def load_vocabulary() -> Vocabulary:
    with open(SCREENING_CONFIG, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    reasons = tuple(
        Reason(code=r["code"], description=r["description"],
               stages=tuple(r["stages"]), requires_note=bool(r.get("requires_note", False)))
        for r in data["reasons"]
    )
    codes = [r.code for r in reasons]
    if len(codes) != len(set(codes)):
        raise PipelineError(f"Duplicate reason code in {SCREENING_CONFIG.name}: {codes}")
    for reason in reasons:
        unknown = set(reason.stages) - set(STAGES)
        if unknown or not reason.stages:
            raise PipelineError(
                f"{reason.code}: stages must be a non-empty subset of {STAGES}, got {reason.stages}"
            )
    bases = tuple(DecisionBasis(code=b["code"], description=b["description"])
                  for b in data.get("decision_bases", []))
    basis_codes = [b.code for b in bases]
    if len(basis_codes) != len(set(basis_codes)):
        raise PipelineError(f"Duplicate decision_basis in {SCREENING_CONFIG.name}: {basis_codes}")

    vocab = Vocabulary(
        decisions=tuple(data["decisions"]),
        retrieval_statuses=tuple(data["retrieval_statuses"]),
        reasons=reasons,
        decision_bases=bases,
    )
    for required in (INCLUDE, EXCLUDE, UNRESOLVED):
        if required not in vocab.decisions:
            raise PipelineError(f"{SCREENING_CONFIG.name}: decisions must include '{required}'")
    # Without these two the distinction D010 requires cannot be represented in the data.
    for required in (ADOPTED, ADJUDICATED):
        if required not in basis_codes:
            raise PipelineError(
                f"{SCREENING_CONFIG.name}: decision_bases must include '{required}'")
    return vocab
