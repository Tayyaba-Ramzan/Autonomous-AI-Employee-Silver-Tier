---
name: dashboard-manager
description: |
  Manage and update the Dashboard.md file with real-time status information. Updates
  task counts, recent activity, alerts, and quick stats. Use when completing tasks
  or when status changes occur that should be reflected in the dashboard.
---

# Dashboard Manager

Manage and update the AI Employee Dashboard with real-time status.

## When to Use

- Update task completion counts
- Add recent activity entries
- Create or clear alerts
- Update quick stats (bank balance, pending items)
- Refresh dashboard after major actions
- Generate status summaries

## Dashboard Structure

The Dashboard.md file should contain:

```markdown
# AI Employee Dashboard

**Last Updated:** 2026-03-09 10:30:00

---

## Quick Stats

| Metric | Value | Status |
|--------|-------|--------|
| Bank Balance | $12,450.00 | ✅ Healthy |
| Pending Tasks | 3 | ⚠️ Attention |
| Pending Approvals | 1 | 🔔 Review |
| Completed Today | 5 | ✅ On Track |
| Active Projects | 2 | ✅ Active |

---

## Alerts

### 🔴 Critical
- None

### ⚠️ Warning
- 1 approval request pending for 4 hours (LinkedIn post)

### ℹ️ Info
- 2 new emails in Needs_Action folder

---

## Recent Activity

| Time | Action | Status |
|------|--------|--------|
| 10:25 | Sent email to john@example.com | ✅ Completed |
| 10:15 | Created LinkedIn post approval | 🔔 Pending |
| 10:00 | Processed file drop: invoice_123.pdf | ✅ Completed |
| 09:45 | Updated accounting records | ✅ Completed |
| 09:30 | Responded to WhatsApp message | ✅ Completed |

---

## Pending Tasks

### High Priority
1. **EMAIL_client_inquiry_20260309.md** - New client inquiry (2 hours old)

### Medium Priority
1. **LINKEDIN_POST_product_update_20260309.md** - Awaiting approval
2. **FILE_contract_review_20260309.md** - Contract needs review

### Low Priority
1. **TASK_organize_files_20260309.md** - Routine file organization

---

## Active Projects

### Q1 Business Development
- Status: On Track
- Progress: 60%
- Next Milestone: March 15
- Tasks: 3 pending, 7 completed

### Website Redesign
- Status: In Progress
- Progress: 40%
- Next Milestone: March 20
- Tasks: 5 pending, 4 completed

---

## This Week Summary

- **Tasks Completed:** 23
- **Emails Processed:** 15
- **LinkedIn Posts:** 2
- **Payments Made:** 3 ($1,250 total)
- **Files Organized:** 12

---

## System Health

| Component | Status | Last Check |
|-----------|--------|------------|
| Gmail Watcher | ✅ Running | 10:29 |
| WhatsApp Watcher | ✅ Running | 10:28 |
| Email MCP | ✅ Connected | 10:25 |
| Playwright MCP | ✅ Connected | 10:20 |
| Vault Sync | ✅ Synced | 10:00 |
```

## Workflow

### 1. Read Current Dashboard

```bash
# Read the current dashboard state
# Use Read tool on: AI_Employee_Vault/Dashboard.md
```

### 2. Update Specific Section

Use Edit tool to update relevant sections:

**Update Quick Stats:**
```markdown
| Metric | Value | Status |
|--------|-------|--------|
| Pending Tasks | 2 | ✅ Normal |
```

**Add Recent Activity:**
```markdown
| 10:30 | Processed email from client | ✅ Completed |
```

**Add Alert:**
```markdown
### ⚠️ Warning
- Payment approval pending for 6 hours (Invoice #1234)
```

### 3. Update Timestamp

Always update the "Last Updated" timestamp:

```markdown
**Last Updated:** 2026-03-09 10:30:00
```

### 4. Maintain Activity History

Keep recent activity limited to last 10-20 entries. Archive older entries to `/Logs/dashboard_history.md`.

## Update Triggers

Update Dashboard when:
- Task completed
- Task created
- Approval requested
- Approval granted/rejected
- Alert condition detected
- System status changes
- Significant action taken

## Quick Stats Calculations

**Bank Balance:**
- Read from `/Accounting/balance.md`
- Update when transactions occur
- Flag if below threshold

**Pending Tasks:**
- Count files in `/Needs_Action`
- Categorize by priority
- Flag if over threshold (>5)

**Pending Approvals:**
- Count files in `/Pending_Approval`
- Flag if any are urgent or expired
- Show oldest approval age

**Completed Today:**
- Count files moved to `/Done` today
- Reset at midnight
- Compare to daily target

**Active Projects:**
- Read from `/Projects/*.md`
- Count projects with status "active"
- Track progress percentage

## Alert Management

### Alert Levels

**🔴 Critical:**
- System failures
- Expired urgent approvals
- Security issues
- Bank balance below critical threshold

**⚠️ Warning:**
- Approvals pending >4 hours
- High priority tasks aging
- System performance issues
- Bank balance below warning threshold

**ℹ️ Info:**
- New tasks available
- Routine notifications
- System updates
- General status changes

### Alert Creation

```markdown
### ⚠️ Warning
- [Description of issue] ([time/context])
```

### Alert Resolution

When issue is resolved, remove the alert and optionally add to Recent Activity:

```markdown
| 10:35 | Resolved: Payment approval completed | ✅ Completed |
```

## Dashboard Templates

### Minimal Dashboard (Bronze Tier)

```markdown
# AI Employee Dashboard

**Last Updated:** [timestamp]

## Quick Stats
- Pending Tasks: [count]
- Completed Today: [count]

## Recent Activity
[Last 5 actions]

## Alerts
[Current alerts]
```

### Full Dashboard (Silver Tier)

Includes all sections shown in Dashboard Structure above.

### Executive Dashboard (Gold Tier)

Adds:
- Revenue tracking
- Business metrics
- CEO briefing section
- Cross-domain integration status

## Update Patterns

### After Task Completion

```markdown
1. Decrement "Pending Tasks"
2. Increment "Completed Today"
3. Add to "Recent Activity"
4. Clear related alerts
5. Update timestamp
```

### After Approval Request

```markdown
1. Increment "Pending Approvals"
2. Add alert if urgent
3. Add to "Recent Activity"
4. Update timestamp
```

### After System Check

```markdown
1. Update "System Health" section
2. Add alerts if issues detected
3. Update timestamp
```

## Integration with Other Skills

- **vault-processor** - Triggers dashboard updates
- **email-processor** - Updates after email actions
- **linkedin-automation** - Updates after posts
- **approval-manager** - Updates approval counts
- **plan-generator** - Updates task progress

## Key Principles

1. **Real-time updates** - Keep dashboard current
2. **Concise information** - Show what matters most
3. **Visual clarity** - Use emojis and tables for readability
4. **Actionable alerts** - Highlight what needs attention
5. **Historical context** - Show recent activity for context
6. **System transparency** - Show health of all components

## File Naming Conventions

- Dashboard: `Dashboard.md` (single file in vault root)
- History archive: `Logs/dashboard_history_[date].md`

## Tips

- Update dashboard after every significant action
- Keep recent activity to last 10-20 entries
- Use consistent emoji indicators
- Archive old activity to keep dashboard clean
- Prioritize critical information at top
- Use tables for structured data
- Include timestamps for all activities
- Clear resolved alerts promptly
- Update system health regularly (every 5-10 minutes)
