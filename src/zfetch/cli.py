"""Command line interface for zfetch."""

import argparse
import sys

from zfetch import __version__
from zfetch.renderer.terminal import render_fetch
from zfetch.utils.logger import setup_logger


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser for zfetch."""
    parser = argparse.ArgumentParser(
        prog="zfetch",
        description="A beautiful, modern, and highly customizable Linux system fetch for Arch Linux.",
        epilog="Run 'zfetch --setup' to launch the interactive TUI configuration menu.",
        add_help=True,
    )

    parser.add_argument(
        "--setup",
        action="store_true",
        help="Launch the interactive TUI setup and customization tool.",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Display the fetch output using the currently active configuration.",
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Display fetch with a randomly selected style, theme, and ASCII art.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"zfetch {__version__}",
        help="Show program version and exit.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging to ~/.config/zfetch/debug.log.",
    )
    parser.add_argument(
        "--config",
        metavar="PATH",
        type=str,
        default=None,
        help="Path to an alternative config.toml file.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main CLI entrypoint for zfetch."""
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.debug:
        setup_logger(debug_mode=True)

    from zfetch.config import ConfigManager

    cfg_mgr = ConfigManager(config_path=args.config)
    config = cfg_mgr.load()

    if args.setup:
        try:
            # We lazy import textual TUI here so normal runs stay instant
            from zfetch.tui.app import run_tui
            return run_tui(config_path=args.config)
        except ImportError as e:
            sys.stderr.write(f"Error launching TUI setup: {e}\nPlease ensure textual is installed.\n")
            return 1

    # Normal fetch and preview
    print(render_fetch(config=config))
    return 0


if __name__ == "__main__":
    sys.exit(main())
