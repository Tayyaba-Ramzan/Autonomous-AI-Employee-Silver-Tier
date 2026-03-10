"""
LinkedIn Watcher - Enhanced with Retry Logic and Error Handling

Improvements:
- Network retry with exponential backoff
- Better error handling
- Persistent browser context
- Health checks
"""

import sys
import time
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from base_watcher import BaseWatcher


class LinkedInWatcher(BaseWatcher):
    """Watch LinkedIn notifications via Playwright browser automation"""

    def __init__(self, vault_path, check_interval=180, session_path=None):
        """
        Initialize LinkedIn Watcher

        Args:
            vault_path: Path to Obsidian vault
            check_interval: Seconds between checks (default 180)
            session_path: Path to save browser session
        """
        super().__init__(vault_path, check_interval)

        # Session storage path
        if session_path:
            self.session_path = Path(session_path)
        else:
            self.session_path = Path("sessions/linkedin_session")

        self.session_path.mkdir(parents=True, exist_ok=True)

        self.logger.info("LinkedIn Watcher initialized")
        self.logger.info(f"Session path: {self.session_path}")

        # Retry configuration
        self.max_retries = 3
        self.retry_delay = 5  # seconds

    def retry_with_backoff(self, func, *args, **kwargs):
        """
        Retry a function with exponential backoff

        Args:
            func: Function to retry
            *args, **kwargs: Arguments to pass to function

        Returns:
            Result of function or None if all retries fail
        """
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    self.logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    self.logger.error(f"All {self.max_retries} attempts failed: {e}")
                    raise

    def check_for_updates(self):
        """Check LinkedIn for new notifications with retry logic"""
        browser = None
        try:
            with sync_playwright() as p:
                # Launch persistent browser context
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False,
                    args=['--disable-blink-features=AutomationControlled']
                )

                page = browser.pages[0] if browser.pages else browser.new_page()

                # Navigate with retry
                def navigate_to_linkedin():
                    self.logger.info("Navigating to LinkedIn...")
                    page.goto('https://www.linkedin.com/feed/', timeout=60000, wait_until='domcontentloaded')
                    time.sleep(2)
                    return page.url

                try:
                    current_url = self.retry_with_backoff(navigate_to_linkedin)
                except Exception as e:
                    self.logger.error(f"Failed to navigate to LinkedIn after retries: {e}")
                    if browser:
                        browser.close()
                    return

                # Check if login required
                if 'login' in current_url.lower() or 'authwall' in current_url.lower():
                    self.logger.info("=" * 60)
                    self.logger.info("LOGIN REQUIRED - Please log in to LinkedIn")
                    self.logger.info("=" * 60)
                    self.logger.info("Waiting for login (5 minutes)...")

                    try:
                        page.wait_for_url(
                            lambda url: 'login' not in url.lower() and 'authwall' not in url.lower(),
                            timeout=300000
                        )
                        self.logger.info("Login successful!")
                        time.sleep(2)
                    except PlaywrightTimeout:
                        self.logger.error("Login timeout - skipping this check")
                        browser.close()
                        return
                else:
                    self.logger.info("Already logged in")

                # Navigate to notifications with retry
                def navigate_to_notifications():
                    self.logger.info("Navigating to notifications...")
                    page.goto('https://www.linkedin.com/notifications/', timeout=60000, wait_until='domcontentloaded')
                    time.sleep(3)

                try:
                    self.retry_with_backoff(navigate_to_notifications)
                except Exception as e:
                    self.logger.error(f"Failed to navigate to notifications: {e}")
                    browser.close()
                    return

                # Find notifications
                self.logger.info("Checking for notifications...")
                notifications = page.query_selector_all('[data-test-notification-card]')

                if not notifications:
                    notifications = page.query_selector_all('.notification-card')

                if not notifications:
                    self.logger.info("No notifications found")
                    browser.close()
                    return

                self.logger.info(f"Found {len(notifications)} notification(s)")

                # Process notifications
                for i, notification in enumerate(notifications[:10]):
                    try:
                        text = notification.inner_text()
                        notif_id = f"linkedin_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                        if not self.is_processed(notif_id):
                            lines = text.split('\n')
                            person = lines[0] if lines else 'Someone'
                            notif_type = self.classify_notification(text)

                            self.logger.info(f"New notification: {notif_type} from {person}")
                            self.create_linkedin_action_file(person, text, notif_type)
                            self.mark_as_processed(notif_id)

                    except Exception as e:
                        self.logger.error(f"Error processing notification {i}: {e}")
                        continue

                browser.close()

        except Exception as e:
            self.logger.error(f"Error checking LinkedIn: {e}", exc_info=True)
            if browser:
                try:
                    browser.close()
                except:
                    pass

    def classify_notification(self, text):
        """Classify notification type based on text"""
        text_lower = text.lower()

        if 'message' in text_lower or 'sent you' in text_lower:
            return 'message'
        elif 'comment' in text_lower:
            return 'comment'
        elif 'mention' in text_lower:
            return 'mention'
        elif 'invitation' in text_lower or 'connect' in text_lower:
            return 'connection_request'
        elif 'liked' in text_lower or 'reacted' in text_lower:
            return 'engagement'
        elif 'viewed' in text_lower:
            return 'profile_view'
        else:
            return 'notification'

    def create_linkedin_action_file(self, person, text, notif_type):
        """Create action file for LinkedIn notification"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        person_clean = person.replace(' ', '_')[:20]

        filename = f"LINKEDIN_{notif_type.upper()}_{person_clean}_{timestamp}.md"

        priority_map = {
            'message': 'high',
            'comment': 'high',
            'mention': 'high',
            'connection_request': 'medium',
            'engagement': 'low',
            'profile_view': 'low',
            'notification': 'medium'
        }

        priority = priority_map.get(notif_type, 'medium')

        frontmatter = {
            'type': 'linkedin',
            'notification_type': notif_type,
            'person': person,
            'created': datetime.now().isoformat(),
            'status': 'pending',
            'priority': priority
        }

        content = f"""
## LinkedIn Notification: {notif_type.replace('_', ' ').title()}

**From:** {person}

**Detected:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Notification Details

{text}

### Required Action

- [ ] Go to LinkedIn and view the full notification
- [ ] Take appropriate action
- [ ] Mark as done when complete

### Notes

[Add notes here]

### LinkedIn Link

Visit https://www.linkedin.com/notifications/ to view and respond.
"""

        self.create_action_file(filename, frontmatter, content)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='LinkedIn Watcher')
    parser.add_argument('--vault-path', required=True, help='Path to Obsidian vault')
    parser.add_argument('--check-interval', type=int, default=180, help='Check interval in seconds')
    parser.add_argument('--session-path', help='Path to save browser session')

    args = parser.parse_args()

    watcher = LinkedInWatcher(
        vault_path=args.vault_path,
        check_interval=args.check_interval,
        session_path=args.session_path
    )

    watcher.run()
