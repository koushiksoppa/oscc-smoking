"""Generate the project presentation as a PowerPoint file.

    python -m scripts.reporting.build_presentation

Writes results/final_submission/Research_Project_Presentation.pptx.

There is no third-party presentation library here and installing one was not authorised, so the
.pptx is written directly as OOXML through `zipfile` — the same approach the manuscript builder
takes for .docx. A .pptx is a ZIP container holding a presentation part, a slide master, a slide
layout, a theme and one XML part per slide; this module writes the minimum valid set.

Slide content is declared as data at the foot of the file, so the deck's wording lives in one place
and can be checked against the repository. Every number quoted on a slide is also asserted in
`tests/test_build_presentation.py` against `scripts.screening.prisma.gather()`, so a slide cannot
drift from the data it describes.

Deterministic: no timestamps are written into the package, so the same inputs produce the same file.
"""
from __future__ import annotations

import argparse
import html
import sys
import zipfile
from pathlib import Path

from scripts.common.config import ROOT, PipelineError

OUT = ROOT / "results" / "final_submission" / "Research_Project_Presentation.pptx"
FIGDIR = ROOT / "results" / "final_submission" / "figures"

# 16:9 at 13.333in x 7.5in, in English Metric Units (914400 EMU per inch).
W, H = 12192000, 6858000
INK = "1A1A1A"
ACCENT = "2F4858"
MUTED = "5A5A5A"
GREEN = "2E7D4F"
AMBER = "B7791F"
RED = "B3261E"


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def _tx_body(paras: str) -> str:
    return (f'<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0">'
            f'<a:normAutofit/></a:bodyPr><a:lstStyle/>{paras}</p:txBody>')


def _para(runs: str, *, align: str = "l", indent: int = 0, space_before: int = 0,
          bullet: bool = False) -> str:
    mar = f' marL="{indent * 285750}" indent="{-228600 if bullet else 0}"' if (indent or bullet) else ""
    buf = ('<a:buChar char="•"/>' if bullet else "<a:buNone/>")
    spc = f'<a:spcBef><a:spcPts val="{space_before}"/></a:spcBef>' if space_before else ""
    return f'<a:p><a:pPr algn="{align}"{mar}>{spc}{buf}</a:pPr>{runs}</a:p>'


def _run(text: str, *, size: int, bold: bool = False, colour: str = INK,
         italic: bool = False) -> str:
    return (f'<a:r><a:rPr lang="en-GB" sz="{size * 100}" b="{1 if bold else 0}" '
            f'i="{1 if italic else 0}" dirty="0"><a:solidFill><a:srgbClr val="{colour}"/>'
            f'</a:solidFill><a:latin typeface="Calibri"/></a:rPr>'
            f'<a:t>{esc(text)}</a:t></a:r>')


def _shape(idx: int, name: str, x: int, y: int, cx: int, cy: int, body: str) -> str:
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{idx}" name="{esc(name)}"/>'
            f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>{body}</p:sp>')


def _rect(idx: int, x: int, y: int, cx: int, cy: int, colour: str) -> str:
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{idx}" name="bar{idx}"/><p:cNvSpPr/><p:nvPr/>'
            f'</p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/>'
            f'</a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="{colour}"/></a:solidFill></p:spPr>'
            f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>')


def _pic(idx: int, rid: str, x: int, y: int, cx: int, cy: int) -> str:
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="{idx}" name="fig{idx}"/>'
            f'<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch>'
            f'</p:blipFill><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/>'
            f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')


def slide_xml(shapes: str) -> str:
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
            f'<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/>'
            f'</p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
            f'<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>{shapes}'
            '</p:spTree></p:cSld><p:clrMapOvr><a:overrideClrMapping bg1="lt1" tx1="dk1" '
            'bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" '
            'accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" '
            'folHlink="folHlink"/></p:clrMapOvr></p:sld>')


THEME = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
         '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Report">'
         '<a:themeElements><a:clrScheme name="Report">'
         '<a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1>'
         '<a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>'
         '<a:dk2><a:srgbClr val="1A1A1A"/></a:dk2><a:lt2><a:srgbClr val="F4F4F2"/></a:lt2>'
         '<a:accent1><a:srgbClr val="2F4858"/></a:accent1>'
         '<a:accent2><a:srgbClr val="2E7D4F"/></a:accent2>'
         '<a:accent3><a:srgbClr val="B7791F"/></a:accent3>'
         '<a:accent4><a:srgbClr val="8A8A8A"/></a:accent4>'
         '<a:accent5><a:srgbClr val="4A5A7A"/></a:accent5>'
         '<a:accent6><a:srgbClr val="B3261E"/></a:accent6>'
         '<a:hlink><a:srgbClr val="2F4858"/></a:hlink>'
         '<a:folHlink><a:srgbClr val="5A5A5A"/></a:folHlink></a:clrScheme>'
         '<a:fontScheme name="Report"><a:majorFont><a:latin typeface="Calibri Light"/>'
         '<a:ea typeface=""/><a:cs typeface=""/></a:majorFont>'
         '<a:minorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/>'
         '</a:minorFont></a:fontScheme><a:fmtScheme name="Report">'
         '<a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
         '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
         '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>'
         '<a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
         '<a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
         '<a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
         '</a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle>'
         '<a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/>'
         '</a:effectStyle></a:effectStyleLst>'
         '<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
         '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
         '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>'
         '</a:fmtScheme></a:themeElements></a:theme>')

EMPTY_TREE = ('<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/>'
              '</p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
              '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
              '</p:spTree></p:cSld>')

MASTER = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
          'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
          + EMPTY_TREE +
          '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" '
          'accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" '
          'folHlink="folHlink"/><p:sldLayoutIdLst>'
          '<p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst></p:sldMaster>')

LAYOUT = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
          'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
          'type="blank" preserve="1">' + EMPTY_TREE +
          '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')


def build(slides: list[dict], out: Path) -> dict:
    out.parent.mkdir(parents=True, exist_ok=True)
    media: list[Path] = []
    for s in slides:
        if s.get("image"):
            p = FIGDIR / s["image"]
            if not p.exists():
                raise PipelineError(f"slide figure not found: {p}")
            if p not in media:
                media.append(p)

    n = len(slides)
    ct = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.'
          'relationships+xml"/>',
          '<Default Extension="xml" ContentType="application/xml"/>',
          '<Default Extension="png" ContentType="image/png"/>',
          '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.'
          'openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
          '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.'
          'openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
          '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.'
          'openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
          '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.'
          'openxmlformats-officedocument.theme+xml"/>']
    for i in range(1, n + 1):
        ct.append(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.'
                  f'openxmlformats-officedocument.presentationml.slide+xml"/>')
    ct.append("</Types>")

    pres_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/'
                 'relationships">',
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/'
                 'officeDocument/2006/relationships/slideMaster" Target="slideMasters/'
                 'slideMaster1.xml"/>']
    sld_ids = []
    for i in range(1, n + 1):
        rid = f"rId{i + 1}"
        pres_rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
                         f'officeDocument/2006/relationships/slide" '
                         f'Target="slides/slide{i}.xml"/>')
        sld_ids.append(f'<p:sldId id="{255 + i}" r:id="{rid}"/>')
    pres_rels.append(f'<Relationship Id="rId{n + 2}" Type="http://schemas.openxmlformats.org/'
                     f'officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>')
    pres_rels.append("</Relationships>")

    presentation = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                    '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/'
                    'main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/'
                    'relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/'
                    '2006/main" saveSubsetFonts="1">'
                    '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/>'
                    '</p:sldMasterIdLst>'
                    f'<p:sldIdLst>{"".join(sld_ids)}</p:sldIdLst>'
                    f'<p:sldSz cx="{W}" cy="{H}"/><p:notesSz cx="{H}" cy="{W}"/>'
                    '</p:presentation>')

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "".join(ct))
        z.writestr("_rels/.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/'
                   'relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.'
                   'org/officeDocument/2006/relationships/officeDocument" '
                   'Target="ppt/presentation.xml"/></Relationships>')
        z.writestr("ppt/presentation.xml", presentation)
        z.writestr("ppt/_rels/presentation.xml.rels", "".join(pres_rels))
        z.writestr("ppt/theme/theme1.xml", THEME)
        z.writestr("ppt/slideMasters/slideMaster1.xml", MASTER)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/'
                   'relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.'
                   'org/officeDocument/2006/relationships/slideLayout" '
                   'Target="../slideLayouts/slideLayout1.xml"/>'
                   '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/'
                   'officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>'
                   '</Relationships>')
        z.writestr("ppt/slideLayouts/slideLayout1.xml", LAYOUT)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/'
                   'relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.'
                   'org/officeDocument/2006/relationships/slideMaster" '
                   'Target="../slideMasters/slideMaster1.xml"/></Relationships>')

        for p in media:
            z.writestr(f"ppt/media/{p.name}", p.read_bytes())

        for i, s in enumerate(slides, 1):
            shapes, rels = render(s, i)
            z.writestr(f"ppt/slides/slide{i}.xml", slide_xml(shapes))
            body = "".join(
                f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
                f'officeDocument/2006/relationships/image" Target="../media/{tgt}"/>'
                for rid, tgt in rels)
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels",
                       '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                       '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/'
                       'relationships"><Relationship Id="rIdL" Type="http://schemas.'
                       'openxmlformats.org/officeDocument/2006/relationships/slideLayout" '
                       'Target="../slideLayouts/slideLayout1.xml"/>' + body + "</Relationships>")

    return {"slides": n, "media": len(media), "bytes": out.stat().st_size}


MARGIN = 685800            # 0.75in
CONTENT_W = W - 2 * MARGIN


def render(s: dict, num: int) -> tuple[str, list[tuple[str, str]]]:
    """One slide's shape XML plus its image relationships."""
    out: list[str] = []
    rels: list[tuple[str, str]] = []
    idx = 2

    if s.get("kind") == "title":
        out.append(_rect(idx, 0, 0, W, 2400000, ACCENT)); idx += 1
        out.append(_shape(idx, "title", MARGIN, 620000, CONTENT_W, 1500000,
                          _tx_body(_para(_run(s["title"], size=30, bold=True, colour="FFFFFF")))))
        idx += 1
        out.append(_shape(idx, "sub", MARGIN, 2750000, CONTENT_W, 1500000,
                          _tx_body("".join(
                              _para(_run(line, size=15, colour=INK), space_before=600)
                              for line in s["lines"]))))
        idx += 1
        out.append(_shape(idx, "foot", MARGIN, H - 900000, CONTENT_W, 500000,
                          _tx_body(_para(_run(s["foot"], size=11, italic=True, colour=MUTED)))))
        return "".join(out), rels

    # standard slide: rule, number, title, then body
    out.append(_rect(idx, MARGIN, 520000, CONTENT_W, 22000, ACCENT)); idx += 1
    out.append(_shape(idx, "num", W - MARGIN - 700000, 180000, 700000, 300000,
                      _tx_body(_para(_run(f"{num} / 15", size=10, colour=MUTED), align="r"))))
    idx += 1
    out.append(_shape(idx, "title", MARGIN, 150000, CONTENT_W - 800000, 400000,
                      _tx_body(_para(_run(s["title"], size=22, bold=True, colour=ACCENT)))))
    idx += 1

    y = 820000
    if s.get("lead"):
        out.append(_shape(idx, "lead", MARGIN, y, CONTENT_W, 450000,
                          _tx_body(_para(_run(s["lead"], size=14, italic=True, colour=MUTED)))))
        idx += 1
        y += 560000

    if s.get("image"):
        name = s["image"]
        rid = "rId9"
        rels.append((rid, name))
        iw = CONTENT_W if s.get("wide", True) else int(CONTENT_W * 0.72)
        ih = int(iw * s.get("ratio", 0.58))
        avail = H - y - 500000
        if ih > avail:
            ih = avail
            iw = int(ih / s.get("ratio", 0.58))
        out.append(_pic(idx, rid, MARGIN + (CONTENT_W - iw) // 2, y, iw, ih))
        idx += 1
        y += ih + 120000

    for b in s.get("bullets", []):
        text, lvl, colour, bold = (b if isinstance(b, tuple) else (b, 0, INK, False))
        size = 15 if lvl == 0 else 13
        out.append(_shape(idx, f"b{idx}", MARGIN + lvl * 300000, y,
                          CONTENT_W - lvl * 300000, 420000,
                          _tx_body(_para(_run(text, size=size, bold=bold, colour=colour),
                                         bullet=True, indent=0))))
        idx += 1
        y += 330000 if lvl else 390000

    if s.get("note"):
        out.append(_shape(idx, "note", MARGIN, H - 760000, CONTENT_W, 480000,
                          _tx_body(_para(_run(s["note"], size=11, italic=True, colour=RED)))))
        idx += 1
    return "".join(out), rels


def slides() -> list[dict]:
    """Deck content. Numbers here are asserted against the repository in the test suite."""
    B = INK
    return [
        {"kind": "title",
         "title": "A Reproducible Systematic Review and Meta-Analysis Pipeline",
         "lines": [
             "Is smoked tobacco use associated with an increased risk of squamous cell "
             "carcinoma of the oral cavity?",
             "",
             "Soppa Shiva Sai Koushik",
             "13 November 2026"],
         "foot": "Status: protocol and infrastructure complete. No study included; no pooled "
                 "estimate. This deck reports an instrument, not a finding."},

        {"title": "Background and motivation",
         "lead": "Why this question, and why the method matters as much as the answer",
         "bullets": [
             ("Oral cavity SCC carries a high burden in South and South-East Asia", 0, B, False),
             ("The relevant exposure is broader than cigarettes: bidis, chuttas, cigars, pipes, "
              "reverse smoking", 0, B, False),
             ("Oral cavity is NOT interchangeable with oropharynx — different HPV-related "
              "aetiology, so pooling across sites distorts the estimate", 0, B, False),
             ("Methodological gap: reviews are called reproducible far more often than they are",
              0, ACCENT, True),
             ("Where automated screening is used, a worksheet showing 194 decisions rarely says "
              "whether a human read 194 abstracts or accepted 194 machine outputs at once",
              1, MUTED, False)]},

        {"title": "Research objectives",
         "lead": "Eight infrastructure objectives achieved; the scientific objective is not",
         "bullets": [
             ("O1–O2  Specify a recorded protocol; checksum-gated acquisition", 0, GREEN, False),
             ("O3–O4  Deduplication with no silent merging; screening that separates suggestion "
              "from decision", 0, GREEN, False),
             ("O5–O6  Blinded verification with a reproducible frame; a 93-field extraction "
              "schema", 0, GREEN, False),
             ("O7–O8  Meta-analytic computation with declared limits; reproducible generation of "
              "all outputs", 0, GREEN, False),
             ("O9  Produce a pooled estimate answering the review question", 0, RED, True),
             ("NOT ACHIEVED — blocked on reviewer work and on open protocol decisions",
              1, RED, False)]},

        {"title": "Eligibility criteria (PECO)",
         "bullets": [
             ("Population — human adults, no restriction by country, sex or setting  [settled]",
              0, B, False),
             ("Exposure — any smoked tobacco: cigarettes, bidis, cigars, pipes  [settled, D009]",
              0, B, False),
             ("Comparator — never-smokers and/or study-defined non-smokers, recorded verbatim  "
              "[settled, D025]", 0, B, False),
             ("Outcome — oral cavity cancer, SCC confirmed or a stated majority of at least 90%  "
              "[settled in part, D008]", 0, B, False),
             ("Designs — case–control and cohort; effect estimate with 95% CI, or data to "
              "compute one  [settled]", 0, B, False),
             ("13-code controlled vocabulary for exclusions; 4 codes restricted to full text "
              "because an abstract cannot support them", 0, ACCENT, True)],
         "note": "Ten anatomical and histological scope questions remain open — one affects 14 of "
                 "the 85 carried-forward reports."},

        {"title": "Literature identification and search strategy",
         "lead": "One database searched. The executed query is narrower than its own protocol.",
         "bullets": [
             ("pubmed_v1r — 194 records, unfiltered, registered with a SHA-256 checksum",
              0, GREEN, True),
             ("pubmed_v1 — the original 138-record export is LOST; recorded as missing, never "
              "substituted", 0, RED, False),
             ("68 of 194 records use the phrase ‘oral cancer’, which the query does not "
              "require", 0, AMBER, False),
             ("98 of 194 matched the design block only through the single word ‘cohort’",
              0, AMBER, False),
             ("Corrected strategy ADOPTED (D023, 13 Nov 2026) with no design block — 8,190 "
              "records against 5,008 with one — but NOT yet executed", 0, B, False)],
         "note": "Counts-only interrogations for strategy validation. These are not search "
                 "yields: nothing was retrieved, exported or screened."},

        {"title": "Pipeline architecture",
         "image": "pipeline_architecture.png", "ratio": 0.60,
         "note": "Colour is assigned from the repository at build time, so the diagram cannot "
                 "drift from what the code actually does."},

        {"title": "Deduplication and record management",
         "bullets": [
             ("Identifier hierarchy: normalised DOI → PMID → exact title+author+year "
              "fingerprint", 0, B, False),
             ("Similar-but-not-identical titles are flagged needs_review and NEVER merged "
              "automatically", 0, ACCENT, True),
             ("Result: 194 records in, 0 duplicates, 0 needing review, 194 unique reports",
              0, GREEN, False),
             ("Zero duplicates is expected for a single-database search — the rules are "
              "exercised by 63 tests, not by this result", 1, MUTED, False),
             ("D004 identifier chain: record_id → report_id → study_id → "
              "estimate_id; the study is the unit of analysis", 0, B, False)]},

        {"title": "Screening and verification architecture",
         "lead": "The central design decision of the project",
         "bullets": [
             ("Every decision records a basis: adopted_from_suggestion or "
              "independently_adjudicated", 0, ACCENT, True),
             ("A row counts as adjudicated only when all five fields are present — including a "
              "separate adjudicated_date, so a basis cannot be flipped without dating the act",
              0, B, False),
             ("PRISMA flow is SPLIT: formal counts adjudicated decisions only; provisional "
              "counts appear outside the flow", 0, B, False),
             ("Current state: every one of the 194 records carries a provisional "
              "classification — 0 of 194 independently adjudicated", 0, RED, True),
             ("Blinded verification sample: 40 of 194 reports (20.6%), 120 response cells, 0 "
              "complete", 0, AMBER, False)]},

        {"title": "Data flow and provenance",
         "image": "data_flow.png", "ratio": 0.62,
         "note": "The suggestion file is deliberately separate from the decision file: an "
                 "automated suggestion is never written into a decision field."},

        {"title": "Statistical analysis architecture",
         "lead": "Implemented and tested; never run on research data, because no estimate exists",
         "bullets": [
             ("Effect measures OR / RR / HR, computed on the log scale; three SE routes — from "
              "CI, from 2×2 counts, as reported", 0, B, False),
             ("Inverse-variance weighting; fixed-effect and random-effects, with "
              "DerSimonian–Laird and REML estimators of τ²", 0, B, False),
             ("Heterogeneity: Cochran's Q with its χ² p-value, I², τ²",
              0, B, False),
             ("Leave-one-out sensitivity analysis implemented; five subgroup analyses planned",
              0, B, False),
             ("Egger's test REFUSES below 10 studies; declared gaps: no HKSJ interval, no "
              "Mantel–Haenszel, no meta-regression, REML unvalidated externally",
              0, AMBER, True)],
         "note": "No pooled estimate, forest plot or funnel plot exists. Publication bias has "
                 "NOT been assessed."},

        {"title": "Technology stack",
         "image": "tech_stack.png", "ratio": 0.60,
         "note": "pandas is not used anywhere: all tabular work uses the standard-library csv "
                 "module. Claiming unused tooling would itself be a reproducibility failure."},

        {"title": "Numerical results",
         "lead": "Every figure recomputed from the repository, not transcribed",
         "image": "record_status.png", "ratio": 0.40,
         "bullets": [
             ("194 identified → 194 unique → 109 provisionally excluded, 85 carried "
              "forward → 0 formally screened → 0 included", 0, B, False),
             ("Each of the 194 is a provisional classification adopted from an automated "
              "suggestion, not a reviewer decision", 0, RED, False)],
         "note": "The zeros are the result. They show the gates working, not a search that found "
                 "nothing."},

        {"title": "Validation and reproducibility",
         "bullets": [
             ("615 tests passed, 1 skipped by design (the lost export's raw-source test)",
              0, GREEN, True),
             ("Protected: raw-export SHA-256, five verification-seed constants, seven screening "
              "and processed data files — all verify", 0, GREEN, False),
             ("Deterministic generation verified by rebuilding to a clean path: PRISMA figure, "
              "extraction workbook, all four report figures — byte-identical", 0, B, False),
             ("Cross-format validation opens the produced files: 19/19 headings, 164/164 table "
              "cells, 109/109 numeric tokens, 80/80 sentences", 0, B, False),
             ("Regression tests encode specific defects found and fixed, so they cannot return",
              0, B, False)]},

        {"title": "Limitations",
         "lead": "Stated plainly, because the project's value depends on stating them",
         "bullets": [
             ("One database; the executed query is narrower than its own eligibility criteria",
              0, RED, True),
             ("No formal independent human screening: 0 of 194 adjudicated", 0, RED, False),
             ("0 full texts retrieved, 0 studies included, 0 estimates extracted, 0 risk-of-bias "
              "assessments, 0 pooled analyses", 0, RED, False),
             ("Verification sample unanswered: 0 of 120 cells, so no kappa and no acceptance "
              "verdict exists", 0, AMBER, False),
             ("Automated suggestions are unvalidated on this corpus; a false exclusion is "
              "invisible, a false inclusion is caught at full text", 0, AMBER, False),
             ("P007 open and no subscription database access verified; not prospectively "
              "registered. P013 resolved by D023: no design block, so retrieval \u2248 8,190 "
              "records, and the number of additional eligible studies recovered is unknown",
              0, AMBER, False)]},

        {"title": "Future work and conclusion",
         "bullets": [
             ("Researcher decisions first: P007 databases, P014–P022 scope, P023 "
              "instrument (P013 settled by D023; P003/P004 by D025/D026)", 0, B, False),
             ("Then execute the corrected search and register each export under D011",
              0, B, False),
             ("Then the reviewer's own work, which cannot be generated: 194 adjudications, 120 "
              "verification cells, 85 full texts, extraction, appraisal", 0, ACCENT, True),
             ("Only then: synthesis, with REML cross-checked against an established "
              "implementation", 0, B, False),
             ("Conclusion — integrity properties usually asserted in a methods section have "
              "been made properties of a system: the pipeline refuses to produce an estimate it "
              "cannot justify", 0, GREEN, True)],
         "note": "The clearest evidence that the design works is the set of zeros in the results."},
    ]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    result = build(slides(), Path(args.out))
    print(f"  presentation -> {args.out}")
    print(f"  {result['slides']} slides, {result['media']} embedded figures, "
          f"{result['bytes']:,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
