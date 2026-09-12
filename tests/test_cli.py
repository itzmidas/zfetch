"""Tests for CLI argument parsing and execution."""

import pytest
from zfetch.cli import build_parser, main
from zfetch import __version__


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
    args = parser.parse_args(["--setup", "--debug", "--config", "/tmp/test.toml"])
    assert args.setup is True
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
