# Template Sync Workflow

How changes flow from `work-brain` (private) to `work-brain-template` (public).

---

## How It Works

There is no scheduled sync or file-diffing. Detection is **proactive and conversational**:

When working in `work-brain`, the AI recognizes template-worthy changes as they happen and prompts:

> "This looks template-worthy. Want me to publish a sanitized version to work-brain-template?"

If confirmed, the AI sanitizes, copies, bumps the version, logs the change, and commits + pushes.

---

## What Triggers a Sync Prompt

Any of these events in `work-brain` should trigger a prompt:

| Event | Example |
|-------|---------|
| New skill added | New skill directory in `~/.claude/skills/` |
| Workflow file created or significantly modified | `inbox-triage.md`, `teams-triage.md`, any `project-refresh.md` |
| CLAUDE.md updated with new sections, schemas, or conventions | New frontmatter schema, new workflow trigger, new naming convention |
| PROMPTS.md updated with new prompt templates | New prompt added or existing prompt restructured |
| New slash command added | New file in `.claude/commands/` |
| FILE_REGISTRY.md gains new structural patterns | New folder convention, new file type |
| New setup wizard feature | New role preset, new wizard phase |

---

## What Does NOT Trigger a Sync

- Adding PII-specific content (client names, contacts, meeting notes)
- Updating reports, triage results, or project master-reports
- Changes to personal systems (expense tracking, secure vault, agent memory)
- Obsidian-specific commands or features
- Changes to `agentic-evolution/`, `plans/`, `deploy/`, `deploy2/`, `deploypdf/`

---

## Sync Process

When the user confirms a sync:

### 1. Sanitize

Apply these replacements before copying:

| Original | Template Placeholder |
|----------|---------------------|
| Real client names (SMBC, Mizuho, MUFG, etc.) | `{{ACCOUNT_LIST}}` or `{{ACCOUNT_1}}`, `{{ACCOUNT_2}}` |
| Real person names | `{{TEAM_MEMBER_1}}`, `{{STAKEHOLDER_1}}`, etc. |
| User's name | `{{YOUR_NAME}}` |
| GitHub username | `{{GITHUB_USER}}` |
| Hardcoded timezone (e.g., "Eastern Time") | `{{TIMEZONE}}` |
| Client-specific language | Generic equivalents |

### 2. Copy to template

- Place the sanitized file in its template location
- If it's a new file/folder, create the directory structure
- If it's a skill, copy to `skills/{skill-name}/`

### 3. Update template files

- `FILE_REGISTRY.md` — add new entries if structure changed
- `CLAUDE.md` — add reference if new workflow or skill
- `.github/copilot-instructions.md` — re-copy from CLAUDE.md if it changed
- `CHANGELOG.md` — add entry under new version or existing unreleased section
- `deploy/setup-wizard.md` — update if new folders/options needed

### 4. Log the sync

Append to `deploy/sync-log.jsonl`:

```jsonl
{"date":"YYYY-MM-DD","action":"update|new_skill|new_workflow|new_command","description":"what changed","source_files":["work-brain/path"],"dest_files":["template/path"],"version":"X.Y.Z"}
```

### 5. PII verification

Run the PII scan before committing:

```bash
cd ~/Projects/work-brain-template
grep -ri "\bmizuho\b\|\bsmbc\b\|\bmufg\b\|\bdesi\b\|villanueva\|iovine\|dezgit\|hao.luo\|phil.feinberg" . 2>/dev/null
```

Must return 0 results.

### 6. Commit and push

```bash
git add -A
git commit --author="Des Villa <desi4k@gmail.com>" -m "description of what was synced"
git push
```

No Co-Authored-By. No Claude references in commits.

---

## Sync Log

`deploy/sync-log.jsonl` is the audit trail of all published changes. One JSON object per line.

**Schema:**
```jsonl
{"date":"YYYY-MM-DD","action":"initial|update|new_skill|new_workflow|new_command|new_section","description":"human-readable summary","source_files":["relative paths in work-brain"],"dest_files":["relative paths in template"],"version":"semver"}
```

**Versioning convention:**
- Patch (`1.0.1`) — updated existing file (workflow tweak, CLAUDE.md refinement)
- Minor (`1.1.0`) — new skill, new workflow, new slash command
- Major (`2.0.0`) — structural change to template (new wizard phase, folder reorganization)

---

## Asking About Sync Status

When the user asks "what's been synced to the template?" or "is the template up to date?":

1. Read `deploy/sync-log.jsonl` for the last sync date and version
2. Report what's been published and when
3. If working in work-brain, check recent changes that might be template-worthy but haven't been synced yet
