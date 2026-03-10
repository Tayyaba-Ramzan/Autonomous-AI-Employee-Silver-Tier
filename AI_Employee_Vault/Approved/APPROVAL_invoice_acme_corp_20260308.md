---
type: approval_request
action: send_invoice_email
priority: high
amount: 2500.00
recipient: Acme Corp
recipient_email: acme@example.com
invoice_number: INV-2026-001
created: 2026-03-08T22:14:00Z
expires: 2026-03-09T22:14:00Z
status: pending
approval_triggers:
  - new_contact
  - financial_transaction
  - email_to_new_contact
---

## Approval Required: Send Invoice to New Client

**⚠️ REQUIRES HUMAN APPROVAL**

This action has been flagged for approval based on Company Handbook rules.

### Action Summary

**Type:** Send invoice email to new client
**Priority:** High
**Financial Impact:** $2,500.00

### Details

- **Client:** Acme Corp (NEW CLIENT)
- **Email:** acme@example.com
- **Invoice Number:** INV-2026-001
- **Amount:** $2,500.00
- **Services:** Q1 Consulting Services
- **Payment Terms:** Net 30

### Why Approval is Required

According to Company Handbook rules, this action requires approval because:

1. ✓ **New Contact** - "Never send emails to new contacts without approval"
2. ✓ **Financial Transaction** - "Any financial transaction" requires approval
3. ✓ **Email to New Contact** - Sending email to acme@example.com (not in contact list)

### Proposed Action

If approved, the AI Employee will:
1. Draft professional invoice email
2. Attach invoice document (INV-2026-001)
3. Send to acme@example.com
4. Log transaction in /Accounting
5. Update Dashboard
6. Move task to /Done

### Risk Assessment

- **Low Risk:** Standard invoice for completed services
- **Verification Needed:** Confirm Acme Corp is legitimate client
- **Amount:** $2,500 is within normal range

### To Approve

Move this file to `/Approved` folder:
```bash
mv AI_Employee_Vault/Pending_Approval/APPROVAL_invoice_acme_corp_20260308.md AI_Employee_Vault/Approved/
```

### To Reject

Move this file to `/Rejected` folder:
```bash
mv AI_Employee_Vault/Pending_Approval/APPROVAL_invoice_acme_corp_20260308.md AI_Employee_Vault/Rejected/
```

### Additional Notes

- Invoice draft can be reviewed before final send
- Client contact information should be verified
- Payment terms are standard (Net 30)
- This is a high-priority task with end-of-week deadline

---
*Approval request created by AI Employee*
*Awaiting human decision*
