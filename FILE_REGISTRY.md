# Work Brain — File Registry

> **What is this?** Single source of truth for vault structure, file inventory, naming conventions, and workflows. This is the ONE file to update when adding new content.
>
> **Updated by:** Setup wizard (auto), manual edits

---

## Root Layout

```
work-brain-template/
├── CLAUDE.md                   ← agent behavior & pointers (rarely changes)
├── FILE_REGISTRY.md            ← this file — structure + inventory (update this one)
├── PROMPTS.md                  ← central prompt library for all workflows
├── CHANGELOG.md                ← version tracking for template releases
├── README.md                   ← public-facing usage guide
├── .github/
│   └── copilot-instructions.md ← copy of CLAUDE.md for Copilot CLI
├── .claude/
│   ├── settings.json           ← WorkIQ MCP server config
│   └── commands/
│       └── setup.md            ← interactive setup wizard (Claude Code)
├── deploy/
│   ├── install-work-brain.md   ← technical install guide
│   └── setup-wizard.md         ← interactive setup wizard (standalone)
├── work-email-check/           ← email triage workflow
├── work-teams-check/           ← teams triage workflow
├── projects/                   ← account/project trackers
├── coding-projects/            ← coding session logs from any repo
├── coding-tasks/               ← coding to-dos saved from any project
├── work/                       ← active work items (clients, contacts, decisions)
├── inbox/                      ← unprocessed items
├── resources/                  ← reference materials
├── skills/docx/                ← Word document generation skill
├── sessions/                   ← session artifacts
├── archive/                    ← completed/archived items
├── backups/                    ← backup copies
└── _trash/                     ← soft-deleted items
```

---

## System Files

| File | What it is | Updated by |
|------|-----------|------------|
| `CLAUDE.md` | Agent instructions — behavior, conventions, pointers to this file | Manual, setup wizard |
| `FILE_REGISTRY.md` | This file — vault structure, all files, naming conventions, workflows | Setup wizard, manual |
| `PROMPTS.md` | Central prompt library for all workflows (email, Teams, project refresh) | Manual, setup wizard |
| `.github/copilot-instructions.md` | Copy of CLAUDE.md for Copilot CLI | Setup wizard |
| `.claude/settings.json` | WorkIQ MCP server configuration | Manual |

---

## work-email-check/

Email inbox triage workflow — scans for unread/important emails and categorizes by priority.

```
work-email-check/
├── inbox-triage.md             ← workflow prompt + instructions
├── triage-index.jsonl          ← rolling dedup index (JSONL)
└── reports/
    ├── inbox-triage-full-<date>.md    ← 3-week scan results
    └── inbox-triage-quick-<date>.md   ← 1-week scan results
```

---

## work-teams-check/

Teams chat triage workflow — scans for direct asks and account updates.

```
work-teams-check/
├── teams-triage.md             ← workflow prompt + instructions
├── triage-index.jsonl          ← rolling dedup index (JSONL)
└── reports/
    ├── teams-triage-full-<date>.md    ← 3-week scan results
    └── teams-triage-quick-<date>.md   ← 1-week scan results
```

---

## projects/

Account and project-specific trackers. Each project follows a standard layout:

```
projects/<project-name>/
├── project-refresh.md          ← workflow prompt for refreshing the project
├── master-report.md            ← living document, always current
├── backup/
│   └── master-report-<timestamp>.md    ← snapshots before each refresh
├── raw/
│   └── findings-<timestamp>.md         ← raw WorkIQ output per scan
└── reports/
    └── <ad-hoc-reports>.md             ← one-off reports or exports
```

### Template Projects

- `_example-project/` — Example layout (copy when adding new projects)

---

## coding-projects/

Coding session logs from any repo. Tracks what was coded, current progress, blockers, and next steps.

```
coding-projects/
├── _index.md                           ← dashboard of all coding projects
├── snapshots/
│   └── master-summary-<timestamp>.md   ← historical full scan snapshots
└── <project-name>/
    ├── overview.md                     ← living doc (overwritten each scan)
    └── snapshots/
        └── snapshot-<timestamp>.md     ← historical per-project snapshots
```

---

## coding-tasks/

Coding to-dos and review items.

```
coding-tasks/
├── _index.md                           ← dashboard of all coding tasks
├── active/
│   └── <project>-<slug>-<date>.md      ← tasks currently tracked
└── backlog/
    └── <project>-<slug>-<date>.md      ← deprioritized / someday tasks
```

### Task File Schema

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

### Naming Convention

`<project>-<short-slug>-<YYYY-MM-DD>.md`

---

## work/

Active work items organized by type and client.

```
work/
├── decisions/                  ← decision records
├── meetings/                   ← meeting notes
├── people/                     ← people/contact notes
└── clients/
    └── _example-client/
        ├── overview.md         ← client bible (single source of truth)
        ├── contacts/           ← individual contact notes
        ├── decisions/          ← client-specific decisions
        ├── meetings/           ← client meeting notes
        └── notes/              ← general notes + draft emails
```

---

## skills/docx/

Word document generation skill. Symlink to `~/.claude/skills/docx` for Claude Code discovery.

```
skills/docx/
├── SKILL.md                    ← quick reference + design standards
├── creating.md                 ← creating docs from scratch
└── editing.md                  ← editing existing docs
```

---

## Workflow Configs (All Triggers)

| Workflow | Trigger phrase | Config file | Output location |
|----------|---------------|-------------|-----------------|
| Email triage | "run the inbox triage" | `work-email-check/inbox-triage.md` | `work-email-check/reports/` |
| Teams triage | "run the teams triage" | `work-teams-check/teams-triage.md` | `work-teams-check/reports/` |
| Project refresh | "refresh the {project} project" | `projects/{project}/project-refresh.md` | `projects/{project}/reports/` |

---

## Reports (Generated Output)

| Location | What goes here | Generated by |
|----------|---------------|-------------|
| `work-email-check/reports/` | Email triage reports (`full-` or `quick-` prefix) | inbox-triage workflow |
| `work-teams-check/reports/` | Teams triage reports (`full-` or `quick-` prefix) | teams-triage workflow |
| `projects/{project}/reports/` | Ad-hoc project reports and exports | project-refresh workflow |

---

## Naming Conventions

- **Timestamps:** ISO-ish format `YYYY-MM-DDTHHMM` (e.g., `2026-03-05T1334`)
- **Scan types:** `full` (3-week) or `quick` (1-week) prefix
- **Draft emails:** `email-draft-{client}-{recipient}-{topic}-{date}.md` → `work/clients/{client}/notes/`
- **Coding tasks:** `{project}-{short-slug}-{YYYY-MM-DD}.md`
- **Resolved items:** Marked `(RESOLVED)` in master reports — never deleted
- **Backups:** Always taken before amending master reports

---

## Other Files

| File | What it is |
|------|-----------|
| `inbox/README.md` | Inbox landing page — quick capture instructions |
| `resources/README.md` | Resources folder — reference materials |
| `backups/` | Backup copies of important files |
| `_trash/` | Soft-deleted items (recoverable) |
