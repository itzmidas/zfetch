"""System helper utilities for zfetch."""

import os
import subprocess
from pathlib import Path
from typing import Optional

from zfetch.utils.logger import get_logger

logger = get_logger()


def read_file_safe(path: Path | str) -> Optional[str]:
    """Safely read a file, returning its content as a string or None if unreadable."""
    try:
        p = Path(path)
        if p.is_file():
            return p.read_text(encoding="utf-8", errors="replace").strip()
    except Exception as e:
        logger.debug("Failed reading file %s: %s", path, e)
    return None


def run_command_safe(cmd: list[str], timeout: float = 1.0) -> Optional[str]:
    """Safely run an external command with timeout and return stripped stdout."""
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=timeout,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        logger.debug("Command failed %s: %s", cmd, e)
    return None


def format_bytes(num_bytes: int | float) -> str:
    """Format bytes into human-readable GiB or MiB."""
    gib = num_bytes / (1024**3)
    if gib >= 1.0:
        return f"{gib:.1f} GiB"
    mib = num_bytes / (1024**2)
    return f"{mib:.0f} MiB"


def format_seconds(total_seconds: float) -> str:
    """Format duration in seconds into human-readable uptime (e.g. 2d 4h 12m)."""
    seconds = int(total_seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, _ = divmod(seconds, 60)

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0 or days > 0:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")

    return " ".join(parts)
