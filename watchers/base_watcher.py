"""
Base Watcher Abstract Class

All watchers inherit from this class and implement the abstract methods.
"""

import os
import time
import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path


class BaseWatcher(ABC):
    """Abstract base class for all watchers"""

    def __init__(self, vault_path, check_interval=60):
        """
        Initialize the watcher

        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks
        """
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        self.needs_action_dir = self.vault_path / "Needs_Action"
        self.logs_dir = self.vault_path / "Logs"

        # Create directories if they don't exist
        self.needs_action_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = self.setup_logger()

        # Track processed items to avoid duplicates
        self.processed_items = self.load_processed_items()

    def setup_logger(self):
        """Setup logging for this watcher"""
        logger_name = self.__class__.__name__
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        # File handler
        log_file = self.logs_dir / f"{logger_name.lower()}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def load_processed_items(self):
        """Load set of already processed item IDs"""
        processed_file = self.logs_dir / f"{self.__class__.__name__.lower()}_processed.json"
        if processed_file.exists():
            with open(processed_file, 'r') as f:
                return set(json.load(f))
        return set()

    def save_processed_items(self):
        """Save set of processed item IDs"""
        processed_file = self.logs_dir / f"{self.__class__.__name__.lower()}_processed.json"
        with open(processed_file, 'w') as f:
            json.dump(list(self.processed_items), f)

    def mark_as_processed(self, item_id):
        """Mark an item as processed to avoid duplicates"""
        self.processed_items.add(item_id)
        self.save_processed_items()

    def is_processed(self, item_id):
        """Check if an item has already been processed"""
        return item_id in self.processed_items

    def create_action_file(self, filename, frontmatter, content):
        """
        Create an action file in /Needs_Action

        Args:
            filename: Name of the file (e.g., EMAIL_john_20260309.md)
            frontmatter: Dictionary of frontmatter metadata
            content: Main content of the file
        """
        filepath = self.needs_action_dir / filename

        # Build frontmatter
        fm_lines = ["---"]
        for key, value in frontmatter.items():
            if isinstance(value, str):
                fm_lines.append(f"{key}: {value}")
            else:
                fm_lines.append(f"{key}: {json.dumps(value)}")
        fm_lines.append("---")
        fm_lines.append("")

        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(fm_lines))
            f.write(content)

        self.logger.info(f"Created action file: {filename}")
        return filepath

    @abstractmethod
    def check_for_updates(self):
        """
        Check for new items to process
        Must be implemented by subclasses
        """
        pass

    def run(self):
        """Main loop - runs continuously"""
        self.logger.info(f"{self.__class__.__name__} started")
        self.logger.info(f"Vault path: {self.vault_path}")
        self.logger.info(f"Check interval: {self.check_interval} seconds")

        while True:
            try:
                self.logger.info("Checking for updates...")
                self.check_for_updates()
                time.sleep(self.check_interval)
            except KeyboardInterrupt:
                self.logger.info("Watcher stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}", exc_info=True)
                # Wait before retrying to avoid rapid error loops
                time.sleep(self.check_interval)
