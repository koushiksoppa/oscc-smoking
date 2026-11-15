"""Independent audit of the generated manuscript deliverables.

    python -m scripts.reporting.audit_deliverables

Inspects the produced files themselves rather than trusting the build log: DOCX text is read from
the OOXML `w:t` elements, PDF text is recovered by decompressing the content streams and decoding
the UTF-16BE string operands. The two are then compared for content equivalence, and every
numerical claim is checked against the repository's own data.
"""
from __future__ import annotations

import csv
import html
import pathlib
import random
import re
import sys
import zipfile
import zlib
from collections import Counter

from scripts.common.config import ROOT

MAN = "Smoked_Tobacco_and_Oral_Cavity_SCC_Systematic_Review_Final"
SUP = "Smoked_Tobacco_and_Oral_Cavity_SCC_Supplementary_Material"
OUT = ROOT / "results" / "manuscript"

PDF_STRING = re.compile(rb"\((?:\\.|[^\\()])*\)", re.S)
PDF_ESCAPE = re.compile(rb"\\([()\\])")
WT = re.compile(r"<w:t(?![^>]*/>)[^>]*>(.*?)</w:t>", re.S)


def docx_paragraphs(path: pathlib.Path) -> list[str]:
    """Text of each w:p paragraph, via a real XML parser.

    Regex extraction is unsafe here: an empty self-closing <w:t/> has no closing tag, so a
    non-greedy capture runs on to the next </w:t> and swallows markup into the "text". Paragraphs
    are kept separate so that a heading, which carries no terminal punctuation, is never
    concatenated with the body text that follows it.
    """
    import xml.etree.ElementTree as ET
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    paras = []
    for para in root.iter(f"{ns}p"):
        txt = re.sub(r"\s+", " ", " ".join(e.text or "" for e in para.iter(f"{ns}t"))).strip()
        if txt:
            paras.append(txt)
    return paras


def docx_text(path: pathlib.Path) -> str:
    return " ".join(docx_paragraphs(path))


def pdf_text(path: pathlib.Path) -> str:
    raw = path.read_bytes()
    parts: list[str] = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", raw, re.S):
        try:
            blob = zlib.decompress(m.group(1))
        except Exception:
            continue
        for tok in PDF_STRING.findall(blob):
            s = PDF_ESCAPE.sub(rb"\1", tok[1:-1])
            parts.append(s.decode("utf-16-be", "replace"))
    return re.sub(r"\s+", " ", " ".join(parts)).replace("\x00", "")


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def present(sentence: str, pdf: str) -> bool:
    """Is this DOCX sentence in the PDF text?

    A sentence that straddles a page break has the running footer (the page number) spliced into
    the middle of it in the extraction stream, so the whole span never matches as one piece. The
    split point is located by binary search on the longest matching prefix, and the remainder is
    then required to appear as well. A sentence genuinely absent from the PDF matches neither.
    """
    k = norm(sentence)
    if k in pdf:
        return True
    lo, hi = 0, len(k)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if k[:mid] in pdf:
            lo = mid
        else:
            hi = mid - 1
    return lo >= 20 and len(k) - lo >= 10 and k[lo:] in pdf


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    fails = 0

    def check(label, cond, detail=""):
        nonlocal fails
        if not cond:
            fails += 1
        print(f"  {'OK  ' if cond else '** FAIL **'} {label}{('  ' + detail) if detail else ''}")

    print("=== 2. CROSS-FORMAT CONSISTENCY ===")
    for stem in (MAN, SUP):
        d, p = OUT / f"{stem}.docx", OUT / f"{stem}.pdf"
        D, P = norm(docx_text(d)), norm(pdf_text(p))
        print(f"\n  -- {stem[:52]} --")
        print(f"     DOCX normalised chars {len(D):,} | PDF {len(P):,} | coverage {len(P)/max(1,len(D)):.3f}")
        sents = [s.strip() for para in docx_paragraphs(d)
                 for s in re.split(r"(?<=[.;:])\s+", para) if len(s.strip()) > 45]
        random.seed(7)
        sample = random.sample(sents, min(80, len(sents)))
        hit = sum(1 for s in sample if present(s, P))
        check(f"sampled DOCX prose present in PDF ({len(sample)} sentences)",
              hit == len(sample), f"{hit}/{len(sample)}")
        items = ["Abstract", "Keywords", "Introduction", "Methods", "Results", "Discussion",
                 "Conclusion", "References", "Declarations", "Supplementary"] if stem == MAN else \
                ["Search strategies", "Blinded verification sample", "Decision record",
                 "Extraction schema", "Reporting checklists"]
        for it in items:
            k = norm(it)
            check(f"both formats contain '{it}'", k in D and k in P, f"docx={k in D} pdf={k in P}")

    print("\n=== 3. SCIENTIFIC ACCURACY — manuscript claims vs repository data ===")
    from scripts.screening import prisma, verify_sample as vs
    f = prisma.gather()
    ta = list(csv.DictReader(open(ROOT / "data/screening/screening_ta.csv",
                                  encoding="utf-8", newline="")))
    ft = list(csv.DictReader(open(ROOT / "data/screening/screening_ft.csv",
                                  encoding="utf-8", newline="")))
    sm = list(csv.DictReader(open(ROOT / "data/screening/verification_sample.csv",
                                  encoding="utf-8", newline="")))
    rc = Counter(r["reason_code"] for r in ta if r["reason_code"])
    cells = sum(1 for r in sm for x in vs.RESPONSE if (r[x] or "").strip())
    D = norm(docx_text(OUT / f"{MAN}.docx"))

    truth = {
        "194 identified": f["identified"] == 194,
        "0 duplicates removed": f["duplicates_removed"] == 0,
        "194 unique reports": f["unique_reports"] == 194,
        "0 formal adjudications": f["ta_screened"] == 0 and f["ta_included"] == 0,
        "194 provisional classifications": f["ta_adopted"] == 194,
        "109 provisional exclusions": f["prov_excluded"] == 109,
        "85 provisional carry-forward": f["prov_included"] == 85,
        "85 provisional FT rows / 0 formally sought":
            f["ft_provisional_sought"] == 85 and f["ft_sought"] == 0,
        "0 full texts retrieved": sum(1 for r in ft if r["full_text_status"].strip()) == 0,
        "0 full-text eligibility decisions": sum(1 for r in ft if r["decision"].strip()) == 0,
        "0 included studies": not (ROOT / "data/extraction").exists(),
        "0 extracted estimates": not (ROOT / "data/extraction").exists(),
        "0 risk-of-bias assessments": not (ROOT / "data/extraction").exists(),
        "0 completed verification cells of 120": cells == 0 and len(sm) * 3 == 120,
        "exclusion reasons 63/33/10/2/1":
            [rc[k] for k in ("wrong_outcome", "wrong_design", "review_or_meta",
                             "not_english", "wrong_population")] == [63, 33, 10, 2, 1],
    }
    for k, v in truth.items():
        check(f"data: {k}", v)

    print("\n  -- the manuscript states these, verbatim --")
    for claim in ["Reports screened", "Studies included", "194 unique reports",
                  "109", "85", "0 of 120", "Not yet available", "Not performed"]:
        check(f"manuscript contains '{claim}'", norm(claim) in D)

    print("\n  -- prohibited representations --")
    bad = {
        "provisional described as completed screening":
            any(norm(s) in D for s in ["screening is complete", "screening was completed",
                                       "194 of 194 screened", "completed human screening"]),
        "claims a completed meta-analysis":
            any(norm(s) in D for s in ["meta-analysis was performed", "we pooled",
                                       "pooled estimate of", "meta-analysis was conducted"]),
        "fabricated statistics": bool(re.search(r"(OR\s*=\s*\d|I²\s*=\s*\d|p\s*[<=]\s*0\.\d)",
                                                docx_text(OUT / f"{MAN}.docx"))),
        "AI/vendor reference": bool(re.search(
            r"\bAI\b|Claude|Anthropic|ChatGPT|OpenAI|GPT-|Copilot|Gemini|\bLLM\b",
            docx_text(OUT / f"{MAN}.docx"))),
    }
    for k, v in bad.items():
        check(f"absent: {k}", not v)

    print("\n=== 4. EXTRACTION WORKBOOK ===")
    from scripts.extraction.schema import load_schema, load_rob_schema, STUDIES, ESTIMATES
    sch = load_schema()
    rob = load_rob_schema()
    wb = OUT / "extraction_workbook"
    for name, tbl, want in (("studies_template.csv", STUDIES, 34),
                            ("estimates_template.csv", ESTIMATES, 47)):
        rows = list(csv.reader(open(wb / name, encoding="utf-8", newline="")))
        hdr = rows[0]
        check(f"{name}: {want} columns", len(hdr) == want, f"found {len(hdr)}")
        check(f"{name}: matches schema exactly", hdr == list(sch.table(tbl).columns))
        check(f"{name}: ZERO data rows", len(rows) == 1, f"data rows={len(rows)-1}")
    rb_hdr = list(csv.reader(open(wb / "risk_of_bias_template.csv", encoding="utf-8", newline="")))[0]
    check("risk_of_bias_template.csv: matches schema exactly", rb_hdr == list(rob.columns))
    dd = list(csv.DictReader(open(wb / "data_dictionary.csv", encoding="utf-8", newline="")))
    total = sum(len(t.fields) for t in sch.tables.values()) + len(rob.fields)
    check(f"data_dictionary: all {total} fields defined", len(dd) == total, f"found {len(dd)}")
    check("data_dictionary: unresolved fields flagged",
          {r["field"] for r in dd if r["status"] == "unresolved"} ==
          {"comparator_type", "exposure_contrast", "tool", "domain", "judgement"})
    check("data_dictionary: documents the risk-of-bias sheet",
          {r["field"] for r in dd if r["table"] == "risk_of_bias"} == set(rob.columns))
    check("workbook README names the real generator",
          "scripts/reporting/build_workbook.py" in (wb / "README.md").read_text(encoding="utf-8"))
    rb = list(csv.reader(open(wb / "risk_of_bias_template.csv", encoding="utf-8", newline="")))
    check("risk_of_bias_template: ZERO rows", len(rb) == 1, f"data rows={len(rb)-1}")
    readme = (wb / "README.md").read_text(encoding="utf-8")
    check("workbook README states TEMPLATES ONLY", "TEMPLATES ONLY" in readme)
    flat = re.sub(r"\s+", " ", readme)
    check("workbook README states no study included", "nothing to extract" in flat)

    print(f"\n=== RESULT: {fails} failing check(s) ===")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
