"""Logging utilities for zfetch."""

import logging
import os
from pathlib import Path
from typing import Optional

_logger: Optional[logging.Logger] = None


def get_default_log_path() -> Path:
    """Return the default path for the debug log file."""
    config_dir = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "zfetch"
    return config_dir / "debug.log"


def setup_logger(debug_mode: bool = False, log_file: Optional[Path] = None) -> logging.Logger:
    """Initialize and return the zfetch logger."""
    global _logger
    logger = logging.getLogger("zfetch")

    if not debug_mode:
        logger.setLevel(logging.CRITICAL)
        logger.handlers = [logging.NullHandler()]
        _logger = logger
        return logger

    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    target_path = log_file or get_default_log_path()
    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(target_path, encoding="utf-8")
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s (%(module)s:%(lineno)d): %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception:
        # If writing to log file fails, fallback to null handler to prevent crash
        logger.addHandler(logging.NullHandler())

    _logger = logger
    return logger


def get_logger() -> logging.Logger:
    """Get the active logger, initializing with defaults if needed."""
    global _logger
    if _logger is None:
        _logger = setup_logger(debug_mode=False)
    return _logger
