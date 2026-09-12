"""Built-in ASCII art library for zfetch.

Original clean ASCII art representations for Linux distributions and logos.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AsciiArt:
    """Represents an ASCII art entry."""

    key: str
    name: str
    lines: list[str]
    default_colors: list[str]
    description: str = ""

    @property
    def width(self) -> int:
        """Maximum character width across all lines."""
        return max((len(line) for line in self.lines), default=0)

    @property
    def height(self) -> int:
        """Number of lines in the ASCII art."""
        return len(self.lines)


ARCH_DEFAULT = [
    r"       /\       ",
    r"      /  \      ",
    r"     /\   \     ",
    r"    /      \    ",
    r"   /   ,,   \   ",
    r"  /   |  |  -\  ",
    r" /_-''    ''-_\ ",
]

ARCH_SMALL = [
    r"   /\   ",
    r"  /  \  ",
    r" / /\ \ ",
    r"/ /__\ " + "\\",
]

ARCH_CLEAN = [
    r"       /\       ",
    r"      /  \      ",
    r"     / /\ \     ",
    r"    / /  \ \    ",
    r"   / /    \ \   ",
    r"  / /______\ \  ",
    r" /____________\ ",
]

ARCH_LARGE = [
    r"         /\         ",
    r"        /  \        ",
    r"       /\   \       ",
    r"      /      \      ",
    r"     /   ,,   \     ",
    r"    /   |  |  -\    ",
    r"   /_-''    ''-_\   ",
    r"  /                \  ",
    r" /__________________\ ",
]

LINUX_LOGO = [
    r"    .---.    ",
    r"   /     \   ",
    r"  | ()_() |  ",
    r"  (   -   )  ",
    r"   \  =  /   ",
    r"   /`---'\   ",
    r"  /       \  ",
]

TUX_LOGO = [
    r"   .--.   ",
    r"  |o_o |  ",
    r"  |:_/ |  ",
    r" //   \ \ ",
    r"(|     | )",
    r"/'\_   _/`" + "\\",
    r"\___)=(___/ ",
]

ZFETCH_LOGO = [
    r" _____ _____ ",
    r"|__  /|  ___|",
    r"  / / | |_   ",
    r" / /_ |  _|  ",
    r"/____||_|    ",
]

BUILTIN_ARTS: dict[str, AsciiArt] = {
    "arch": AsciiArt(
        key="arch",
        name="Arch Linux (Standard)",
        lines=ARCH_DEFAULT,
        default_colors=["cyan", "blue"],
        description="Standard Arch Linux logo",
    ),
    "arch_clean": AsciiArt(
        key="arch_clean",
        name="Arch Linux (Clean)",
        lines=ARCH_CLEAN,
        default_colors=["cyan", "blue"],
        description="Clean geometric Arch Linux logo",
    ),
    "arch_small": AsciiArt(
        key="arch_small",
        name="Arch Linux (Small)",
        lines=ARCH_SMALL,
        default_colors=["cyan"],
        description="Compact 4-line Arch logo for small terminals",
    ),
    "arch_large": AsciiArt(
        key="arch_large",
        name="Arch Linux (Large)",
        lines=ARCH_LARGE,
        default_colors=["cyan", "blue"],
        description="Detailed tall Arch logo",
    ),
    "linux": AsciiArt(
        key="linux",
        name="Linux",
        lines=LINUX_LOGO,
        default_colors=["yellow", "white"],
        description="Generic Linux mascot outline",
    ),
    "tux": AsciiArt(
        key="tux",
        name="Tux Penguin",
        lines=TUX_LOGO,
        default_colors=["yellow", "white"],
        description="Classic Tux penguin silhouette",
    ),
    "zfetch": AsciiArt(
        key="zfetch",
        name="zfetch Logo",
        lines=ZFETCH_LOGO,
        default_colors=["magenta", "cyan"],
        description="Modern block zfetch typography",
    ),
}


def get_builtin_ascii(name: str) -> Optional[AsciiArt]:
    """Retrieve built-in ASCII art by name/key."""
    return BUILTIN_ARTS.get(name.lower())


def list_builtin_arts() -> list[AsciiArt]:
    """List all available built-in ASCII arts."""
    return list(BUILTIN_ARTS.values())
