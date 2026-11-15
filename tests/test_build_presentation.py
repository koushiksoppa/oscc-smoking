"""The deck and the report figures must be valid, deterministic, and true to the repository.

A slide that quotes a number which the data does not support is the same class of defect as a
manuscript that does so, and is harder to catch by eye. These tests assert the deck's claims
against `scripts.screening.prisma.gather()` rather than against a transcription.
"""
from __future__ import annotations

import posixpath
import re
import xml.etree.ElementTree as ET
import zipfile

import pytest

from scripts.reporting import build_presentation as bp
from scripts.screening import prisma

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
RELS = "{http://schemas.openxmlformats.org/package/2006/relationships}"
CT = "{http://schemas.openxmlformats.org/package/2006/content-types}"


@pytest.fixture(scope="module")
def deck(tmp_path_factory):
    out = tmp_path_factory.mktemp("deck") / "deck.pptx"
    bp.build(bp.slides(), out)
    return out


def _zip(deck):
    return zipfile.ZipFile(deck)


def slide_text(deck, i: int) -> str:
    root = ET.fromstring(_zip(deck).read(f"ppt/slides/slide{i}.xml"))
    return " ".join(t.text or "" for t in root.iter(f"{A}t"))


def all_text(deck) -> str:
    return " ".join(slide_text(deck, i) for i in range(1, len(bp.slides()) + 1))


def test_deck_has_fifteen_slides(deck):
    names = _zip(deck).namelist()
    assert len([n for n in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)]) == 15


def test_every_part_is_well_formed_xml(deck):
    z = _zip(deck)
    for name in z.namelist():
        if name.endswith((".xml", ".rels")):
            ET.fromstring(z.read(name))


def test_required_package_parts_exist(deck):
    names = set(_zip(deck).namelist())
    for required in ("[Content_Types].xml", "_rels/.rels", "ppt/presentation.xml",
                     "ppt/_rels/presentation.xml.rels",
                     "ppt/slideMasters/slideMaster1.xml",
                     "ppt/slideLayouts/slideLayout1.xml", "ppt/theme/theme1.xml"):
        assert required in names, required


def test_every_relationship_resolves(deck):
    """A dangling r:id is the usual reason a hand-written package refuses to open."""
    z = _zip(deck)
    names = set(z.namelist())
    for part in [n for n in names if n.endswith(".xml") and not n.endswith(".rels")]:
        ids = set(re.findall(r'r:(?:id|embed)="([^"]+)"', z.read(part).decode("utf-8")))
        if not ids:
            continue
        d, b = posixpath.split(part)
        relpath = posixpath.join(d, "_rels", b + ".rels")
        assert relpath in names, f"{part} references {ids} but has no .rels"
        rels = {r.get("Id"): r.get("Target")
                for r in ET.fromstring(z.read(relpath)).findall(f"{RELS}Relationship")}
        for rid in ids:
            assert rid in rels, f"{part}: {rid} missing"
            target = posixpath.normpath(posixpath.join(d, rels[rid]))
            assert target in names, f"{part}: {rid} -> {target} does not exist"


def test_every_part_has_a_content_type(deck):
    z = _zip(deck)
    ct = ET.fromstring(z.read("[Content_Types].xml"))
    defaults = {d.get("Extension").lower() for d in ct.findall(f"{CT}Default")}
    overrides = {o.get("PartName").lstrip("/") for o in ct.findall(f"{CT}Override")}
    for name in z.namelist():
        if name == "[Content_Types].xml" or name in overrides:
            continue
        assert name.rsplit(".", 1)[-1].lower() in defaults, name


def test_generation_is_deterministic(tmp_path):
    a, b = tmp_path / "a.pptx", tmp_path / "b.pptx"
    bp.build(bp.slides(), a)
    bp.build(bp.slides(), b)
    za, zb = zipfile.ZipFile(a), zipfile.ZipFile(b)
    assert za.namelist() == zb.namelist()
    for name in za.namelist():
        assert za.read(name) == zb.read(name), name


def test_figures_are_embedded_not_linked(deck):
    z = _zip(deck)
    media = [n for n in z.namelist() if n.startswith("ppt/media/")]
    assert len(media) == 4
    for name in media:
        assert z.read(name)[:8] == b"\x89PNG\r\n\x1a\n", name


# --- the deck must agree with the data -------------------------------------------------

def test_slide_numbers_match_the_repository(deck):
    flow = prisma.gather()
    text = all_text(deck)
    assert str(flow["identified"]) == "194"
    for claim in (f"{flow['identified']} identified",
                  f"{flow['prov_excluded']} provisionally excluded",
                  f"{flow['ta_adjudicated']} of {flow['ta_total']} independently adjudicated"):
        assert claim in text, claim


def test_deck_states_zero_formal_screening(deck):
    flow = prisma.gather()
    assert flow["ta_screened"] == 0 and flow["ta_adjudicated"] == 0
    text = all_text(deck)
    assert "0 of 194 independently adjudicated" in text
    assert "0 of 120" in text


def test_deck_never_claims_a_completed_synthesis(deck):
    text = all_text(deck).lower()
    for forbidden in ("pooled estimate of", "we pooled", "meta-analysis was performed",
                      "odds ratio of", "statistically significant", "we found an association"):
        assert forbidden not in text, forbidden


def test_deck_states_no_pooled_estimate_exists(deck):
    text = all_text(deck)
    assert "No pooled estimate, forest plot or funnel plot exists" in text
    assert "Publication bias has NOT been assessed" in text


def test_deck_labels_automated_output_as_provisional(deck):
    text = all_text(deck)
    assert "provisional classification" in text.lower()
    assert "adopted_from_suggestion" in text or "adopted from an automated suggestion" in text


def test_deck_does_not_present_counts_as_search_yields(deck):
    text = all_text(deck)
    assert "8,190" in text and "5,008" in text
    assert "these are not search yields" in text.lower()


def test_deck_names_no_unused_technology(deck):
    """Claiming tooling the repository does not import would itself be a reproducibility defect."""
    text = all_text(deck).lower()
    assert "pandas is not used" in text
    for absent in ("tensorflow", "pytorch", "django", "flask", "spark"):
        assert absent not in text, absent


def test_deck_does_not_name_a_risk_of_bias_instrument_as_chosen(deck):
    text = all_text(deck)
    for instrument in ("Newcastle", "ROBINS", "QUIPS", "GRADE"):
        assert instrument not in text, instrument


def test_missing_figure_is_refused(tmp_path):
    from scripts.common.config import PipelineError
    bad = [{"title": "x", "image": "no_such_figure.png"}]
    with pytest.raises(PipelineError, match="figure not found"):
        bp.build(bad, tmp_path / "x.pptx")
