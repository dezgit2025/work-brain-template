# Work Brain — Setup Wizard

Interactive setup that personalizes your work-brain vault. Run this on first use, or re-run to add more clients/projects.

## How to Trigger

- **Claude Code:** `/setup`
- **Any AI assistant:** "read deploy/setup-wizard.md and run the setup"

---

## Instructions for the AI

Read this file completely, then execute the phases below in order. Ask the user each question and wait for their response before proceeding. Do not skip questions or assume answers.

### Phase 1 — User Profile

Ask these questions one at a time:

1. **"What's your name?"** → Store as `{{YOUR_NAME}}`
2. **"What's your timezone?"** (e.g., Eastern Time, Pacific Time, JST, UTC) → Store as `{{TIMEZONE}}`
3. **"What's your GitHub username?"** → Store as `{{GITHUB_USER}}`

### Phase 2 — Role Preset

Ask: **"Pick a role preset (or choose Custom):"**

Present these options:

| # | Preset | Triage Focus | Key Folders |
|---|--------|-------------|-------------|
| 1 | **Account Manager** | Client escalations, deal status, stakeholder asks | `work/clients/`, `work/meetings/`, `work/decisions/` |
| 2 | **Engineer** | Code reviews, deployments, incident threads, PRs | `coding-projects/`, `coding-tasks/`, `resources/` |
| 3 | **PM / Program Manager** | Milestones, decisions, blockers, status updates | `projects/`, `work/decisions/`, `work/meetings/` |
| 4 | **Custom** | You define your own focus | You pick folders |

Based on the selected preset, set these internal variables:

**Account Manager:**
- `{{TRIAGE_FOCUS}}` = "client escalations, deal status, stakeholder asks, and relationship updates"
- `{{CATEGORIES_EMAIL}}` = "Action Required, Review Needed, Informational"
- `{{CATEGORIES_TEAMS}}` = "Direct Asks, Account Updates, FYI"

**Engineer:**
- `{{TRIAGE_FOCUS}}` = "code reviews, deployment issues, incident threads, pull requests, and technical discussions"
- `{{CATEGORIES_EMAIL}}` = "Action Required, Build/Deploy, Informational"
- `{{CATEGORIES_TEAMS}}` = "Direct Asks, Technical Updates, FYI"

**PM / Program Manager:**
- `{{TRIAGE_FOCUS}}` = "milestones, decisions, blockers, status updates, and cross-team coordination"
- `{{CATEGORIES_EMAIL}}` = "Action Required, Decision Needed, Status Update"
- `{{CATEGORIES_TEAMS}}` = "Direct Asks, Decision Needed, Status Update"

**Custom:**
- Ask: "What topics should triage prioritize?"
- Ask: "What are your 3 email categories?" (default: Action Required, Review Needed, Informational)
- Ask: "What are your 3 Teams categories?" (default: Direct Asks, Account Updates, FYI)

### Phase 3 — Accounts & Projects

Ask: **"What accounts or clients do you track? (comma-separated, or 'none')"**

For each account name provided:
- Create `work/clients/{name}/` with subfolders: `contacts/`, `decisions/`, `meetings/`, `notes/`
- Create `work/clients/{name}/overview.md` from the client overview template (see below)
- Add `.gitkeep` to each empty subfolder

Ask: **"Any active projects? (comma-separated, or 'none')"**

For each project name:
- Ask: "Which client is '{project}' for? (or 'standalone')"
- Create `projects/{project}/` with subfolders: `backup/`, `raw/`, `reports/`
- Create `projects/{project}/project-refresh.md` from the project refresh template (see below)
- Create `projects/{project}/master-report.md` from the master report template (see below)
- Add `.gitkeep` to each empty subfolder

### Phase 4 — Triage Sources

Ask: **"Which triage workflows do you want?"**
1. Email triage (Outlook via WorkIQ)
2. Teams triage (Teams via WorkIQ)
3. Both (default)

### Phase 5 — Scaffold

Now perform all replacements and file creation:

1. **Replace placeholders** in these files:
   - `CLAUDE.md` — replace `{{YOUR_NAME}}`, `{{TIMEZONE}}`, `{{GITHUB_USER}}`
   - `PROMPTS.md` — replace `{{YOUR_NAME}}`, `{{TIMEZONE}}`, `{{ACCOUNT_*}}`, `{{TRIAGE_FOCUS}}`, `{{CATEGORIES_*}}`
   - `work-email-check/inbox-triage.md` — replace `{{TIMEZONE}}`, `{{CATEGORIES_EMAIL}}`
   - `work-teams-check/teams-triage.md` — replace `{{ACCOUNT_*}}`, `{{TIMEZONE}}`, `{{CATEGORIES_TEAMS}}`, `{{TRIAGE_FOCUS}}`

2. **Update FILE_REGISTRY.md** with the actual folder structure created

3. **Copy CLAUDE.md to .github/copilot-instructions.md** (overwrite the template version)

4. **Remove unused triage folders** if user chose only email or only Teams

5. **Print summary:**
   ```
   Setup complete! Here's what was created:

   Name: {{YOUR_NAME}}
   Role: {{PRESET}}
   Timezone: {{TIMEZONE}}
   Clients: [list]
   Projects: [list]
   Triage: [email/teams/both]

   Files modified:
   - CLAUDE.md (personalized)
   - PROMPTS.md (personalized)
   - .github/copilot-instructions.md (synced from CLAUDE.md)
   - work-email-check/inbox-triage.md (personalized)
   - work-teams-check/teams-triage.md (personalized)
   - FILE_REGISTRY.md (updated)

   Folders created:
   - [list of client and project folders]

   Try it out:
   - "run the inbox triage" — scan your email
   - "run the teams triage" — scan your Teams
   - "refresh the {project} project" — update a project report
   ```

---

## Re-Running the Wizard

The wizard is safe to re-run. When re-running:

- **Existing folders are NOT overwritten** — only new clients/projects are created
- **Already-personalized files are NOT reset** — placeholder replacement only applies to files that still contain `{{` placeholders
- **New clients/projects are appended** to FILE_REGISTRY.md

To detect if a file has already been personalized, check if it contains any `{{` placeholder strings. If not, skip replacement for that file.

---

## Templates

### Client Overview Template

```markdown
---
tags: [client-overview]
company: "{{CLIENT_NAME}}"
status: active
last_updated: {{TODAY}}
---

# {{CLIENT_NAME}}

## Overview

<!-- Brief description of the account relationship -->

## Key Contacts

### {{CLIENT_NAME}}

| Name | Email | Role |
|------|-------|------|
| | | |

### Account Team

| Name | Email | Role |
|------|-------|------|
| | | |

## Active Projects

- <!-- List active projects -->

## Recent Activity

- <!-- Recent notes, decisions, escalations -->

## Open Questions

- <!-- Unresolved items -->
```

### Project Refresh Template

```markdown
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
```

### Master Report Template

```markdown
---
tags: [project, master-report]
project: "{{PROJECT_NAME}}"
client: "{{CLIENT_NAME}}"
status: active
last_refreshed:
---

# {{PROJECT_NAME}} — Master Report

## Key Facts

- <!-- Core facts about the project -->

## Milestones & Timeline

- <!-- Key dates and deliverables -->

## Open Questions

- <!-- Unanswered items -->

## Blockers

- <!-- Current blockers -->

## Concerns & Risks

- <!-- Risks and concerns -->

## Decisions Made

- <!-- Finalized decisions -->

## Next Steps

- <!-- Upcoming actions -->
```
