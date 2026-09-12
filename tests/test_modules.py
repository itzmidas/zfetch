"""Unit tests for zfetch information modules."""

from unittest.mock import MagicMock, patch
import pytest

from zfetch.modules.base import ModuleRegistry
from zfetch.modules.os_info import OSModule, KernelModule, UptimeModule, HostnameModule, LocaleModule
from zfetch.modules.packages import PackagesModule
from zfetch.modules.terminal import ShellModule, TerminalModule, TerminalFontModule
from zfetch.modules.desktop import DEModule, WMModule, GTKThemeModule, IconThemeModule
from zfetch.modules.hardware import CPUModule, GPUModule, MemoryModule, SwapModule, DiskModule, BatteryModule, ResolutionModule


def test_hostname_module():
    mod = HostnameModule()
    with patch("getpass.getuser", return_value="alice"), patch("socket.gethostname", return_value="archbox"):
        res = mod.fetch()
        assert res is not None
        assert res.label == "User"
        assert res.value == "alice@archbox"


def test_os_module():
    mod = OSModule()
    mock_os_release = 'NAME="Arch Linux"\nPRETTY_NAME="Arch Linux"\nID=arch\n'
    with patch("zfetch.modules.os_info.read_file_safe", return_value=mock_os_release), \
         patch("platform.machine", return_value="x86_64"):
        res = mod.fetch()
        assert res is not None
        assert res.label == "OS"
        assert "Arch Linux x86_64" in res.value


def test_kernel_module():
    mod = KernelModule()
    with patch("platform.release", return_value="6.12.1-arch1-1"):
        res = mod.fetch()
        assert res is not None
        assert res.label == "Kernel"
        assert res.value == "6.12.1-arch1-1"


def test_uptime_module():
    mod = UptimeModule()
    # 7320 seconds = 2h 2m
    with patch("zfetch.modules.os_info.read_file_safe", return_value="7320.45 14000.00"):
        res = mod.fetch()
        assert res is not None
        assert res.label == "Uptime"
        assert "2h" in res.value
        assert "2m" in res.value


def test_uptime_module_unreadable():
    mod = UptimeModule()
    with patch("zfetch.modules.os_info.read_file_safe", return_value=None):
        res = mod.fetch()
        assert res is None


def test_packages_module(tmp_path):
    mod = PackagesModule()
    # Mock pacman local directory
    p_dir = tmp_path / "pacman" / "local"
    p_dir.mkdir(parents=True)
    (p_dir / "pkg1-1.0").mkdir()
    (p_dir / "pkg2-2.0").mkdir()
    (p_dir / ".hidden").mkdir()

    with patch("zfetch.modules.packages.Path") as mock_path:
        mock_path.side_effect = lambda p: p_dir if "pacman" in str(p) else tmp_path / "empty"
        mock_path.home.return_value = tmp_path
        res = mod.fetch()
        assert res is not None
        assert "2 (pacman)" in res.value


def test_shell_module():
    mod = ShellModule()
    with patch.dict("os.environ", {"SHELL": "/bin/bash"}), \
         patch("zfetch.modules.terminal.run_command_safe", return_value="GNU bash, version 5.2.26(1)-release"):
        res = mod.fetch()
        assert res is not None
        assert res.label == "Shell"
        assert "bash" in res.value
        assert "5.2.26" in res.value


def test_desktop_de_module():
    mod = DEModule()
    with patch.dict("os.environ", {"XDG_CURRENT_DESKTOP": "KDE"}):
        res = mod.fetch()
        assert res is not None
        assert res.label == "DE"
        assert res.value == "KDE Plasma"


def test_desktop_wm_module():
    mod = WMModule()
    mock_proc = MagicMock()
    mock_proc.info = {"name": "kwin_wayland"}
    with patch("psutil.process_iter", return_value=[mock_proc]):
        res = mod.fetch()
        assert res is not None
        assert res.label == "WM"
        assert "KWin (Wayland)" in res.value


def test_cpu_module():
    mod = CPUModule()
    mock_cpuinfo = "processor : 0\nmodel name : AMD Ryzen 7 7800X3D 8-Core Processor\nprocessor : 1\nmodel name : AMD Ryzen 7 7800X3D 8-Core Processor\n"
    with patch("zfetch.modules.hardware.read_file_safe", side_effect=lambda p: mock_cpuinfo if str(p) == "/proc/cpuinfo" else "4200000"):
        res = mod.fetch()
        assert res is not None
        assert res.label == "CPU"
        assert "AMD Ryzen 7 7800X3D" in res.value
        assert "(2)" in res.value
        assert "@ 4.20 GHz" in res.value


def test_gpu_module():
    mod = GPUModule()
    mock_lspci = "01:00.0 VGA compatible controller: NVIDIA Corporation GA106 [GeForce RTX 3060] (rev a1)"
    with patch("zfetch.modules.hardware.run_command_safe", return_value=mock_lspci):
        res = mod.fetch()
        assert res is not None
        assert res.label == "GPU"
        assert "NVIDIA" in res.value
        assert "GeForce RTX 3060" in res.value


def test_memory_module():
    mod = MemoryModule()
    mock_vm = MagicMock()
    mock_vm.used = 4 * 1024**3
    mock_vm.total = 16 * 1024**3
    mock_vm.percent = 25.0
    with patch("psutil.virtual_memory", return_value=mock_vm):
        res = mod.fetch()
        assert res is not None
        assert res.label == "Memory"
        assert "4.0 GiB / 16.0 GiB (25%)" in res.value


def test_battery_module():
    mod = BatteryModule()
    mock_sbatt = MagicMock()
    mock_sbatt.percent = 92.0
    mock_sbatt.power_plugged = True
    with patch("psutil.sensors_battery", return_value=mock_sbatt):
        res = mod.fetch()
        assert res is not None
        assert res.label == "Battery"
        assert "92% [Charging]" in res.value

    # Battery None (e.g. desktop)
    with patch("psutil.sensors_battery", return_value=None):
        res = mod.fetch()
        assert res is None


def test_resolution_module():
    mod = ResolutionModule()
    with patch("glob.glob", return_value=["/sys/class/drm/card0-DP-1/modes"]), \
         patch("zfetch.modules.hardware.read_file_safe", return_value="2560x1440\n1920x1080"):
        res = mod.fetch()
        assert res is not None
        assert res.label == "Resolution"
        assert res.value == "2560x1440"


def test_registry_canonical_order():
    all_mods = ModuleRegistry.get_all()
    ids = [m.id for m in all_mods]
    assert "hostname" in ids
    assert "os" in ids
    assert "cpu" in ids
    assert ids.index("hostname") < ids.index("os")
    assert ids.index("os") < ids.index("cpu")
