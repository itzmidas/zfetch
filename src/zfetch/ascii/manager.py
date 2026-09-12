"""ASCII art manager for builtin and custom user-provided artworks."""

import os
from pathlib import Path
from typing import Optional

from zfetch.ascii.builtin import BUILTIN_ARTS, AsciiArt, get_builtin_ascii
from zfetch.config.manager import get_custom_ascii_dir
from zfetch.utils.logger import get_logger
from zfetch.utils.system import read_file_safe

logger = get_logger()


class AsciiManager:
    """Discovers and retrieves both builtin and custom ASCII arts."""

    def __init__(self, custom_dir: Optional[Path | str] = None) -> None:
        self.custom_dir = Path(custom_dir) if custom_dir else get_custom_ascii_dir()

    def get_custom_arts(self) -> dict[str, AsciiArt]:
        """Scan custom ASCII directory for .txt files."""
        custom_arts: dict[str, AsciiArt] = {}
        if not self.custom_dir.is_dir():
            return custom_arts

        try:
            for entry in sorted(os.scandir(self.custom_dir), key=lambda e: e.name):
                if entry.is_file() and entry.name.endswith(".txt"):
                    try:
                        content = Path(entry.path).read_text(encoding="utf-8", errors="replace")
                        lines = [line.rstrip("\r\n") for line in content.splitlines()]
                        # Remove trailing blank lines
                        while lines and not lines[-1].strip():
                            lines.pop()
                        if lines:
                            key = Path(entry.name).stem.lower()
                            name = f"Custom: {Path(entry.name).stem}"
                            custom_arts[key] = AsciiArt(
                                key=key,
                                name=name,
                                lines=lines,
                                default_colors=["cyan"],
                                description=f"User custom ASCII file: {entry.name}",
                            )
                    except Exception as e:
                        logger.debug("Failed reading %s: %s", entry.path, e)
        except Exception as e:
            logger.debug("Failed reading custom ASCII directory: %s", e)

        return custom_arts

    def get_art(self, key: str) -> Optional[AsciiArt]:
        """Get an ASCII art by key, searching custom first, then builtin."""
        key_lower = key.lower().strip()
        custom = self.get_custom_arts()
        if key_lower in custom:
            return custom[key_lower]
        return get_builtin_ascii(key_lower)

    def list_all(self) -> list[AsciiArt]:
        """List all available ASCII arts (custom + builtin)."""
        arts: list[AsciiArt] = []
        # Add custom arts first
        custom = self.get_custom_arts()
        arts.extend(custom.values())
        # Add builtin arts
        arts.extend(BUILTIN_ARTS.values())
        return arts
