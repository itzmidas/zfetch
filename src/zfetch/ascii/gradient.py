"""Color gradient generator for ASCII art and terminal rendering."""

import re
from typing import Optional


def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    """Convert hex string (e.g. '#1793d1' or '1793d1') to (R, G, B)."""
    clean_hex = hex_str.lstrip("#").strip()
    if len(clean_hex) == 3:
        clean_hex = "".join([c * 2 for c in clean_hex])
    if len(clean_hex) != 6:
        # Fallback to cyan
        return (0, 215, 255)

    try:
        r = int(clean_hex[0:2], 16)
        g = int(clean_hex[2:4], 16)
        b = int(clean_hex[4:6], 16)
        return (r, g, b)
    except ValueError:
        return (0, 215, 255)


def rgb_to_ansi(r: int, g: int, b: int) -> str:
    """Format RGB tuple as 24-bit TrueColor ANSI escape sequence."""
    return f"\033[38;2;{r};{g};{b}m"


def interpolate_rgb(c1: tuple[int, int, int], c2: tuple[int, int, int], factor: float) -> tuple[int, int, int]:
    """Linearly interpolate between two RGB colors by factor (0.0 to 1.0)."""
    factor = max(0.0, min(1.0, factor))
    r = int(c1[0] + (c2[0] - c1[0]) * factor)
    g = int(c1[1] + (c2[1] - c1[1]) * factor)
    b = int(c1[2] + (c2[2] - c1[2]) * factor)
    return (r, g, b)


def generate_gradient_palette(colors: list[str], steps: int) -> list[str]:
    """Generate a list of TrueColor ANSI strings forming a smooth multi-stop gradient."""
    if steps <= 0:
        return []
    if steps == 1:
        r, g, b = hex_to_rgb(colors[0] if colors else "#00d7ff")
        return [rgb_to_ansi(r, g, b)]

    if len(colors) < 2:
        colors = ["#1793d1", "#00d7ff"]

    rgb_stops = [hex_to_rgb(c) for c in colors]
    num_segments = len(rgb_stops) - 1
    steps_per_segment = (steps - 1) / num_segments

    palette: list[str] = []
    for i in range(steps):
        # Determine which segment i falls into
        seg_idx = min(int(i / steps_per_segment), num_segments - 1)
        seg_start = seg_idx * steps_per_segment
        factor = (i - seg_start) / steps_per_segment if steps_per_segment > 0 else 0.0
        r, g, b = interpolate_rgb(rgb_stops[seg_idx], rgb_stops[seg_idx + 1], factor)
        palette.append(rgb_to_ansi(r, g, b))

    return palette


def apply_gradient_to_lines(lines: list[str], gradient_colors: list[str]) -> list[str]:
    """Apply vertical gradient to ASCII art lines."""
    if not lines:
        return []
    palette = generate_gradient_palette(gradient_colors, len(lines))
    reset = "\033[0m"
    colored_lines: list[str] = []
    for i, line in enumerate(lines):
        color = palette[i] if i < len(palette) else ""
        colored_lines.append(f"{color}{line}{reset}")
    return colored_lines
