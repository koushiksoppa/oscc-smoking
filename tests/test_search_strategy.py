"""The operative PubMed strategy must stay as adopted, and its corrections must stay applied.

Regression tests for D023 (no study-design block) and D024/PC-1 (removal of an ineffective quoted
phrase). The strategy lives in prose documents rather than in code, so nothing else would notice if
a term were reintroduced, dropped or silently edited.
"""
from __future__ import annotations

import re

import pytest

from scripts.common.config import ROOT

ADOPTED = ROOT / "docs" / "methods" / "recommended_search_strategy.md"
TRANSLATIONS = ROOT / "docs" / "search" / "database_search_strategies.md"
SUPPLEMENT = ROOT / "docs" / "reports" / "supplementary_material.md"
REGISTER = ROOT / "docs" / "decisions" / "decision_log.md"

HISTORICAL = [ROOT / "docs" / "search" / "search_v1_pubmed.md",
              ROOT / "docs" / "search" / "search_v1r_pubmed_reexecution.md",
              ROOT / "docs" / "search" / "search_v2_pubmed.md"]

REMOVED = '"epidermoid carcinoma of the mouth"[tiab]'
RETAINED = '"oral epidermoid carcinoma"[tiab]'
UNQUOTED = "epidermoid carcinoma of the mouth[tiab]"

QUERY = re.compile(r'\(\s*\n\s*"Mouth Neoplasms"\[Mesh\].*?\n\)\s*\nAND\s*\n\(.*?\n\)', re.S)


def text(path):
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def pubmed_query(path) -> str:
    """The operative PubMed query block, normalised for line endings."""
    m = QUERY.search(text(path))
    assert m, f"no PubMed query block found in {path.name}"
    return m.group(0)


# --- D024 / PC-1 ---------------------------------------------------------------------

@pytest.mark.parametrize("path", [ADOPTED, TRANSLATIONS, SUPPLEMENT],
                         ids=["adopted", "translations", "supplement"])
def test_removed_phrase_is_absent(path):
    """PC-1: the dead term returned 0 results with QuotedPhraseNotFound and was removed."""
    assert REMOVED not in text(path)


@pytest.mark.parametrize("path", [ADOPTED, TRANSLATIONS, SUPPLEMENT],
                         ids=["adopted", "translations", "supplement"])
def test_retained_phrase_is_present(path):
    """PC-1 removed one phrase from a two-phrase line; the other must survive."""
    assert RETAINED in text(path)


@pytest.mark.parametrize("path", [ADOPTED, TRANSLATIONS, SUPPLEMENT],
                         ids=["adopted", "translations", "supplement"])
def test_unquoted_alternative_was_not_adopted(path):
    """The unquoted form returned 28 records, but that is a different search, not a repair."""
    body = text(path)
    # the bare form, not preceded by a quote mark
    assert not re.search(r'(?<!")' + re.escape(UNQUOTED), body)


def test_decision_register_records_pc1_as_d024():
    body = text(REGISTER)
    assert "### D024" in body
    assert body.count("### D024") == 1
    entry = body[body.index("### D024"):]
    entry = entry[:entry.index("\n### ")] if "\n### " in entry else entry
    assert "ADOPTED 2026-11-14" in entry
    assert REMOVED in entry, "the entry must name the term it removed"
    assert "D021" not in entry, "D021 is reserved and must not be reused"


# --- D023 remains intact -------------------------------------------------------------

DESIGN_TERMS = re.compile(
    r"case[- ]control|\bcohort\b|Epidemiologic Studies|Risk Factors\[|Odds Ratio\[|"
    r"cross[- ]sectional|\bretrospective\b|\bprospective\b", re.I)


@pytest.mark.parametrize("path", [ADOPTED, TRANSLATIONS], ids=["adopted", "translations"])
def test_no_study_design_block_in_the_operative_query(path):
    """D023: the primary search carries no design block. PC-1 must not have reintroduced one."""
    assert not DESIGN_TERMS.search(pubmed_query(path))


@pytest.mark.parametrize("path", [ADOPTED, TRANSLATIONS], ids=["adopted", "translations"])
def test_no_filters_in_the_operative_query(path):
    """No language, date, species or publication-type filter (D013)."""
    q = pubmed_query(path)
    for tag in ("[lang]", "[dp]", "[pt]", "humans[mesh]", "english[lang]", "[filter]"):
        assert tag.lower() not in q.lower(), tag


def test_d023_entry_is_unchanged_by_pc1():
    body = text(REGISTER)
    assert "### D023 — No study-design block in the primary search" in body
    assert body.count("### D023") == 1


# --- static structural checks --------------------------------------------------------

@pytest.mark.parametrize("path", [ADOPTED, TRANSLATIONS], ids=["adopted", "translations"])
def test_query_is_structurally_balanced(path):
    q = pubmed_query(path)
    assert q.count("(") == q.count(")"), "unbalanced parentheses"
    assert q.count('"') % 2 == 0, "unpaired double quotes"


@pytest.mark.parametrize("path", [ADOPTED, TRANSLATIONS], ids=["adopted", "translations"])
def test_exactly_one_top_level_and(path):
    """Two concept blocks joined by one AND. An OR escaping its group is the catastrophic error."""
    depth, tops = 0, 0
    for tok in re.finditer(r"[()]|\bAND\b", pubmed_query(path)):
        s = tok.group(0)
        if s == "(":
            depth += 1
        elif s == ")":
            depth -= 1
        elif depth <= 1:
            tops += 1
    assert tops == 1


def test_the_two_operative_copies_are_byte_identical():
    """The adopted strategy and its copy in the translations file must never drift apart."""
    assert pubmed_query(ADOPTED) == pubmed_query(TRANSLATIONS)


def test_supplement_carries_the_same_terms_in_its_own_layout():
    """The supplement reformats the query for publication, so compare terms, not bytes."""
    terms = set(re.findall(r'"[^"]+"\[tiab\]', pubmed_query(ADOPTED)))
    supplement = text(SUPPLEMENT)
    missing = sorted(t for t in terms if t not in supplement)
    assert not missing, f"terms missing from the supplement: {missing}"


# --- historical records stay untouched -----------------------------------------------

@pytest.mark.parametrize("path", HISTORICAL, ids=lambda p: p.name)
def test_historical_search_records_carry_no_operative_correction(path):
    """v1, v1r and v2 are historical. PC-1 applies to the operative strategy only."""
    body = text(path)
    assert "epidermoid" not in body.lower(), (
        f"{path.name} is a historical record and was not expected to contain the corrected term"
    )
    assert "D024" not in body, f"{path.name} must not be rewritten to cite a later decision"
