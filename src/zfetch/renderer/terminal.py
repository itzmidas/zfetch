"""Terminal rendering logic for zfetch."""

import sys
from typing import Optional

from zfetch.ascii.builtin import AsciiArt, get_builtin_ascii
import zfetch.modules  # Ensures all modules are registered
from zfetch.modules.base import ModuleRegistry, ModuleResult


# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
BLUE = "\033[34m"
WHITE = "\033[37m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
RED = "\033[31m"


def render_color_dots() -> str:
    """Render terminal color dots/blocks."""
    colors_normal = [f"\033[4{i}m   \033[0m" for i in range(8)]
    colors_bright = [f"\033[10{i}m   \033[0m" for i in range(8)]
    return "".join(colors_normal) + "\n" + "".join(colors_bright)


def render_fetch(
    art: Optional[AsciiArt] = None,
    modules: Optional[list[ModuleResult]] = None,
    separator: str = "❯",
    label_color: str = CYAN,
    value_color: str = WHITE,
    art_color: str = CYAN,
    show_color_dots: bool = True,
    spacing: int = 4,
) -> str:
    """Render the full fetch output combining ASCII art and information modules."""
    if art is None:
        art = get_builtin_ascii("arch")

    ascii_lines = [f"{art_color}{line}{RESET}" for line in (art.lines if art else [])]
    ascii_width = art.width if art else 0

    if modules is None:
        # Collect from registry
        modules = []
        for mod in ModuleRegistry.get_all():
            if mod.default_enabled:
                res = mod.fetch()
                if res:
                    modules.append(res)

    # Format info lines
    info_lines: list[str] = []
    max_label_len = max((len(m.label) for m in modules), default=8)

    for m in modules:
        icon_part = f"{m.icon} " if m.icon else ""
        label_part = f"{BOLD}{label_color}{icon_part}{m.label.ljust(max_label_len)}{RESET}"
        sep_part = f"{DIM}{separator}{RESET}"
        val_part = f"{value_color}{m.value}{RESET}"
        info_lines.append(f"{label_part} {sep_part} {val_part}")

    if show_color_dots:
        info_lines.append("")  # empty gap
        # Render a compact color dot row
        dots = "".join([f"\033[38;5;{c}m● {RESET}" for c in [1, 2, 3, 4, 5, 6, 7, 8]])
        info_lines.append(dots)

    # Combine ASCII lines and Info lines side by side
    total_lines = max(len(ascii_lines), len(info_lines))
    output_lines: list[str] = []

    space_gap = " " * spacing

    for i in range(total_lines):
        left = ascii_lines[i] if i < len(ascii_lines) else " " * ascii_width
        # Ensure left padding matches ascii_width even if line is shorter
        raw_left_len = len(art.lines[i]) if (art and i < len(art.lines)) else 0
        fill_spaces = " " * max(0, ascii_width - raw_left_len)

        right = info_lines[i] if i < len(info_lines) else ""

        if right:
            output_lines.append(f"{left}{fill_spaces}{space_gap}{right}")
        else:
            output_lines.append(f"{left}{fill_spaces}")

    return "\n" + "\n".join(output_lines) + "\n"
