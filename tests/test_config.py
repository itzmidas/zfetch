"""Tests for yfetch configuration system."""

from pathlib import Path
import pytest

from yfetch.config import Config, ConfigManager


def test_default_config():
    cfg = Config()
    assert cfg.ascii.art == "arch"
    assert cfg.ascii.color_mode == "theme"
    assert "hostname" in cfg.modules.enabled
    assert "os" in cfg.modules.enabled
    assert cfg.appearance.separator == "❯"
    assert cfg.appearance.spacing == 4
    assert cfg.appearance.nerd_fonts is True


def test_save_and_load_config(tmp_path):
    conf_file = tmp_path / "test_config.toml"
    mgr = ConfigManager(config_path=conf_file)

    # Modify and save
    cfg = Config()
    cfg.ascii.art = "tux"
    cfg.appearance.separator = "→"
    cfg.appearance.spacing = 6
    cfg.modules.enabled = ["os", "kernel"]

    assert mgr.save(cfg) is True
    assert conf_file.is_file()

    # Load back
    loaded = mgr.load(auto_create=False)
    assert loaded.ascii.art == "tux"
    assert loaded.appearance.separator == "→"
    assert loaded.appearance.spacing == 6
    assert loaded.modules.enabled == ["os", "kernel"]


def test_corrupted_config_recovery(tmp_path):
    conf_file = tmp_path / "corrupt_config.toml"
    conf_file.write_text("this is [[[ totally broken toml == syntax !!!", encoding="utf-8")

    mgr = ConfigManager(config_path=conf_file)
    # Should not raise exception; falls back to default
    loaded = mgr.load(auto_create=False)
    assert loaded is not None
    assert loaded.ascii.art == "arch"
    assert loaded.appearance.separator == "❯"


def test_missing_config_autocreate(tmp_path):
    conf_file = tmp_path / "sub" / "config.toml"
    mgr = ConfigManager(config_path=conf_file)

    loaded = mgr.load(auto_create=True)
    assert loaded is not None
    assert conf_file.is_file()


def test_partial_dict_recovery():
    partial_data = {
        "ascii": {"art": "linux"},
        "appearance": {"spacing": 8},
        "unknown_section": {"foo": "bar"},
    }
    cfg = Config.from_dict(partial_data)
    assert cfg.ascii.art == "linux"
    assert cfg.appearance.spacing == 8
    # Defaults should remain intact for unspecified fields
    assert cfg.appearance.separator == "❯"
    assert "os" in cfg.modules.enabled
