"""Configuration manager for loading, saving, and migrating yfetch config."""

import os
from pathlib import Path
from typing import Optional
import tomllib

import tomli_w

from yfetch.config.schema import Config
from yfetch.utils.logger import get_logger

logger = get_logger()


def get_default_config_dir() -> Path:
    """Return ~/.config/yfetch or $XDG_CONFIG_HOME/yfetch."""
    base = os.environ.get("XDG_CONFIG_HOME")
    if base:
        return Path(base) / "yfetch"
    return Path.home() / ".config" / "yfetch"


def get_default_config_path() -> Path:
    """Return path to ~/.config/yfetch/config.toml."""
    return get_default_config_dir() / "config.toml"


def get_custom_ascii_dir() -> Path:
    """Return path to ~/.config/yfetch/ascii/."""
    return get_default_config_dir() / "ascii"


def ensure_config_dirs() -> None:
    """Ensure ~/.config/yfetch and ~/.config/yfetch/ascii exist."""
    try:
        get_default_config_dir().mkdir(parents=True, exist_ok=True)
        get_custom_ascii_dir().mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.debug("Failed creating config directories: %s", e)


class ConfigManager:
    """Manages reading and writing yfetch configuration."""

    def __init__(self, config_path: Optional[Path | str] = None) -> None:
        self.config_path = Path(config_path) if config_path else get_default_config_path()

    def load(self, auto_create: bool = True) -> Config:
        """Load configuration from disk. If missing or corrupted, return default Config."""
        ensure_config_dirs()

        if not self.config_path.is_file():
            logger.debug("Config file not found at %s. Using defaults.", self.config_path)
            default_cfg = Config()
            if auto_create:
                self.save(default_cfg)
            return default_cfg

        try:
            with open(self.config_path, "rb") as f:
                data = tomllib.load(f)
            logger.debug("Loaded config from %s", self.config_path)
            return Config.from_dict(data)
        except tomllib.TOMLDecodeError as e:
            logger.warning("Corrupted config file at %s: %s. Falling back to default settings.", self.config_path, e)
            return Config()
        except Exception as e:
            logger.warning("Error reading config at %s: %s. Falling back to default settings.", self.config_path, e)
            return Config()

    def save(self, config: Config) -> bool:
        """Save configuration to disk in TOML format."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            data = config.to_dict()
            toml_str = tomli_w.dumps(data)
            self.config_path.write_text(toml_str, encoding="utf-8")
            logger.debug("Successfully saved config to %s", self.config_path)
            return True
        except Exception as e:
            logger.warning("Failed to save config to %s: %s", self.config_path, e)
            return False

    def reset(self) -> Config:
        """Reset configuration to defaults and persist."""
        default_cfg = Config()
        self.save(default_cfg)
        return default_cfg
