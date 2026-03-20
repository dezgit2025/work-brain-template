# work-brain

AI-powered work memory system. Integrates Claude Code and GitHub Copilot CLI via MCP (Model Context Protocol) with WorkIQ (Microsoft 365 Copilot) for contact enrichment, daily email/Teams triage workflows, project lifecycle tracking, and client account management. All data is plain markdown files, git-backed, no cloud required.

## Quick Start

Run the setup wizard to personalize your vault:
- **Claude Code:** `/setup`
- **Copilot CLI:** "read deploy/setup-wizard.md and run the setup"

The wizard asks your name, role, accounts, and projects — then scaffolds everything.

---

## WorkIQ MCP — Customer Contact Lookup

When creating or updating customer notes (especially in `inbox/` or `work/people/`), use the WorkIQ MCP to enrich contact information:

1. Query `ask_work_iq` with the company name and known contact names
2. Extract: full names, email addresses, roles/titles
3. Distinguish between **customer contacts** and **your organization's account team** members
4. Update the note with a structured contacts table:

```markdown
### Company Name

| Name | Email | Role |
|------|-------|------|
| Full Name | email@domain.com | Title |

### Account Team

| Name | Email | Role |
|------|-------|------|
| Full Name | email@company.com | Title |
```

5. Move unconfirmed names to **Open Questions** section

---

## Draft Email Convention

Draft emails are stored in the relevant client's notes folder:

- **Location:** `work/clients/{client}/notes/`
- **Naming:** `email-draft-{client}-{recipient}-{topic}-{date}.md`

Frontmatter:

```yaml
---
tags: [draft-email, {topic-tag}]
company: "[[client]]"
to: "[[recipient-link]]"
project: "[[project-link]]"
date: YYYY-MM-DD
status: draft
---
```

---

## Customer Note Template

Notes in `inbox/` use this frontmatter:

```yaml
---
tags: customer-note
company:
stakeholder:
role:
date: YYYY-MM-DD
project:
priority:
follow_up:
status: active
---
```

---

## Vault Structure & File Inventory

**See `FILE_REGISTRY.md` for the complete vault structure, all file inventories, naming conventions, and folder layouts.**

`FILE_REGISTRY.md` is the single source of truth. When adding new files or folders, update FILE_REGISTRY.md only — not this file.

---

## Triage Workflows

Trigger-based workflows that use WorkIQ MCP to scan email/Teams. Always read the config file for full instructions before executing.

| Workflow | Trigger phrase | Config file | Output location |
|----------|---------------|-------------|-----------------|
| Email triage | "run the inbox triage" | `work-email-check/inbox-triage.md` | `work-email-check/reports/` |
| Teams triage | "run the teams triage" | `work-teams-check/teams-triage.md` | `work-teams-check/reports/` |
| Project refresh | "refresh the {{PROJECT_NAME}} project" | `projects/{project}/project-refresh.md` | `projects/{project}/reports/` |

---

## Project Note Schema

Project notes use this frontmatter:

```yaml
---
type: poc | experiment
client: "[[client-name]]"
status: active | waiting | blocked | complete
phase: 1
git_repo: github.com/org/repo
next_phase_start: YYYY-MM-DD
next_phase_label: "Phase name"
poc_parent: "[[poc-name]]"  # experiments only
whats_next:
  - "Action item 1"
  - "Action item 2"
---
```

---

## Coding Projects

Session logs from any repo. Tracks what was coded, current progress, blockers, and next steps.

- **Dashboard:** `coding-projects/_index.md`
- **Per-project:** `coding-projects/{project-name}/overview.md`
- **Snapshots:** `coding-projects/snapshots/` (historical full-scan snapshots)

---

## Coding Tasks

To-dos and review items saved from any project.

- **Dashboard:** `coding-tasks/_index.md`
- **Active:** `coding-tasks/active/{project}-{slug}-{date}.md`
- **Backlog:** `coding-tasks/backlog/{project}-{slug}-{date}.md`

Task file schema:

```yaml
---
tags: coding-task
title: "<short title>"
project: "<project-name>"
type: review | fix | feature | refactor | research | decision
priority: high | medium | low
status: active | backlog | completed
created: YYYY-MM-DD
source_branch: "<branch>"
source_dir: "<working directory>"
---
```

Naming convention: `{project}-{short-slug}-{YYYY-MM-DD}.md`

---

## Docx Skill

Create and edit Word documents using `python-docx` via `uv`. The skill is bundled at `skills/docx/`.

**To install for Claude Code:**
```bash
ln -s "$(pwd)/skills/docx" ~/.claude/skills/docx
```

**Dependency:** Requires `uv` (`brew install uv` on macOS).

See `skills/docx/SKILL.md` for the full reference.

---

## Naming Conventions

- **Timestamps:** ISO-ish format `YYYY-MM-DDTHHMM` (e.g., `2026-03-05T1334`)
- **Scan types:** `full` (3-week) or `quick` (1-week) prefix
- **Draft emails:** `email-draft-{client}-{recipient}-{topic}-{date}.md`
- **Coding tasks:** `{project}-{short-slug}-{YYYY-MM-DD}.md`
- **Resolved items:** Marked `(RESOLVED)` in master reports — never deleted
- **Backups:** Always taken before amending master reports

---

## Setup Wizard

Personalize this template for your workflow:

- **Claude Code:** Run `/setup` — interactive wizard that asks questions and scaffolds your vault
- **Copilot CLI / other agents:** Say "read deploy/setup-wizard.md and run the setup"

The wizard creates client folders, project trackers, and personalizes all workflow files. It can be re-run to add more clients or projects without overwriting existing customizations.
