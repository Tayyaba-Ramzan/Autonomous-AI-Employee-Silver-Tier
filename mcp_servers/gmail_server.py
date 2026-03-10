#!/usr/bin/env python3
"""
Gmail MCP Server
Implements Model Context Protocol for Gmail email sending
"""

import json
import sys
import os
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
ALLOWED_RECIPIENT = "tayyabaramzan2026@gmail.com"

class GmailMCPServer:
    """MCP Server for Gmail operations"""

    def __init__(self):
        self.credentials_path = "credentials/gmail_credentials.json"
        self.token_path = "credentials/gmail_token_sender.pickle"
        self.service = None
        self.allowed_recipient = ALLOWED_RECIPIENT

    def validate_recipient(self, email):
        """Validate that recipient is allowed"""
        if email != self.allowed_recipient:
            raise ValueError(
                f"BLOCKED: Email can only be sent to {self.allowed_recipient}. "
                f"Attempted to send to: {email}"
            )
        return True

    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None

        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)
        return True

    def send_email(self, to, subject, body, cc=None, bcc=None):
        """Send email via Gmail API"""
        # STRICT VALIDATION: Only allow configured recipient
        self.validate_recipient(to)

        if not self.service:
            self.authenticate()

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

        result = self.service.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()

        return {
            "success": True,
            "message_id": result['id'],
            "to": to,
            "subject": subject
        }

    def handle_request(self, request):
        """Handle MCP protocol request"""
        method = request.get("method")
        params = request.get("params", {})

        if method == "tools/list":
            return {
                "tools": [
                    {
                        "name": "send_email",
                        "description": "Send an email via Gmail",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "to": {
                                    "type": "string",
                                    "description": "Recipient email address"
                                },
                                "subject": {
                                    "type": "string",
                                    "description": "Email subject"
                                },
                                "body": {
                                    "type": "string",
                                    "description": "Email body text"
                                },
                                "cc": {
                                    "type": "string",
                                    "description": "CC recipients (optional)"
                                },
                                "bcc": {
                                    "type": "string",
                                    "description": "BCC recipients (optional)"
                                }
                            },
                            "required": ["to", "subject", "body"]
                        }
                    }
                ]
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            if tool_name == "send_email":
                result = self.send_email(
                    to=arguments.get("to"),
                    subject=arguments.get("subject"),
                    body=arguments.get("body"),
                    cc=arguments.get("cc"),
                    bcc=arguments.get("bcc")
                )
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }

        elif method == "initialize":
            return {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "gmail-mcp-server",
                    "version": "1.0.0"
                }
            }

        return {"error": "Unknown method"}

    def run(self):
        """Run MCP server (stdio mode)"""
        for line in sys.stdin:
            try:
                request = json.loads(line)
                response = self.handle_request(request)

                # Add id from request to response
                if "id" in request:
                    response["id"] = request["id"]

                print(json.dumps(response), flush=True)
            except Exception as e:
                error_response = {
                    "error": str(e)
                }
                if "id" in request:
                    error_response["id"] = request["id"]
                print(json.dumps(error_response), flush=True)


def main():
    server = GmailMCPServer()
    server.run()


if __name__ == "__main__":
    main()
