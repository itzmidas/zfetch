"""Terminal rendering logic for zfetch."""

from typing import Optional

from zfetch.ascii.builtin import AsciiArt, get_builtin_ascii
from zfetch.config.schema import Config
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
    return "".join([f"\033[38;5;{c}m● {RESET}" for c in [1, 2, 3, 4, 5, 6, 7, 8]])


def render_fetch(
    config: Optional[Config] = None,
    art: Optional[AsciiArt] = None,
    modules: Optional[list[ModuleResult]] = None,
) -> str:
    """Render the full fetch output combining ASCII art and information modules."""
    if config is None:
        config = Config()

    # 1. Resolve ASCII Art
    ascii_position = config.layout.ascii_position.lower()
    if ascii_position == "off":
        art = None
    elif art is None:
        art = get_builtin_ascii(config.ascii.art) or get_builtin_ascii("arch")

    art_color = CYAN  # In Phase 4 this will be enhanced with themes & gradients
    ascii_lines = [f"{art_color}{line}{RESET}" for line in (art.lines if art else [])]
    ascii_width = art.width if art else 0

    # 2. Resolve Modules
    if modules is None:
        modules = []
        for mod_id in config.modules.enabled:
            mod = ModuleRegistry.get(mod_id)
            if mod:
                res = mod.fetch()
                if res:
                    # Apply custom label override if configured
                    if mod_id in config.modules.custom_labels:
                        res.label = config.modules.custom_labels[mod_id]
                    # Apply nerd_fonts toggle
                    if not config.appearance.nerd_fonts:
                        res.icon = ""
                    modules.append(res)

    # 3. Format Info lines
    separator = config.appearance.separator
    bold_prefix = BOLD if config.appearance.bold_labels else ""
    label_color = CYAN
    value_color = WHITE

    info_lines: list[str] = []
    max_label_len = max((len(m.label) for m in modules), default=8)

    for m in modules:
        icon_part = f"{m.icon} " if m.icon else ""
        label_part = f"{bold_prefix}{label_color}{icon_part}{m.label.ljust(max_label_len)}{RESET}"
        sep_part = f"{DIM}{separator}{RESET}"
        val_part = f"{value_color}{m.value}{RESET}"
        info_lines.append(f"{label_part} {sep_part} {val_part}")

    if config.appearance.show_color_dots:
        info_lines.append("")  # gap
        info_lines.append(render_color_dots())

    # 4. Assemble Output according to Layout Position
    spacing = config.appearance.spacing
    padding_left = " " * config.appearance.padding_left
    space_gap = " " * spacing
    output_lines: list[str] = []

    if ascii_position == "top" and art:
        # ASCII on top, Info below
        for line in ascii_lines:
            output_lines.append(f"{padding_left}{line}")
        output_lines.append("")  # blank line
        for line in info_lines:
            output_lines.append(f"{padding_left}{line}")

    elif ascii_position == "right" and art:
        # Info on left, ASCII on right
        max_info_len = max((len(l) for l in info_lines), default=0)
        total_lines = max(len(ascii_lines), len(info_lines))
        for i in range(total_lines):
            left = info_lines[i] if i < len(info_lines) else ""
            right = ascii_lines[i] if i < len(ascii_lines) else ""
            output_lines.append(f"{padding_left}{left.ljust(max_info_len)}{space_gap}{right}".rstrip())

    elif not art or ascii_position == "off":
        # Info only
        for line in info_lines:
            output_lines.append(f"{padding_left}{line}")

    else:
        # Default: ASCII on left, Info on right
        total_lines = max(len(ascii_lines), len(info_lines))
        for i in range(total_lines):
            if i < len(ascii_lines):
                raw_left_len = len(art.lines[i]) if art else 0
                fill_spaces = " " * max(0, ascii_width - raw_left_len)
                left_col = f"{ascii_lines[i]}{fill_spaces}"
            else:
                left_col = " " * ascii_width

            right = info_lines[i] if i < len(info_lines) else ""
            if right:
                output_lines.append(f"{padding_left}{left_col}{space_gap}{right}")
            else:
                output_lines.append(f"{padding_left}{left_col}".rstrip())

    return "\n" + "\n".join(output_lines) + "\n"
