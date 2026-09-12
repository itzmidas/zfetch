"""Quick style presets for instant setup and one-click styling."""

from dataclasses import dataclass
from typing import Callable, Optional

from yfetch.config.schema import Config


@dataclass
class QuickStyle:
    """Represents a pre-packaged visual preset."""

    key: str
    name: str
    description: str
    apply: Callable[[Config], None]


def apply_arch_style(cfg: Config) -> None:
    """Standard Arch Linux look."""
    cfg.ascii.art = "arch"
    cfg.ascii.color_mode = "gradient"
    cfg.ascii.gradient_colors = ["#1793d1", "#00d7ff"]
    cfg.colors.theme = "default"
    cfg.colors.label_color = "#1793d1"
    cfg.colors.value_color = "#ffffff"
    cfg.colors.separator_color = "dim"
    cfg.appearance.separator = "❯"
    cfg.appearance.spacing = 4
    cfg.appearance.bold_labels = True
    cfg.appearance.show_color_dots = True
    cfg.appearance.nerd_fonts = True
    cfg.layout.ascii_position = "left"


def apply_cyberpunk_style(cfg: Config) -> None:
    """Vibrant futuristic neon aesthetic."""
    cfg.ascii.art = "yfetch"
    cfg.ascii.color_mode = "gradient"
    cfg.ascii.gradient_colors = ["#ff003c", "#fcee0a", "#00f0ff"]
    cfg.colors.theme = "cyberpunk"
    cfg.colors.label_color = "#00f0ff"
    cfg.colors.value_color = "#fcee0a"
    cfg.colors.separator_color = "#ff003c"
    cfg.appearance.separator = "⚡"
    cfg.appearance.spacing = 4
    cfg.appearance.bold_labels = True
    cfg.appearance.show_color_dots = True
    cfg.appearance.nerd_fonts = True
    cfg.layout.ascii_position = "left"


def apply_nord_style(cfg: Config) -> None:
    """Frosty Arctic blue Nord aesthetic."""
    cfg.ascii.art = "arch_clean"
    cfg.ascii.color_mode = "gradient"
    cfg.ascii.gradient_colors = ["#5e81ac", "#81a1c1", "#88c0d0"]
    cfg.colors.theme = "nord"
    cfg.colors.label_color = "#88c0d0"
    cfg.colors.value_color = "#eceff4"
    cfg.colors.separator_color = "#4c566a"
    cfg.appearance.separator = "•"
    cfg.appearance.spacing = 4
    cfg.appearance.bold_labels = True
    cfg.appearance.show_color_dots = True
    cfg.appearance.nerd_fonts = True
    cfg.layout.ascii_position = "left"


def apply_dracula_style(cfg: Config) -> None:
    """Dark vampire Dracula aesthetic."""
    cfg.ascii.art = "arch"
    cfg.ascii.color_mode = "gradient"
    cfg.ascii.gradient_colors = ["#6272a4", "#bd93f9", "#ff79c6"]
    cfg.colors.theme = "dracula"
    cfg.colors.label_color = "#bd93f9"
    cfg.colors.value_color = "#f8f8f2"
    cfg.colors.separator_color = "#ff79c6"
    cfg.appearance.separator = "→"
    cfg.appearance.spacing = 4
    cfg.appearance.bold_labels = True
    cfg.appearance.show_color_dots = True
    cfg.appearance.nerd_fonts = True
    cfg.layout.ascii_position = "left"


def apply_minimal_style(cfg: Config) -> None:
    """Minimal text-only layout with clean typography and no ASCII art."""
    cfg.ascii.art = "arch_small"
    cfg.layout.ascii_position = "off"
    cfg.colors.theme = "monochrome"
    cfg.colors.label_color = "#ffffff"
    cfg.colors.value_color = "#cccccc"
    cfg.colors.separator_color = "dim"
    cfg.appearance.separator = ":"
    cfg.appearance.spacing = 2
    cfg.appearance.bold_labels = True
    cfg.appearance.show_color_dots = False
    cfg.appearance.nerd_fonts = False


def apply_classic_style(cfg: Config) -> None:
    """Classic compact fetch layout with small logo."""
    cfg.ascii.art = "arch_small"
    cfg.ascii.color_mode = "theme"
    cfg.colors.theme = "default"
    cfg.colors.label_color = "cyan"
    cfg.colors.value_color = "white"
    cfg.colors.separator_color = "dim"
    cfg.appearance.separator = ":"
    cfg.appearance.spacing = 3
    cfg.appearance.bold_labels = True
    cfg.appearance.show_color_dots = True
    cfg.appearance.nerd_fonts = True
    cfg.layout.ascii_position = "left"


QUICK_STYLES: dict[str, QuickStyle] = {
    "arch": QuickStyle("arch", "Arch Linux", "Standard Arch cyan gradient and icons", apply_arch_style),
    "cyberpunk": QuickStyle("cyberpunk", "Cyberpunk", "High-contrast neon yellow and bright cyan", apply_cyberpunk_style),
    "nord": QuickStyle("nord", "Nord Arctic", "Nord palette with calm frost blues", apply_nord_style),
    "dracula": QuickStyle("dracula", "Dracula Dark", "Vampire purple with pink accents", apply_dracula_style),
    "minimal": QuickStyle("minimal", "Ultra Minimal", "Text-only display without ASCII logo", apply_minimal_style),
    "classic": QuickStyle("classic", "Classic Neofetch", "Classic compact style with small logo", apply_classic_style),
}


def apply_quick_style_by_name(cfg: Config, name: str) -> bool:
    """Apply quick style to config by name."""
    qs = QUICK_STYLES.get(name.lower())
    if qs:
        qs.apply(cfg)
        return True
    return False
