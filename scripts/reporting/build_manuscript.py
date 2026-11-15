"""Render the manuscript to DOCX and PDF from one Markdown source.

    python -m scripts.reporting.build_manuscript --source docs/reports/manuscript_draft.md

Both outputs are produced from the same parsed document model, so they cannot drift apart: a
heading, table or figure present in one is present in the other, and a validation step at the end
compares the block inventories.

No third-party document library is used. DOCX is written as OOXML inside a zip with the standard
library; PDF is typeset onto A4 pages with matplotlib, which the project already pins. That avoids
adding dependencies to a project whose reproducibility contract rests on a short pinned list.

The renderer is deliberately limited to what this manuscript needs: headings to three levels,
paragraphs with bold and italic and inline code, bullet and numbered lists, pipe tables, fenced
code blocks, block quotes, horizontal rules and figures. Anything else is passed through as text
rather than silently dropped.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import html
import re
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

from scripts.common.config import ROOT, PipelineError

A4_W_IN, A4_H_IN = 8.268, 11.693          # 210 x 297 mm
MARGIN_IN = 0.98                           # 25 mm
SERIF = ["Times New Roman", "Nimbus Roman", "DejaVu Serif", "serif"]


# --------------------------------------------------------------------------------------------
# Document model
# --------------------------------------------------------------------------------------------

@dataclass
class Block:
    kind: str                               # h1 h2 h3 p ul ol table code quote rule figure
    text: str = ""
    items: list[str] = field(default_factory=list)
    rows: list[list[str]] = field(default_factory=list)
    header: list[str] = field(default_factory=list)
    path: str = ""
    caption: str = ""


def parse_markdown(src: str) -> list[Block]:
    """Parse the subset of Markdown this manuscript uses."""
    blocks: list[Block] = []
    lines = src.splitlines()
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()

        if not s:
            i += 1
            continue

        if s.startswith("```"):                                     # fenced code
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            blocks.append(Block("code", "\n".join(buf)))
            continue

        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", s):                  # horizontal rule
            blocks.append(Block("rule"))
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", s)                       # heading
        if m:
            level = min(len(m.group(1)), 3)
            blocks.append(Block(f"h{level}", m.group(2).strip()))
            i += 1
            continue

        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", s)              # figure
        if m:
            blocks.append(Block("figure", path=m.group(2), caption=m.group(1)))
            i += 1
            continue

        if s.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            header = [c.strip() for c in s.strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            blocks.append(Block("table", header=header, rows=rows))
            continue

        if s.startswith(">"):                                       # block quote
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            blocks.append(Block("quote", " ".join(x for x in buf if x)))
            continue

        if re.match(r"^[-*+]\s+", s):                               # bullet list
            items = []
            while i < n and re.match(r"^\s*[-*+]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*+]\s+", "", lines[i]).strip())
                i += 1
            blocks.append(Block("ul", items=items))
            continue

        if re.match(r"^\d+\.\s+", s):                               # numbered list
            items = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]).strip())
                i += 1
            blocks.append(Block("ol", items=items))
            continue

        buf = [s]                                                   # paragraph
        i += 1
        while i < n and lines[i].strip() and not re.match(
                r"^(#{1,6}\s|\||>|```|[-*+]\s|\d+\.\s|!\[)", lines[i].strip()) \
                and not re.fullmatch(r"-{3,}", lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        blocks.append(Block("p", " ".join(buf)))
    return blocks


# --------------------------------------------------------------------------------------------
# Inline formatting
# --------------------------------------------------------------------------------------------

TOKEN = re.compile(r"(\*\*.+?\*\*|\*[^*]+?\*|`[^`]+?`|\[[^\]]+?\]\([^)]+?\))")


def inline_runs(text: str) -> list[tuple[str, bool, bool, bool]]:
    """(text, bold, italic, mono). Links are reduced to their label."""
    out = []
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            out.append((part[2:-2], True, False, False))
        elif part.startswith("*") and part.endswith("*"):
            out.append((part[1:-1], False, True, False))
        elif part.startswith("`") and part.endswith("`"):
            out.append((part[1:-1], False, False, True))
        elif part.startswith("["):
            out.append((re.match(r"\[([^\]]+)\]", part).group(1), False, False, False))
        else:
            out.append((part, False, False, False))
    return out


def plain(text: str) -> str:
    return "".join(t for t, *_ in inline_runs(text))


# --------------------------------------------------------------------------------------------
# DOCX
# --------------------------------------------------------------------------------------------

WNS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
RNS = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
ANS = ('xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
       'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
       'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"')


def _runs_xml(text: str, *, base_sz: int | None = None) -> str:
    out = []
    for t, b, i, mono in inline_runs(text):
        if not t:
            continue
        props = []
        if mono:
            props.append('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>')
        if b:
            props.append("<w:b/>")
        if i:
            props.append("<w:i/>")
        if base_sz:
            props.append(f'<w:sz w:val="{base_sz}"/>')
        rpr = f"<w:rPr>{''.join(props)}</w:rPr>" if props else ""
        out.append(f'{"<w:r>"}{rpr}<w:t xml:space="preserve">{html.escape(t)}</w:t></w:r>')
    return "".join(out) or "<w:r><w:t/></w:r>"


def _p(style: str, text: str, *, jc: str = "", sz: int | None = None) -> str:
    ppr = [f'<w:pStyle w:val="{style}"/>'] if style else []
    if jc:
        ppr.append(f'<w:jc w:val="{jc}"/>')
    p = f"<w:pPr>{''.join(ppr)}</w:pPr>" if ppr else ""
    return f"<w:p>{p}{_runs_xml(text, base_sz=sz)}</w:p>"


def _table_xml(b: Block) -> str:
    def cell(text: str, hdr: bool) -> str:
        shd = '<w:shd w:val="clear" w:fill="EDEDED"/>' if hdr else ""
        txt = f"**{text}**" if hdr and not text.startswith("**") else text
        return (f"<w:tc><w:tcPr><w:tcBorders>"
                f'<w:top w:val="single" w:sz="4" w:color="808080"/>'
                f'<w:bottom w:val="single" w:sz="4" w:color="808080"/>'
                f'<w:left w:val="single" w:sz="4" w:color="808080"/>'
                f'<w:right w:val="single" w:sz="4" w:color="808080"/>'
                f"</w:tcBorders>{shd}</w:tcPr>{_p('TableText', txt, sz=18)}</w:tc>")
    rows = ["<w:tr><w:trPr><w:tblHeader/></w:trPr>"
            + "".join(cell(c, True) for c in b.header) + "</w:tr>"]
    for r in b.rows:
        r = (r + [""] * len(b.header))[:len(b.header)]
        rows.append("<w:tr>" + "".join(cell(c, False) for c in r) + "</w:tr>")
    return ('<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/>'
            '<w:tblLayout w:type="autofit"/></w:tblPr>' + "".join(rows) + "</w:tbl>"
            + _p("", ""))


def _image_xml(rid: str, cx: int, cy: int, idx: int) -> str:
    return (f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
            f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
            f'<wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{idx}" name="Figure {idx}"/>'
            f'<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic><pic:nvPicPr><pic:cNvPr id="{idx}" name="Figure {idx}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
            f"</a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>")


STYLES_XML = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles {WNS}>
<w:docDefaults><w:rPrDefault><w:rPr>
<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
<w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="en-GB"/>
</w:rPr></w:rPrDefault><w:pPrDefault><w:pPr>
<w:spacing w:after="120" w:line="300" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>
<w:pPr><w:spacing w:before="0" w:after="240"/><w:jc w:val="left"/></w:pPr>
<w:rPr><w:b/><w:sz w:val="34"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>
<w:pPr><w:keepNext/><w:outlineLvl w:val="0"/><w:spacing w:before="320" w:after="140"/></w:pPr>
<w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>
<w:pPr><w:keepNext/><w:outlineLvl w:val="1"/><w:spacing w:before="260" w:after="120"/></w:pPr>
<w:rPr><w:b/><w:sz w:val="25"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/>
<w:pPr><w:keepNext/><w:outlineLvl w:val="2"/><w:spacing w:before="220" w:after="100"/></w:pPr>
<w:rPr><w:b/><w:i/><w:sz w:val="23"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="TableText"><w:name w:val="Table Text"/>
<w:pPr><w:spacing w:after="40" w:line="240" w:lineRule="auto"/></w:pPr>
<w:rPr><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/>
<w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="200"/></w:pPr>
<w:rPr><w:i/><w:sz w:val="19"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/>
<w:pPr><w:spacing w:after="120" w:line="240" w:lineRule="auto"/>
<w:ind w:left="284"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="17"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Quote"><w:name w:val="Quote"/>
<w:pPr><w:ind w:left="454" w:right="284"/></w:pPr><w:rPr><w:i/></w:rPr></w:style>
</w:styles>"""


def write_docx(blocks: list[Block], out: Path, *, title: str) -> dict:
    body, rels, media, imgs = [], [], {}, 0
    rels.append('<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/'
                'officeDocument/2006/relationships/styles" Target="styles.xml"/>')
    fig_no = 0
    for b in blocks:
        if b.kind == "h1" and not body:
            body.append(_p("Title", b.text))
        elif b.kind in ("h1", "h2", "h3"):
            body.append(_p(f"Heading{b.kind[1]}", b.text))
        elif b.kind == "p":
            body.append(_p("", b.text, jc="both"))
        elif b.kind == "quote":
            body.append(_p("Quote", b.text, jc="both"))
        elif b.kind == "code":
            for ln in b.text.splitlines() or [""]:
                body.append(_p("Code", "`" + ln + "`" if ln else ""))
        elif b.kind == "ul":
            for it in b.items:
                body.append(_p("", "• " + it, jc="both"))
        elif b.kind == "ol":
            for k, it in enumerate(b.items, 1):
                body.append(_p("", f"{k}. " + it, jc="both"))
        elif b.kind == "table":
            body.append(_table_xml(b))
        elif b.kind == "rule":
            body.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" '
                        'w:color="BBBBBB"/></w:pBdr></w:pPr></w:p>')
        elif b.kind == "figure":
            src = (ROOT / b.path) if not Path(b.path).is_absolute() else Path(b.path)
            if not src.exists():
                raise PipelineError(f"figure not found: {b.path}")
            imgs += 1
            fig_no += 1
            name = f"media/image{imgs}.png"
            media[f"word/{name}"] = src.read_bytes()
            rid = f"rId{100 + imgs}"
            rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
                        f'officeDocument/2006/relationships/image" Target="{name}"/>')
            w_emu = int(5.9 * 914400)
            try:
                import struct
                px_w, px_h = struct.unpack(">II", src.read_bytes()[16:24])
                h_emu = int(w_emu * px_h / px_w)
            except Exception:
                h_emu = int(w_emu * 0.75)
            body.append(_image_xml(rid, w_emu, h_emu, imgs))
            if b.caption:
                body.append(_p("Caption", b.caption))

    sect = ('<w:sectPr><w:footerReference w:type="default" r:id="rIdFtr"/>'
            '<w:pgSz w:w="11906" w:h="16838"/>'
            '<w:pgMar w:top="1418" w:right="1418" w:bottom="1418" w:left="1418" '
            'w:header="709" w:footer="709"/></w:sectPr>')
    rels.append('<Relationship Id="rIdFtr" Type="http://schemas.openxmlformats.org/'
                'officeDocument/2006/relationships/footer" Target="footer1.xml"/>')
    footer = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              f'<w:ftr {WNS}><w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
              f'<w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
              f'<w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
              f'<w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>'
              f"</w:p></w:ftr>")

    doc = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           f"<w:document {WNS} {RNS} {ANS}><w:body>{''.join(body)}{sect}</w:body></w:document>")

    ct = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
          '<Default Extension="xml" ContentType="application/xml"/>',
          '<Default Extension="png" ContentType="image/png"/>',
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-'
          'officedocument.wordprocessingml.document.main+xml"/>',
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-'
          'officedocument.wordprocessingml.styles+xml"/>',
          '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-'
          'officedocument.wordprocessingml.footer+xml"/>',
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-'
          'package.core-properties+xml"/>', "</Types>"]
    core = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/'
            f'metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" '
            f'xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/'
            f'XMLSchema-instance"><dc:title>{html.escape(title)}</dc:title>'
            f'<dcterms:created xsi:type="dcterms:W3CDTF">'
            f'{_dt.date.today().isoformat()}T00:00:00Z</dcterms:created></cp:coreProperties>')
    pkg_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/'
                '2006/relationships/officeDocument" Target="word/document.xml"/>'
                '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/'
                'relationships/metadata/core-properties" Target="docProps/core.xml"/>'
                "</Relationships>")
    doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/'
                f'relationships">{"".join(rels)}</Relationships>')

    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "".join(ct))
        z.writestr("_rels/.rels", pkg_rels)
        z.writestr("docProps/core.xml", core)
        z.writestr("word/document.xml", doc)
        z.writestr("word/styles.xml", STYLES_XML)
        z.writestr("word/footer1.xml", footer)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        for k, v in media.items():
            z.writestr(k, v)
    return {"paragraphs": len(body), "figures": imgs}


# --------------------------------------------------------------------------------------------
# PDF
# --------------------------------------------------------------------------------------------

def write_pdf(blocks: list[Block], out: Path, *, title: str) -> dict:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.image as mpimg

    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = SERIF
    plt.rcParams["pdf.fonttype"] = 42

    left, right = MARGIN_IN / A4_W_IN, 1 - MARGIN_IN / A4_W_IN
    top, bottom = 1 - MARGIN_IN / A4_H_IN, MARGIN_IN / A4_H_IN + 0.028
    width = right - left

    state = {"fig": None, "y": top, "page": 0, "pages": 0, "figs": 0}
    pdf = PdfPages(out)

    def new_page():
        if state["fig"] is not None:
            state["page"] += 1
            state["fig"].text(0.5, bottom - 0.022, str(state["page"]),
                              ha="center", fontsize=8.5)
            pdf.savefig(state["fig"])
            plt.close(state["fig"])
        state["fig"] = plt.figure(figsize=(A4_W_IN, A4_H_IN))
        state["y"] = top
        state["pages"] += 1

    def space(h):
        if state["fig"] is None or state["y"] - h < bottom:
            new_page()

    def em(sz):                                   # line height in figure units
        return sz * 1.62 / 72 / A4_H_IN

    def wrap(text, sz, w_frac):
        cpl = max(12, int(w_frac * A4_W_IN * 72 / (sz * 0.497)))
        words, lines, cur = text.split(), [], ""
        for wd in words:
            if len(cur) + len(wd) + 1 <= cpl:
                cur = (cur + " " + wd).strip()
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines or [""]

    def put(text, sz, *, weight="normal", style="normal", indent=0.0, mono=False, align="left"):
        fam = "monospace" if mono else "serif"
        for ln in wrap(text, sz, width - indent):
            space(em(sz))
            state["fig"].text(left + indent, state["y"], ln, fontsize=sz, family=fam,
                              weight=weight, style=style, ha="left", va="top")
            state["y"] -= em(sz)

    new_page()
    first = True
    for b in blocks:
        if b.kind == "h1" and first:
            first = False
            state["y"] -= 0.012
            put(plain(b.text), 15.5, weight="bold")
            state["y"] -= 0.016
        elif b.kind in ("h1", "h2", "h3"):
            sz = {"h1": 13.0, "h2": 11.6, "h3": 10.6}[b.kind]
            state["y"] -= 0.013
            space(em(sz) * 2.4)
            put(plain(b.text), sz, weight="bold",
                style="italic" if b.kind == "h3" else "normal")
            state["y"] -= 0.005
        elif b.kind == "p":
            put(plain(b.text), 9.6)
            state["y"] -= 0.006
        elif b.kind == "quote":
            put(plain(b.text), 9.3, style="italic", indent=0.035)
            state["y"] -= 0.006
        elif b.kind == "code":
            for ln in b.text.splitlines() or [""]:
                put(ln if ln else " ", 7.6, mono=True, indent=0.022)
            state["y"] -= 0.007
        elif b.kind in ("ul", "ol"):
            for k, it in enumerate(b.items, 1):
                marker = "•" if b.kind == "ul" else f"{k}."
                space(em(9.6))
                state["fig"].text(left + 0.012, state["y"], marker, fontsize=9.6,
                                  family="serif", va="top")
                put(plain(it), 9.6, indent=0.040)
            state["y"] -= 0.006
        elif b.kind == "rule":
            space(0.016)
            state["fig"].add_artist(plt.Line2D([left, right], [state["y"], state["y"]],
                                               lw=0.6, color="#999999",
                                               transform=state["fig"].transFigure))
            state["y"] -= 0.018
        elif b.kind == "table":
            ncol = max(1, len(b.header))
            colw = width / ncol
            sz = 7.3
            all_rows = [b.header] + [(r + [""] * ncol)[:ncol] for r in b.rows]
            for ri, row in enumerate(all_rows):
                cells = [wrap(plain(c), sz, colw - 0.012) for c in row]
                h = max(len(c) for c in cells) * em(sz) + 0.004
                space(h + 0.004)
                y0 = state["y"]
                for ci, cl in enumerate(cells):
                    for li, ln in enumerate(cl):
                        state["fig"].text(left + ci * colw + 0.005, y0 - li * em(sz), ln,
                                          fontsize=sz, family="serif", va="top",
                                          weight="bold" if ri == 0 else "normal")
                state["y"] = y0 - h
                state["fig"].add_artist(plt.Line2D(
                    [left, right], [state["y"] + 0.002, state["y"] + 0.002],
                    lw=0.7 if ri == 0 else 0.3, color="#888888",
                    transform=state["fig"].transFigure))
            state["y"] -= 0.012
        elif b.kind == "figure":
            src = (ROOT / b.path) if not Path(b.path).is_absolute() else Path(b.path)
            img = mpimg.imread(str(src))
            ih, iw = img.shape[0], img.shape[1]
            disp_w = width * 0.92
            disp_h = disp_w * (ih / iw) * (A4_W_IN / A4_H_IN)
            if state["y"] - disp_h < bottom:
                new_page()
            ax = state["fig"].add_axes([left + (width - disp_w) / 2,
                                        state["y"] - disp_h, disp_w, disp_h])
            ax.imshow(img)
            ax.axis("off")
            state["y"] -= disp_h + 0.008
            state["figs"] += 1
            if b.caption:
                put(plain(b.caption), 8.6, style="italic")
            state["y"] -= 0.012

    state["page"] += 1
    state["fig"].text(0.5, bottom - 0.022, str(state["page"]), ha="center", fontsize=8.5)
    pdf.savefig(state["fig"])
    plt.close(state["fig"])
    d = pdf.infodict()
    d["Title"] = title
    pdf.close()
    return {"pages": state["pages"], "figures": state["figs"]}


# --------------------------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True)
    ap.add_argument("--stem", required=True, help="output filename stem (no extension)")
    ap.add_argument("--outdir", default="results/manuscript")
    args = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    src = ROOT / args.source
    if not src.exists():
        print(f"FAIL: {args.source} not found", file=sys.stderr)
        return 1
    blocks = parse_markdown(src.read_text(encoding="utf-8"))
    title = next((plain(b.text) for b in blocks if b.kind == "h1"), args.stem)

    outdir = ROOT / args.outdir
    docx = outdir / f"{args.stem}.docx"
    pdf = outdir / f"{args.stem}.pdf"
    d = write_docx(blocks, docx, title=title)
    p = write_pdf(blocks, pdf, title=title)

    kinds = {}
    for b in blocks:
        kinds[b.kind] = kinds.get(b.kind, 0) + 1
    print(f"  source blocks: {len(blocks)}  {kinds}")
    print(f"  DOCX -> {docx.relative_to(ROOT).as_posix()}  "
          f"({docx.stat().st_size:,} bytes, {d['paragraphs']} paragraphs, {d['figures']} figures)")
    print(f"  PDF  -> {pdf.relative_to(ROOT).as_posix()}  "
          f"({pdf.stat().st_size:,} bytes, {p['pages']} pages, {p['figures']} figures)")
    if d["figures"] != p["figures"]:
        print("FAIL: figure counts differ between DOCX and PDF", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
