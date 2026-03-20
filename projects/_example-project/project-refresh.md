# {{PROJECT_NAME}} — Project Refresh Workflow

## Purpose
Periodically scan Teams chats and emails for new project activity, then amend the master report with updated findings.

## How to Use
Say: "refresh the {{PROJECT_NAME}} project"

## Refresh Process
1. **Backup** — Copy current `master-report.md` to `backup/master-report-<timestamp>.md`
2. **Scan** — Run the prompt below via WorkIQ
3. **Save raw** — Save WorkIQ output to `raw/findings-<timestamp>.md`
4. **Amend master** — Update `master-report.md` with new/changed items:
   - Add new milestones, decisions, blockers, questions
   - Mark resolved items as `(RESOLVED)` — don't delete them
   - Update dates and ownership as needed
   - Add a `## Last Refreshed` line at the top with the current date

## Prompt Template

Replace `{{LOOKBACK}}` with the scan window.

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

## Lookback Options
| Option | Window | Use Case |
|--------|--------|----------|
| 1 (default) | 2 weeks | Regular refresh |
| 2 | 4 weeks | Deep catch-up |
