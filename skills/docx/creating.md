# Creating Word Documents from Scratch

## Workflow

1. Write a standalone Python script using `python-docx`
2. Run the script via `uv run --with python-docx python3 script.py`
3. Run QA (content + style checks from SKILL.md)
4. Delete the generation script (keep the workspace clean)

**No venvs or pip installs needed.** `uv run --with` fetches `python-docx` on-demand and caches it automatically.

## Boilerplate

```python
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

doc = Document()

# -- Page setup --
section = doc.sections[0]
section.page_width = Inches(8.5)
section.page_height = Inches(11)
section.top_margin = Cm(1.5)
section.bottom_margin = Cm(1.5)
section.left_margin = Cm(2.0)
section.right_margin = Cm(2.0)
```

## Style Configuration

Always configure styles before adding content:

```python
# Normal (body text)
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(10.5)
style.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
style.paragraph_format.space_after = Pt(4)
style.paragraph_format.line_spacing = 1.15

# Headings — customize colors per palette
PALETTE = {
    'primary': RGBColor(0x1B, 0x2A, 0x4A),
    'accent': RGBColor(0x2B, 0x57, 0x9A),
    'accent2': RGBColor(0x3A, 0x6E, 0xA5),
    'alert': RGBColor(0xC0, 0x39, 0x2B),
    'text': RGBColor(0x33, 0x33, 0x33),
    'muted': RGBColor(0x99, 0x99, 0x99),
}

heading_config = [
    (1, Pt(26), PALETTE['primary']),
    (2, Pt(16), PALETTE['accent']),
    (3, Pt(13), PALETTE['accent2']),
]
for level, size, color in heading_config:
    h = doc.styles[f'Heading {level}']
    h.font.name = 'Calibri'
    h.font.size = size
    h.font.color.rgb = color
    h.font.bold = True
    h.paragraph_format.space_before = Pt(0 if level == 1 else 18)
    h.paragraph_format.space_after = Pt(6)
```

## Table Helper Functions

### Cell Shading

```python
def set_cell_shading(cell, color_hex):
    """Set background color on a table cell. color_hex without #."""
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)
```

### Styled Table Builder

```python
def add_styled_table(doc, headers, rows, col_widths=None, accent_color="1B2A4A"):
    """Create a professionally styled table with colored header and alternating rows."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True

    # Header row — white text on colored background
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        run = p.add_run(header)
        run.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        run.font.name = 'Calibri'
        set_cell_shading(cell, accent_color)

    # Data rows — alternating shading
    for r_idx, row_data in enumerate(rows):
        for c_idx, cell_text in enumerate(row_data):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ''
            p = cell.paragraphs[0]
            run = p.add_run(str(cell_text))
            run.font.size = Pt(9.5)
            run.font.name = 'Calibri'
            run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
            if r_idx % 2 == 0:
                set_cell_shading(cell, "F2F6FA")

    # Column widths
    if col_widths:
        for row in table.rows:
            for i, width in enumerate(col_widths):
                row.cells[i].width = Inches(width)

    # Table borders — colored top/bottom, subtle internal
    tblPr = table._tbl.tblPr or parse_xml(f'<w:tblPr {nsdecls("w")}></w:tblPr>')
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="{accent_color}"/>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{accent_color}"/>'
        f'  <w:insideH w:val="single" w:sz="2" w:space="0" w:color="D0D0D0"/>'
        f'  <w:insideV w:val="single" w:sz="2" w:space="0" w:color="D0D0D0"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

    return table
```

## Common Patterns

### Confidentiality Tag

```python
p = doc.add_paragraph()
run = p.add_run('CONFIDENTIAL')
run.font.size = Pt(9)
run.font.color.rgb = PALETTE['alert']
run.font.name = 'Calibri'
run.bold = True
```

### Accent Divider

```python
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after = Pt(12)
run = p.add_run('\u2501' * 72)  # ━ character
run.font.size = Pt(6)
run.font.color.rgb = PALETTE['primary']
```

### Mixed-Style Paragraph (Bold Names, Red Alerts)

```python
p = doc.add_paragraph()
run = p.add_run('John Smith')
run.bold = True
run = p.add_run(' announced a ')
run = p.add_run('hard stop')
run.bold = True
run.font.color.rgb = PALETTE['alert']
run = p.add_run(' on all new projects.')
```

### Styled Bullet List

```python
items = [
    ('Item label', 'Description text'),
    ('Another item', 'More details here'),
]
for label, detail in items:
    p = doc.add_paragraph(style='List Bullet')
    run = p.add_run(label)
    run.bold = True
    run.font.size = Pt(10)
    run = p.add_run(f'  \u2014  {detail}')  # em dash
    run.font.size = Pt(10)
```

### Colored Status Text in Tables

```python
STATUS_COLORS = {
    'OPEN': 'E74C3C',
    'CRITICAL': 'C0392B',
    'PARTIAL': 'F39C12',
    'RESOLVED': '27AE60',
    'IN PROGRESS': '2B579A',
}

# After creating a table, color status cells:
for row in table.rows[1:]:  # skip header
    cell = row.cells[-1]  # last column = status
    status = cell.text.strip()
    if status in STATUS_COLORS:
        hex_color = STATUS_COLORS[status]
        for run in cell.paragraphs[0].runs:
            run.font.color.rgb = RGBColor(
                int(hex_color[0:2], 16),
                int(hex_color[2:4], 16),
                int(hex_color[4:6], 16)
            )
            run.bold = True
```

### Footer

```python
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('Confidential  \u2022  Client Name  \u2022  Month Year')
run.font.size = Pt(8)
run.font.color.rgb = PALETTE['muted']
run.font.name = 'Calibri'
```

## Save & Cleanup

```python
doc.save('/path/to/output.docx')
print(f"Saved: /path/to/output.docx")
```

Run: `uv run --with python-docx python3 /path/to/script.py`

After the script runs successfully, **delete the generation script** to keep the workspace clean.
