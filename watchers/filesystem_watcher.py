"""
File System Watcher - Monitors a drop folder for new files.

This watcher monitors a designated drop folder and creates action files
in the Obsidian vault when new files are detected.
"""

import os
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class DropFolderHandler(FileSystemEventHandler):
    """Handler for file system events in the drop folder."""

    def __init__(self, vault_path: str):
        """
        Initialize the drop folder handler.

        Args:
            vault_path: Path to the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.logger = logging.getLogger(self.__class__.__name__)

        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)

    def on_created(self, event):
        """
        Handle file creation events.

        Args:
            event: The file system event
        """
        if event.is_directory:
            return

        source = Path(event.src_path)

        # Ignore hidden files and temporary files
        if source.name.startswith('.') or source.name.startswith('~'):
            return

        self.logger.info(f'New file detected: {source.name}')

        try:
            # Create metadata file
            self.create_metadata(source)
            self.logger.info(f'Created action file for: {source.name}')
        except Exception as e:
            self.logger.error(f'Error processing file {source.name}: {e}')

    def create_metadata(self, source: Path):
        """
        Create a metadata file in Needs_Action folder.

        Args:
            source: Path to the source file
        """
        timestamp = datetime.now().isoformat()
        file_size = source.stat().st_size

        # Create sanitized filename
        safe_name = self.sanitize_filename(source.stem)
        meta_filename = f'FILE_{safe_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        meta_path = self.needs_action / meta_filename

        content = f"""---
type: file_drop
original_name: {source.name}
original_path: {source.absolute()}
size_bytes: {file_size}
size_human: {self.format_size(file_size)}
detected: {timestamp}
priority: medium
status: pending
---

## New File Detected

A new file has been dropped and requires processing.

### File Details
- **Name:** {source.name}
- **Size:** {self.format_size(file_size)}
- **Location:** `{source.absolute()}`
- **Type:** {source.suffix or 'No extension'}

### Suggested Actions
- [ ] Review file contents
- [ ] Determine appropriate action
- [ ] Process or categorize the file
- [ ] Move to appropriate location
- [ ] Update Dashboard with status

### Notes

Add any relevant notes or observations here.

---
*Created by File System Watcher*
"""

        meta_path.write_text(content, encoding='utf-8')

    def sanitize_filename(self, name: str) -> str:
        """Sanitize a string for use in filenames."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        return name[:50]

    def format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"


def main():
    """Main entry point for the file system watcher."""
    # Get configuration from environment
    vault_path = os.getenv('VAULT_PATH', 'AI_Employee_Vault')
    drop_folder = os.getenv('DROP_FOLDER_PATH', 'AI_Employee_Vault/Drop_Folder')

    logger = logging.getLogger('FileSystemWatcher')
    logger.info('Starting File System Watcher')
    logger.info(f'Vault path: {vault_path}')
    logger.info(f'Drop folder: {drop_folder}')

    # Ensure drop folder exists
    drop_path = Path(drop_folder)
    drop_path.mkdir(parents=True, exist_ok=True)

    # Create event handler and observer
    event_handler = DropFolderHandler(vault_path)
    observer = Observer()
    observer.schedule(event_handler, str(drop_path), recursive=False)

    # Start monitoring
    observer.start()
    logger.info(f'Monitoring {drop_path} for new files...')
    logger.info('Press Ctrl+C to stop')

    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        logger.info('Stopping File System Watcher...')
        observer.stop()

    observer.join()
    logger.info('File System Watcher stopped')


if __name__ == '__main__':
    main()
