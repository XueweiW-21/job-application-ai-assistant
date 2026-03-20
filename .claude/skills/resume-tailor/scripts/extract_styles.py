"""
Extract formatting styles from a template DOCX into resume_styles.yml.

Reads your formatted resume template, classifies each paragraph by type
(name, contact, section header, bullet, etc.), and saves the formatting
to a YAML config. generate_docx.py then reads this config to produce
output that matches your template exactly.

Usage:
    python extract_styles.py <template.docx>

Output:
    resume_styles.yml in the same directory as the template.

Requires:
    pip install python-docx pyyaml
"""

import sys
import re
from pathlib import Path

try:
    from docx import Document
    from docx.oxml.ns import qn
except ImportError:
    print("ERROR: python-docx is not installed. Run: pip install python-docx")
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is not installed. Run: pip install pyyaml")
    sys.exit(1)


# ── Paragraph inspection helpers ─────────────────────────────────────────────

def _font_props(para):
    """Extract font properties from the first meaningful run."""
    for r in para.runs:
        if not r.text.strip():
            continue
        return {
            "font_name": r.font.name or None,
            "font_size": r.font.size.pt if r.font.size else None,
            "bold": bool(r.bold),
            "italic": bool(r.italic),
        }
    return {}


def _para_props(para):
    """Extract paragraph-level formatting."""
    pf = para.paragraph_format
    props = {}

    # Alignment
    align_map = {0: "left", 1: "center", 2: "right", 3: "justify"}
    props["alignment"] = align_map.get(para.alignment, "left") if para.alignment is not None else "left"

    # Spacing (stored as integer EMU)
    props["space_before"] = int(pf.space_before) if pf.space_before else 0
    props["space_after"] = int(pf.space_after) if pf.space_after else 0

    # Indentation
    props["left_indent"] = int(pf.left_indent) if pf.left_indent else 0
    props["first_line_indent"] = int(pf.first_line_indent) if pf.first_line_indent else 0

    # Keep with next
    props["keep_with_next"] = bool(pf.keep_with_next)

    # Right tab stop
    pPr = para._p.find(qn("w:pPr"))
    if pPr is not None:
        tabs_el = pPr.find(qn("w:tabs"))
        if tabs_el is not None:
            for tab in tabs_el.findall(qn("w:tab")):
                if tab.get(qn("w:val")) == "right":
                    props["right_tab_position"] = int(tab.get(qn("w:pos"), 0))

    # Bottom border
    if pPr is not None:
        pBdr = pPr.find(qn("w:pBdr"))
        props["bottom_border"] = pBdr is not None and pBdr.find(qn("w:bottom")) is not None
    else:
        props["bottom_border"] = False

    return props


def _bullet_props(para):
    """Extract bullet-specific properties (character and its font size)."""
    if para.runs and para.runs[0].text.strip():
        char = para.runs[0].text.strip()[0]
        if ord(char) > 127:  # non-ASCII = likely a bullet symbol
            result = {"bullet_char": char}
            if para.runs[0].font.size:
                result["bullet_font_size"] = para.runs[0].font.size.pt
            # Get text font from the second run (the actual content)
            if len(para.runs) > 1:
                if para.runs[1].font.size:
                    result["font_size"] = para.runs[1].font.size.pt
                if para.runs[1].font.name:
                    result["font_name"] = para.runs[1].font.name
            return result
    return {}


# ── Classification ───────────────────────────────────────────────────────────

def _has_bottom_border(para):
    pPr = para._p.find(qn("w:pPr"))
    if pPr is None:
        return False
    pBdr = pPr.find(qn("w:pBdr"))
    return pBdr is not None and pBdr.find(qn("w:bottom")) is not None


def classify_paragraphs(doc):
    """Walk through the document and classify each paragraph by element type."""
    classified = []
    current_section = None

    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if not text:
            classified.append((i, None, para))
            continue

        fp = _font_props(para)
        pp = _para_props(para)

        # Name: first paragraph, large bold centered
        if i == 0 and fp.get("font_size", 0) > 14 and fp.get("bold"):
            classified.append((i, "name", para))
            continue

        # Contact: contains @ or Email, centered
        if current_section is None and ("@" in text or "Email" in text) and pp.get("alignment") == "center":
            classified.append((i, "contact", para))
            continue

        # Section header: has bottom border or is all-caps bold
        if _has_bottom_border(para) or (text.isupper() and fp.get("bold") and len(text) < 40):
            lower = text.lower()
            if "education" in lower:
                current_section = "education"
            elif "skill" in lower:
                current_section = "skills"
            elif "experience" in lower:
                current_section = "experience"
            elif "publication" in lower:
                current_section = "publications"
            else:
                current_section = lower
            classified.append((i, "section_header", para))
            continue

        # Within Education
        if current_section == "education":
            if fp.get("bold") and pp.get("right_tab_position"):
                classified.append((i, "institution", para))
            elif pp.get("left_indent", 0) > 0:
                classified.append((i, "education_detail", para))
            else:
                classified.append((i, "degree", para))
            continue

        # Within Skills
        if current_section == "skills":
            classified.append((i, "skills_line", para))
            continue

        # Within Experience
        if current_section == "experience":
            if fp.get("bold") and pp.get("right_tab_position"):
                classified.append((i, "role_header", para))
            elif fp.get("italic") or (not fp.get("bold") and pp.get("left_indent", 0) == 0 and pp.get("keep_with_next")):
                classified.append((i, "job_title", para))
            elif pp.get("left_indent", 0) > 0:
                classified.append((i, "bullet", para))
            else:
                classified.append((i, "job_title", para))
            continue

        # Within Publications
        if current_section == "publications":
            classified.append((i, "publication", para))
            continue

        classified.append((i, "unknown", para))

    return classified


# ── Style extraction ─────────────────────────────────────────────────────────

def extract_styles(docx_path):
    doc = Document(docx_path)

    # Page margins
    sec = doc.sections[0]
    page = {
        "top_margin": int(sec.top_margin) if sec.top_margin else 914400,
        "bottom_margin": int(sec.bottom_margin) if sec.bottom_margin else 914400,
        "left_margin": int(sec.left_margin) if sec.left_margin else 914400,
        "right_margin": int(sec.right_margin) if sec.right_margin else 914400,
    }

    classified = classify_paragraphs(doc)

    # Collect first instance of each type
    styles = {}
    role_header_space_befores = []

    for idx, elem_type, para in classified:
        if elem_type is None or elem_type == "unknown":
            continue

        # Track all role_header space_before values to find first vs rest
        if elem_type == "role_header":
            sb = int(para.paragraph_format.space_before) if para.paragraph_format.space_before else 0
            role_header_space_befores.append(sb)

        if elem_type in styles:
            continue

        fp = _font_props(para)
        pp = _para_props(para)
        entry = {}
        entry.update(pp)
        entry.update(fp)

        # Bullet: extract bullet char and text font separately
        if elem_type == "bullet":
            bp = _bullet_props(para)
            entry.update(bp)

        # Clean up: remove None values and False booleans that are just noise
        entry = {k: v for k, v in entry.items() if v is not None}

        styles[elem_type] = entry

    # Role header: detect first_space_before (first role often has extra space)
    if "role_header" in styles and len(role_header_space_befores) > 1:
        styles["role_header"]["first_space_before"] = role_header_space_befores[0]
        # Use second role's space_before as the standard
        styles["role_header"]["space_before"] = role_header_space_befores[1]

    # Bullet: detect last_space_after by scanning last bullet before each role
    bullet_space_afters = []
    prev_was_bullet = False
    for idx, elem_type, para in classified:
        if elem_type == "bullet":
            sa = int(para.paragraph_format.space_after) if para.paragraph_format.space_after else 0
            bullet_space_afters.append(sa)
            prev_was_bullet = True
        else:
            prev_was_bullet = False

    if "bullet" in styles and bullet_space_afters:
        # The non-zero one at the end of a group is the "last" spacing
        last_values = [v for v in bullet_space_afters if v > 0]
        if last_values:
            styles["bullet"]["last_space_after"] = last_values[0]

    return {"page": page, "styles": styles}


# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_styles.py <template.docx>")
        sys.exit(1)

    docx_path = sys.argv[1]
    if not Path(docx_path).exists():
        print(f"ERROR: {docx_path} not found")
        sys.exit(1)

    result = extract_styles(docx_path)

    output_path = Path(docx_path).parent / "resume_styles.yml"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Resume formatting styles extracted from template.\n")
        f.write("# Edit values to fine-tune. Re-run extract_styles.py to regenerate.\n")
        f.write(f"# Source: {Path(docx_path).name}\n\n")
        yaml.dump(result, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"Styles extracted to: {output_path}")
    print(f"Found {len(result['styles'])} element types:")
    for name in result["styles"]:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
