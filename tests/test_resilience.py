"""Tests for error resilience, edge cases, and graceful degradation."""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

from yfetch.ascii.manager import AsciiManager
from yfetch.config import Config, ConfigManager
from yfetch.modules.base import BaseModule, ModuleRegistry, ModuleResult
from yfetch.renderer.terminal import render_fetch
from yfetch.utils.logger import setup_logger


def test_corrupted_custom_ascii_unreadable(tmp_path):
    ascii_dir = tmp_path / "ascii"
    ascii_dir.mkdir()
    bad_file = ascii_dir / "broken.txt"
    bad_file.write_bytes(b"\xff\xfe\x00\x00invalid")

    mgr = AsciiManager(custom_dir=ascii_dir)
    # Should not crash
    arts = mgr.get_custom_arts()
    assert isinstance(arts, dict)


def test_empty_custom_ascii_file(tmp_path):
    ascii_dir = tmp_path / "ascii"
    ascii_dir.mkdir()
    empty_file = ascii_dir / "empty.txt"
    empty_file.write_text("   \n\n  \n", encoding="utf-8")

    mgr = AsciiManager(custom_dir=ascii_dir)
    arts = mgr.get_custom_arts()
    assert "empty" not in arts  # empty art without lines should not be registered


def test_failing_module_graceful_handling():
    class BrokenModule(BaseModule):
        id = "broken_mod"
        title = "Broken"
        description = "Throws an exception intentionally"

        def fetch(self):
            raise RuntimeError("Unexpected failure!")

    ModuleRegistry.register(BrokenModule)
    cfg = Config()
    cfg.modules.enabled = ["broken_mod", "hostname"]

    # render_fetch should catch any module issue and continue without error
    out = render_fetch(config=cfg)
    assert out is not None
    assert "User" in out


def test_narrow_terminal_responsive_layout():
    cfg = Config()
    # Mock terminal width to 30 columns (narrow)
    with patch("shutil.get_terminal_size", return_value=os.terminal_size((30, 20))):
        out = render_fetch(config=cfg)
        assert out is not None
        # Should render successfully without exception


def test_debug_logging(tmp_path):
    log_file = tmp_path / "test_debug.log"
    logger = setup_logger(debug_mode=True, log_file=log_file)
    logger.debug("Test debug entry for resilience verification")

    assert log_file.is_file()
    assert "Test debug entry" in log_file.read_text(encoding="utf-8")
