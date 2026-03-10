"""
AI Employee System Health Check
Verifies all components are ready and working
"""

import sys
from pathlib import Path
import subprocess

class HealthCheck:
    """System health checker"""

    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = []

    def check(self, name, condition, error_msg=""):
        """Run a health check"""
        print(f"Checking {name}...", end=" ")
        if condition:
            print("[OK]")
            self.checks_passed += 1
            return True
        else:
            print("[FAIL]")
            if error_msg:
                print(f"  Error: {error_msg}")
            self.checks_failed += 1
            return False

    def warn(self, message):
        """Add a warning"""
        print(f"[WARNING] {message}")
        self.warnings.append(message)

    def run_checks(self):
        """Run all health checks"""
        print("=" * 60)
        print("AI Employee System Health Check")
        print("=" * 60)
        print()

        # Check Python
        try:
            version = sys.version_info
            self.check(
                "Python version",
                version.major == 3 and version.minor >= 8,
                f"Python 3.8+ required, found {version.major}.{version.minor}"
            )
        except:
            self.check("Python version", False, "Could not determine Python version")

        # Check directories
        self.check(
            "AI_Employee_Vault directory",
            Path("AI_Employee_Vault").exists(),
            "Vault directory not found"
        )

        self.check(
            "Watchers directory",
            Path("watchers").exists(),
            "Watchers directory not found"
        )

        self.check(
            "Credentials directory",
            Path("credentials").exists(),
            "Credentials directory not found"
        )

        # Check watcher scripts
        self.check(
            "Gmail watcher script",
            Path("watchers/gmail_watcher.py").exists(),
            "gmail_watcher.py not found"
        )

        self.check(
            "LinkedIn watcher script",
            Path("watchers/linkedin_watcher.py").exists(),
            "linkedin_watcher.py not found"
        )

        # Check automation scripts
        self.check(
            "LinkedIn automation script",
            Path("linkedin_automation.py").exists(),
            "linkedin_automation.py not found"
        )

        self.check(
            "Process manager script",
            Path("process_manager.py").exists(),
            "process_manager.py not found"
        )

        # Check credentials
        gmail_creds = Path("credentials/gmail_credentials.json")
        if gmail_creds.exists():
            self.check("Gmail credentials", True)
        else:
            self.check("Gmail credentials", False, "Gmail credentials not found")
            self.warn("Gmail watcher will not work without credentials")

        gmail_token = Path("credentials/gmail_token.pickle")
        if gmail_token.exists():
            self.check("Gmail token", True)
        else:
            self.warn("Gmail token not found - first run will require authentication")

        # Check vault structure
        vault_dirs = [
            "AI_Employee_Vault/Needs_Action",
            "AI_Employee_Vault/Pending_Approval",
            "AI_Employee_Vault/Approved",
            "AI_Employee_Vault/Done",
            "AI_Employee_Vault/Logs"
        ]

        for dir_path in vault_dirs:
            self.check(
                f"Vault folder: {dir_path.split('/')[-1]}",
                Path(dir_path).exists()
            )

        # Check Python packages
        print()
        print("Checking Python packages...")

        # Map package names to their import names
        packages = {
            "playwright": "playwright",
            "google-auth": "google.auth",
            "google-auth-oauthlib": "google_auth_oauthlib",
            "google-api-python-client": "googleapiclient"
        }

        for package, import_name in packages.items():
            try:
                __import__(import_name)
                self.check(f"Package: {package}", True)
            except ImportError:
                self.check(f"Package: {package}", False, f"Run: pip install {package}")

        # Check Playwright browsers
        print()
        print("Checking Playwright browsers...")
        try:
            result = subprocess.run(
                ["python", "-m", "playwright", "install", "--dry-run"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if "chromium" in result.stdout.lower() or result.returncode == 0:
                self.check("Playwright browsers", True)
            else:
                self.warn("Playwright browsers may need installation: python -m playwright install")
        except:
            self.warn("Could not verify Playwright browsers")

        # Summary
        print()
        print("=" * 60)
        print("Health Check Summary")
        print("=" * 60)
        print(f"Checks passed: {self.checks_passed}")
        print(f"Checks failed: {self.checks_failed}")
        print(f"Warnings: {len(self.warnings)}")
        print()

        if self.checks_failed == 0:
            print("[OK] System is ready to run!")
            print()
            print("To start the AI Employee system:")
            print("  Windows: start_ai_employee.bat")
            print("  Linux/Mac: bash start_ai_employee.sh")
            print("  Manual: python process_manager.py")
            return True
        else:
            print("[ERROR] System has issues that need to be fixed")
            print("Please resolve the failed checks above")
            return False

def main():
    checker = HealthCheck()
    success = checker.run_checks()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
