---
name: email-processor
description: |
  Process email-related tasks from the vault. Reads email action files, drafts responses
  according to Company_Handbook rules, creates approval requests for outgoing emails,
  and manages email workflow. Use when processing Gmail notifications or email tasks.
---

# Email Processor

Process and manage email-related tasks in the AI Employee vault.

## When to Use

- Process email notifications from Gmail Watcher
- Draft email responses based on Company Handbook rules
- Create approval requests for outgoing emails
- Send approved emails via Email MCP
- Archive completed email tasks

## Workflow

### 1. Process Incoming Email Task

```bash
# Check for email tasks in Needs_Action
ls AI_Employee_Vault/Needs_Action/EMAIL_*.md
```

### 2. Read Email Content

Use Read tool to examine the email task file. Look for:
- Sender information
- Subject line
- Email body
- Priority level
- Required response type

### 3. Consult Company Handbook

Read `AI_Employee_Vault/Company_Handbook.md` for:
- Email response guidelines
- Tone and style requirements
- Approval thresholds
- Auto-response rules

### 4. Draft Response

Create a draft response following these principles:
- Match the tone (professional, friendly, formal)
- Address all questions/concerns
- Include necessary information
- Keep it concise
- Proofread for errors

### 5. Create Approval Request

For outgoing emails, create approval file in `/Pending_Approval`:

```markdown
---
type: approval_request
action: email_send
recipient: john@example.com
subject: Re: Project Update
created: 2026-03-09T10:00:00Z
expires: 2026-03-10T10:00:00Z
status: pending
---

## Email Details

**To:** john@example.com
**Subject:** Re: Project Update
**Priority:** Medium

## Draft Email Body

[Your drafted email content here]

## Context

This is a response to John's inquiry about the Q1 project timeline.
He asked for an update on deliverables and next steps.

## Approval Instructions

- **To Approve:** Move this file to `/Approved` folder
- **To Reject:** Move this file to `/Rejected` folder with reason
- **To Edit:** Modify the draft above and leave in this folder

## Risk Assessment

- Low risk: Known contact, routine business communication
- No sensitive information disclosed
- Professional tone maintained
```

### 6. Send Approved Emails

When email is approved (file moved to `/Approved`):

```bash
# Use Email MCP to send
# This would be triggered by orchestrator watching /Approved folder
```

### 7. Log and Archive

After sending:
- Log the action to `/Logs`
- Move original task to `/Done`
- Move approval request to `/Done`
- Update Dashboard

## Email Classification

**Auto-Response Candidates (Low Risk):**
- Thank you messages
- Acknowledgment receipts
- Meeting confirmations
- Status updates to known contacts

**Requires Approval (Medium/High Risk):**
- First-time contacts
- Sensitive information
- Financial discussions
- Legal matters
- Complaints or disputes

## Response Templates

### Professional Response
```
Dear [Name],

Thank you for reaching out regarding [topic].

[Main response content]

Please let me know if you need any additional information.

Best regards,
[Your Name]
```

### Quick Acknowledgment
```
Hi [Name],

Thanks for your email. I've received your message about [topic] and will get back to you by [date].

Best,
[Your Name]
```

### Meeting Request
```
Hi [Name],

I'd be happy to discuss [topic]. I'm available:
- [Option 1]
- [Option 2]
- [Option 3]

Please let me know what works best for you.

Best regards,
[Your Name]
```

## Error Handling

If email processing fails:
1. Log error to `/Logs/errors.md`
2. Create alert in Dashboard
3. Move task back to `/Needs_Action` with error note
4. Do not retry automatically

## Integration with Email MCP

The Email MCP server should be configured in `~/.config/claude-code/mcp.json`:

```json
{
  "servers": [
    {
      "name": "email",
      "command": "node",
      "args": ["/path/to/email-mcp/index.js"],
      "env": {
        "GMAIL_CREDENTIALS": "/path/to/credentials.json"
      }
    }
  ]
}
```

## Key Principles

1. **Always read Company_Handbook.md** - Follow communication guidelines
2. **Draft before sending** - Never send without review
3. **Request approval for new contacts** - Better safe than sorry
4. **Maintain professional tone** - Represent the user well
5. **Log all actions** - Maintain audit trail
6. **Respond promptly** - Process emails within 24 hours

## File Naming Conventions

- Email tasks: `EMAIL_[sender]_[date].md`
- Approval requests: `APPROVAL_EMAIL_[recipient]_[date].md`
- Logs: `LOG_EMAIL_[date].md`

## Tips

- Check for urgent keywords: "urgent", "asap", "important"
- Prioritize emails from VIP contacts
- Batch similar responses together
- Use templates for common scenarios
- Always verify recipient email addresses
- Double-check attachments if mentioned
