# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Personal AI Employee** (Digital FTE) hackathon project. The goal is to build an autonomous agent that proactively manages personal and business affairs 24/7 using Claude Code as the reasoning engine and Obsidian as the management dashboard.

**Core Architecture: Perception → Reasoning → Action**

- **The Brain:** Claude Code (you) acts as the reasoning engine
- **The Memory/GUI:** Obsidian vault with local Markdown files
- **The Senses:** Python Watcher scripts monitor Gmail, WhatsApp, file systems
- **The Hands:** MCP servers handle external actions (email, browser automation, payments)

## Hackathon Tiers

This project follows a tiered approach:

- **Bronze Tier** (8-12 hours): Basic vault structure, one Watcher, Claude reading/writing to vault
- **Silver Tier** (20-30 hours): Multiple Watchers, MCP integration, human-in-the-loop approval, LinkedIn automation
- **Gold Tier** (40+ hours): Full cross-domain integration, Odoo accounting, social media (Facebook/Instagram/Twitter), CEO briefings, Ralph Wiggum loop
- **Platinum Tier** (60+ hours): Cloud deployment (24/7), work-zone specialization (Cloud drafts, Local approves), vault sync via Git

## Vault Folder Structure

The Obsidian vault uses this structure:

```
/Inbox              - New items awaiting triage
/Needs_Action       - Tasks requiring immediate attention
/In_Progress        - Currently being worked on
/Done               - Completed tasks
/Pending_Approval   - Sensitive actions awaiting human approval
/Approved           - Human-approved actions ready to execute
/Rejected           - Rejected approval requests
/Accounting         - Financial transactions and reports
/Plans              - Task plans with checkboxes
/Updates            - Status updates from Cloud agent (Platinum tier)
```

## Key Files

- **Dashboard.md**: Real-time summary of bank balance, pending messages, active projects
- **Company_Handbook.md**: Rules of engagement (e.g., "Always be polite on WhatsApp", "Flag payments over $500")
- **Plan.md files**: Created by Claude with checkboxes for multi-step tasks

## Watcher Pattern

Watchers are lightweight Python scripts that run continuously and create actionable files:

**Base Pattern:**
1. Monitor external source (Gmail, WhatsApp, file drops)
2. Detect new items matching criteria
3. Create .md file in `/Needs_Action` with frontmatter metadata
4. Trigger Claude Code to process

**Available Watchers:**
- `gmail_watcher.py` - Monitors Gmail for important/unread messages
- `whatsapp_watcher.py` - Monitors WhatsApp Web for urgent keywords
- `filesystem_watcher.py` - Monitors drop folder for new files

## MCP Server Integration

MCP servers are Claude's "hands" for external actions. Configure in `~/.config/claude-code/mcp.json`:

**Common MCP Servers:**
- `filesystem` - Built-in, use for vault operations
- `email-mcp` - Send/draft emails
- `browser-mcp` - Navigate, click, fill forms (payment portals)
- `calendar-mcp` - Schedule events
- `slack-mcp` - Team communication

**Playwright Browser Automation:**
The `browsing-with-playwright` skill is already configured. See `.claude/skills/browsing-with-playwright/SKILL.md` for usage.

## Human-in-the-Loop (HITL) Pattern

For sensitive actions (payments, important emails), Claude should:

1. Create approval request file in `/Pending_Approval` with frontmatter metadata
2. Include action details and consequences
3. Wait for human to move file to `/Approved` or `/Rejected`
4. Orchestrator watches `/Approved` and triggers MCP action

**Sensitive actions requiring approval:**
- Payments over $500 (or threshold in Company_Handbook.md)
- Sending emails on behalf of user
- Posting to social media
- Modifying accounting records

## Ralph Wiggum Loop (Gold Tier)

The "Ralph Wiggum" pattern uses a Stop hook to keep Claude iterating until a task is complete:

1. Orchestrator creates state file with prompt
2. Claude works on task
3. Claude tries to exit
4. Stop hook checks: Is task file in `/Done`?
5. If NO → Block exit, re-inject prompt (loop continues)
6. If YES → Allow exit (complete)

**Completion strategies:**
- Promise-based: Claude outputs `<promise>TASK_COMPLETE</promise>`
- File movement: Stop hook detects task file moved to `/Done`

## Agent Skills

**CRITICAL:** All AI functionality must be implemented as Agent Skills (not standalone scripts). This ensures:
- Reusability across conversations
- Proper encapsulation of domain logic
- Easy invocation via skill system

When building new capabilities, convert them to skills in `.claude/skills/`.

## Workflow Example

1. **Watcher detects** urgent Gmail message → creates `EMAIL_12345.md` in `/Needs_Action`
2. **Claude reads** `/Needs_Action` and `/Company_Handbook.md`
3. **Claude reasons** about appropriate response based on rules
4. **Claude creates** `Plan.md` with checkboxes for steps
5. **Claude drafts** reply and creates approval request in `/Pending_Approval`
6. **Human approves** by moving file to `/Approved`
7. **Orchestrator triggers** email MCP to send reply
8. **Claude moves** task to `/Done` and updates `Dashboard.md`

## Development Commands

**Start Playwright MCP server:**
```bash
bash .claude/skills/browsing-with-playwright/scripts/start-server.sh
```

**Stop Playwright MCP server:**
```bash
bash .claude/skills/browsing-with-playwright/scripts/stop-server.sh
```

**Verify Playwright server:**
```bash
python3 .claude/skills/browsing-with-playwright/scripts/verify.py
```

**Run a Watcher (example):**
```bash
python3 watchers/gmail_watcher.py --vault-path /path/to/vault
```

## Important Principles

1. **Local-first**: All data stays in local Markdown files (privacy-focused)
2. **Human-in-the-loop**: Never execute sensitive actions without approval
3. **Audit trail**: Every action creates a file record
4. **Proactive not reactive**: Watchers wake the agent, don't wait for user input
5. **Autonomous iteration**: Use Ralph Wiggum loop for multi-step tasks
6. **Skills-based**: Implement all functionality as reusable Agent Skills

## Security Rules

- Never commit secrets (.env, tokens, credentials, WhatsApp sessions)
- Vault sync (Platinum tier) includes only markdown/state files
- Cloud agent (Platinum tier) never stores banking credentials or payment tokens
- Always validate approval files before executing sensitive actions

## Reference Documentation

- Full hackathon guide: `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- Playwright skill: `.claude/skills/browsing-with-playwright/SKILL.md`
- Weekly research meetings: Wednesdays 10:00 PM on Zoom (details in hackathon doc)
