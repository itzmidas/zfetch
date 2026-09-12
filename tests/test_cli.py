"""Tests for CLI argument parsing and execution."""

from unittest.mock import patch
import pytest

from zfetch import __version__
from zfetch.cli import build_parser, main
from zfetch.config import Config, ConfigManager


def test_cli_parser_defaults():
    parser = build_parser()
    args = parser.parse_args([])
    assert args.setup is False
    assert args.preview is False
    assert args.random is False
    assert args.debug is False
    assert args.config is None


def test_cli_parser_flags():
    parser = build_parser()
    args = parser.parse_args(["--setup", "--debug", "--preview", "--random", "--config", "/tmp/test.toml"])
    assert args.setup is True
    assert args.preview is True
    assert args.random is True
    assert args.debug is True
    assert args.config == "/tmp/test.toml"


def test_cli_version(capsys):
    parser = build_parser()
    with pytest.raises(SystemExit) as exc:
        parser.parse_args(["--version"])
    assert exc.value.code == 0
    captured = capsys.readouterr()
    assert f"zfetch {__version__}" in captured.out


def test_cli_main_default(capsys):
    ret = main([])
    assert ret == 0
    captured = capsys.readouterr()
    assert "User" in captured.out
    assert "OS" in captured.out
    assert "Kernel" in captured.out


def test_cli_main_preview(capsys):
    ret = main(["--preview"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "User" in captured.out
    assert "OS" in captured.out


def test_cli_main_random(capsys):
    ret = main(["--random"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "User" in captured.out
    assert "OS" in captured.out


def test_cli_main_custom_config(tmp_path, capsys):
    conf_file = tmp_path / "custom.toml"
    cfg = Config()
    cfg.ascii.art = "tux"
    cfg.appearance.separator = "══>"
    ConfigManager(conf_file).save(cfg)

    ret = main(["--config", str(conf_file)])
    assert ret == 0
    captured = capsys.readouterr()
    assert "══>" in captured.out


def test_cli_main_setup_mocked():
    with patch("zfetch.tui.app.run_tui", return_value=0) as mock_tui:
        ret = main(["--setup"])
        assert ret == 0
        mock_tui.assert_called_once()
