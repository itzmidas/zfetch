"""Packages information module."""

import os
from pathlib import Path
from typing import Optional

from zfetch.modules.base import BaseModule, ModuleResult, register_module
from zfetch.utils.logger import get_logger

logger = get_logger()


@register_module
class PackagesModule(BaseModule):
    id = "packages"
    title = "Packages"
    description = "Number of installed system and flatpak/snap packages"
    icon = ""
    default_enabled = True
    category = "system"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            parts = []

            # 1. Pacman (Arch Linux)
            pacman_dir = Path("/var/lib/pacman/local")
            if pacman_dir.is_dir():
                try:
                    count = sum(
                        1
                        for entry in os.scandir(pacman_dir)
                        if entry.is_dir() and not entry.name.startswith(".")
                    )
                    if count > 0:
                        parts.append(f"{count} (pacman)")
                except Exception as e:
                    logger.debug("Failed counting pacman packages: %s", e)

            # 2. Flatpak
            flatpak_dirs = [
                Path("/var/lib/flatpak/app"),
                Path.home() / ".local/share/flatpak/app",
            ]
            flatpak_count = 0
            for fd in flatpak_dirs:
                if fd.is_dir():
                    try:
                        flatpak_count += sum(
                            1
                            for entry in os.scandir(fd)
                            if entry.is_dir() and not entry.name.startswith(".")
                        )
                    except Exception as e:
                        logger.debug("Failed counting flatpak packages in %s: %s", fd, e)
            if flatpak_count > 0:
                parts.append(f"{flatpak_count} (flatpak)")

            # 3. Snap
            snap_dir = Path("/var/lib/snapd/snaps")
            if snap_dir.is_dir():
                try:
                    snap_count = sum(
                        1 for entry in os.scandir(snap_dir) if entry.name.endswith(".snap")
                    )
                    if snap_count > 0:
                        parts.append(f"{snap_count} (snap)")
                except Exception as e:
                    logger.debug("Failed counting snap packages: %s", e)

            if not parts:
                return None

            return ModuleResult(
                module_id=self.id,
                label="Packages",
                value=", ".join(parts),
                icon=self.icon,
            )
        except Exception as e:
            logger.debug("PackagesModule error: %s", e)
            return None
