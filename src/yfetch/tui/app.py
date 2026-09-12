"""Interactive TUI configuration tool for yfetch built with Textual."""

import copy
import os
from pathlib import Path
from typing import Optional

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import Footer, Header, Label, ListItem, ListView, Static

from yfetch.ascii.manager import AsciiManager
from yfetch.config import Config, ConfigManager
from yfetch.modules.base import ModuleRegistry, ModuleResult
from yfetch.renderer.terminal import render_fetch
from yfetch.themes.definitions import THEMES, list_themes
from yfetch.themes.quick_styles import QUICK_STYLES, apply_quick_style_by_name
from yfetch.tui.screens.save_modal import SaveExitModal
from yfetch.tui.widgets import LivePreviewWidget, MenuItem


class YFetchApp(App):
    """Interactive TUI configurator application."""

    CSS = """
    Screen {
        background: #12151c;
        color: #e0e6ed;
    }

    #app-container {
        height: 1fr;
    }

    #left-panel {
        width: 48;
        border-right: solid #2a324b;
        background: #161b26;
        padding: 0 1;
    }

    #panel-title {
        text-align: center;
        padding: 1;
        background: #1f2637;
        color: #00d7ff;
        text-style: bold;
        margin-bottom: 1;
    }

    #menu-list {
        height: 1fr;
        background: transparent;
    }

    ListItem {
        padding: 1 1;
        margin: 0;
        background: transparent;
    }

    ListItem:hover {
        background: #252e42;
    }

    ListItem.-selected {
        background: #2b3956;
        color: #00d7ff;
    }

    #right-panel {
        width: 1fr;
        height: 100%;
        background: #12151c;
        padding: 0 1;
    }

    #preview-title {
        text-align: center;
        padding: 1;
        background: #1a202c;
        color: #a0aec0;
        text-style: bold;
    }

    #preview-box {
        height: 1fr;
        border: round #2a324b;
        background: #0d1117;
        margin: 1 0;
        overflow-y: auto;
        overflow-x: auto;
    }
    """

    BINDINGS = [
        Binding("escape", "handle_back", "Back / Exit", show=True),
        Binding("q", "handle_back", "Quit", show=False),
        Binding("s", "quick_save", "Save & Exit", show=True),
    ]

    def __init__(self, config_path: Optional[Path | str] = None) -> None:
        super().__init__()
        self.config_manager = ConfigManager(config_path)
        self.original_config = self.config_manager.load()
        # Working copy of config
        self.cfg: Config = copy.deepcopy(self.original_config)
        self.current_view = "main"
        self.ascii_manager = AsciiManager()
        self.all_arts = self.ascii_manager.list_all()
        # Pre-cache module results so preview updates in 0.1ms
        self.cached_module_results: dict[str, ModuleResult] = {}

    def on_mount(self) -> None:
        """Pre-cache module data and render initial preview."""
        self._precache_modules()
        self.update_preview()

    def _precache_modules(self) -> None:
        """Fetch all modules once for fast real-time preview updates."""
        for mod in ModuleRegistry.get_all():
            try:
                res = mod.fetch()
                if res:
                    self.cached_module_results[mod.id] = res
            except Exception:
                pass

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="app-container"):
            with Vertical(id="left-panel"):
                yield Label("⚡ yfetch Setup & Customization", id="panel-title")
                yield ListView(id="menu-list")
            with Vertical(id="right-panel"):
                yield Label("👁️ Live Preview", id="preview-title")
                with Container(id="preview-box"):
                    yield LivePreviewWidget(id="preview-content")
        yield Footer()

    def on_ready(self) -> None:
        self.show_main_menu()

    def update_preview(self) -> None:
        """Re-render preview pane instantly with current working config."""
        try:
            # Build list of active ModuleResults from cached results
            active_results = []
            for mod_id in self.cfg.modules.enabled:
                res = self.cached_module_results.get(mod_id)
                if res:
                    # Make shallow copy so label changes don't mutate cache
                    r_copy = copy.copy(res)
                    if mod_id in self.cfg.modules.custom_labels:
                        r_copy.label = self.cfg.modules.custom_labels[mod_id]
                    if not self.cfg.appearance.nerd_fonts:
                        r_copy.icon = ""
                    active_results.append(r_copy)

            rendered = render_fetch(config=self.cfg, modules=active_results)
            preview_widget = self.query_one("#preview-content", LivePreviewWidget)
            preview_widget.update(Text.from_ansi(rendered))
        except Exception as e:
            pass

    def show_main_menu(self) -> None:
        """Display top-level menu."""
        self.current_view = "main"
        title_label = self.query_one("#panel-title", Label)
        title_label.update("⚡ yfetch Setup & Customization")

        list_view = self.query_one("#menu-list", ListView)
        list_view.clear()
        list_view.extend([
            MenuItem("ascii", "ASCII Art", "Choose logo, custom artwork, or gradients", icon="🖼️"),
            MenuItem("modules", "Information", "Toggle system data blocks (Space to toggle)", icon="📋"),
            MenuItem("appearance", "Appearance", "Presets, separators, bold labels, spacing", icon="🎨"),
            MenuItem("colors", "Colors & Themes", "Nord, Dracula, Gruvbox, Tokyo Night, etc.", icon="🌈"),
            MenuItem("layout", "Layout", "Logo on left, right, top, or text-only", icon="📐"),
            MenuItem("styles", "Quick Styles", "One-click aesthetic presets (Cyberpunk, etc.)", icon="⚡"),
            MenuItem("advanced", "Advanced", "Reset configuration, debug logging, paths", icon="⚙️"),
            MenuItem("save", "Save & Exit", "Save changes to config.toml and exit", icon="💾"),
            MenuItem("discard", "Exit without saving", "Cancel modifications and exit", icon="✕"),
        ])
        list_view.focus()

    def show_ascii_menu(self) -> None:
        """Display ASCII art selection menu."""
        self.current_view = "ascii"
        title_label = self.query_one("#panel-title", Label)
        title_label.update("🖼️ ASCII Art Selection")

        list_view = self.query_one("#menu-list", ListView)
        list_view.clear()
        items = [MenuItem("back", "⬅ Back to Main Menu", "Return to main settings")]

        # List all available arts
        for art in self.all_arts:
            is_active = self.cfg.ascii.art.lower() == art.key.lower()
            badge = " [ACTIVE]" if is_active else ""
            items.append(MenuItem(f"art_{art.key}", f"{art.name}{badge}", art.description))

        # Color modes
        items.append(MenuItem("sep1", "─── ASCII Color Mode ───", ""))
        for mode, desc in [
            ("gradient", "Smooth RGB color gradient across lines"),
            ("theme", "Match primary accent of current theme"),
            ("single", "Monochrome single color"),
            ("raw", "Original uncolored text"),
        ]:
            active_badge = " [ACTIVE]" if self.cfg.ascii.color_mode.lower() == mode else ""
            items.append(MenuItem(f"mode_{mode}", f"Mode: {mode.capitalize()}{active_badge}", desc))

        list_view.extend(items)
        list_view.focus()

    def show_modules_menu(self) -> None:
        """Display information modules checklist."""
        self.current_view = "modules"
        title_label = self.query_one("#panel-title", Label)
        title_label.update("📋 Information Modules (Space to toggle)")

        list_view = self.query_one("#menu-list", ListView)
        list_view.clear()
        items = [MenuItem("back", "⬅ Back to Main Menu", "Return to main settings")]

        for mod in ModuleRegistry.get_all():
            is_enabled = mod.id in self.cfg.modules.enabled
            box = "☑" if is_enabled else "☐"
            icon = mod.icon if self.cfg.appearance.nerd_fonts else ""
            items.append(MenuItem(
                f"mod_{mod.id}",
                f"{box} {icon} {mod.title}".strip(),
                mod.description
            ))

        list_view.extend(items)
        list_view.focus()

    def show_appearance_menu(self) -> None:
        """Display appearance options."""
        self.current_view = "appearance"
        title_label = self.query_one("#panel-title", Label)
        title_label.update("🎨 Appearance Settings")

        list_view = self.query_one("#menu-list", ListView)
        list_view.clear()
        items = [
            MenuItem("back", "⬅ Back to Main Menu", "Return to main settings"),
            MenuItem("toggle_bold", f"Bold Labels: {'ON' if self.cfg.appearance.bold_labels else 'OFF'}", "Display info module keys in bold text"),
            MenuItem("toggle_nerd", f"Nerd Font Icons: {'ON' if self.cfg.appearance.nerd_fonts else 'OFF'}", "Show glyph icons next to labels"),
            MenuItem("toggle_dots", f"Color Dots: {'ON' if self.cfg.appearance.show_color_dots else 'OFF'}", "Display terminal color dot palette at bottom"),
            MenuItem("cycle_sep", f"Separator: '{self.cfg.appearance.separator}'", "Cycle through separators (❯, •, :, →, ⚡, |)"),
            MenuItem("cycle_spacing", f"Spacing: {self.cfg.appearance.spacing}", "Gap distance between logo and system info"),
        ]
        list_view.extend(items)
        list_view.focus()

    def show_colors_menu(self) -> None:
        """Display theme selector."""
        self.current_view = "colors"
        title_label = self.query_one("#panel-title", Label)
        title_label.update("🌈 Colors & Themes")

        list_view = self.query_one("#menu-list", ListView)
        list_view.clear()
        items = [MenuItem("back", "⬅ Back to Main Menu", "Return to main settings")]

        for th in list_themes():
            is_active = self.cfg.colors.theme.lower() == th.key.lower()
            badge = " [ACTIVE]" if is_active else ""
            items.append(MenuItem(f"theme_{th.key}", f"{th.name}{badge}", th.description))

        list_view.extend(items)
        list_view.focus()

    def show_layout_menu(self) -> None:
        """Display layout position options."""
        self.current_view = "layout"
        title_label = self.query_one("#panel-title", Label)
        title_label.update("📐 Layout Position")

        list_view = self.query_one("#menu-list", ListView)
        list_view.clear()
        items = [MenuItem("back", "⬅ Back to Main Menu", "Return to main settings")]

        for pos, desc in [
            ("left", "ASCII Art on left, information on right (Default)"),
            ("right", "Information on left, ASCII Art on right"),
            ("top", "ASCII Art on top, information below"),
            ("off", "Information only, disable ASCII Art"),
        ]:
            is_active = self.cfg.layout.ascii_position.lower() == pos
            badge = " [ACTIVE]" if is_active else ""
            items.append(MenuItem(f"pos_{pos}", f"{pos.capitalize()}{badge}", desc))

        list_view.extend(items)
        list_view.focus()

    def show_styles_menu(self) -> None:
        """Display Quick Styles presets."""
        self.current_view = "styles"
        title_label = self.query_one("#panel-title", Label)
        title_label.update("⚡ Quick Styles (1-Click Presets)")

        list_view = self.query_one("#menu-list", ListView)
        list_view.clear()
        items = [MenuItem("back", "⬅ Back to Main Menu", "Return to main settings")]

        for key, qs in QUICK_STYLES.items():
            items.append(MenuItem(f"style_{key}", qs.name, qs.description))

        list_view.extend(items)
        list_view.focus()

    def show_advanced_menu(self) -> None:
        """Display advanced configuration options."""
        self.current_view = "advanced"
        title_label = self.query_one("#panel-title", Label)
        title_label.update("⚙️ Advanced Settings")

        list_view = self.query_one("#menu-list", ListView)
        list_view.clear()
        items = [
            MenuItem("back", "⬅ Back to Main Menu", "Return to main settings"),
            MenuItem("toggle_debug", f"Debug Mode: {'ON' if self.cfg.general.debug else 'OFF'}", "Log detailed traces to ~/.config/yfetch/debug.log"),
            MenuItem("reset_config", "Reset to Defaults", "Restore all settings to factory default values"),
            MenuItem("path_info", f"Config File: {self.config_manager.config_path.name}", str(self.config_manager.config_path)),
        ]
        list_view.extend(items)
        list_view.focus()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle selection in active list view."""
        if not isinstance(event.item, MenuItem):
            return

        key = event.item.item_key
        if key == "back":
            self.show_main_menu()
            return

        if self.current_view == "main":
            if key == "ascii":
                self.show_ascii_menu()
            elif key == "modules":
                self.show_modules_menu()
            elif key == "appearance":
                self.show_appearance_menu()
            elif key == "colors":
                self.show_colors_menu()
            elif key == "layout":
                self.show_layout_menu()
            elif key == "styles":
                self.show_styles_menu()
            elif key == "advanced":
                self.show_advanced_menu()
            elif key == "save":
                self.action_quick_save()
            elif key == "discard":
                self.exit(result=0)

        elif self.current_view == "ascii":
            if key.startswith("art_"):
                self.cfg.ascii.art = key.replace("art_", "")
                self.update_preview()
                self.show_ascii_menu()
            elif key.startswith("mode_"):
                self.cfg.ascii.color_mode = key.replace("mode_", "")
                self.update_preview()
                self.show_ascii_menu()

        elif self.current_view == "modules":
            if key.startswith("mod_"):
                mod_id = key.replace("mod_", "")
                if mod_id in self.cfg.modules.enabled:
                    self.cfg.modules.enabled.remove(mod_id)
                else:
                    self.cfg.modules.enabled.append(mod_id)
                self.update_preview()
                cur_idx = self.query_one("#menu-list", ListView).index
                self.show_modules_menu()
                self.query_one("#menu-list", ListView).index = cur_idx

        elif self.current_view == "appearance":
            if key == "toggle_bold":
                self.cfg.appearance.bold_labels = not self.cfg.appearance.bold_labels
            elif key == "toggle_nerd":
                self.cfg.appearance.nerd_fonts = not self.cfg.appearance.nerd_fonts
            elif key == "toggle_dots":
                self.cfg.appearance.show_color_dots = not self.cfg.appearance.show_color_dots
            elif key == "cycle_sep":
                seps = ["❯", "•", ":", "→", "⚡", "|", "»"]
                cur_idx = seps.index(self.cfg.appearance.separator) if self.cfg.appearance.separator in seps else -1
                self.cfg.appearance.separator = seps[(cur_idx + 1) % len(seps)]
            elif key == "cycle_spacing":
                spacings = [2, 3, 4, 6, 8]
                cur_idx = spacings.index(self.cfg.appearance.spacing) if self.cfg.appearance.spacing in spacings else 1
                self.cfg.appearance.spacing = spacings[(cur_idx + 1) % len(spacings)]
            self.update_preview()
            self.show_appearance_menu()

        elif self.current_view == "colors":
            if key.startswith("theme_"):
                th_key = key.replace("theme_", "")
                self.cfg.colors.theme = th_key
                self.update_preview()
                self.show_colors_menu()

        elif self.current_view == "layout":
            if key.startswith("pos_"):
                self.cfg.layout.ascii_position = key.replace("pos_", "")
                self.update_preview()
                self.show_layout_menu()

        elif self.current_view == "styles":
            if key.startswith("style_"):
                st_key = key.replace("style_", "")
                apply_quick_style_by_name(self.cfg, st_key)
                self.update_preview()
                self.show_styles_menu()

        elif self.current_view == "advanced":
            if key == "toggle_debug":
                self.cfg.general.debug = not self.cfg.general.debug
                self.show_advanced_menu()
            elif key == "reset_config":
                self.cfg = Config()
                self.update_preview()
                self.show_advanced_menu()

    def key_space(self) -> None:
        """Handle Space key to toggle item."""
        if self.current_view == "modules":
            list_view = self.query_one("#menu-list", ListView)
            if list_view.highlighted_child and isinstance(list_view.highlighted_child, MenuItem):
                key = list_view.highlighted_child.item_key
                if key.startswith("mod_"):
                    mod_id = key.replace("mod_", "")
                    if mod_id in self.cfg.modules.enabled:
                        self.cfg.modules.enabled.remove(mod_id)
                    else:
                        self.cfg.modules.enabled.append(mod_id)
                    self.update_preview()
                    cur_idx = list_view.index
                    self.show_modules_menu()
                    list_view.index = cur_idx

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """Instantly update live preview as user navigates through themes or layouts."""
        if not isinstance(event.item, MenuItem):
            return
        key = event.item.item_key
        # Live preview on hover for themes
        if self.current_view == "colors" and key.startswith("theme_"):
            th_key = key.replace("theme_", "")
            temp_theme = self.cfg.colors.theme
            self.cfg.colors.theme = th_key
            self.update_preview()
            self.cfg.colors.theme = temp_theme  # Keep current until selected
        elif self.current_view == "ascii" and key.startswith("art_"):
            art_key = key.replace("art_", "")
            temp_art = self.cfg.ascii.art
            self.cfg.ascii.art = art_key
            self.update_preview()
            self.cfg.ascii.art = temp_art

    def action_handle_back(self) -> None:
        """Handle Esc or q: go up one menu level, or open save prompt if at root."""
        if self.current_view != "main":
            self.show_main_menu()
            self.update_preview()
        else:
            self._prompt_save_exit()

    def action_quick_save(self) -> None:
        """Save configuration immediately and exit."""
        self.config_manager.save(self.cfg)
        self.exit(result=0)

    def _prompt_save_exit(self) -> None:
        """Show save confirmation modal."""
        def _handle_modal_result(choice: Optional[str]) -> None:
            if choice == "save":
                self.config_manager.save(self.cfg)
                self.exit(result=0)
            elif choice == "apply":
                # Exit and print new fetch output to terminal
                self.exit(result="apply")
            elif choice == "discard":
                self.exit(result=0)

        self.push_screen(SaveExitModal(), _handle_modal_result)


def run_tui(config_path: Optional[Path | str] = None) -> int:
    """Launch the interactive TUI setup."""
    app = YFetchApp(config_path=config_path)
    result = app.run()

    if result == "apply":
        # Print applied output to terminal once
        print(render_fetch(config=app.cfg))

    return 0
