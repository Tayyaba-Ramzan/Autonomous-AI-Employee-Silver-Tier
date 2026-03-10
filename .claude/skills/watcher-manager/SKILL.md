---
name: watcher-manager
description: |
  Manage and monitor Watcher scripts that detect external events. Start/stop watchers,
  check their health, view logs, and troubleshoot issues. Use when setting up the
  monitoring system or diagnosing watcher problems.
---

# Watcher Manager

Manage and monitor the Watcher scripts that detect external events.

## When to Use

- Start or stop Watcher scripts
- Check Watcher health and status
- View Watcher logs
- Troubleshoot Watcher issues
- Configure Watcher settings
- Monitor Watcher performance

## Available Watchers

### Gmail Watcher
- **Script:** `watchers/gmail_watcher.py`
- **Purpose:** Monitor Gmail for important/unread messages
- **Check Interval:** 120 seconds
- **Output:** Creates `EMAIL_*.md` files in `/Needs_Action`

### WhatsApp Watcher
- **Script:** `watchers/whatsapp_watcher.py`
- **Purpose:** Monitor WhatsApp Web for urgent keywords
- **Check Interval:** 30 seconds
- **Output:** Creates `WHATSAPP_*.md` files in `/Needs_Action`

### Filesystem Watcher
- **Script:** `watchers/filesystem_watcher.py`
- **Purpose:** Monitor drop folder for new files
- **Check Interval:** 10 seconds
- **Output:** Creates `FILE_*.md` files in `/Needs_Action`

## Workflow

### 1. Start Watchers

```bash
# Start Gmail Watcher
python3 watchers/gmail_watcher.py --vault-path AI_Employee_Vault &

# Start WhatsApp Watcher
python3 watchers/whatsapp_watcher.py --vault-path AI_Employee_Vault &

# Start Filesystem Watcher
python3 watchers/filesystem_watcher.py --vault-path AI_Employee_Vault --watch-dir ~/Dropbox/AI_Drop &
```

### 2. Check Watcher Status

```bash
# Check if watchers are running
ps aux | grep watcher

# Check watcher logs
tail -f AI_Employee_Vault/Logs/gmail_watcher.log
tail -f AI_Employee_Vault/Logs/whatsapp_watcher.log
tail -f AI_Employee_Vault/Logs/filesystem_watcher.log
```

### 3. Stop Watchers

```bash
# Stop all watchers
pkill -f gmail_watcher.py
pkill -f whatsapp_watcher.py
pkill -f filesystem_watcher.py

# Or stop specific watcher by PID
kill [PID]
```

### 4. Restart Watchers

```bash
# Stop and restart
pkill -f gmail_watcher.py
sleep 2
python3 watchers/gmail_watcher.py --vault-path AI_Employee_Vault &
```

## Watcher Configuration

### Gmail Watcher Config

```python
# watchers/config/gmail_config.json
{
  "check_interval": 120,
  "credentials_path": "credentials/gmail_credentials.json",
  "token_path": "credentials/gmail_token.json",
  "filters": {
    "is_unread": true,
    "is_important": true,
    "exclude_labels": ["spam", "promotions"]
  },
  "urgent_keywords": ["urgent", "asap", "important", "critical"]
}
```

### WhatsApp Watcher Config

```python
# watchers/config/whatsapp_config.json
{
  "check_interval": 30,
  "session_path": "credentials/whatsapp_session",
  "urgent_keywords": ["urgent", "asap", "invoice", "payment", "help"],
  "monitored_contacts": ["Client A", "Client B", "Boss"],
  "browser_headless": true
}
```

### Filesystem Watcher Config

```python
# watchers/config/filesystem_config.json
{
  "check_interval": 10,
  "watch_directories": [
    "~/Dropbox/AI_Drop",
    "~/Downloads/AI_Process"
  ],
  "file_patterns": ["*.pdf", "*.docx", "*.xlsx", "*.txt"],
  "ignore_patterns": [".*", "~*"]
}
```

## Watcher Health Monitoring

### Health Check Script

```bash
# Check watcher health
python3 watchers/health_check.py

# Expected output:
# ✅ Gmail Watcher: Running (last check: 30s ago)
# ✅ WhatsApp Watcher: Running (last check: 15s ago)
# ✅ Filesystem Watcher: Running (last check: 5s ago)
```

### Health Indicators

**Healthy:**
- Process running
- Recent log activity
- Creating action files
- No error messages

**Unhealthy:**
- Process not found
- No log activity >5 minutes
- Error messages in logs
- Not creating action files

## Troubleshooting

### Gmail Watcher Issues

**Problem:** Not detecting emails
```bash
# Check credentials
ls -la credentials/gmail_credentials.json
ls -la credentials/gmail_token.json

# Check Gmail API quota
# View logs for API errors
tail -50 AI_Employee_Vault/Logs/gmail_watcher.log
```

**Problem:** Authentication errors
```bash
# Re-authenticate
python3 watchers/gmail_watcher.py --reauth
```

### WhatsApp Watcher Issues

**Problem:** Browser not connecting
```bash
# Check if WhatsApp Web is accessible
# Verify session file exists
ls -la credentials/whatsapp_session/

# Run in non-headless mode to debug
python3 watchers/whatsapp_watcher.py --vault-path AI_Employee_Vault --headless false
```

**Problem:** QR code scan needed
```bash
# Run with QR display
python3 watchers/whatsapp_watcher.py --vault-path AI_Employee_Vault --show-qr
```

### Filesystem Watcher Issues

**Problem:** Not detecting files
```bash
# Check watch directory exists
ls -la ~/Dropbox/AI_Drop

# Check permissions
# Verify file patterns match
```

## Watcher Logs

### Log Format

```
2026-03-09 10:30:15 [INFO] Gmail Watcher started
2026-03-09 10:30:20 [INFO] Checking for new emails...
2026-03-09 10:30:22 [INFO] Found 2 unread emails
2026-03-09 10:30:23 [INFO] Created action file: EMAIL_john_20260309.md
2026-03-09 10:30:24 [INFO] Created action file: EMAIL_jane_20260309.md
2026-03-09 10:32:15 [INFO] Checking for new emails...
2026-03-09 10:32:16 [INFO] No new emails
```

### Log Rotation

```bash
# Rotate logs daily
# Keep last 30 days
# Archive to /Logs/archive/
```

## Watcher Metrics

Track these metrics in `/Logs/watcher_metrics.md`:

- Total items detected
- Action files created
- Average detection time
- Error count
- Uptime percentage
- Last successful check

## Scheduling Watchers

### Using Cron (Mac/Linux)

```bash
# Edit crontab
crontab -e

# Add watcher startup on reboot
@reboot cd /path/to/project && python3 watchers/gmail_watcher.py --vault-path AI_Employee_Vault &
@reboot cd /path/to/project && python3 watchers/whatsapp_watcher.py --vault-path AI_Employee_Vault &
@reboot cd /path/to/project && python3 watchers/filesystem_watcher.py --vault-path AI_Employee_Vault --watch-dir ~/Dropbox/AI_Drop &
```

### Using Task Scheduler (Windows)

```powershell
# Create scheduled task to start watchers on login
schtasks /create /tn "Gmail Watcher" /tr "python watchers\gmail_watcher.py --vault-path AI_Employee_Vault" /sc onlogon
```

## Watcher Base Class

All watchers inherit from `BaseWatcher`:

```python
from abc import ABC, abstractmethod

class BaseWatcher(ABC):
    def __init__(self, vault_path, check_interval):
        self.vault_path = vault_path
        self.check_interval = check_interval
        self.logger = self.setup_logger()

    @abstractmethod
    def check_for_updates(self):
        """Check for new items to process"""
        pass

    @abstractmethod
    def create_action_file(self, item):
        """Create action file in /Needs_Action"""
        pass

    def run(self):
        """Main loop"""
        while True:
            try:
                self.check_for_updates()
                time.sleep(self.check_interval)
            except Exception as e:
                self.logger.error(f"Error: {e}")
```

## Key Principles

1. **Continuous monitoring** - Watchers run 24/7
2. **Fault tolerance** - Handle errors gracefully
3. **Avoid duplicates** - Track processed items
4. **Efficient polling** - Use appropriate check intervals
5. **Comprehensive logging** - Log all activity
6. **Health monitoring** - Track watcher status

## File Naming Conventions

- Watcher scripts: `watchers/[name]_watcher.py`
- Config files: `watchers/config/[name]_config.json`
- Log files: `Logs/[name]_watcher.log`

## Tips

- Start watchers in background with `&`
- Use `nohup` for persistent processes
- Monitor logs regularly for errors
- Set up health check alerts
- Test watchers before deploying
- Use appropriate check intervals (don't spam APIs)
- Implement exponential backoff for errors
- Keep credentials secure and separate
