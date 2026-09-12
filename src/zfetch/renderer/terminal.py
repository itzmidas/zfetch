"""Terminal rendering logic for zfetch with theme, gradient, and layout support."""

from typing import Optional

from zfetch.ascii.builtin import AsciiArt, get_builtin_ascii
from zfetch.ascii.gradient import apply_gradient_to_lines
from zfetch.ascii.manager import AsciiManager
from zfetch.config.schema import Config
import zfetch.modules  # Ensures all modules are registered
from zfetch.modules.base import ModuleRegistry, ModuleResult
from zfetch.themes.definitions import color_to_ansi, get_theme

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"


def render_color_dots() -> str:
    """Render terminal color dots."""
    return "".join([f"\033[38;5;{c}m● {RESET}" for c in [1, 2, 3, 4, 5, 6, 7, 8]])


def render_fetch(
    config: Optional[Config] = None,
    art: Optional[AsciiArt] = None,
    modules: Optional[list[ModuleResult]] = None,
) -> str:
    """Render the full fetch output combining ASCII art and information modules."""
    if config is None:
        config = Config()

    # 1. Resolve Theme
    theme = get_theme(config.colors.theme)

    # Resolve label, value, separator colors
    label_ansi = color_to_ansi(config.colors.label_color if config.colors.label_color != "cyan" else theme.label_color)
    val_ansi = color_to_ansi(config.colors.value_color if config.colors.value_color != "white" else theme.value_color)
    sep_ansi = color_to_ansi(config.colors.separator_color if config.colors.separator_color != "dim" else theme.separator_color)

    # 2. Resolve ASCII Art
    ascii_position = config.layout.ascii_position.lower()
    if ascii_position == "off":
        art = None
    elif art is None:
        art_mgr = AsciiManager()
        art = art_mgr.get_art(config.ascii.art) or get_builtin_ascii("arch")

    # Format ASCII lines according to color mode
    ascii_lines: list[str] = []
    ascii_width = art.width if art else 0

    if art and ascii_position != "off":
        mode = config.ascii.color_mode.lower()
        if mode == "gradient":
            grad_colors = config.ascii.gradient_colors or theme.gradient_colors or ["#1793d1", "#00d7ff"]
            ascii_lines = apply_gradient_to_lines(art.lines, grad_colors)
        elif mode == "single":
            single_ansi = color_to_ansi(config.ascii.custom_color)
            ascii_lines = [f"{single_ansi}{line}{RESET}" for line in art.lines]
        elif mode == "raw":
            ascii_lines = list(art.lines)
        else:  # "theme"
            primary_ansi = color_to_ansi(theme.primary)
            ascii_lines = [f"{primary_ansi}{line}{RESET}" for line in art.lines]

    # 3. Resolve Modules
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

    # 4. Format Info lines
    separator = config.appearance.separator
    bold_prefix = BOLD if config.appearance.bold_labels else ""

    info_lines: list[str] = []
    max_label_len = max((len(m.label) for m in modules), default=8)

    for m in modules:
        icon_part = f"{m.icon} " if m.icon else ""
        label_part = f"{bold_prefix}{label_ansi}{icon_part}{m.label.ljust(max_label_len)}{RESET}"
        sep_part = f"{sep_ansi}{separator}{RESET}"
        val_part = f"{val_ansi}{m.value}{RESET}"
        info_lines.append(f"{label_part} {sep_part} {val_part}")

    if config.appearance.show_color_dots:
        info_lines.append("")  # gap
        info_lines.append(render_color_dots())

    # 5. Assemble Output according to Layout Position
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
        # Strip ANSI to measure visual width of info lines
        import re
        ansi_regex = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        plain_lens = [len(ansi_regex.sub("", l)) for l in info_lines]
        max_plain_len = max(plain_lens, default=0)

        total_lines = max(len(ascii_lines), len(info_lines))
        for i in range(total_lines):
            left = info_lines[i] if i < len(info_lines) else ""
            left_plain_len = plain_lens[i] if i < len(plain_lens) else 0
            pad = " " * max(0, max_plain_len - left_plain_len)
            right = ascii_lines[i] if i < len(ascii_lines) else ""
            output_lines.append(f"{padding_left}{left}{pad}{space_gap}{right}".rstrip())

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
