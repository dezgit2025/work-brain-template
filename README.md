# work-brain-template

AI-powered work memory system for professionals who use AI coding assistants. Track clients, projects, emails, Teams chats, contacts, and decisions — all in plain markdown, git-backed, no cloud required.

Works with **Claude Code**, **GitHub Copilot CLI**, or any AI assistant that supports MCP (Model Context Protocol) and Microsoft 365 Copilot (WorkIQ).

## What You Get

- **Email triage** — Scan your Outlook inbox, categorize by priority, deduplicate across runs
- **Teams triage** — Scan Teams chats for direct asks, account updates, and action items
- **Project tracking** — Living master reports refreshed from email/Teams activity
- **Client management** — Per-client folders for contacts, decisions, meetings, and notes
- **Coding project logs** — Track what you built, where, and what's next
- **Coding task backlog** — Save to-dos from any project into a central queue
- **Contact enrichment** — WorkIQ MCP pulls names, emails, and roles from Microsoft 365
- **Word document generation** — Create styled .docx files via the bundled docx skill

## Prerequisites

- [Git](https://git-scm.com/)
- An AI assistant: [Claude Code](https://docs.anthropic.com/en/docs/claude-code) or [GitHub Copilot CLI](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line)
- [WorkIQ MCP](https://mcp.workiq.microsoft.com) access (Microsoft 365 Copilot license required)
- [uv](https://docs.astral.sh/uv/) — for the docx skill (`brew install uv` on macOS)

## Quick Start

```bash
# Clone the template
git clone https://github.com/YOUR_USER/work-brain-template.git
cd work-brain-template
```

### Claude Code

```bash
# Run the interactive setup wizard
/setup
```

### Copilot CLI / Other Agents

```
read deploy/setup-wizard.md and run the setup
```

The wizard will ask your name, role, accounts, and projects — then scaffold your personalized vault.

## How It Works

### Triage Workflows

Say "run the inbox triage" or "run the teams triage" to scan your Microsoft 365 inbox or Teams chats. The AI:

1. Queries WorkIQ MCP in chunked 7-day windows (avoids timeouts)
2. Categorizes items by priority (Action Required / Review Needed / Informational)
3. Deduplicates against a rolling JSONL index (semantic matching, not just string comparison)
4. Saves a report to the appropriate `reports/` folder

### Project Refresh

Say "refresh the {project} project" to scan email/Teams for project activity and update the master report. The AI backs up the current report, scans for new findings, and amends the master doc.

### Contact Enrichment

When creating customer notes, the AI queries WorkIQ to pull contact details (names, emails, roles) and structures them into tables. Distinguish between customer contacts and your account team.

## Template Placeholders

After cloning, the setup wizard replaces these placeholders:

| Placeholder | What it becomes |
|------------|-----------------|
| `{{YOUR_NAME}}` | Your name |
| `{{TIMEZONE}}` | Your timezone (e.g., Eastern Time) |
| `{{GITHUB_USER}}` | Your GitHub username |
| `{{ACCOUNT_1}}`, `{{ACCOUNT_2}}`, ... | Your client/account names |
| `{{PROJECT_NAME}}` | Your project names |

## Structure

```
work-brain-template/
├── CLAUDE.md                 # Agent instructions
├── FILE_REGISTRY.md          # Vault structure reference
├── PROMPTS.md                # Central prompt library
├── .claude/
│   ├── settings.json         # WorkIQ MCP config
│   └── commands/
│       └── setup.md          # Setup wizard (Claude Code)
├── deploy/
│   ├── install-work-brain.md # Technical install guide
│   └── setup-wizard.md       # Setup wizard (standalone)
├── work-email-check/         # Email triage workflow
├── work-teams-check/         # Teams triage workflow
├── projects/                 # Project trackers
├── coding-projects/          # Coding session logs
├── coding-tasks/             # Coding to-do backlog
├── work/clients/             # Client folders
├── inbox/                    # Unprocessed items
├── resources/                # Reference materials
├── skills/docx/              # Word document skill
└── ...
```

See `FILE_REGISTRY.md` for the complete inventory.

## Copilot CLI Compatibility

This template works with both Claude Code and GitHub Copilot CLI:

- `CLAUDE.md` — Agent instructions (read by Claude Code automatically)
- `.github/copilot-instructions.md` — Same content, read by Copilot CLI automatically
- `/setup` slash command — Claude Code only
- `deploy/setup-wizard.md` — Works with any AI assistant

**Note:** Slash commands (files in `.claude/commands/`) are a Claude Code feature. Copilot CLI users can achieve the same results by asking the AI to read and execute the relevant workflow file directly.

## Adding Clients or Projects Later

Re-run the setup wizard at any time. It detects existing folders and only creates new ones — your customized files are never overwritten.

## License

MIT
