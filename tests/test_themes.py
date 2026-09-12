"""Unit tests for themes, color conversions, and quick styles."""

from yfetch.config.schema import Config
from yfetch.themes.definitions import THEMES, color_to_ansi, get_theme, list_themes
from yfetch.themes.quick_styles import QUICK_STYLES, apply_quick_style_by_name


def test_theme_retrieval():
    nord = get_theme("nord")
    assert nord.name == "Nord"
    assert nord.primary == "#88c0d0"

    dracula = get_theme("dracula")
    assert dracula.name == "Dracula"

    # Default fallback
    unknown = get_theme("nonexistent")
    assert unknown.key == "default"


def test_color_to_ansi():
    assert color_to_ansi("red") == "\033[31m"
    assert color_to_ansi("cyan") == "\033[36m"
    assert color_to_ansi("dim") == "\033[2m"
    # Hex TrueColor conversion
    ansi_hex = color_to_ansi("#1793d1")
    assert "\033[38;2;23;147;209m" == ansi_hex


def test_quick_styles_presets():
    cfg = Config()
    assert apply_quick_style_by_name(cfg, "cyberpunk") is True
    assert cfg.colors.theme == "cyberpunk"
    assert cfg.ascii.art == "yfetch"
    assert cfg.appearance.separator == "⚡"

    # Test minimal style
    assert apply_quick_style_by_name(cfg, "minimal") is True
    assert cfg.layout.ascii_position == "off"
    assert cfg.appearance.show_color_dots is False

    # Test nonexistent style
    assert apply_quick_style_by_name(cfg, "invalid") is False
