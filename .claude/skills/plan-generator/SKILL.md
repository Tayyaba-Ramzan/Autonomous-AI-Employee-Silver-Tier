---
name: plan-generator
description: |
  Generate structured task plans with checkboxes for multi-step tasks. Breaks down complex
  tasks into actionable steps, tracks progress, and manages plan lifecycle. Use when processing
  tasks that require multiple steps or coordination.
---

# Plan Generator

Create and manage structured task plans with checkboxes.

## When to Use

- Break down complex tasks into steps
- Create actionable plans for multi-step workflows
- Track progress on ongoing tasks
- Document reasoning and approach
- Coordinate between multiple actions

## Workflow

### 1. Analyze Task

Read the task file from `/Needs_Action` and understand:
- What needs to be accomplished
- What resources are required
- What dependencies exist
- What risks are involved
- What approval is needed

### 2. Consult Company Handbook

Read `AI_Employee_Vault/Company_Handbook.md` for:
- Relevant policies and procedures
- Approval requirements
- Risk thresholds
- Communication guidelines

### 3. Create Plan File

Generate a structured plan in `/Plans` folder:

```markdown
---
created: 2026-03-09T10:00:00Z
task_id: TASK_001
task_type: email_response
priority: high
status: in_progress
estimated_duration: 30min
requires_approval: true
---

## Objective

[Clear, concise description of what needs to be accomplished]

## Context

[Background information, why this task is important, relevant details]

## Steps

- [ ] Step 1: Read and analyze the incoming email
- [ ] Step 2: Research relevant information from past communications
- [ ] Step 3: Draft response following Company Handbook guidelines
- [ ] Step 4: Create approval request in /Pending_Approval
- [ ] Step 5: Wait for human approval
- [ ] Step 6: Send approved email via Email MCP
- [ ] Step 7: Log action and update Dashboard
- [ ] Step 8: Move task to /Done

## Approval Required

**Yes** - This is a response to a new client inquiry and requires human review before sending.

**Approval Type:** Email send
**Risk Level:** Medium
**Reason:** First-time contact, represents company brand

## Dependencies

- Email MCP server must be running
- Gmail credentials must be valid
- Company_Handbook.md must be accessible

## Success Criteria

- [ ] Email sent successfully
- [ ] Professional tone maintained
- [ ] All questions answered
- [ ] Response sent within 24 hours
- [ ] Action logged in audit trail

## Risks and Mitigation

**Risk:** Email contains incorrect information
**Mitigation:** Verify all facts before drafting, request approval

**Risk:** Email sent to wrong recipient
**Mitigation:** Double-check email address, use approval workflow

## Notes

[Any additional context, observations, or considerations]

## Progress Log

- 2026-03-09 10:00 - Plan created
- 2026-03-09 10:15 - Email analyzed, draft in progress
- 2026-03-09 10:30 - Draft completed, approval requested
```

### 4. Update Plan Progress

As work progresses, update the plan:

```bash
# Mark steps as completed by changing [ ] to [x]
# Add progress log entries
# Update status field in frontmatter
```

### 5. Handle Blockers

If a step is blocked:

```markdown
## Blockers

- **Step 4 blocked:** Waiting for human approval (moved to /Pending_Approval)
- **Expected resolution:** Within 4 hours
- **Next action:** Check /Approved folder for approval
```

### 6. Complete Plan

When all steps are done:
- Mark all checkboxes as complete
- Update status to `completed`
- Add completion timestamp
- Move plan to `/Done`
- Update Dashboard

## Plan Templates

### Email Response Plan

```markdown
---
task_type: email_response
priority: medium
requires_approval: true
---

## Objective
Respond to [sender] regarding [topic]

## Steps
- [ ] Read and analyze email
- [ ] Check Company Handbook for guidelines
- [ ] Draft response
- [ ] Create approval request
- [ ] Wait for approval
- [ ] Send email
- [ ] Log and archive

## Approval Required
Yes - New contact / Sensitive topic
```

### LinkedIn Post Plan

```markdown
---
task_type: linkedin_post
priority: low
requires_approval: true
---

## Objective
Create LinkedIn post about [topic] to generate leads

## Steps
- [ ] Research topic and gather insights
- [ ] Draft post content (hook, value, CTA)
- [ ] Select relevant hashtags
- [ ] Create approval request
- [ ] Wait for approval
- [ ] Post to LinkedIn via Playwright
- [ ] Log and track engagement

## Approval Required
Yes - All social media posts require approval
```

### Payment Processing Plan

```markdown
---
task_type: payment
priority: high
requires_approval: true
---

## Objective
Process payment of $[amount] to [recipient] for [reason]

## Steps
- [ ] Verify invoice details
- [ ] Check budget and approval threshold
- [ ] Create approval request (payment >$500)
- [ ] Wait for approval
- [ ] Navigate to payment portal via Playwright
- [ ] Enter payment details
- [ ] Confirm transaction
- [ ] Log to /Accounting
- [ ] Update Dashboard

## Approval Required
Yes - Payment exceeds $500 threshold
```

### File Processing Plan

```markdown
---
task_type: file_processing
priority: medium
requires_approval: false
---

## Objective
Process and organize [file_name] from drop folder

## Steps
- [ ] Read file content
- [ ] Determine file type and purpose
- [ ] Extract relevant information
- [ ] Create summary in vault
- [ ] Move file to appropriate folder
- [ ] Update Dashboard
- [ ] Log action

## Approval Required
No - Routine file organization
```

## Plan Status Values

- `pending` - Not yet started
- `in_progress` - Currently working on it
- `blocked` - Waiting for dependency or approval
- `completed` - All steps finished successfully
- `failed` - Encountered unrecoverable error
- `cancelled` - No longer needed

## Priority Levels

- `critical` - Urgent, time-sensitive, high impact
- `high` - Important, should be done today
- `medium` - Normal priority, within 2-3 days
- `low` - Nice to have, when time permits

## Best Practices

1. **Be specific** - Each step should be clear and actionable
2. **Be realistic** - Don't create 50-step plans, break into sub-plans
3. **Track progress** - Update checkboxes as you complete steps
4. **Document blockers** - Note what's preventing progress
5. **Estimate time** - Help prioritize and schedule work
6. **Identify risks** - Think ahead about what could go wrong
7. **Define success** - Know when the task is truly complete

## Integration with Other Skills

- **vault-processor** - Reads tasks, triggers plan generation
- **email-processor** - Uses plans for email workflows
- **linkedin-automation** - Uses plans for posting workflows
- **approval-manager** - Plans identify what needs approval
- **dashboard-manager** - Plans update Dashboard status

## Error Handling

If plan execution fails:
1. Mark the failed step in the plan
2. Document the error in Notes section
3. Update status to `failed` or `blocked`
4. Create alert in Dashboard
5. Log error to `/Logs/errors.md`
6. Do not proceed to next steps

## Key Principles

1. **Plan before acting** - Think through the approach
2. **Break down complexity** - Make tasks manageable
3. **Track progress** - Know where you are in the workflow
4. **Document reasoning** - Explain why you're doing what you're doing
5. **Identify approval needs** - Flag sensitive actions early
6. **Update regularly** - Keep plans current and accurate

## File Naming Conventions

- Plans: `PLAN_[task_type]_[description]_[date].md`
- Example: `PLAN_EMAIL_client_inquiry_20260309.md`
- Example: `PLAN_LINKEDIN_product_launch_20260309.md`

## Tips

- Create plans for any task with 3+ steps
- Use checkboxes for trackable progress
- Update plans in real-time as work progresses
- Archive completed plans to /Done
- Review failed plans to improve future planning
- Keep plans focused - one objective per plan
