# ⚡ yfetch

> **A beautiful, modern, and highly customizable Linux system fetch with an interactive TUI setup.**

`yfetch` combines rich system information with a next-generation interactive terminal configurator (`yfetch --setup`). Adjust your themes, ASCII logos, information modules, and layouts in real-time with an instant split-screen Live Preview — without ever touching a configuration file.

```text
       /\            User       ❯ archuser05@acer-aspire-5
      /  \           OS         ❯ Arch Linux x86_64
     /\   \          Kernel     ❯ 7.2.4-arch1-2
    /      \         Uptime     ❯ 2h 21m
   /   ,,   \        Packages   ❯ 1102 (pacman), 3 (flatpak)
  /   |  |  -\       Shell      ❯ bash 5.3.15
 /_-''    ''-_\     🖥 Resolution ❯ 1920x1080
                     DE         ❯ KDE Plasma
                     WM         ❯ KWin (Wayland)
                     Theme      ❯ Breeze
                     Icons      ❯ breeze-dark
                     Terminal   ❯ Alacritty
                     CPU        ❯ AMD Ryzen 5 5500U (12) @ 4.06 GHz
                     GPU        ❯ AMD Radeon Lucienne
                     Memory     ❯ 5.8 GiB / 7.1 GiB (82%)
                     Disk (/)   ❯ 38.8 GiB / 46.1 GiB (89%)

                    ● ● ● ● ● ● ● ● 
```

---

## ✨ Key Features

- **⚡ Fast & Lightweight**: Optimized for fast startup using direct `/proc` and `/sys` interfaces — smooth integration into `.bashrc` or `.zshrc`.
- **🛠️ Interactive TUI Setup (`yfetch --setup`)**: Full keyboard-driven configuration interface with instant Live Preview.
- **📊 Comprehensive Multi-Distro System Data**:
  - OS & Architecture, Kernel, Hostname, Uptime, Locale
  - Multi-distribution package detection: Pacman, DPKG/APT, RPM/DNF, APK, XBPS, Portage (Emerge), Nix, Homebrew, Flatpak, and Snap
  - Shell (with version), Terminal emulator, Terminal font
  - Desktop Environment (DE), Window Manager (WM), GTK Theme, Icon Theme
  - CPU (model, threads, clock frequency), GPU (PCI and DRM sysfs fallback), RAM, Swap, Disk mount usage, Battery state, Display Resolution
  - Terminal color dots / palette
- **🖼️ Built-in & Custom ASCII Art**:
  - Preloaded with logos for Arch Linux (Standard, Clean, Small, Large), Debian, Ubuntu, Fedora, Linux mascot, Tux the Penguin, and yfetch.
  - Drop your own `.txt` ASCII files into `~/.config/yfetch/ascii/` and they are discovered automatically.
- **🌈 Smooth TrueColor Gradients & Themes**:
  - Built-in palettes: **Arch Cyan (Default)**, **Nord**, **Dracula**, **Gruvbox**, **Tokyo Night**, **Catppuccin (Mocha)**, **Cyberpunk**, and **Monochrome**.
  - Multi-stop TrueColor gradient interpolation for ASCII art.
- **⚡ 1-Click Quick Styles**:
  - Instant aesthetic presets (Arch, Cyberpunk, Nord, Dracula, Minimal, Classic).
- **🛡️ Rock-Solid Resilience**:
  - Automatic fallback on damaged or missing configuration.
  - Isolated modules that gracefully degrade if hardware or tools are missing — no ugly tracebacks.

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/itzmidas/yfetch.git
cd yfetch
python3 -m venv ~/.local/share/yfetch/venv
~/.local/share/yfetch/venv/bin/pip install .
mkdir -p ~/.local/bin
ln -sf ~/.local/share/yfetch/venv/bin/yfetch ~/.local/bin/yfetch
```
*(Make sure `~/.local/bin` is in your `$PATH`! See [INSTALL.md](INSTALL.md) for full instructions).*

### 2. Run
```bash
# Standard instant fetch
yfetch

# Interactive visual setup with live preview
yfetch --setup

# Display fetch with random themes and artwork
yfetch --random

# Preview current active configuration
yfetch --preview
```

---

## 🖥️ Interactive Setup (`yfetch --setup`)

Launch the visual configurator:

```bash
yfetch --setup
```

```text
╭──────────────────────────────────────────────╮
│                  yfetch                      │
│          Setup & Customization               │
├──────────────────────────────────────────────┤
│  ❯ 🖼️  ASCII Art                             │
│    📋  Information                           │
│    🎨  Appearance                            │
│    🌈  Colors & Themes                       │
│    📐  Layout                                │
│    ⚡  Quick Styles                           │
│    ⚙️  Advanced                              │
│                                              │
│    💾  Save & Exit                           │
│    ✕   Exit without saving                   │
├──────────────────────────────────────────────┤
│ ↑↓ Navigate   Enter Select   Space Toggle    │
│ Esc Back      s Quick Save   q Quit          │
╰──────────────────────────────────────────────╯
```

### Navigation Keys:
- **`↑ / ↓`**: Navigate between menu items.
- **`Enter`**: Select menu option or enter submenu.
- **`Space`**: Toggle checkboxes (e.g. enable/disable information modules).
- **`Esc`**: Return to previous menu or open save dialog from main screen.
- **`s`**: Quick Save changes to `~/.config/yfetch/config.toml` and exit.

---

## ⚙️ CLI Reference

| Command | Description |
| :--- | :--- |
| `yfetch` | Run standard system fetch using saved configuration |
| `yfetch --setup` | Open interactive TUI configurator with live preview |
| `yfetch --preview` | Render output with active configuration |
| `yfetch --random` | Display fetch with randomly selected artwork and theme |
| `yfetch --config <PATH>` | Load specific alternative `config.toml` file |
| `yfetch --debug` | Enable verbose debugging log in `~/.config/yfetch/debug.log` |
| `yfetch --version` | Display version information |
| `yfetch --help` | Display command-line options |

---

## 📁 Configuration & Custom ASCII

Configuration is saved in:
```text
~/.config/yfetch/config.toml
```

To add custom ASCII artwork, simply place any plain text file (`.txt`) in:
```text
~/.config/yfetch/ascii/mylogo.txt
```
It will immediately appear in `yfetch --setup` under **ASCII Art**!

---

## 📖 Installation Guide

For step-by-step instructions for Linux beginners, multi-distro setup, troubleshooting, Nerd Font setup, and uninstallation, check out the comprehensive **[INSTALL.md](INSTALL.md)** guide.

---

## 📜 License

MIT License.
