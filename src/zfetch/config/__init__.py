"""Configuration package for zfetch."""

from zfetch.config.manager import (
    ConfigManager,
    ensure_config_dirs,
    get_custom_ascii_dir,
    get_default_config_dir,
    get_default_config_path,
)
from zfetch.config.schema import (
    AppearanceConfig,
    AsciiConfig,
    ColorsConfig,
    Config,
    GeneralConfig,
    LayoutConfig,
    ModulesConfig,
)

__all__ = [
    "ConfigManager",
    "Config",
    "AsciiConfig",
    "ModulesConfig",
    "AppearanceConfig",
    "ColorsConfig",
    "LayoutConfig",
    "GeneralConfig",
    "ensure_config_dirs",
    "get_default_config_dir",
    "get_default_config_path",
    "get_custom_ascii_dir",
]
