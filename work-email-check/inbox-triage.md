# Inbox Triage — Email Check Workflow

## Purpose
Scan inbox for unread/unanswered emails, categorize by priority, and display in a terminal-friendly format.

## How to Use
Tell your AI assistant: "run the inbox triage" — you'll be prompted to pick a lookback window:
- **Option 1) Full scan (default)** — 3 weeks lookback (chunked into 3 x 7-day queries)
- **Option 2) Quick scan** — 1 week lookback (single query)

---

## Execution Strategy — Chunked Queries

WorkIQ queries timeout (`MCP error -32001`) on large lookback windows.
**Solution: break multi-week scans into 7-day chunks, then merge results.**

### Full Scan (3 weeks) — 3 sequential chunks

Run the **Full Prompt** below 3 times, one chunk at a time. Wait for each to complete before starting the next.

| Chunk | Window | Date hint |
|-------|--------|-----------|
| 1 | "last 7 days" | Most recent week |
| 2 | "between 7 and 14 days ago (approximately {{DATE_14D}} to {{DATE_7D}})" | Middle week |
| 3 | "between 14 and 21 days ago (approximately {{DATE_21D}} to {{DATE_14D}})" | Oldest week |

Replace `{{DATE_*}}` with actual dates based on today's date.

### Quick Scan (1 week) — single query

Run the **Full Prompt** once with `{{LOOKBACK}} = "last 7 days"`.

### Per-Chunk Fallback (if a chunk times out)

If a chunk times out, retry that chunk ONCE with the **Simplified Prompt** (shorter, top-10 focus).
If the simplified prompt also times out, retry with the **Minimal Prompt**.
If all 3 levels fail for a chunk, skip it and note the gap in the report.
Wait 5 seconds between retries.

---

## Full Prompt

**Replace `{{LOOKBACK}}` with the chunk's time window.**

```
Show me all emails from {{LOOKBACK}} that I haven't responded to yet, or that seem important and need my attention. Be thorough — scan ALL emails in the window, not just the most recent ones. Include customer escalations and external requests even if they are older but still within the window. Exclude any emails with "[WORKIQ-SUMMARY]" in the subject.

For each email, use this exact format (no tables):

[number]) Subject Line
From: Sender full name
Date: date and time in {{TIMEZONE}}
Summary: 2-3 bullet points summarizing the email content, what's being asked, and what action is needed. Each bullet should be 3-4 sentences max.
Link: direct Outlook Web URL on its own line

Group emails into these categories, in this order:
🔴 Action Required — emails where I am directly asked a question or explicitly need to respond
🟠 Review Needed — emails with deliverables, decisions, or time-sensitive info directed at me
🟢 Informational — emails where I'm CC'd, FYI threads, automated reports, or no response expected

Only put emails in 🔴 if I am specifically and directly asked to do something or reply. Being CC'd or included in a group thread does NOT count as action required. Do NOT use markdown tables. Use a simple numbered list format optimized for narrow terminal display.
```

## Simplified Prompt (Fallback 1 — on timeout)

Used automatically when the full prompt times out for a chunk.

```
What are my most important unread or unanswered emails from {{LOOKBACK}}? List up to 10 emails with subject, sender, date, and a brief summary of what action is needed. Exclude any emails with "[WORKIQ-SUMMARY]" in the subject.

For each email, format as:
[number]) Subject Line
From: Sender name
Date: date in {{TIMEZONE}}
Summary: 2-3 sentences on what's needed
Link: Outlook Web URL

Group into: 🔴 Action Required, 🟠 Review Needed, 🟢 Informational
```

## Minimal Prompt (Fallback 2 — if simplified also times out)

Bare minimum query. If this fails too, skip the chunk.

```
List my top 5 most important unanswered emails from {{LOOKBACK}}. For each, give the subject, sender, and one sentence on what's needed. Include Outlook links.
```

---

## Post-Run — Dedup, Merge & Save

### Rolling Index — `work-email-check/triage-index.jsonl`

This JSONL file is the **master source of truth** for all previously surfaced items. One JSON object per line.

**Schema:**
```jsonl
{"id":"email-YYYY-MM-DD-NNN","source":"email","subject":"...","from":"...","date":"YYYY-MM-DD","category":"action|review|info","status":"open|resolved|snoozed","first_seen":"YYYY-MM-DD","last_seen":"YYYY-MM-DD"}
```

Optional fields for resolved items:
```jsonl
{"resolved_at":"YYYY-MM-DD","resolution":"Short description of what was done"}
```

**Status values:**
| Status | Meaning |
|--------|---------|
| `open` | Still needs attention |
| `resolved` | User marked as done — skip in future reports |
| `snoozed` | Temporarily hidden — re-surface after `snooze_until` date |

### Dedup Process — AI-Assisted (run BEFORE generating the report)

The agent performing the triage does the dedup inline — no external scripts needed.
Use **semantic matching**, not just string comparison. Two items are a match if they refer to
the same email thread/topic, even if the subject wording differs between runs.

**Match criteria (use judgment, not exact string match):**
- Same sender + same topic/thread → match (even if subject is worded differently)
- Different sender + similar subject → probably different items, check context

**Steps:**

1. **Read** `work-email-check/triage-index.jsonl` into memory
2. **For each item from WorkIQ**, semantically compare `subject` + `from` against existing index entries
3. **If match found AND status = `resolved`** → skip it entirely (do not include in report)
4. **If match found AND status = `snoozed`** → skip if today < `snooze_until`, otherwise re-surface
5. **If match found AND status = `open`** → update `last_seen` date, include in report with a `(recurring)` tag
6. **If no match** → it's new. Add to index and include in report with a `(new)` tag
7. **Write** updated index back to `triage-index.jsonl`

### Marking Items Resolved

When the user says "mark item N resolved" or "mark N done":
1. Find the item by its report number
2. Update the index entry: `status` → `resolved`, add `resolved_at` and `resolution`
3. Confirm the change

### Merge & Save

After dedup:

1. **Merge** results from all chunks into a single report, re-numbered sequentially
2. **Re-sort** within each category (🔴 → 🟠 → 🟢) by date, newest first
3. **Tag** each item as `(new)` or `(recurring)` based on index lookup
4. **Save** the merged report:
   - `work-email-check/reports/inbox-triage-full-<date>.md` (3-week scan)
   - `work-email-check/reports/inbox-triage-quick-<date>.md` (1-week scan)

### Report Frontmatter

```yaml
---
tags: [email-triage, report]
scan_type: full | quick
date: YYYY-MM-DD
chunks_attempted: 3
chunks_succeeded: 3
fallback_used: [chunk_number: fallback_level]
new_items: 5
recurring_items: 3
skipped_resolved: 2
---
```

## Lookback Options
| Option | Window | Chunks | Use Case |
|--------|--------|--------|----------|
| 1 (default) | 3 weeks | 3 x 7 days | Full catch-up, after PTO, or Monday morning |
| 2 | 1 week | 1 x 7 days | Quick mid-week check |
