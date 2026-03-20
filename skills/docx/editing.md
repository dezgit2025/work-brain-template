# Editing Existing Word Documents

## Workflow

1. Extract text to understand current content
2. Load with python-docx, inspect structure
3. Make targeted edits preserving existing styles
4. Save to a **new file** (never overwrite without asking)
5. Run QA

## Step 1 — Extract Text

```bash
uv run --with "markitdown[docx]" markitdown document.docx
```

This gives you a markdown representation of the content including tables.

## Step 2 — Inspect Structure

```python
from docx import Document

doc = Document('document.docx')

# List all paragraphs with styles
for i, p in enumerate(doc.paragraphs):
    if p.text.strip():
        runs_info = []
        for r in p.runs:
            runs_info.append(f"bold={r.bold} size={r.font.size} color={r.font.color.rgb}")
        print(f"[{i}] ({p.style.name}) {p.text[:80]}")
        for ri in runs_info:
            print(f"     {ri}")

# List all tables
for i, t in enumerate(doc.tables):
    print(f"\nTable {i}: {len(t.rows)} rows x {len(t.columns)} cols")
    for j, row in enumerate(t.rows):
        cells = [cell.text[:30] for cell in row.cells]
        print(f"  Row {j}: {cells}")
```

## Step 3 — Common Edit Operations

### Replace Text in a Paragraph (Preserve Formatting)

```python
# Find and replace within runs (preserves bold/color/size)
for p in doc.paragraphs:
    for run in p.runs:
        if 'old text' in run.text:
            run.text = run.text.replace('old text', 'new text')
```

### Add a New Section After a Heading

```python
from docx.shared import Pt, RGBColor

# Find the heading
for i, p in enumerate(doc.paragraphs):
    if 'Target Heading' in p.text:
        # Insert after this paragraph
        new_p = doc.paragraphs[i]._element
        from docx.oxml import OxmlElement
        from copy import deepcopy

        # Add paragraph after
        new_para = OxmlElement('w:p')
        new_p.addnext(new_para)
        # Now access it via doc and add runs
        break
```

### Update a Table Cell

```python
# Target table by index, row, column
table = doc.tables[0]
cell = table.rows[2].cells[1]  # row 2, col 1

# Clear and rewrite (preserves cell formatting)
cell.text = ''
p = cell.paragraphs[0]
run = p.add_run('Updated content')
run.font.size = Pt(9.5)
run.font.name = 'Calibri'
```

### Add a Row to an Existing Table

```python
table = doc.tables[0]
row = table.add_row()
row.cells[0].text = 'New item'
row.cells[1].text = 'Details'
```

### Change a Heading Color

```python
for p in doc.paragraphs:
    if p.style.name.startswith('Heading'):
        for run in p.runs:
            run.font.color.rgb = RGBColor(0x1B, 0x2A, 0x4A)
```

## Step 4 — Save

```python
# Always save to a new file first
doc.save('document-updated.docx')
```

## Gotchas

- **Runs split unpredictably** — Word splits text into multiple runs at formatting boundaries. A sentence like "Hello **world**" has 2+ runs. When searching, check `paragraph.text` first, then locate across runs.
- **Styles may be inherited** — if `run.font.size` is `None`, the size comes from the paragraph style or document default. Don't assume `None` means "no formatting."
- **Tables have nested paragraphs** — each cell contains one or more paragraphs. Access via `cell.paragraphs[0]`.
- **Images are inline shapes** — they live inside runs. Deleting a run deletes its image.
- **Headers/footers are per-section** — `doc.sections[0].header` is independent from `doc.sections[1].header`.
