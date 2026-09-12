"""Unit tests for ASCII art library, custom art discovery, and gradients."""

from pathlib import Path
from unittest.mock import patch

from zfetch.ascii.builtin import BUILTIN_ARTS, get_builtin_ascii, list_builtin_arts
from zfetch.ascii.gradient import (
    apply_gradient_to_lines,
    generate_gradient_palette,
    hex_to_rgb,
    interpolate_rgb,
)
from zfetch.ascii.manager import AsciiManager


def test_builtin_ascii():
    arch = get_builtin_ascii("arch")
    assert arch is not None
    assert arch.width > 0
    assert arch.height > 0

    tux = get_builtin_ascii("tux")
    assert tux is not None
    assert "tux" in tux.name.lower()

    zfetch = get_builtin_ascii("zfetch")
    assert zfetch is not None

    all_builtin = list_builtin_arts()
    assert len(all_builtin) >= 4


def test_custom_ascii_discovery(tmp_path):
    ascii_dir = tmp_path / "ascii"
    ascii_dir.mkdir()
    custom_file = ascii_dir / "mylogo.txt"
    custom_file.write_text(" /\\\n/__\\", encoding="utf-8")

    mgr = AsciiManager(custom_dir=ascii_dir)
    arts = mgr.get_custom_arts()
    assert "mylogo" in arts
    assert arts["mylogo"].lines == [" /\\", "/__\\"]

    # Test get_art priority
    resolved = mgr.get_art("mylogo")
    assert resolved is not None
    assert resolved.name == "Custom: mylogo"


def test_hex_to_rgb():
    assert hex_to_rgb("#ffffff") == (255, 255, 255)
    assert hex_to_rgb("000000") == (0, 0, 0)
    assert hex_to_rgb("#ff0000") == (255, 0, 0)
    assert hex_to_rgb("#f00") == (255, 0, 0)
    # Invalid fallback
    assert hex_to_rgb("invalid") == (0, 215, 255)


def test_rgb_interpolation():
    c1 = (0, 0, 0)
    c2 = (100, 200, 50)
    mid = interpolate_rgb(c1, c2, 0.5)
    assert mid == (50, 100, 25)


def test_generate_gradient_palette():
    palette = generate_gradient_palette(["#ff0000", "#0000ff"], steps=5)
    assert len(palette) == 5
    for p in palette:
        assert "\033[38;2;" in p


def test_apply_gradient_to_lines():
    lines = ["Line 1", "Line 2", "Line 3"]
    colored = apply_gradient_to_lines(lines, ["#1793d1", "#00d7ff"])
    assert len(colored) == 3
    for l in colored:
        assert "\033[38;2;" in l
        assert "\033[0m" in l
