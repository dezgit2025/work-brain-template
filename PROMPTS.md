# Work Brain — Prompt Library

Central store of all reusable prompts for workflows, triage, and project tracking.

---

## Email Inbox Triage

**Trigger:** "run the inbox triage"
**Workflow file:** `work-email-check/inbox-triage.md`
**Lookback:** 3 weeks (full) or 1 week (quick)

```
Show me all emails from the last {{LOOKBACK}} that I haven't responded to yet, or that seem important and need my attention. Be thorough — scan ALL emails in the window, not just the most recent ones. Include customer escalations and external requests even if they are older but still within the window. Exclude any emails with "[WORKIQ-SUMMARY]" in the subject.

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

---

## Teams Chat Triage

**Trigger:** "run the teams triage"
**Workflow file:** `work-teams-check/teams-triage.md`
**Lookback:** 3 weeks (full) or 1 week (quick)

```
Scan all my Teams chats and channel messages from the last {{LOOKBACK}}. Focus on messages related to these accounts: {{ACCOUNT_LIST}}. Also surface any messages where I am directly @mentioned or asked a question, regardless of account.

For each message or thread, use this exact format (no tables):

[number]) Thread/Topic summary
Type: 1:1 chat, group chat, or channel (include channel/team name)
Participants: list of people in the chat or thread
From: Sender full name (who sent the key message)
Date: exact date and time in {{TIMEZONE}}
Summary: 2-3 bullet points summarizing what was said, any decisions made, and what action is needed from me. Each bullet should be 3-4 sentences max.
Link: direct Teams message link if available

Group messages into these categories, in this order:
🔴 Direct Asks — I am @mentioned, asked a question, or assigned an action item. These go first no matter what.
🟠 Account Updates — key decisions, blockers, status changes, or new info about my tracked accounts that I should know about, especially if decisions were made in threads I didn't respond to.
🟢 FYI — general discussion, links shared, meeting recaps, or chatter with no action needed from me.

Only put messages in 🔴 if I am specifically and directly asked to do something or respond. Do NOT use markdown tables. Use a simple numbered list format optimized for narrow terminal display.
```

---

## Project Refresh

**Trigger:** "refresh the {{PROJECT_NAME}} project"
**Workflow file:** `projects/{project}/project-refresh.md`
**Lookback:** 2 weeks (regular) or 4 weeks (deep catch-up)

```
Look at all Teams messages and emails related to the "{{PROJECT_NAME}}" project over the last {{LOOKBACK}}. Include all participants involved in this project.

Produce a comprehensive project status summary using this exact format (no tables):

## Key Facts
- List the core facts about what this project is, what it does, the tech stack, and current state

## Milestones & Timeline
- List each milestone or key event with estimated or actual dates
- Include demos, meetings, deliverables, deadlines

## Open Questions
- List any unanswered questions from the chat threads with who asked them and approximate date

## Blockers
- List anything currently blocking progress, with estimated impact and who owns the resolution

## Concerns & Risks
- List any concerns raised by team members about architecture, compliance, timeline, or customer expectations

## Decisions Made
- List key decisions that have been finalized, with approximate date and who made them

## Next Steps
- List upcoming actions, who owns them, and any known deadlines

Be thorough and include as much detail as possible. Use bullet points with 2-3 sentences per item.
```

---

## Formatting Rules (All Prompts)

- **No markdown tables** — use numbered lists for terminal readability
- **Bullet summaries** — 2-3 bullets per item, 3-4 sentences max each
- **Dates in {{TIMEZONE}}** — always use your configured timezone
- **Priority order** — 🔴 first, then 🟠, then 🟢
- **Classification rule** — 🔴 only for direct asks to {{YOUR_NAME}}; CC/group threads do NOT count
- **Exclude tag** — skip any emails with `[WORKIQ-SUMMARY]` in subject
