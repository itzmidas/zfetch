"""Theme definitions and color palettes for yfetch."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Theme:
    """Represents a visual color theme."""

    key: str
    name: str
    description: str
    primary: str  # Hex or ANSI name
    secondary: str
    label_color: str
    value_color: str
    separator_color: str
    gradient_colors: list[str] = field(default_factory=list)


# ANSI 16-color name mappings
COLOR_MAP = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "purple": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "dim": "\033[2m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}


def color_to_ansi(color_spec: str) -> str:
    """Convert a color name or hex code into an ANSI escape sequence."""
    c = color_spec.strip().lower()
    if c in COLOR_MAP:
        return COLOR_MAP[c]

    # Check if hex code
    if c.startswith("#") or (len(c) in (3, 6) and all(ch in "0123456789abcdef" for ch in c)):
        from yfetch.ascii.gradient import hex_to_rgb, rgb_to_ansi
        r, g, b = hex_to_rgb(c)
        return rgb_to_ansi(r, g, b)

    return "\033[36m"  # Cyan fallback


THEMES: dict[str, Theme] = {
    "default": Theme(
        key="default",
        name="Arch Cyan (Default)",
        description="Classic Arch Linux cyan and blue palette",
        primary="#1793d1",
        secondary="#00d7ff",
        label_color="#1793d1",
        value_color="#ffffff",
        separator_color="#555555",
        gradient_colors=["#1793d1", "#00d7ff", "#ffffff"],
    ),
    "nord": Theme(
        key="nord",
        name="Nord",
        description="Arctic, north-bluish palette based on Nord theme",
        primary="#88c0d0",
        secondary="#81a1c1",
        label_color="#88c0d0",
        value_color="#eceff4",
        separator_color="#4c566a",
        gradient_colors=["#5e81ac", "#81a1c1", "#88c0d0"],
    ),
    "dracula": Theme(
        key="dracula",
        name="Dracula",
        description="Dark vampire theme with vibrant purple and pink accents",
        primary="#bd93f9",
        secondary="#ff79c6",
        label_color="#bd93f9",
        value_color="#f8f8f2",
        separator_color="#6272a4",
        gradient_colors=["#6272a4", "#bd93f9", "#ff79c6"],
    ),
    "gruvbox": Theme(
        key="gruvbox",
        name="Gruvbox",
        description="Retro groove warm earthy colors with orange accents",
        primary="#d79921",
        secondary="#fe8019",
        label_color="#fabd2f",
        value_color="#ebdbb2",
        separator_color="#665c54",
        gradient_colors=["#cc241d", "#d79921", "#ebdbb2"],
    ),
    "tokyo_night": Theme(
        key="tokyo_night",
        name="Tokyo Night",
        description="A clean, dark Tokyo city lights theme with vibrant blues",
        primary="#7aa2f7",
        secondary="#bb9af7",
        label_color="#7aa2f7",
        value_color="#c0caf5",
        separator_color="#565f89",
        gradient_colors=["#7aa2f7", "#bb9af7", "#7dcfff"],
    ),
    "catppuccin": Theme(
        key="catppuccin",
        name="Catppuccin (Mocha)",
        description="Soothing warm pastel theme with lavender and rosewater",
        primary="#cba6f7",
        secondary="#89b4fa",
        label_color="#cba6f7",
        value_color="#cdd6f4",
        separator_color="#6c7086",
        gradient_colors=["#89b4fa", "#cba6f7", "#f5c2e7"],
    ),
    "cyberpunk": Theme(
        key="cyberpunk",
        name="Cyberpunk",
        description="High-contrast neon yellow, bright cyan, and laser pink",
        primary="#fcee0a",
        secondary="#00f0ff",
        label_color="#00f0ff",
        value_color="#fcee0a",
        separator_color="#ff003c",
        gradient_colors=["#ff003c", "#fcee0a", "#00f0ff"],
    ),
    "monochrome": Theme(
        key="monochrome",
        name="Monochrome",
        description="Minimalist black, gray, and bright white",
        primary="#e0e0e0",
        secondary="#a0a0a0",
        label_color="#ffffff",
        value_color="#cccccc",
        separator_color="#666666",
        gradient_colors=["#666666", "#aaaaaa", "#ffffff"],
    ),
}


def get_theme(key: str) -> Theme:
    """Get theme by key, falling back to default."""
    return THEMES.get(key.lower(), THEMES["default"])


def list_themes() -> list[Theme]:
    """List all available built-in themes."""
    return list(THEMES.values())
