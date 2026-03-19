"""
Generate an ATS-friendly .docx resume from a tailored markdown resume.

ATS design decisions:
  - Name and contact live in the document BODY (no Word header/footer).
  - Word header/footer is cleared entirely — name never repeats on page 2.
  - Section names use standard ATS keywords (Publications, not Select Publications).
  - Role header lines have keep_with_next=True to prevent orphaned headers.
  - No tables, text boxes, or columns — plain paragraphs only.

Usage:
    python generate_docx.py <input.md> <output.docx>

Requires:
    pip install python-docx pyyaml
"""

import sys
import re
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, Emu, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    print("ERROR: python-docx is not installed. Run: pip install python-docx")
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is not installed. Run: pip install pyyaml")
    sys.exit(1)


# ── Load configuration from profile.yml ──────────────────────────────────────

def load_profile():
    """Load user profile from profile.yml in the project root."""
    # Walk up from script location to find project root (where profile.yml lives)
    script_dir = Path(__file__).resolve().parent
    for parent in [script_dir] + list(script_dir.parents):
        profile_path = parent / "profile.yml"
        if profile_path.exists():
            with open(profile_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
    print("WARNING: profile.yml not found. Using defaults.")
    return {}


PROFILE       = load_profile()
FONT_NAME     = PROFILE.get("font", "Times New Roman")
CONTACT_LINKS = PROFILE.get("links", {})

# Look for a .docx template in the templates directory
_TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
_TEMPLATE_FILES = list(_TEMPLATES_DIR.glob("*.docx")) if _TEMPLATES_DIR.exists() else []
TEMPLATE_PATH = _TEMPLATE_FILES[0] if _TEMPLATE_FILES else None

# EMU spacing constants
INDENT_BULLET        = Emu(457200)
SPACE_ROLE_BEFORE    = Emu(76200)
SPACE_ROLE_AFTER     = Emu(38100)
SPACE_SUBROLE_BEFORE = Emu(38100)
SPACE_SUBROLE_AFTER  = Emu(19050)
SPACE_BULLET_AFTER   = Emu(0)
SPACE_BULLET_LAST    = Emu(38100)


# ── Core run factory ──────────────────────────────────────────────────────────

def run(paragraph, text, bold=False, italic=False, size=11.0):
    """Add a run. Always sets font name and size explicitly."""
    r = paragraph.add_run(text)
    r.font.name  = FONT_NAME
    r.font.size  = Pt(size)
    r.bold       = bold
    r.italic     = italic
    return r


def add_hyperlink(paragraph, text, url, size=10.0):
    """
    Add a hyperlink run to a paragraph.
    Renders as blue underlined text linking to url.
    """
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hl = OxmlElement("w:hyperlink")
    hl.set(qn("r:id"), r_id)

    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")

    rFonts = OxmlElement("w:rFonts")
    rFonts.set(qn("w:ascii"), FONT_NAME)
    rFonts.set(qn("w:hAnsi"), FONT_NAME)
    rPr.append(rFonts)

    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(size * 2)))
    szCs = OxmlElement("w:szCs")
    szCs.set(qn("w:val"), str(int(size * 2)))
    rPr.append(sz)
    rPr.append(szCs)

    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rPr.append(u)

    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")  # standard Word hyperlink blue
    rPr.append(color)

    new_run.append(rPr)
    t = OxmlElement("w:t")
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = text
    new_run.append(t)

    hl.append(new_run)
    paragraph._p.append(hl)


# ── XML helpers ───────────────────────────────────────────────────────────────

def add_bottom_border(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "4")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "000000")
    pBdr.append(bottom)
    existing = pPr.find(qn("w:pBdr"))
    if existing is not None:
        pPr.remove(existing)
    pPr.append(pBdr)


def add_right_tab(paragraph, pos_twips=9360):
    pPr = paragraph._p.get_or_add_pPr()
    tabs = OxmlElement("w:tabs")
    tab  = OxmlElement("w:tab")
    tab.set(qn("w:val"), "right")
    tab.set(qn("w:pos"), str(pos_twips))
    tabs.append(tab)
    pPr.append(tabs)


def clear_body(doc):
    body = doc.element.body
    for child in list(body):
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if tag in ("p", "tbl"):
            body.remove(child)


def clear_headers_footers(doc):
    """Remove all header/footer content so name never repeats on page 2."""
    for section in doc.sections:
        section.different_first_page_header_footer = False
        for hdr in (section.header, section.footer,
                    section.first_page_header, section.first_page_footer,
                    section.even_page_header, section.even_page_footer):
            try:
                for p in hdr.paragraphs:
                    p.clear()
            except Exception:
                pass


# ── Inline markdown renderer ──────────────────────────────────────────────────

def _render_inline(paragraph, text, default_bold=False, size=11.0):
    """Render **bold** and *italic* markdown markers into runs."""
    parts = re.split(r"(\*\*.*?\*\*|\*[^*]+\*)", text)
    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            run(paragraph, part[2:-2], bold=True, size=size)
        elif part.startswith("*") and part.endswith("*"):
            run(paragraph, part[1:-1], italic=True, size=size)
        elif part:
            run(paragraph, part, bold=default_bold, size=size)


# ── Header block (name + contact in body) ────────────────────────────────────

def _extract_link_label(token):
    """Return display text from a markdown [text](url) token, or the token itself."""
    m = re.match(r'\[([^\]]+)\]\([^)]+\)', token.strip())
    return m.group(1) if m else token.strip()


def add_name_contact_block(doc, md_text):
    """
    Render name, contact line, and location as body paragraphs.
    Known link labels from profile.yml are rendered as clickable hyperlinks.
    """
    name     = ""
    contact  = ""
    location = ""

    for line in md_text.split("\n"):
        s = line.strip()
        if s.startswith("# ") and not s.startswith("## "):
            name = s[2:].strip()
        elif not contact and "@" in s and not s.startswith("#"):
            contact = s
        elif not location and contact and not s.startswith("#") and not s.startswith("---") and s:
            location = s
            break

    if name:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(2)
        run(p, name, bold=True, size=20)

    if contact:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(0) if location else Pt(4)

        tokens = [t.strip() for t in contact.split("|")]
        for i, token in enumerate(tokens):
            if i > 0:
                run(p, " | ", size=10)
            label = _extract_link_label(token)
            if label in CONTACT_LINKS:
                add_hyperlink(p, label, CONTACT_LINKS[label], size=10)
            else:
                run(p, label, size=10)

    if location:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(4)
        run(p, location, size=10)


# ── Paragraph builders ────────────────────────────────────────────────────────

def add_section_header(doc, title):
    display = re.sub(r"^select\s+", "", title, flags=re.IGNORECASE)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Emu(76200)
    p.paragraph_format.space_after  = Emu(38100)
    run(p, display.upper(), bold=True)
    add_bottom_border(p)


def add_role_line(doc, company_text, date_text, is_first=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before    = Emu(88900) if is_first else SPACE_ROLE_BEFORE
    p.paragraph_format.space_after     = SPACE_ROLE_AFTER
    p.paragraph_format.keep_with_next  = True
    add_right_tab(p)
    run(p, company_text, bold=True)
    if date_text:
        run(p, "\t")
        run(p, date_text)


def add_subrole_line(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before   = SPACE_SUBROLE_BEFORE
    p.paragraph_format.space_after    = SPACE_SUBROLE_AFTER
    p.paragraph_format.keep_with_next = True
    _render_inline(p, text)


def add_bullet(doc, text, is_last=False):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent       = INDENT_BULLET
    p.paragraph_format.first_line_indent = Emu(-114300)
    p.paragraph_format.space_before      = Emu(0)
    p.paragraph_format.space_after       = SPACE_BULLET_LAST if is_last else SPACE_BULLET_AFTER
    run(p, "\u25cf  ", size=6)
    _render_inline(p, text)


def add_institution_line(doc, text, date_text=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before   = Pt(0)
    p.paragraph_format.space_after    = Pt(0)
    p.paragraph_format.keep_with_next = True
    if date_text:
        add_right_tab(p)
    _render_inline(p, text, default_bold=True)
    if date_text:
        run(p, "\t")
        run(p, date_text)


def add_indented_line(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent  = INDENT_BULLET
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(0)
    _render_inline(p, text)


def add_skills_line(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(0)
    m = re.match(r"(\*\*.*?\*\*:?)\s*(.*)", text)
    if m:
        label = m.group(1).strip("*").rstrip(":")
        items = m.group(2)
        run(p, label + ": ", bold=True)
        if items:
            run(p, items)
    else:
        run(p, text)


def add_publication(doc, citation, summary=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(0)
    _render_inline(p, citation, size=11)

    if summary:
        ps = doc.add_paragraph()
        ps.paragraph_format.space_before = Pt(0)
        ps.paragraph_format.space_after  = Pt(0)
        run(ps, summary, size=11)

    blank = doc.add_paragraph()
    blank.paragraph_format.space_before = Pt(0)
    blank.paragraph_format.space_after  = Pt(0)


# ── Section renderers ─────────────────────────────────────────────────────────

def render_education(doc, lines):
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if line.startswith("  ") or line.startswith("\t") or s.startswith("-"):
            text = s.lstrip("- ").strip()
            add_indented_line(doc, text)
        elif "|" in s:
            parts = s.split("|", 1)
            add_institution_line(doc, parts[0].strip(), date_text=parts[1].strip())
        else:
            add_institution_line(doc, s)


def render_skills(doc, lines):
    for line in lines:
        s = line.strip()
        if not s or s.startswith("---") or s.startswith("###"):
            continue
        if s.startswith("**") or "**" in s:
            add_skills_line(doc, s)
        elif s.startswith("-"):
            add_skills_line(doc, s.lstrip("- "))
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after  = Pt(0)
            run(p, s)


def render_experience(doc, lines):
    roles   = []
    current = None
    for line in lines:
        s = line.strip()
        if not s or s.startswith("---"):
            continue
        if s.startswith("### "):
            if current:
                roles.append(current)
            current = {"header": s[4:].strip(), "subtitle": None, "bullets": []}
        elif current is not None:
            if s.startswith("*") and s.endswith("*") and not s.startswith("**"):
                current["subtitle"] = s.strip("*").strip()
            elif s.startswith("- "):
                current["bullets"].append(s[2:].strip())
    if current:
        roles.append(current)

    for i, role in enumerate(roles):
        header    = role["header"]
        date_text = ""
        if "|" in header:
            parts       = header.rsplit("|", 1)
            header_text = parts[0].strip()
            date_text   = parts[1].strip()
        else:
            header_text = header

        add_role_line(doc, header_text, date_text, is_first=(i == 0))
        if role["subtitle"]:
            add_subrole_line(doc, role["subtitle"])
        bullets = role["bullets"]
        for j, bullet in enumerate(bullets):
            add_bullet(doc, bullet, is_last=(j == len(bullets) - 1))


def render_publications(doc, lines):
    citation = None
    summary  = None

    def flush():
        if citation:
            add_publication(doc, citation, summary)

    for line in lines:
        s = line.strip()
        if not s or s.startswith("---"):
            continue
        if re.match(r"^\d+\.\s", s):
            flush()
            citation = re.sub(r"^\d+\.\s+", "", s)
            summary  = None
        elif s.startswith("(") and s.endswith(")"):
            summary = s
        else:
            flush()
            citation = s
            summary  = None
    flush()


def render_section(doc, name, lines):
    add_section_header(doc, name)
    n = re.sub(r"^select\s+", "", name.upper().strip())
    if n == "EDUCATION":
        render_education(doc, lines)
    elif n in ("SKILLS SUMMARY", "SKILLS"):
        render_skills(doc, lines)
    elif n == "EXPERIENCE":
        render_experience(doc, lines)
    elif "PUBLICATION" in n:
        render_publications(doc, lines)
    else:
        for line in lines:
            s = line.strip()
            if s:
                p = doc.add_paragraph()
                run(p, s)


# ── Markdown parser ───────────────────────────────────────────────────────────

def parse_resume_md(md_text):
    sections        = []
    current_section = None
    current_lines   = []

    def flush():
        if current_section is not None:
            sections.append({"section": current_section, "lines": list(current_lines)})

    for line in md_text.split("\n"):
        s = line.strip()
        if s.startswith("# ") and not s.startswith("## "):
            continue
        if ("Email" in s or "Tel" in s or "@" in s) and not s.startswith("##") and not s.startswith("#"):
            continue
        if not s.startswith("#") and not s.startswith("##") and current_section is None and s and not s.startswith("---"):
            continue
        if s.startswith("## "):
            flush()
            current_section = s[3:].strip()
            current_lines   = []
        else:
            current_lines.append(line)

    flush()
    return sections


# ── ATS section ordering ──────────────────────────────────────────────────────

_ATS_ORDER = ["education", "skills summary", "skills", "experience",
              "publications", "select publications"]


def sort_sections_for_ats(sections):
    def key(s):
        n = re.sub(r"^select\s+", "", s["section"].lower().strip())
        for i, label in enumerate(_ATS_ORDER):
            if n == label or n.startswith(label):
                return i
        return 99
    return sorted(sections, key=key)


# ── Entry point ───────────────────────────────────────────────────────────────

def generate_docx(md_path, output_path):
    md_text = Path(md_path).read_text(encoding="utf-8")

    if TEMPLATE_PATH and TEMPLATE_PATH.exists():
        doc = Document(str(TEMPLATE_PATH))
        clear_headers_footers(doc)
        clear_body(doc)
    else:
        doc = Document()

    add_name_contact_block(doc, md_text)

    for section in sort_sections_for_ats(parse_resume_md(md_text)):
        render_section(doc, section["section"], section["lines"])

    doc.save(output_path)
    print(f"Resume saved: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_docx.py <input.md> <output.docx>")
        sys.exit(1)
    generate_docx(sys.argv[1], sys.argv[2])
