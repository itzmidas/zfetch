"""Packages information module with dynamic multi-distro package manager detection."""

import os
import shutil
from pathlib import Path
from typing import Optional

from yfetch.modules.base import BaseModule, ModuleResult, register_module
from yfetch.utils.logger import get_logger
from yfetch.utils.system import read_file_safe, run_command_safe

logger = get_logger()


@register_module
class PackagesModule(BaseModule):
    id = "packages"
    title = "Packages"
    description = "Number of installed system and flatpak/snap packages across distros"
    icon = ""
    default_enabled = True
    category = "system"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            parts = []

            # 1. Pacman (Arch Linux, Manjaro, EndeavourOS, Artix)
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
                    logger.debug("Failed counting pacman packages via dir: %s", e)
            elif shutil.which("pacman"):
                out = run_command_safe(["pacman", "-Qq"])
                if out:
                    count = len(out.splitlines())
                    parts.append(f"{count} (pacman)")

            # 2. DPKG / APT (Debian, Ubuntu, Linux Mint, Pop!_OS)
            dpkg_status = Path("/var/lib/dpkg/status")
            if dpkg_status.is_file():
                try:
                    content = read_file_safe(dpkg_status)
                    if content:
                        count = sum(1 for line in content.splitlines() if line.startswith("Package: "))
                        if count > 0:
                            parts.append(f"{count} (dpkg)")
                except Exception as e:
                    logger.debug("Failed counting dpkg packages: %s", e)
            elif shutil.which("dpkg-query"):
                out = run_command_safe(["dpkg-query", "-f", ".\\n", "-W"])
                if out:
                    count = len(out.splitlines())
                    parts.append(f"{count} (dpkg)")

            # 3. RPM / DNF / Zypper (Fedora, RHEL, CentOS, openSUSE)
            if shutil.which("rpm"):
                out = run_command_safe(["rpm", "-qa"])
                if out:
                    count = len(out.splitlines())
                    if count > 0:
                        parts.append(f"{count} (rpm)")

            # 4. APK (Alpine Linux)
            apk_installed = Path("/lib/apk/db/installed")
            if apk_installed.is_file():
                try:
                    content = read_file_safe(apk_installed)
                    if content:
                        count = sum(1 for line in content.splitlines() if line.startswith("P:"))
                        if count > 0:
                            parts.append(f"{count} (apk)")
                except Exception as e:
                    logger.debug("Failed counting apk packages: %s", e)

            # 5. XBPS (Void Linux)
            if shutil.which("xbps-query"):
                out = run_command_safe(["xbps-query", "-l"])
                if out:
                    count = len(out.splitlines())
                    if count > 0:
                        parts.append(f"{count} (xbps)")

            # 6. Portage / Emerge (Gentoo)
            gentoo_pkg_dir = Path("/var/db/pkg")
            if gentoo_pkg_dir.is_dir():
                try:
                    count = 0
                    for cat in os.scandir(gentoo_pkg_dir):
                        if cat.is_dir() and not cat.name.startswith("."):
                            count += sum(1 for pkg in os.scandir(cat.path) if pkg.is_dir())
                    if count > 0:
                        parts.append(f"{count} (emerge)")
                except Exception as e:
                    logger.debug("Failed counting portage packages: %s", e)

            # 7. Nix (NixOS / Nix package manager)
            nix_profile = Path.home() / ".nix-profile/manifest.nix"
            if nix_profile.is_file() or Path("/nix/var/nix/profiles/default").is_dir():
                if shutil.which("nix-store"):
                    out = run_command_safe(["nix-store", "-q", "--requisites", "/run/current-system/sw"])
                    if out:
                        count = len(out.splitlines())
                        parts.append(f"{count} (nix)")

            # 8. Homebrew (Linuxbrew)
            for brew_dir in [Path("/home/linuxbrew/.linuxbrew/Cellar"), Path.home() / ".linuxbrew/Cellar"]:
                if brew_dir.is_dir():
                    try:
                        count = sum(1 for entry in os.scandir(brew_dir) if entry.is_dir() and not entry.name.startswith("."))
                        if count > 0:
                            parts.append(f"{count} (brew)")
                            break
                    except Exception:
                        pass

            # 9. Flatpak (Universal)
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

            # 10. Snap (Universal)
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
