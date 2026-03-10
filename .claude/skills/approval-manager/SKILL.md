---
name: approval-manager
description: |
  Manage human-in-the-loop approval workflow. Creates approval requests for sensitive actions,
  monitors approval status, executes approved actions, and handles rejections. Use when
  processing tasks that require human authorization.
---

# Approval Manager

Manage the human-in-the-loop (HITL) approval workflow for sensitive actions.

## When to Use

- Create approval requests for sensitive actions
- Monitor `/Pending_Approval` folder for status changes
- Execute approved actions from `/Approved` folder
- Handle rejected actions from `/Rejected` folder
- Track approval metrics and response times

## Workflow

### 1. Identify Actions Requiring Approval

Based on Company Handbook rules, these actions require approval:
- Sending emails (especially to new contacts)
- Payments over threshold (e.g., $500)
- Social media posts (LinkedIn, Twitter, etc.)
- Modifying accounting records
- Any irreversible actions
- Actions with brand/reputation impact

### 2. Create Approval Request

Generate a detailed approval request file:

```markdown
---
type: approval_request
action: email_send
recipient: john@example.com
subject: Re: Partnership Inquiry
created: 2026-03-09T10:00:00Z
expires: 2026-03-10T10:00:00Z
status: pending
priority: medium
risk_level: medium
---

## Action Summary

**Action Type:** Send Email
**Target:** john@example.com
**Subject:** Re: Partnership Inquiry

## Action Details

### Email Content

[Full email draft here]

### Context

John reached out via LinkedIn asking about potential partnership opportunities.
This is our first communication with him. He represents a mid-size consulting
firm that could be a good referral partner.

### Why This Action

- Respond to legitimate business inquiry
- Establish new business relationship
- Potential revenue opportunity

## Risk Assessment

**Risk Level:** Medium

**Potential Risks:**
- First-time contact (unknown reputation)
- Represents company brand
- Could lead to business commitment

**Mitigation:**
- Professional tone maintained
- No commitments made in email
- Suggests exploratory call first

## Approval Instructions

### To Approve
Move this file to `/Approved` folder. The action will be executed automatically.

### To Reject
Move this file to `/Rejected` folder and add rejection reason in Notes section below.

### To Edit
Modify the action details above and leave in `/Pending_Approval` folder.

## Expiration

This approval request expires on 2026-03-10 at 10:00 AM.
If not approved by then, it will be automatically moved to `/Rejected`.

## Notes

[Human can add notes here]
```

### 3. Monitor Approval Status

Check folders for status changes:

```bash
# Check pending approvals
ls AI_Employee_Vault/Pending_Approval/

# Check approved actions
ls AI_Employee_Vault/Approved/

# Check rejected actions
ls AI_Employee_Vault/Rejected/
```

### 4. Execute Approved Actions

When file is moved to `/Approved`:

```bash
# Read the approved action file
# Extract action type and parameters
# Execute via appropriate MCP server or skill
# Log the execution
# Move to /Done
```

**Action Execution by Type:**

**Email Send:**
```bash
# Use Email MCP to send
# Log to /Logs/email_sent.md
# Update Dashboard
```

**LinkedIn Post:**
```bash
# Use Playwright browser automation
# Post content to LinkedIn
# Take screenshot confirmation
# Log to /Logs/linkedin_posts.md
```

**Payment:**
```bash
# Use Playwright to navigate payment portal
# Enter payment details
# Confirm transaction
# Log to /Accounting/transactions.md
```

### 5. Handle Rejections

When file is moved to `/Rejected`:

```bash
# Read rejection reason
# Log the rejection
# Notify via Dashboard
# Archive to /Done with rejection note
# Learn from feedback for future requests
```

### 6. Handle Expirations

Check for expired approval requests:

```bash
# Find requests past expiration time
# Move to /Rejected with "Expired" reason
# Alert via Dashboard
# Log the expiration
```

## Approval Request Templates

### Email Approval

```markdown
---
type: approval_request
action: email_send
recipient: [email]
subject: [subject]
---

## Email Content
[Draft email]

## Context
[Why sending this email]

## Risk Assessment
[Low/Medium/High and why]
```

### Payment Approval

```markdown
---
type: approval_request
action: payment
recipient: [payee]
amount: [amount]
currency: USD
---

## Payment Details
- **Amount:** $[amount]
- **Recipient:** [name]
- **Purpose:** [reason]
- **Invoice:** [invoice_number]

## Budget Impact
[How this affects budget]

## Verification
- [ ] Invoice verified
- [ ] Amount correct
- [ ] Recipient confirmed
- [ ] Budget available
```

### Social Media Approval

```markdown
---
type: approval_request
action: social_post
platform: linkedin
---

## Post Content
[Full post text]

## Hashtags
[List of hashtags]

## Target Audience
[Who this is for]

## Expected Outcome
[Goals and metrics]
```

## Approval Metrics

Track these metrics in `/Logs/approval_metrics.md`:

- Total approval requests created
- Approval rate (approved vs rejected)
- Average approval time
- Expired requests
- Approval requests by type
- Approval requests by risk level

## Approval Workflow States

```
pending → approved → executed → done
        ↓
        rejected → archived
        ↓
        expired → archived
```

## Risk Levels

**Low Risk:**
- Known contacts
- Routine communications
- Small payments (<$100)
- Internal actions

**Medium Risk:**
- New contacts
- Brand representation
- Moderate payments ($100-$500)
- Public posts

**High Risk:**
- Large payments (>$500)
- Legal/compliance matters
- Sensitive information
- Irreversible actions

## Auto-Approval Rules

Some actions can be auto-approved based on rules:

```markdown
## Auto-Approval Criteria

- Emails to known contacts (in whitelist)
- Payments under $50 to verified vendors
- Scheduled posts (pre-approved in advance)
- Routine status updates
```

**Implementation:**
- Check action against auto-approval rules
- If matches, skip approval and execute directly
- Log as "auto-approved" for audit trail

## Error Handling

If action execution fails after approval:
1. Log the error with full details
2. Create alert in Dashboard
3. Move approval back to `/Pending_Approval` with error note
4. Notify human of failure
5. Do not retry automatically

## Integration with Other Skills

- **email-processor** - Creates email approval requests
- **linkedin-automation** - Creates post approval requests
- **plan-generator** - Plans identify approval needs
- **dashboard-manager** - Updates approval status
- **vault-processor** - Triggers approval workflow

## Key Principles

1. **Default to approval** - When in doubt, ask for approval
2. **Clear communication** - Explain what will happen and why
3. **Risk transparency** - Be honest about potential risks
4. **Respect decisions** - Honor rejections without retry
5. **Learn from feedback** - Improve future requests based on patterns
6. **Audit everything** - Log all approval decisions

## File Naming Conventions

- Approval requests: `APPROVAL_[action]_[description]_[date].md`
- Example: `APPROVAL_EMAIL_client_inquiry_20260309.md`
- Example: `APPROVAL_PAYMENT_invoice_1234_20260309.md`
- Example: `APPROVAL_LINKEDIN_product_launch_20260309.md`

## Tips

- Provide enough context for informed decisions
- Include risk assessment in every request
- Set reasonable expiration times
- Make approval/reject actions easy (just move file)
- Track approval patterns to improve auto-approval rules
- Always explain why approval is needed
- Include preview of what will happen
- Offer edit option for minor changes
