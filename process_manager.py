"""
AI Employee Process Manager
Keeps watchers running and restarts them if they crash
"""

import subprocess
import time
import sys
from pathlib import Path
from datetime import datetime
import signal

class ProcessManager:
    """Manage and monitor watcher processes"""

    def __init__(self):
        self.processes = {}
        self.running = True
        self.log_file = Path("AI_Employee_Vault/Logs/process_manager.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(self, message):
        """Log message to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')

    def start_process(self, name, command):
        """Start a process"""
        try:
            self.log(f"Starting {name}...")
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes[name] = {
                'process': process,
                'command': command,
                'start_time': datetime.now(),
                'restarts': 0
            }
            self.log(f"{name} started (PID: {process.pid})")
            return True
        except Exception as e:
            self.log(f"Failed to start {name}: {e}")
            return False

    def check_process(self, name):
        """Check if process is running"""
        if name not in self.processes:
            return False

        process_info = self.processes[name]
        process = process_info['process']

        # Check if process is still running
        if process.poll() is None:
            return True
        else:
            return False

    def restart_process(self, name):
        """Restart a crashed process"""
        if name not in self.processes:
            return False

        process_info = self.processes[name]
        process_info['restarts'] += 1

        self.log(f"{name} crashed! Restarting (restart #{process_info['restarts']})...")

        # Wait before restart
        time.sleep(5)

        # Start new process
        return self.start_process(name, process_info['command'])

    def stop_all(self):
        """Stop all processes"""
        self.log("Stopping all processes...")
        for name, info in self.processes.items():
            try:
                process = info['process']
                if process.poll() is None:
                    self.log(f"Stopping {name} (PID: {process.pid})...")
                    process.terminate()
                    process.wait(timeout=10)
                    self.log(f"{name} stopped")
            except Exception as e:
                self.log(f"Error stopping {name}: {e}")

    def check_approved_emails(self):
        """Check for approved emails and process them"""
        approved_dir = Path("AI_Employee_Vault/Approved")
        if not approved_dir.exists():
            return

        # Find approved email drafts
        email_drafts = list(approved_dir.glob("DRAFT_*.md"))

        if email_drafts:
            self.log(f"Found {len(email_drafts)} approved email(s) to send")
            try:
                # Run MCP-based email sender
                result = subprocess.run(
                    ["python", "email_sender_mcp.py"],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode == 0:
                    self.log("Email sending via MCP completed successfully")
                else:
                    self.log(f"Email sending via MCP failed: {result.stderr}")
            except Exception as e:
                self.log(f"Error running MCP email sender: {e}")

    def run(self):
        """Main monitoring loop"""
        self.log("=" * 60)
        self.log("AI Employee Process Manager Started")
        self.log("=" * 60)

        # Define watchers to run
        watchers = {
            'Gmail Watcher': 'python watchers/gmail_watcher.py --vault-path AI_Employee_Vault',
            'LinkedIn Watcher': 'python watchers/linkedin_watcher.py --vault-path AI_Employee_Vault'
        }

        # Start all watchers
        for name, command in watchers.items():
            self.start_process(name, command)

        self.log("All watchers started. Monitoring...")
        self.log("Press Ctrl+C to stop")

        # Monitor loop
        try:
            check_count = 0
            while self.running:
                time.sleep(30)  # Check every 30 seconds
                check_count += 1

                # Check watcher processes
                for name in list(self.processes.keys()):
                    if not self.check_process(name):
                        self.log(f"[ALERT] {name} is not running!")
                        self.restart_process(name)

                # Check for approved emails every 2 minutes (4 cycles)
                if check_count % 4 == 0:
                    self.check_approved_emails()

        except KeyboardInterrupt:
            self.log("\nShutdown signal received")
            self.running = False
            self.stop_all()
            self.log("Process Manager stopped")

def main():
    manager = ProcessManager()
    manager.run()

if __name__ == "__main__":
    main()
