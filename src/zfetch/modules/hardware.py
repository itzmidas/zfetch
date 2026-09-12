"""Hardware modules: CPU, GPU, Memory, Swap, Disk, Battery, and Resolution."""

import glob
import os
import re
from pathlib import Path
from typing import Optional

import psutil

from zfetch.modules.base import BaseModule, ModuleResult, register_module
from zfetch.utils.logger import get_logger
from zfetch.utils.system import format_bytes, read_file_safe, run_command_safe

logger = get_logger()


@register_module
class CPUModule(BaseModule):
    id = "cpu"
    title = "CPU"
    description = "Processor model name, thread count, and peak clock frequency"
    icon = ""
    default_enabled = True
    category = "hardware"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            model = ""
            threads = 0
            cpuinfo = read_file_safe("/proc/cpuinfo")
            if cpuinfo:
                for line in cpuinfo.splitlines():
                    if line.startswith("model name") and not model:
                        model = line.split(":", 1)[1].strip()
                    if line.startswith("processor"):
                        threads += 1

            if not model:
                model = "Unknown CPU"

            # Clean model string
            # Remove (R), (TM), 'CPU', 'with Radeon Graphics', 'Processor', 'Six-Core', etc.
            clean = model
            for rem in ["(R)", "(TM)", "Processor", "with Radeon Graphics", "with Radeon Vega Mobile Gfx"]:
                clean = clean.replace(rem, "")
            clean = re.sub(r"\b\d+-Core\b", "", clean, flags=re.IGNORECASE)
            clean = re.sub(r"\s+", " ", clean).strip()

            # Frequency
            freq_str = ""
            freq_val = read_file_safe("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq")
            if not freq_val:
                freq_val = read_file_safe("/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq")

            if freq_val and freq_val.isdigit():
                ghz = int(freq_val) / 1_000_000
                freq_str = f" @ {ghz:.2f} GHz"

            thread_str = f" ({threads})" if threads > 0 else ""
            val = f"{clean}{thread_str}{freq_str}"

            return ModuleResult(
                module_id=self.id,
                label="CPU",
                value=val,
                icon=self.icon,
            )
        except Exception as e:
            logger.debug("CPUModule error: %s", e)
            return None


@register_module
class GPUModule(BaseModule):
    id = "gpu"
    title = "GPU"
    description = "Graphics card model and manufacturer"
    icon = ""
    default_enabled = True
    category = "hardware"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            # 1. Try lspci
            lspci_out = run_command_safe(["lspci"])
            gpus = []
            if lspci_out:
                for line in lspci_out.splitlines():
                    if any(c in line for c in ["VGA compatible", "3D controller", "Display controller"]):
                        # Example: 05:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Lucienne (rev c2)
                        parts = line.split(":", 2)
                        if len(parts) >= 3:
                            gpu_info = parts[2].strip()
                            gpu_info = re.sub(r"\(rev.*?\)", "", gpu_info).strip()
                            gpu_info = re.sub(r"Advanced Micro Devices, Inc\.\s*", "AMD ", gpu_info)
                            gpu_info = re.sub(r"\[AMD/ATI\]\s*", "Radeon ", gpu_info)
                            gpu_info = re.sub(r"Corporation\s*", "", gpu_info)
                            gpu_info = re.sub(r"\[(.*?)\]", r"\1", gpu_info)
                            gpu_info = re.sub(r"\s+", " ", gpu_info).strip()
                            if gpu_info:
                                gpus.append(gpu_info)

            if gpus:
                # Deduplicate while preserving order
                unique_gpus = list(dict.fromkeys(gpus))
                return ModuleResult(
                    module_id=self.id,
                    label="GPU",
                    value=", ".join(unique_gpus),
                    icon=self.icon,
                )
        except Exception as e:
            logger.debug("GPUModule error: %s", e)
        return None


@register_module
class MemoryModule(BaseModule):
    id = "memory"
    title = "Memory"
    description = "Used and total physical RAM and percentage"
    icon = ""
    default_enabled = True
    category = "hardware"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            mem = psutil.virtual_memory()
            used_str = format_bytes(mem.used)
            total_str = format_bytes(mem.total)
            percent = mem.percent
            return ModuleResult(
                module_id=self.id,
                label="Memory",
                value=f"{used_str} / {total_str} ({percent:.0f}%)",
                icon=self.icon,
            )
        except Exception as e:
            logger.debug("MemoryModule error: %s", e)
            return None


@register_module
class SwapModule(BaseModule):
    id = "swap"
    title = "Swap"
    description = "Used and total swap partition space"
    icon = ""
    default_enabled = False
    category = "hardware"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            swap = psutil.swap_memory()
            if swap.total == 0:
                return None
            used_str = format_bytes(swap.used)
            total_str = format_bytes(swap.total)
            return ModuleResult(
                module_id=self.id,
                label="Swap",
                value=f"{used_str} / {total_str} ({swap.percent:.0f}%)",
                icon=self.icon,
            )
        except Exception as e:
            logger.debug("SwapModule error: %s", e)
            return None


@register_module
class DiskModule(BaseModule):
    id = "disk"
    title = "Disk"
    description = "Used and total root partition disk space"
    icon = ""
    default_enabled = True
    category = "hardware"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            disk = psutil.disk_usage("/")
            used_str = format_bytes(disk.used)
            total_str = format_bytes(disk.total)
            return ModuleResult(
                module_id=self.id,
                label="Disk (/)",
                value=f"{used_str} / {total_str} ({disk.percent:.0f}%)",
                icon=self.icon,
            )
        except Exception as e:
            logger.debug("DiskModule error: %s", e)
            return None


@register_module
class BatteryModule(BaseModule):
    id = "battery"
    title = "Battery"
    description = "Laptop battery percentage and charging status"
    icon = ""
    default_enabled = False
    category = "hardware"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            batt = psutil.sensors_battery()
            if batt is None:
                return None

            status_str = "AC" if batt.power_plugged else "Discharging"
            if batt.power_plugged and batt.percent < 100:
                status_str = "Charging"

            return ModuleResult(
                module_id=self.id,
                label="Battery",
                value=f"{int(batt.percent)}% [{status_str}]",
                icon=self.icon,
            )
        except Exception as e:
            logger.debug("BatteryModule error: %s", e)
            return None


@register_module
class ResolutionModule(BaseModule):
    id = "resolution"
    title = "Resolution"
    description = "Connected monitor display resolution and refresh rate"
    icon = "🖥"
    default_enabled = True
    category = "hardware"

    def fetch(self) -> Optional[ModuleResult]:
        try:
            # 1. Read DRM modes
            modes: list[str] = []
            for p in sorted(glob.glob("/sys/class/drm/*/modes")):
                content = read_file_safe(p)
                if content:
                    first = content.splitlines()[0].strip()
                    if first and "x" in first:
                        modes.append(first)

            if modes:
                return ModuleResult(
                    module_id=self.id,
                    label="Resolution",
                    value=", ".join(modes),
                    icon=self.icon,
                )

            # 2. Try xrandr
            xrandr_out = run_command_safe(["xrandr", "--current"])
            if xrandr_out:
                found_res = re.findall(r"current (\d+ x \d+)", xrandr_out)
                if found_res:
                    return ModuleResult(
                        module_id=self.id,
                        label="Resolution",
                        value=found_res[0].replace(" ", ""),
                        icon=self.icon,
                    )
        except Exception as e:
            logger.debug("ResolutionModule error: %s", e)
            return None
