"""Themes and presets package for yfetch."""

from yfetch.themes.definitions import (
    COLOR_MAP,
    THEMES,
    Theme,
    color_to_ansi,
    get_theme,
    list_themes,
)
from yfetch.themes.quick_styles import (
    QUICK_STYLES,
    QuickStyle,
    apply_quick_style_by_name,
)

__all__ = [
    "Theme",
    "THEMES",
    "get_theme",
    "list_themes",
    "color_to_ansi",
    "COLOR_MAP",
    "QuickStyle",
    "QUICK_STYLES",
    "apply_quick_style_by_name",
]
