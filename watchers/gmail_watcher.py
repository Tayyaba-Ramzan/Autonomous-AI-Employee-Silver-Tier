"""
Gmail Watcher

Monitors Gmail for important/unread messages and creates action files.
"""

import os
import sys
import pickle
import base64
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from base_watcher import BaseWatcher


# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailWatcher(BaseWatcher):
    """Watch Gmail for important/unread messages"""

    def __init__(self, vault_path, check_interval=120, credentials_path=None):
        """
        Initialize Gmail Watcher

        Args:
            vault_path: Path to Obsidian vault
            check_interval: Seconds between checks (default 120)
            credentials_path: Path to Gmail credentials.json
        """
        super().__init__(vault_path, check_interval)

        # Set credentials path
        if credentials_path:
            self.credentials_path = Path(credentials_path)
        else:
            self.credentials_path = Path("credentials/gmail_credentials.json")

        self.token_path = Path("credentials/gmail_token.pickle")

        # Initialize Gmail service
        self.service = self.authenticate()

    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None

        # Load existing token
        if self.token_path.exists():
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                self.logger.info("Refreshing Gmail credentials...")
                creds.refresh(Request())
            else:
                if not self.credentials_path.exists():
                    self.logger.error(f"Credentials file not found: {self.credentials_path}")
                    self.logger.error("Please download credentials.json from Google Cloud Console")
                    raise FileNotFoundError(f"Gmail credentials not found at {self.credentials_path}")

                self.logger.info("Starting OAuth flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
            self.logger.info("Gmail authentication successful")

        return build('gmail', 'v1', credentials=creds)

    def check_for_updates(self):
        """Check Gmail for new unread/important messages"""
        try:
            # Query for unread messages
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=10
            ).execute()

            messages = results.get('messages', [])

            if not messages:
                self.logger.info("No new emails")
                return

            self.logger.info(f"Found {len(messages)} unread email(s)")

            for message in messages:
                msg_id = message['id']

                # Skip if already processed
                if self.is_processed(msg_id):
                    continue

                # Get full message details
                msg = self.service.users().messages().get(
                    userId='me',
                    id=msg_id,
                    format='full'
                ).execute()

                # Extract message details
                headers = {h['name']: h['value'] for h in msg['payload']['headers']}
                subject = headers.get('Subject', 'No Subject')
                sender = headers.get('From', 'Unknown')
                date = headers.get('Date', '')

                # Get message body
                body = self.get_message_body(msg['payload'])

                # Check if important
                labels = msg.get('labelIds', [])
                is_important = 'IMPORTANT' in labels

                # Create action file
                self.create_email_action_file(msg_id, sender, subject, body, date, is_important)

                # Mark as processed
                self.mark_as_processed(msg_id)

        except Exception as e:
            self.logger.error(f"Error checking Gmail: {e}", exc_info=True)

    def get_message_body(self, payload):
        """Extract message body from payload"""
        body = ""

        try:
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        if 'data' in part['body']:
                            body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                            break
                    elif 'parts' in part:
                        # Recursive for nested parts
                        for subpart in part['parts']:
                            if subpart['mimeType'] == 'text/plain' and 'data' in subpart['body']:
                                body = base64.urlsafe_b64decode(subpart['body']['data']).decode('utf-8', errors='ignore')
                                break
            elif 'body' in payload and 'data' in payload['body']:
                body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
        except Exception as e:
            self.logger.error(f"Error extracting message body: {e}")
            body = "[Could not extract message body]"

        return body[:1000]  # Limit to first 1000 chars

    def create_email_action_file(self, msg_id, sender, subject, body, date, is_important):
        """Create action file for email"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Clean sender for filename
        sender_clean = sender.split('<')[0].strip().replace(' ', '_')[:20]
        filename = f"EMAIL_{sender_clean}_{timestamp}.md"

        # Frontmatter
        frontmatter = {
            'type': 'email',
            'message_id': msg_id,
            'sender': sender,
            'subject': subject,
            'date': date,
            'is_important': is_important,
            'created': datetime.now().isoformat(),
            'status': 'pending',
            'priority': 'high' if is_important else 'medium'
        }

        # Content
        content = f"""
## Email from {sender}

**Subject:** {subject}

**Date:** {date}

**Important:** {'Yes' if is_important else 'No'}

### Message Body

{body}

### Required Action

- [ ] Read and analyze email
- [ ] Draft response
- [ ] Create approval request if needed
- [ ] Send response

### Notes

[Add notes here]
"""

        self.create_action_file(filename, frontmatter, content)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Gmail Watcher')
    parser.add_argument('--vault-path', required=True, help='Path to Obsidian vault')
    parser.add_argument('--check-interval', type=int, default=120, help='Check interval in seconds')
    parser.add_argument('--credentials', help='Path to Gmail credentials.json')

    args = parser.parse_args()

    watcher = GmailWatcher(
        vault_path=args.vault_path,
        check_interval=args.check_interval,
        credentials_path=args.credentials
    )

    watcher.run()
