#!/usr/bin/env python3
"""Rebuild Emmanuel_Tekle_CV.pdf from scripts/cv/content.yaml.

The October 2026 PDF was ReportLab platypus output (Helvetica, A4, no
embedded fonts). Side margins match that file: 18 mm plus SimpleDocTemplate's
default 6 pt frame padding. AZ-305 adds 26.5 pt. The same 26.5 pt is taken
back by shortening each inter-block gap by 1 pt and the top margin by 4.5 pt,
so the last line still sits about 41 pt above the page edge on a single page.

Run via scripts/cv/generate.sh. Output is byte-stable (invariant=1).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from xml.sax.saxutils import escape

import yaml
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[2]
CONTENT = Path(__file__).resolve().parent / "content.yaml"
OUTPUTS = (
    ROOT / "static" / "Emmanuel_Tekle_CV.pdf",
    ROOT / "Emmanuel_Tekle_CV.pdf",
)

NAVY = HexColor("#1F3A5F")
GRAY = HexColor("#666666")
INK = HexColor("#222222")
RULE = HexColor("#B8C4D3")

# Side margins match the October 2026 PDF (18 mm + the old 6 pt frame padding).
SIDE = 18 * mm + 6
# Original top margin was 9 mm + 6 pt (31.51 pt). 4.5 pt of that, plus 1 pt
# off every inter-block gap below, pays for the 26.5 pt AZ-305 block.
TOP = 9 * mm + 6 - 4.5
# Frame floor. The last line is placed well above this; it only stops a spill
# onto a second page.
BOTTOM = 28
# Gaps in the October 2026 PDF were 3 pt before a section, 2 pt under its
# rule, and 3 pt after an entry. Each is 1 pt tighter.
GAP_BEFORE_SECTION = 2
GAP_AFTER_RULE = 1
GAP_AFTER_ENTRY = 2
# Fixed timestamp so repeated runs write the same bytes. 8 Nov 2026 UTC,
# the day AZ-305 was earned. Not drawn on the page.
SOURCE_DATE_EPOCH = "1794096000"

BULLET = "•"


class CVDoc(SimpleDocTemplate):
    """SimpleDocTemplate with the frame padding folded into the margins."""

    def build(self, flowables, canvasmaker=canvas.Canvas):
        self._calc()
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            leftPadding=0,
            bottomPadding=0,
            rightPadding=0,
            topPadding=0,
            id="normal",
        )
        self.addPageTemplates(
            [
                PageTemplate(id="First", frames=frame, pagesize=self.pagesize),
                PageTemplate(id="Later", frames=frame, pagesize=self.pagesize),
            ]
        )
        BaseDocTemplate.build(self, flowables, canvasmaker=canvasmaker)


def styles():
    return {
        "name": ParagraphStyle(
            "name", fontName="Helvetica-Bold", fontSize=20, leading=23, textColor=NAVY
        ),
        "sub": ParagraphStyle(
            "sub", fontName="Helvetica", fontSize=10.5, leading=14, textColor=GRAY
        ),
        "contact": ParagraphStyle(
            "contact", fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=GRAY
        ),
        "section": ParagraphStyle(
            "section", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=NAVY
        ),
        "body": ParagraphStyle(
            "body", fontName="Helvetica", fontSize=8.3, leading=10.2, textColor=INK
        ),
        "job": ParagraphStyle(
            "job", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=INK
        ),
        "date": ParagraphStyle(
            "date",
            fontName="Helvetica",
            fontSize=8.5,
            leading=11.5,
            textColor=GRAY,
            alignment=TA_RIGHT,
        ),
        "meta": ParagraphStyle(
            "meta",
            fontName="Helvetica",
            fontSize=8.5,
            leading=11.5,
            textColor=GRAY,
            linkUnderline=1,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName="Helvetica",
            fontSize=8.3,
            leading=10.2,
            textColor=INK,
            bulletFontName="Helvetica",
            bulletFontSize=10,
            bulletIndent=2,
            bulletColor=INK,
            leftIndent=10,
            firstLineIndent=1.5,
        ),
        "skill_label": ParagraphStyle(
            "skill_label", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=INK
        ),
        "skill_value": ParagraphStyle(
            "skill_value", fontName="Helvetica", fontSize=8.3, leading=10.2, textColor=INK
        ),
    }


def xml_text(value: str) -> str:
    return escape(value)


def section_header(title: str, width: float, style: ParagraphStyle) -> Table:
    table = Table([[Paragraph(xml_text(title), style)]], colWidths=[width])
    table.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("LINEBELOW", (0, 0), (-1, -1), 0.7, RULE),
                ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
            ]
        )
    )
    return table


def title_row(title: str, when: str, width: float, style) -> Table:
    table = Table(
        [[Paragraph(xml_text(title), style["job"]), Paragraph(xml_text(when), style["date"])]],
        colWidths=[width * 0.72, width * 0.28],
    )
    table.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
            ]
        )
    )
    return table


def credential_line(credential_id: str, url: str, style) -> Paragraph:
    href = escape(url, {'"': "&quot;"})
    text = (
        f"Credential ID {xml_text(credential_id)} · "
        f'<link href="{href}" color="#1F3A5F">verify on Microsoft Learn</link>'
    )
    return Paragraph(text, style["meta"])


def add_entry(story, item: dict, width: float, style) -> None:
    story.append(title_row(item["title"], item["when"], width, style))
    if item.get("credential_id"):
        story.append(credential_line(item["credential_id"], item["verify_url"], style))
    elif item.get("meta"):
        story.append(Paragraph(xml_text(item["meta"]), style["meta"]))
    for bullet in item.get("bullets") or []:
        story.append(Paragraph(xml_text(bullet), style["bullet"], bulletText=BULLET))
    story.append(Spacer(1, GAP_AFTER_ENTRY))


def add_section(story, title: str, width: float, style) -> None:
    story.append(Spacer(1, GAP_BEFORE_SECTION))
    story.append(section_header(title, width, style["section"]))
    story.append(Spacer(1, GAP_AFTER_RULE))


def build_story(data: dict, width: float, style) -> list:
    story = [
        Paragraph(xml_text(data["name"]), style["name"]),
        Paragraph(xml_text(data["subtitle"]), style["sub"]),
    ]
    for line in data["contact"]:
        story.append(Paragraph(xml_text(line), style["contact"]))

    add_section(story, "PROFILE", width, style)
    story.append(Paragraph(xml_text(data["profile"]), style["body"]))

    add_section(story, "EXPERIENCE", width, style)
    for item in data["experience"]:
        add_entry(story, item, width, style)

    add_section(story, "PROJECTS", width, style)
    for item in data["projects"]:
        add_entry(story, item, width, style)

    add_section(story, "CERTIFICATIONS & EDUCATION", width, style)
    for item in data["certifications"]:
        add_entry(story, item, width, style)
    add_entry(story, data["education"], width, style)

    add_section(story, "SKILLS", width, style)
    rows = [
        [
            Paragraph(xml_text(row["label"]), style["skill_label"]),
            Paragraph(xml_text(row["value"]), style["skill_value"]),
        ]
        for row in data["skills"]
    ]
    skills = Table(rows, colWidths=[width * 0.24, width * 0.76])
    skills.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(skills)

    add_section(story, "LANGUAGES & INTERESTS", width, style)
    story.append(Paragraph(xml_text(data["languages"]), style["body"]))
    return story


def generate(path: Path) -> None:
    os.environ["SOURCE_DATE_EPOCH"] = SOURCE_DATE_EPOCH
    data = yaml.safe_load(CONTENT.read_text(encoding="utf-8"))
    width = A4[0] - 2 * SIDE
    doc = CVDoc(
        str(path),
        pagesize=A4,
        leftMargin=SIDE,
        rightMargin=SIDE,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        title="Emmanuel Tekle - CV",
        author="Emmanuel Tekle",
        invariant=1,
    )
    doc.build(build_story(data, width, styles()))


def main() -> int:
    tmp = OUTPUTS[0].with_suffix(".pdf.tmp")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    try:
        generate(tmp)
        payload = tmp.read_bytes()
        for dest in OUTPUTS:
            dest.write_bytes(payload)
    finally:
        tmp.unlink(missing_ok=True)
    print(f"wrote {len(payload)} bytes")
    for dest in OUTPUTS:
        print(dest.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
