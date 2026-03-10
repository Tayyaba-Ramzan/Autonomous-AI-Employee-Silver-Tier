"""
MCP Client for Gmail Server
Communicates with Gmail MCP server via stdio protocol
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

class MCPClient:
    """Client for communicating with MCP servers"""

    def __init__(self, server_command):
        self.server_command = server_command
        self.process = None
        self.request_id = 0

    def start(self):
        """Start MCP server process"""
        self.process = subprocess.Popen(
            self.server_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # Initialize connection
        init_request = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "gmail-mcp-client",
                    "version": "1.0.0"
                }
            }
        }

        response = self._send_request(init_request)
        return response

    def _next_id(self):
        """Get next request ID"""
        self.request_id += 1
        return self.request_id

    def _send_request(self, request):
        """Send request to MCP server"""
        if not self.process:
            raise Exception("MCP server not started")

        # Send request
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json)
        self.process.stdin.flush()

        # Read response
        response_line = self.process.stdout.readline()
        if not response_line:
            raise Exception("No response from MCP server")

        return json.loads(response_line)

    def call_tool(self, tool_name, arguments):
        """Call a tool on the MCP server"""
        request = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        response = self._send_request(request)

        if "error" in response:
            raise Exception(f"MCP error: {response['error']}")

        return response.get("result", response)

    def send_email(self, to, subject, body, cc=None, bcc=None):
        """Send email via MCP server"""
        arguments = {
            "to": to,
            "subject": subject,
            "body": body
        }

        if cc:
            arguments["cc"] = cc
        if bcc:
            arguments["bcc"] = bcc

        result = self.call_tool("send_email", arguments)

        # Extract result from MCP response
        if "content" in result:
            content = result["content"][0]["text"]
            return json.loads(content)

        return result

    def stop(self):
        """Stop MCP server process"""
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=5)


class GmailMCPEmailSender:
    """Email sender using Gmail MCP server"""

    def __init__(self, vault_path="AI_Employee_Vault"):
        self.vault_path = Path(vault_path)
        self.approved_dir = self.vault_path / "Approved"
        self.done_dir = self.vault_path / "Done"
        self.log_dir = self.vault_path / "Logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "email_mcp.log"

    def log(self, message):
        """Log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')

    def parse_email_file(self, file_path):
        """Parse email draft file"""
        import re

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        email_data = {
            "to": None,
            "subject": None,
            "body": None,
            "cc": None,
            "bcc": None
        }

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

    def process_approved_emails(self):
        """Process approved emails using MCP server"""
        self.log("=" * 60)
        self.log("Gmail MCP Email Sender - Processing Approved Emails")
        self.log("=" * 60)

        if not self.approved_dir.exists():
            self.log("No Approved directory found")
            return

        email_files = list(self.approved_dir.glob("DRAFT_*.md"))

        if not email_files:
            self.log("No approved email drafts found")
            return

        self.log(f"Found {len(email_files)} approved email(s)")

        # Start MCP client
        client = MCPClient(["python", "mcp_servers/gmail_server.py"])

        try:
            self.log("Starting Gmail MCP server...")
            client.start()
            self.log("MCP server started successfully")

            for email_file in email_files:
                try:
                    self.log(f"\nProcessing: {email_file.name}")

                    email_data = self.parse_email_file(email_file)

                    if not email_data["to"] or not email_data["subject"]:
                        self.log(f"[ERROR] Missing required fields (to/subject)")
                        continue

                    self.log(f"Sending via MCP: {email_data['to']}")

                    result = client.send_email(
                        email_data["to"],
                        email_data["subject"],
                        email_data["body"],
                        email_data.get("cc"),
                        email_data.get("bcc")
                    )

                    if result.get("success"):
                        self.log(f"[OK] Email sent (ID: {result['message_id']})")

                        # Log to markdown
                        log_entry = f"""
## Email Sent via MCP - {datetime.now().isoformat()}

**To:** {email_data['to']}
**Subject:** {email_data['subject']}
**Message ID:** {result['message_id']}
**Method:** Gmail MCP Server

### Body
```
{email_data['body']}
```

---
"""
                        email_log = self.log_dir / "emails_sent_mcp.md"
                        with open(email_log, 'a', encoding='utf-8') as f:
                            f.write(log_entry)

                        # Move to Done
                        done_file = self.done_dir / email_file.name
                        email_file.rename(done_file)
                        self.log(f"[OK] Moved to Done: {done_file.name}")

                except Exception as e:
                    self.log(f"[ERROR] Failed to process {email_file.name}: {e}")

        finally:
            client.stop()
            self.log("MCP server stopped")

        self.log("\n" + "=" * 60)
        self.log("Email processing complete")
        self.log("=" * 60)


def main():
    """Main entry point"""
    sender = GmailMCPEmailSender()
    sender.process_approved_emails()


if __name__ == "__main__":
    main()
