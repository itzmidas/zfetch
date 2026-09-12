"""Desktop environment, window manager, and desktop themes modules."""

import os
from pathlib import Path
from typing import Optional

import psutil

from yfetch.modules.base import BaseModule, ModuleResult, register_module
from yfetch.utils.logger import get_logger
from yfetch.utils.system import read_file_safe, run_command_safe

logger = get_logger()

KNOWN_WMS = {
    "kwin_wayland": "KWin (Wayland)",
    "kwin_x11": "KWin (X11)",
    "kwin": "KWin",
    "mutter": "Mutter",
    "sway": "Sway",
    "hyprland": "Hyprland",
    "i3": "i3",
    "bspwm": "bspwm",
    "dwm": "dwm",
    "openbox": "Openbox",
    "xfwm4": "Xfwm4",
    "wayfire": "Wayfire",
    "river": "River",
    "awesome": "AwesomeWM",
    "compiz": "Compiz",
}


@register_module
class DEModule(BaseModule):
    id = "de"
    title = "Desktop Environment"
    description = "Active desktop environment (KDE Plasma, GNOME, XFCE, etc.)"
    icon = ""
    default_enabled = True
    category = "desktop"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            de = (
                os.environ.get("XDG_CURRENT_DESKTOP")
                or os.environ.get("DESKTOP_SESSION")
                or os.environ.get("XDG_SESSION_DESKTOP")
            )
            if not de:
                return None

            # Clean up common names like KDE -> KDE Plasma
            de_clean = de.replace(":", " / ")
            if de_clean.upper() == "KDE":
                de_clean = "KDE Plasma"
            elif de_clean.upper() == "GNOME":
                de_clean = "GNOME"
            elif de_clean.upper() == "XFCE":
                de_clean = "XFCE"

            return ModuleResult(
                module_id=self.id,
                label="DE",
                value=de_clean,
                icon=self.icon,
            )
        except Exception as e:
            logger.debug("DEModule error: %s", e)
            return None


@register_module
class WMModule(BaseModule):
    id = "wm"
    title = "Window Manager"
    description = "Active window manager or Wayland compositor"
    icon = ""
    default_enabled = True
    category = "desktop"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            # Check processes for known WMs
            for p in psutil.process_iter(["name"]):
                try:
                    name = p.info["name"]
                    if name:
                        name_lower = name.lower()
                        for wm_key, wm_name in KNOWN_WMS.items():
                            if wm_key == name_lower:
                                return ModuleResult(
                                    module_id=self.id,
                                    label="WM",
                                    value=wm_name,
                                    icon=self.icon,
                                )
                except Exception:
                    pass

            # Fallback to desktop session or env
            desktop = os.environ.get("XDG_CURRENT_DESKTOP") or ""
            if any(wm in desktop.lower() for wm in ["sway", "hyprland", "i3"]):
                return ModuleResult(
                    module_id=self.id,
                    label="WM",
                    value=desktop,
                    icon=self.icon,
                )
        except Exception as e:
            logger.debug("WMModule error: %s", e)
        return None


def _get_gtk_setting(setting_name: str) -> Optional[str]:
    """Helper to read GTK setting from settings.ini."""
    for conf_path in [
        Path.home() / ".config/gtk-3.0/settings.ini",
        Path.home() / ".config/gtk-4.0/settings.ini",
        Path.home() / ".gtkrc-2.0",
    ]:
        content = read_file_safe(conf_path)
        if content:
            for line in content.splitlines():
                if line.strip().startswith(setting_name):
                    parts = line.split("=", 1)
                    if len(parts) == 2:
                        return parts[1].strip().strip('"\'')
    return None


@register_module
class WMThemeModule(BaseModule):
    id = "wm_theme"
    title = "WM Theme"
    description = "Active Window Manager or decorator theme"
    icon = ""
    default_enabled = False
    category = "desktop"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            # Check KDE kdeglobals or GTK theme as fallback
            kde_globals = Path.home() / ".config/kdeglobals"
            content = read_file_safe(kde_globals)
            if content:
                for line in content.splitlines():
                    if line.strip().startswith("Name="):
                        theme_name = line.split("=", 1)[1].strip()
                        return ModuleResult(
                            module_id=self.id,
                            label="WM Theme",
                            value=theme_name,
                            icon=self.icon,
                        )

            gtk_theme = _get_gtk_setting("gtk-theme-name")
            if gtk_theme:
                return ModuleResult(
                    module_id=self.id,
                    label="WM Theme",
                    value=gtk_theme,
                    icon=self.icon,
                )
        except Exception as e:
            logger.debug("WMThemeModule error: %s", e)
        return None


@register_module
class GTKThemeModule(BaseModule):
    id = "gtk_theme"
    title = "GTK Theme"
    description = "Current GTK application theme"
    icon = ""
    default_enabled = True
    category = "desktop"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            theme = _get_gtk_setting("gtk-theme-name")
            if not theme:
                # Try gsettings if available
                theme = run_command_safe(["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"])
                if theme:
                    theme = theme.strip("'\"")

            if theme:
                return ModuleResult(
                    module_id=self.id,
                    label="Theme",
                    value=theme,
                    icon=self.icon,
                )
        except Exception as e:
            logger.debug("GTKThemeModule error: %s", e)
        return None


@register_module
class IconThemeModule(BaseModule):
    id = "icon_theme"
    title = "Icon Theme"
    description = "Current desktop and application icon theme"
    icon = ""
    default_enabled = True
    category = "desktop"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            icons = _get_gtk_setting("gtk-icon-theme-name")
            if not icons:
                icons = run_command_safe(["gsettings", "get", "org.gnome.desktop.interface", "icon-theme"])
                if icons:
                    icons = icons.strip("'\"")

            if icons:
                return ModuleResult(
                    module_id=self.id,
                    label="Icons",
                    value=icons,
                    icon=self.icon,
                )
        except Exception as e:
            logger.debug("IconThemeModule error: %s", e)
        return None
