"""
Watchers package for AI Employee

Contains all watcher scripts that monitor external sources.
"""

from .base_watcher import BaseWatcher
from .gmail_watcher import GmailWatcher
from .whatsapp_watcher import WhatsAppWatcher
from .filesystem_watcher import FilesystemWatcher

__all__ = [
    'BaseWatcher',
    'GmailWatcher',
    'WhatsAppWatcher',
    'FilesystemWatcher'
]
