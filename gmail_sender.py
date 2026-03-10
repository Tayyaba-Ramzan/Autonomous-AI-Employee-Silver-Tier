"""
Gmail Email Sender
Sends emails using Gmail API (same credentials as Gmail Watcher)
"""

import os
import pickle
from pathlib import Path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import re
import sys

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
ALLOWED_RECIPIENT = "tayyabaramzan2026@gmail.com"

class GmailSender:
    """Send emails via Gmail API"""

    def __init__(self, credentials_path="credentials/gmail_credentials.json"):
        self.credentials_path = credentials_path
        self.token_path = "credentials/gmail_token_sender.pickle"
        self.service = None
        self.allowed_recipient = ALLOWED_RECIPIENT
        self.log_dir = Path("AI_Employee_Vault/Logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "email_sender.log"

    def validate_recipient(self, email):
        """Validate that recipient is allowed"""
        if email != self.allowed_recipient:
            raise ValueError(
                f"BLOCKED: Email can only be sent to {self.allowed_recipient}. "
                f"Attempted to send to: {email}"
            )
        return True

    def log(self, message):
        """Log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')

    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None

        # Load existing token
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                self.log("Refreshing Gmail credentials...")
                creds.refresh(Request())
            else:
                self.log("Starting OAuth flow for Gmail sending...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)
        self.log("Gmail authentication successful")
        return True

    def create_message(self, to, subject, body, cc=None, bcc=None):
        """Create email message"""
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject

        if cc:
            message['cc'] = cc
        if bcc:
            message['bcc'] = bcc

        msg = MIMEText(body, 'plain')
        message.attach(msg)

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return {'raw': raw}

    def send_email(self, to, subject, body, cc=None, bcc=None):
        """Send email via Gmail API"""
        # STRICT VALIDATION: Only allow configured recipient
        self.validate_recipient(to)

        try:
            if not self.service:
                self.authenticate()

            self.log(f"Sending email to: {to}")
            self.log(f"Subject: {subject}")

            message = self.create_message(to, subject, body, cc, bcc)
            result = self.service.users().messages().send(
                userId='me',
                body=message
            ).execute()

            self.log(f"[OK] Email sent successfully (ID: {result['id']})")

            # Log to markdown
            log_entry = f"""
## Email Sent - {datetime.now().isoformat()}

**To:** {to}
**Subject:** {subject}
{f"**CC:** {cc}" if cc else ""}
{f"**BCC:** {bcc}" if bcc else ""}
**Message ID:** {result['id']}

### Body
```
{body}
```

---
"""

            email_log = self.log_dir / "emails_sent.md"
            with open(email_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)

            return {
                "success": True,
                "message_id": result['id'],
                "message": "Email sent successfully"
            }

        except Exception as e:
            self.log(f"[ERROR] Failed to send email: {e}")
            return {
                "success": False,
                "message": str(e)
            }

    def parse_email_file(self, file_path):
        """Parse email draft file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        email_data = {
            "to": None,
            "subject": None,
            "body": None,
            "cc": None,
            "bcc": None
        }

        # Extract frontmatter
        frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)

        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)

            to_match = re.search(r'to:\s*(.+)', frontmatter)
            subject_match = re.search(r'subject:\s*(.+)', frontmatter)
            cc_match = re.search(r'cc:\s*(.+)', frontmatter)
            bcc_match = re.search(r'bcc:\s*(.+)', frontmatter)

            if to_match:
                email_data["to"] = to_match.group(1).strip()
            if subject_match:
                email_data["subject"] = subject_match.group(1).strip()
            if cc_match:
                email_data["cc"] = cc_match.group(1).strip()
            if bcc_match:
                email_data["bcc"] = bcc_match.group(1).strip()

            body_start = frontmatter_match.end()
            email_data["body"] = content[body_start:].strip()
        else:
            email_data["body"] = content.strip()

        return email_data

    def process_approved_emails(self, vault_path="AI_Employee_Vault"):
        """Process all approved email drafts"""
        vault = Path(vault_path)
        approved_dir = vault / "Approved"
        done_dir = vault / "Done"

        self.log("=" * 60)
        self.log("Gmail Email Sender - Processing Approved Emails")
        self.log("=" * 60)

        if not approved_dir.exists():
            self.log("No Approved directory found")
            return

        email_files = list(approved_dir.glob("DRAFT_*.md"))

        if not email_files:
            self.log("No approved email drafts found")
            return

        self.log(f"Found {len(email_files)} approved email(s)")

        for email_file in email_files:
            try:
                self.log(f"\nProcessing: {email_file.name}")

                email_data = self.parse_email_file(email_file)

                if not email_data["to"] or not email_data["subject"]:
                    self.log(f"[ERROR] Missing required fields (to/subject)")
                    continue

                result = self.send_email(
                    email_data["to"],
                    email_data["subject"],
                    email_data["body"],
                    email_data.get("cc"),
                    email_data.get("bcc")
                )

                if result["success"]:
                    done_file = done_dir / email_file.name
                    email_file.rename(done_file)
                    self.log(f"[OK] Moved to Done: {done_file.name}")

            except Exception as e:
                self.log(f"[ERROR] Failed to process {email_file.name}: {e}")

        self.log("\n" + "=" * 60)
        self.log("Email processing complete")
        self.log("=" * 60)


def main():
    """Main entry point"""
    sender = GmailSender()

    if len(sys.argv) == 1:
        # Process approved emails
        sender.process_approved_emails()

    elif len(sys.argv) >= 4:
        # Send single email
        to = sys.argv[1]
        subject = sys.argv[2]
        body = sys.argv[3]

        print("=" * 60)
        print("Gmail Email Sender - Test")
        print("=" * 60)
        print(f"\nTo: {to}")
        print(f"Subject: {subject}")
        print(f"Body: {body[:100]}{'...' if len(body) > 100 else ''}")
        print()

        result = sender.send_email(to, subject, body)

        if result["success"]:
            print(f"\n[OK] Email sent successfully!")
            print(f"Message ID: {result['message_id']}")
            return 0
        else:
            print(f"\n[ERROR] Failed to send email: {result['message']}")
            return 1

    else:
        print("Usage:")
        print("  Process approved emails:")
        print("    python gmail_sender.py")
        print()
        print("  Send single email:")
        print('    python gmail_sender.py "to@example.com" "Subject" "Body text"')
        return 1


if __name__ == "__main__":
    sys.exit(main())
