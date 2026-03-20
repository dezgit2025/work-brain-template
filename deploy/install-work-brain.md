# Work Brain — Install Guide

## Prerequisites

| Tool | Required | Install |
|------|----------|---------|
| Git | Yes | [git-scm.com](https://git-scm.com/) |
| AI Assistant | Yes | Claude Code, GitHub Copilot CLI, or similar |
| WorkIQ MCP | Yes | Microsoft 365 Copilot license → [mcp.workiq.microsoft.com](https://mcp.workiq.microsoft.com) |
| uv | Optional | `brew install uv` (macOS) — needed for docx skill |

## Step 1 — Clone

```bash
git clone https://github.com/YOUR_USER/work-brain-template.git my-work-brain
cd my-work-brain
```

## Step 2 — Run Setup Wizard

### Claude Code
```bash
# Inside the repo directory:
/setup
```

### Copilot CLI / Other Agents
```
read deploy/setup-wizard.md and run the setup
```

The wizard will:
1. Ask your name, timezone, GitHub username
2. Let you pick a role preset (Account Manager, Engineer, PM, Custom)
3. Ask which accounts/clients you track
4. Ask about active projects
5. Create all folders and personalize workflow files

## Step 3 — WorkIQ MCP

The MCP configuration is pre-set in `.claude/settings.json`:

```json
{
  "mcpServers": {
    "workiq": {
      "type": "url",
      "url": "https://mcp.workiq.microsoft.com/sse"
    }
  }
}
```

**First use:** Your AI assistant will prompt you to authenticate with Microsoft 365 when it first calls WorkIQ.

## Step 4 — Docx Skill (Optional)

To enable Word document generation in Claude Code:

```bash
# From the repo root:
ln -s "$(pwd)/skills/docx" ~/.claude/skills/docx
```

Verify it works:
```bash
uv --version  # Should print uv version
```

## Step 5 — Copilot CLI Setup (Optional)

If using GitHub Copilot CLI, the instructions file is already at `.github/copilot-instructions.md`. Copilot reads this automatically.

**Note:** Slash commands (`.claude/commands/`) are Claude Code-specific. Copilot CLI users can achieve the same by asking the AI to read and execute workflow files directly:
- Instead of `/setup` → "read deploy/setup-wizard.md and run the setup"
- Instead of workflow triggers → same trigger phrases work (e.g., "run the inbox triage")

## Verify Setup

After running the wizard, check:

1. **Folders created:** `ls work/clients/` — should show your client names
2. **Projects created:** `ls projects/` — should show your project names
3. **Personalized files:** `grep "{{" CLAUDE.md` — should return 0 matches (all placeholders replaced)
4. **Copilot sync:** `diff CLAUDE.md .github/copilot-instructions.md` — should match

## Updating

When new versions of the template are released:

1. Compare your files against the template repo
2. Pull in new workflow improvements manually
3. The setup wizard can be re-run to add new clients/projects without overwriting existing files
