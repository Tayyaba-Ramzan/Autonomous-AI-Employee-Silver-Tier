---
name: vault-processor
description: |
  Process tasks in the AI Employee Obsidian vault. Reads files from /Needs_Action,
  analyzes them according to Company_Handbook rules, creates plans, and manages
  the task workflow. Use this skill when you need to process pending tasks,
  update the dashboard, or manage the vault workflow.
---

# Vault Processor

Process and manage tasks in the AI Employee Obsidian vault.

## When to Use

- Process files in /Needs_Action folder
- Create task plans with checkboxes
- Update Dashboard with current status
- Move completed tasks to /Done
- Generate status reports
- Analyze pending approvals

## Workflow

### 1. Check for Pending Tasks

```bash
# List all files in Needs_Action
ls AI_Employee_Vault/Needs_Action/
```

### 2. Read Task Files

Use the Read tool to examine each task file. Look for:
- Task type (email, file_drop, etc.)
- Priority level
- Required actions
- Any special instructions

### 3. Consult Company Handbook

Always read `AI_Employee_Vault/Company_Handbook.md` to understand:
- Approval requirements
- Communication guidelines
- Financial rules
- Security policies

### 4. Create Action Plan

For each task, create a plan file in `/Plans`:

```markdown
---
created: 2026-03-08T10:00:00Z
task_id: TASK_001
status: in_progress
---

## Objective
[Clear description of what needs to be done]

## Steps
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Approval Required
[Yes/No and why]

## Notes
[Any relevant context]
```

### 5. Execute or Request Approval

**If approval required:**
- Create file in `/Pending_Approval` with details
- Wait for human to move to `/Approved`

**If no approval required:**
- Execute the task
- Document the outcome

### 6. Update Dashboard

After processing tasks, update `Dashboard.md`:
- Increment completed tasks counter
- Add to recent activity
- Update alerts if needed
- Refresh quick stats

### 7. Move to Done

When task is complete:
- Move original file from `/Needs_Action` to `/Done`
- Move plan file from `/Plans` to `/Done`
- Log the completion

## Example: Processing a File Drop

```bash
# 1. Check for new tasks
ls AI_Employee_Vault/Needs_Action/

# 2. Read the task file
# Use Read tool on: AI_Employee_Vault/Needs_Action/FILE_document_20260308.md

# 3. Read handbook for guidance
# Use Read tool on: AI_Employee_Vault/Company_Handbook.md

# 4. Create a plan
# Use Write tool to create: AI_Employee_Vault/Plans/PLAN_document_20260308.md

# 5. If approval needed, create approval request
# Use Write tool to create: AI_Employee_Vault/Pending_Approval/APPROVAL_document_20260308.md

# 6. Update dashboard
# Use Edit tool to update: AI_Employee_Vault/Dashboard.md

# 7. When complete, move files
# Move files to /Done folder
```

## Key Principles

1. **Always read Company_Handbook.md first** - It contains the rules
2. **Create plans before acting** - Document your reasoning
3. **Request approval for sensitive actions** - Better safe than sorry
4. **Update Dashboard regularly** - Keep status current
5. **Log everything** - Maintain audit trail
6. **Move completed tasks to /Done** - Keep workspace clean

## File Naming Conventions

- Plans: `PLAN_[description]_[date].md`
- Approvals: `APPROVAL_[action]_[description]_[date].md`
- Logs: `LOG_[date].md`

## Status Values

- `pending` - Not yet started
- `in_progress` - Currently working on it
- `awaiting_approval` - Waiting for human approval
- `completed` - Finished successfully
- `failed` - Encountered error
- `cancelled` - No longer needed

## Error Handling

If you encounter an error:
1. Log it in `/Logs` folder
2. Create alert in Dashboard
3. Move problematic file to `/Needs_Action` with error note
4. Do not retry automatically - wait for human review

## Tips

- Process tasks in priority order (high → medium → low)
- Batch similar tasks together for efficiency
- Always verify before taking irreversible actions
- When in doubt, ask for approval
- Keep the Dashboard updated in real-time
