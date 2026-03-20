---
name: docx
description: "Use this skill any time a .docx file is involved in any way — as input, output, or both. This includes: creating Word documents, executive summaries, blocker reports, stakeholder briefs, SOWs, or any business document; reading, parsing, or extracting text from any .docx file; editing, modifying, or updating existing Word documents; working with tables, headers, footers, styles, or sections. Trigger whenever the user mentions \"Word doc,\" \"Word document,\" \"docx,\" \".docx\", \"executive summary,\" \"stakeholder brief,\" or references a .docx filename. If a .docx file needs to be opened, created, or touched, use this skill."
---

# DOCX Skill

## Quick Reference

| Task | Method |
|------|--------|
| Read/extract text | `python -m markitdown document.docx` |
| Create from scratch | Read [creating.md](creating.md) |
| Edit existing | Read [editing.md](editing.md) |

---

## Dependencies

Managed via `uv` — no manual install needed. All commands use `uv run --with` for ephemeral dependency injection.

```bash
# Verify uv is available
uv --version  # requires uv (brew install uv)
```

No venvs, no `pip install`, no `--break-system-packages`. The `uv run --with` pattern fetches dependencies on-demand and caches them automatically.

---

## Reading Content

```bash
# Text extraction (preserves tables as markdown)
uv run --with "markitdown[docx]" markitdown document.docx

# Quick content check
uv run --with python-docx python3 -c "
from docx import Document
doc = Document('document.docx')
for p in doc.paragraphs:
    if p.text.strip():
        print(f'[{p.style.name}] {p.text[:100]}')
"
```

---

## Creating from Scratch

**Read [creating.md](creating.md) for the full Python generation guide.**

Use `python-docx` to generate styled Word documents programmatically. Write a standalone Python script, run it with `uv run --with python-docx`, then clean up the script.

---

## Editing Existing Documents

**Read [editing.md](editing.md) for full details.**

1. Extract text with `uv run --with "markitdown[docx]" markitdown`
2. Load with `python-docx` (via `uv run --with python-docx`), locate target paragraphs/tables
3. Modify content while preserving existing styles
4. Save to new file (never overwrite originals without asking)

---

## Design Standards — Executive Documents

**Don't create boring documents.** Plain text with default formatting won't impress a sales manager or executive. Every document should feel designed and intentional.

### Document Types & Approach

| Type | Tone | Color Weight | Tables | Callouts |
|------|------|-------------|--------|----------|
| **Blocker/Risk Report** | Urgent, clear | Red accents, navy base | Status tables with colored text | Red bold for critical items |
| **Executive Summary** | Confident, polished | Navy/blue base, subtle accents | Stakeholder directories | Quote-style guidance blocks |
| **SOW / Proposal** | Professional, structured | Conservative blue/gray | Scope tables, milestones | Numbered deliverables |
| **Stakeholder Brief** | Informative, scannable | Teal/green for positive, amber for risk | Contact tables | Key takeaway boxes |
| **Meeting Summary** | Action-oriented | Minimal color, bold headers | Action item tables | Decision callouts |

### Color Palettes

| Theme | Primary (Headings) | Accent (Tables/Highlights) | Alert | Use For |
|-------|--------------------|-----------------------------|-------|---------|
| **Executive** | `1B2A4A` navy | `2B579A` blue | `C0392B` red | Default for executive docs |
| **Conservative Banking** | `1A3C5E` dark blue | `4A7C9B` steel | `B8860B` gold | Financial clients |
| **Modern Tech** | `2D3436` charcoal | `0984E3` bright blue | `E17055` coral | Tech proposals |
| **Risk & Compliance** | `2C3E50` midnight | `E74C3C` red | `F39C12` amber | Blocker reports |
| **Growth & Success** | `27AE60` green | `2980B9` blue | `8E44AD` purple | Win reports, case studies |

### Typography Rules

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Document title | Calibri | 24-28pt | Bold | Primary palette color |
| Section heading (H2) | Calibri | 15-18pt | Bold | Primary or accent |
| Subsection (H3) | Calibri | 12-14pt | Bold | Accent color |
| Body text | Calibri | 10.5-11pt | Regular | `#333333` |
| Table header | Calibri | 10pt | Bold White | White on colored bg |
| Table body | Calibri | 9.5-10pt | Regular | `#333333` |
| Footer/metadata | Calibri | 8-9pt | Regular | `#999999` |
| Confidentiality tag | Calibri | 9pt | Bold | `#C0392B` red |

### Table Styling

Every table must have:
- **Colored header row** — white bold text on palette primary/accent background
- **Alternating row shading** — light tint (`#F2F6FA`) on even rows
- **Subtle borders** — thin internal lines (`#D0D0D0`), colored top/bottom borders matching header
- **No default Word grid** — override the default black gridlines

Status text in tables should use semantic colors:
| Status | Color | Hex |
|--------|-------|-----|
| OPEN / BLOCKED | Red bold | `E74C3C` |
| CRITICAL | Dark red bold | `C0392B` |
| PARTIAL / WARNING | Amber bold | `F39C12` |
| RESOLVED / COMPLETE | Green bold | `27AE60` |
| IN PROGRESS | Blue | `2B579A` |

### Avoid (Common Mistakes)

- Don't use default Word styles — always customize heading colors, sizes, and spacing
- Don't use black table borders — use the palette color for top/bottom, light gray for internal
- Don't center body text — left-align everything except the footer
- Don't forget alternating row shading — solid white tables look unpolished
- Don't use more than 2-3 colors — pick a palette and stick to it
- Don't skip the confidentiality tag — executive docs should always have it
- Don't put emojis in Word docs — use text labels (OPEN, CRITICAL) with color instead
- Don't use tiny margins — executives print these; 2cm side margins minimum
- Don't create one giant table — break content into multiple focused tables with headers between them

---

## QA (Required)

**Assume there are problems. Your job is to find them.**

### Content QA

```bash
uv run --with "markitdown[docx]" markitdown output.docx
```

Check for:
- Missing content or sections from the source material
- Typos or formatting artifacts
- Table alignment (markitdown renders tables as markdown — verify column count)
- Placeholder text that wasn't replaced

### Style QA

```bash
uv run --with python-docx python3 -c "
from docx import Document
doc = Document('output.docx')
for p in doc.paragraphs:
    if p.text.strip():
        style = p.style.name
        font = p.runs[0].font if p.runs else None
        size = font.size if font else 'inherited'
        print(f'[{style}] size={size} text={p.text[:60]}')
for i, t in enumerate(doc.tables):
    print(f'Table {i+1}: {len(t.rows)} rows x {len(t.columns)} cols')
"
```

Check for:
- All headings use custom styles (not default black Heading 1)
- Body text is 10.5-11pt Calibri
- Tables have the correct number of rows/columns
- No orphaned empty paragraphs

### Verification Loop

1. Generate document
2. Run content QA — verify all source material is present
3. Run style QA — verify fonts, sizes, colors
4. Open in Word or preview if possible
5. Fix any issues found
6. **Re-verify after fixes**

**Do not declare success until you've completed at least one QA cycle.**

---

## Converting to Other Formats

```bash
# DOCX → PDF (requires LibreOffice)
python scripts/office/soffice.py --headless --convert-to pdf output.docx

# DOCX → Markdown
uv run --with "markitdown[docx]" markitdown output.docx > output.md
```
