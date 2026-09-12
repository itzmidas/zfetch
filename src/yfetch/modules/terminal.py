"""Shell, terminal emulator, and terminal font modules."""

import os
from pathlib import Path
from typing import Optional

import psutil

from yfetch.modules.base import BaseModule, ModuleResult, register_module
from yfetch.utils.logger import get_logger
from yfetch.utils.system import run_command_safe

logger = get_logger()

KNOWN_TERMINALS = [
    "kitty",
    "alacritty",
    "konsole",
    "foot",
    "gnome-terminal",
    "xfce4-terminal",
    "tilix",
    "terminator",
    "xterm",
    "urxvt",
    "st",
    "wezterm",
    "hyper",
    "terminology",
    "yakuake",
    "ghostty",
    "warp",
]


@register_module
class ShellModule(BaseModule):
    id = "shell"
    title = "Shell"
    description = "User default or active command shell and version"
    icon = ""
    default_enabled = True
    category = "terminal"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            shell_env = os.environ.get("SHELL") or ""
            shell_name = Path(shell_env).name if shell_env else "sh"

            # Attempt to get version
            version = ""
            if "bash" in shell_name:
                v_out = run_command_safe([shell_env or "bash", "--version"])
                if v_out:
                    first_line = v_out.splitlines()[0]
                    # Format: GNU bash, version 5.2.37(1)-release
                    for part in first_line.split():
                        if part.replace(".", "").isdigit() or (
                            part.count(".") >= 1 and part[0].isdigit()
                        ):
                            version = part.split("(")[0]
                            break
            elif "zsh" in shell_name:
                v_out = run_command_safe(["zsh", "--version"])
                if v_out:
                    parts = v_out.split()
                    if len(parts) >= 2:
                        version = parts[1]
            elif "fish" in shell_name:
                v_out = run_command_safe(["fish", "--version"])
                if v_out:
                    parts = v_out.split()
                    if len(parts) >= 3:
                        version = parts[2]

            val = f"{shell_name} {version}".strip()
            return ModuleResult(
                module_id=self.id,
                label="Shell",
                value=val,
                icon=self.icon,
            )
        except Exception as e:
            logger.debug("ShellModule error: %s", e)
            return None


@register_module
class TerminalModule(BaseModule):
    id = "terminal"
    title = "Terminal"
    description = "Active terminal emulator"
    icon = ""
    default_enabled = True
    category = "terminal"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            # 1. Environment variables
            term_prog = os.environ.get("TERM_PROGRAM")
            if term_prog:
                return ModuleResult(
                    module_id=self.id,
                    label="Terminal",
                    value=term_prog,
                    icon=self.icon,
                )

            # 2. Check process tree for known terminals
            cur = psutil.Process()
            while cur:
                try:
                    name = cur.name().lower()
                    for term in KNOWN_TERMINALS:
                        if term in name:
                            # Capitalize nicely
                            display_name = term.capitalize()
                            if term == "gnome-terminal":
                                display_name = "GNOME Terminal"
                            elif term == "xfce4-terminal":
                                display_name = "XFCE Terminal"
                            return ModuleResult(
                                module_id=self.id,
                                label="Terminal",
                                value=display_name,
                                icon=self.icon,
                            )
                    cur = cur.parent()
                except Exception:
                    break

            # 3. Fallback to TERM if not 'dumb'
            term_env = os.environ.get("TERM")
            if term_env and term_env.lower() not in ("dumb", "unknown"):
                return ModuleResult(
                    module_id=self.id,
                    label="Terminal",
                    value=term_env,
                    icon=self.icon,
                )
        except Exception as e:
            logger.debug("TerminalModule error: %s", e)
        return None


@register_module
class TerminalFontModule(BaseModule):
    id = "terminal_font"
    title = "Terminal Font"
    description = "Configured font family and size in terminal"
    icon = ""
    default_enabled = False
    category = "terminal"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            # Look in common terminal configs (e.g. alacritty, kitty)
            kitty_conf = Path.home() / ".config/kitty/kitty.conf"
            if kitty_conf.is_file():
                for line in kitty_conf.read_text(errors="ignore").splitlines():
                    if line.startswith("font_family") and len(line.split()) >= 2:
                        font = " ".join(line.split()[1:])
                        return ModuleResult(
                            module_id=self.id,
                            label="Font",
                            value=font,
                            icon=self.icon,
                        )

            alacritty_conf = Path.home() / ".config/alacritty/alacritty.toml"
            if alacritty_conf.is_file():
                import tomllib
                try:
                    data = tomllib.loads(alacritty_conf.read_text(errors="ignore"))
                    family = data.get("font", {}).get("normal", {}).get("family")
                    if family:
                        return ModuleResult(
                            module_id=self.id,
                            label="Font",
                            value=family,
                            icon=self.icon,
                        )
                except Exception:
                    pass
        except Exception as e:
            logger.debug("TerminalFontModule error: %s", e)
        return None
