# Teams Triage — Chat Check Workflow

## Purpose
Scan Teams chats and channels for unread messages, direct asks, and key account updates. Focus on activity for your tracked accounts.

## How to Use
Tell your AI assistant: "run the teams triage" — you'll be prompted to pick a lookback window:
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

Run the **Full Prompt** once with `{{LOOKBACK}} = "the last 7 days"`.

### Per-Chunk Fallback (if a chunk times out)

If a chunk times out, retry that chunk ONCE with the **Simplified Prompt** (shorter, top-10 focus).
If the simplified prompt also times out, retry with the **Minimal Prompt**.
If all 3 levels fail for a chunk, skip it and note the gap in the report.
Wait 5 seconds between retries.

---

## Full Prompt

**Replace `{{LOOKBACK}}` with the chunk's time window.**

```
Scan all my Teams chats and channel messages from {{LOOKBACK}}. Focus on messages related to these accounts: {{ACCOUNT_LIST}}. Also surface any messages where I am directly @mentioned or asked a question, regardless of account.

For each message or thread, use this exact format (no tables):

[number]) Thread/Topic summary
Type: 1:1 chat, group chat, or channel (include channel/team name)
Participants: list of people in the chat or thread
From: Sender full name (who sent the key message)
Date: exact date and time in {{TIMEZONE}} (e.g. Mon, Mar 3, 2026 2:15 PM ET)
Summary: 2-3 bullet points summarizing what was said, any decisions made, and what action is needed from me. Each bullet should be 3-4 sentences max.
Link: direct Teams message link if available

Group messages into these categories, in this order:
🔴 Direct Asks — I am @mentioned, asked a question, or assigned an action item. These go first no matter what.
🟠 Account Updates — key decisions, blockers, status changes, or new info about my tracked accounts that I should know about, especially if decisions were made in threads I didn't respond to.
🟢 FYI — general discussion, links shared, meeting recaps, or chatter with no action needed from me.

Only put messages in 🔴 if I am specifically and directly asked to do something or respond. Do NOT use markdown tables. Use a simple numbered list format optimized for narrow terminal display.
```

## Simplified Prompt (Fallback 1 — on timeout)

Used automatically when the full prompt times out for a chunk.

```
What are my most important unread or unanswered Teams messages from {{LOOKBACK}}? Focus on {{ACCOUNT_LIST}} accounts and any messages where I'm directly asked something. List up to 10 messages with thread topic, sender, date, and a brief summary of what's needed.

For each, format as:
[number]) Thread/Topic
From: Sender name
Date: date in {{TIMEZONE}}
Summary: 2-3 sentences on what's needed
Link: Teams link if available

Group into: 🔴 Direct Asks, 🟠 Account Updates, 🟢 FYI
```

## Minimal Prompt (Fallback 2 — if simplified also times out)

Bare minimum query. If this fails too, skip the chunk.

```
List my top 5 most important unanswered Teams messages from {{LOOKBACK}}, especially anything about {{ACCOUNT_LIST}}. For each, give the topic, sender, and one sentence on what's needed.
```

---

## Post-Run — Dedup, Merge & Save

### Rolling Index — `work-teams-check/triage-index.jsonl`

This JSONL file is the **master source of truth** for all previously surfaced items. One JSON object per line.

**Schema:**
```jsonl
{"id":"teams-YYYY-MM-DD-NNN","source":"teams","subject":"...","from":"...","date":"YYYY-MM-DD","category":"action|review|info","status":"open|resolved|snoozed","first_seen":"YYYY-MM-DD","last_seen":"YYYY-MM-DD"}
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
the same Teams thread/topic, even if the subject wording differs between runs.

**Match criteria (use judgment, not exact string match):**
- Same sender + same topic/thread → match (even if subject is worded differently)
- Different sender + similar subject → probably different items, check context

**Steps:**

1. **Read** `work-teams-check/triage-index.jsonl` into memory
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
   - `work-teams-check/reports/teams-triage-full-<date>.md` (3-week scan)
   - `work-teams-check/reports/teams-triage-quick-<date>.md` (1-week scan)

### Report Frontmatter

```yaml
---
tags: [teams-triage, report]
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
