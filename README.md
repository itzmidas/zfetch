# ⚡ zfetch

> **A beautiful, modern, and highly customizable Linux system fetch for Arch Linux with an interactive TUI setup.**

`zfetch` combines the rich system information of classic tools like Neofetch with a next-generation interactive terminal configurator (`zfetch --setup`). Adjust your themes, ASCII logos, information modules, and layouts in real-time with an instant split-screen Live Preview — without ever touching a configuration file.

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

- **⚡ Blazingly Fast**: Starts in milliseconds (< 50ms) using fast `/proc` and `/sys` kernel interfaces — perfect for `.bashrc` or `.zshrc`.
- **🛠️ Interactive TUI Setup (`zfetch --setup`)**: Full keyboard-driven configuration interface with instant Live Preview.
- **📊 Comprehensive System Data**:
  - OS & Architecture, Kernel, Hostname, Uptime, Locale
  - Pacman & Flatpak package counts
  - Shell (with version), Terminal emulator, Terminal font
  - Desktop Environment (DE), Window Manager (WM), GTK Theme, Icon Theme
  - CPU (model, threads, clock frequency), GPU, RAM, Swap, Disk mount usage, Battery state, Display Resolution
  - Terminal color dots / palette
- **🖼️ Built-in & Custom ASCII Art**:
  - Preloaded with Arch Linux (Standard, Clean, Small, Large), Linux mascot, Tux the Penguin, and zfetch logos.
  - Drop your own `.txt` ASCII files into `~/.config/zfetch/ascii/` and they are discovered automatically.
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
git clone https://github.com/itzmidas/zfetch.git
cd zfetch
python3 -m venv ~/.local/share/zfetch/venv
~/.local/share/zfetch/venv/bin/pip install .
mkdir -p ~/.local/bin
ln -sf ~/.local/share/zfetch/venv/bin/zfetch ~/.local/bin/zfetch
```
*(Make sure `~/.local/bin` is in your `$PATH`! See [INSTALL.md](INSTALL.md) for full instructions).*

### 2. Run
```bash
# Standard instant fetch
zfetch

# Interactive visual setup with live preview
zfetch --setup

# Display fetch with random themes and artwork
zfetch --random

# Preview current active configuration
zfetch --preview
```

---

## 🖥️ Interactive Setup (`zfetch --setup`)

Launch the visual configurator:

```bash
zfetch --setup
```

```text
╭──────────────────────────────────────────────╮
│                  zfetch                      │
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
- **`s`**: Quick Save changes to `~/.config/zfetch/config.toml` and exit.

---

## ⚙️ CLI Reference

| Command | Description |
| :--- | :--- |
| `zfetch` | Run standard system fetch using saved configuration |
| `zfetch --setup` | Open interactive TUI configurator with live preview |
| `zfetch --preview` | Render output with active configuration |
| `zfetch --random` | Display fetch with randomly selected artwork and theme |
| `zfetch --config <PATH>` | Load specific alternative `config.toml` file |
| `zfetch --debug` | Enable verbose debugging log in `~/.config/zfetch/debug.log` |
| `zfetch --version` | Display version information |
| `zfetch --help` | Display command-line options |

---

## 📁 Configuration & Custom ASCII

Configuration is saved in:
```text
~/.config/zfetch/config.toml
```

To add custom ASCII artwork, simply place any plain text file (`.txt`) in:
```text
~/.config/zfetch/ascii/mylogo.txt
```
It will immediately appear in `zfetch --setup` under **ASCII Art**!

---

## 📖 Installation Guide

For step-by-step instructions for Linux beginners, troubleshooting, Nerd Font setup, and uninstallation, check out the comprehensive **[INSTALL.md](INSTALL.md)** guide.

---

## 📜 License

MIT License.
