#!/usr/bin/env python3
"""Generate PDF from docs/TECHNICAL_CONTEXT.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "docs" / "TECHNICAL_CONTEXT.md"
PDF_PATH = ROOT / "docs" / "Technical-Context-Enterprise-Visual-Intelligence-API.pdf"


class ContextPDF(FPDF):
    def footer(self) -> None:
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}", align="C")


def sanitize(text: str) -> str:
    replacements = {
        "\u2014": "-",
        "\u2013": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2192": "->",
        "\u2193": "v",
        "\u2502": "|",
        "\u2514": "L",
        "\u251c": "|-",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def write_wrapped(pdf: ContextPDF, text: str, size: int = 10, style: str = "") -> None:
    pdf.set_font("Helvetica", style, size)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(pdf.epw, size * 0.45, sanitize(text))


def render_markdown(md_path: Path, pdf_path: Path) -> None:
    lines = md_path.read_text(encoding="utf-8").splitlines()
    pdf = ContextPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.set_margins(18, 18, 18)

    in_code = False
    code_buf: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                pdf.set_font("Courier", "", 8)
                pdf.set_fill_color(245, 245, 245)
                block = "\n".join(code_buf)
                pdf.multi_cell(pdf.epw, 4, sanitize(block), fill=True)
                code_buf = []
                in_code = False
                pdf.ln(2)
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_buf.append(line)
            i += 1
            continue

        if not stripped:
            pdf.ln(3)
            i += 1
            continue

        if stripped == "---":
            pdf.ln(2)
            y = pdf.get_y()
            pdf.set_draw_color(200, 200, 200)
            pdf.line(18, y, pdf.w - 18, y)
            pdf.ln(4)
            i += 1
            continue

        if stripped.startswith("# "):
            pdf.ln(2)
            write_wrapped(pdf, stripped[2:], size=16, style="B")
            pdf.ln(2)
            i += 1
            continue

        if stripped.startswith("## "):
            pdf.ln(4)
            write_wrapped(pdf, stripped[3:], size=13, style="B")
            pdf.ln(2)
            i += 1
            continue

        if stripped.startswith("### "):
            pdf.ln(2)
            write_wrapped(pdf, stripped[4:], size=11, style="B")
            pdf.ln(1)
            i += 1
            continue

        if stripped.startswith("|") and "|" in stripped[1:]:
            table_rows: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = lines[i].strip()
                if not re.match(r"^\|[\s\-:|]+\|$", row):
                    cells = [c.strip() for c in row.strip("|").split("|")]
                    table_rows.append("  |  ".join(cells))
                i += 1
            for row in table_rows:
                write_wrapped(pdf, row, size=9)
            pdf.ln(2)
            continue

        if stripped.startswith("- "):
            bullet = re.sub(r"\*\*(.+?)\*\*", r"\1", stripped[2:])
            write_wrapped(pdf, f"  - {bullet}", size=10)
            i += 1
            continue

        text = re.sub(r"\*\*(.+?)\*\*", r"\1", stripped)
        write_wrapped(pdf, text, size=10)
        i += 1

    pdf.output(str(pdf_path))


def main() -> int:
    if not MD_PATH.is_file():
        print(f"Missing markdown: {MD_PATH}", file=sys.stderr)
        return 1
    render_markdown(MD_PATH, PDF_PATH)
    print(f"Wrote {PDF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
