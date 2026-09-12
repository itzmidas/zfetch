"""Operating system, hostname, kernel, uptime, and locale modules."""

import getpass
import os
import platform
import socket
from typing import Optional

from yfetch.modules.base import BaseModule, ModuleResult, register_module
from yfetch.utils.logger import get_logger
from yfetch.utils.system import format_seconds, read_file_safe

logger = get_logger()


@register_module
class HostnameModule(BaseModule):
    id = "hostname"
    title = "Hostname"
    description = "Current username and machine hostname (user@hostname)"
    icon = ""
    default_enabled = True
    category = "system"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            username = getpass.getuser()
        except Exception:
            username = os.environ.get("USER", "user")

        try:
            hostname = socket.gethostname()
        except Exception:
            hostname = "localhost"

        return ModuleResult(
            module_id=self.id,
            label="User",
            value=f"{username}@{hostname}",
            icon=self.icon,
        )


@register_module
class OSModule(BaseModule):
    id = "os"
    title = "Operating System"
    description = "Linux distribution name and architecture"
    icon = ""
    default_enabled = True
    category = "system"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            distro_name = ""
            icon = ""  # generic Linux icon fallback
            os_release = read_file_safe("/etc/os-release")
            distro_id = ""
            if os_release:
                for line in os_release.splitlines():
                    if line.startswith("PRETTY_NAME="):
                        distro_name = line.split("=", 1)[1].strip('"\'')
                    elif line.startswith("ID=") and not distro_id:
                        distro_id = line.split("=", 1)[1].strip('"\'').lower()

            if not distro_name:
                import distro
                distro_name = distro.name(pretty=True) or platform.system() or "Linux"

            # Set distro-specific Nerd font icon if recognized
            if "arch" in distro_id or "arch" in distro_name.lower():
                icon = ""
            elif "debian" in distro_id or "debian" in distro_name.lower():
                icon = ""
            elif "ubuntu" in distro_id or "ubuntu" in distro_name.lower():
                icon = ""
            elif "fedora" in distro_id or "fedora" in distro_name.lower():
                icon = ""
            elif "opensuse" in distro_id or "suse" in distro_name.lower():
                icon = ""
            elif "gentoo" in distro_id or "gentoo" in distro_name.lower():
                icon = ""
            elif "nixos" in distro_id or "nixos" in distro_name.lower():
                icon = ""
            elif "alpine" in distro_id or "alpine" in distro_name.lower():
                icon = ""
            elif "void" in distro_id or "void" in distro_name.lower():
                icon = ""

            arch = platform.machine()
            val = f"{distro_name} {arch}".strip()
            return ModuleResult(
                module_id=self.id,
                label="OS",
                value=val,
                icon=icon,
            )
        except Exception as e:
            logger.debug("OSModule error: %s", e)
            return None


@register_module
class KernelModule(BaseModule):
    id = "kernel"
    title = "Kernel"
    description = "Running Linux kernel version"
    icon = ""
    default_enabled = True
    category = "system"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            krelease = platform.release()
            if not krelease:
                krelease = read_file_safe("/proc/sys/kernel/osrelease") or "Unknown"
            return ModuleResult(
                module_id=self.id,
                label="Kernel",
                value=krelease,
                icon=self.icon,
            )
        except Exception as e:
            logger.debug("KernelModule error: %s", e)
            return None


@register_module
class UptimeModule(BaseModule):
    id = "uptime"
    title = "Uptime"
    description = "System running time since last boot"
    icon = ""
    default_enabled = True
    category = "system"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            uptime_content = read_file_safe("/proc/uptime")
            if uptime_content:
                total_seconds = float(uptime_content.split()[0])
                uptime_str = format_seconds(total_seconds)
                return ModuleResult(
                    module_id=self.id,
                    label="Uptime",
                    value=uptime_str,
                    icon=self.icon,
                )
        except Exception as e:
            logger.debug("UptimeModule error: %s", e)
        return None


@register_module
class LocaleModule(BaseModule):
    id = "locale"
    title = "Locale"
    description = "Active system language and charset encoding"
    icon = ""
    default_enabled = False
    category = "system"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            loc = os.environ.get("LANG") or os.environ.get("LC_ALL")
            if loc:
                return ModuleResult(
                    module_id=self.id,
                    label="Locale",
                    value=loc,
                    icon=self.icon,
                )
        except Exception as e:
            logger.debug("LocaleModule error: %s", e)
        return None
