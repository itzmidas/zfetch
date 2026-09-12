"""Unit and integration tests for interactive TUI configurator."""

import asyncio
from textual.widgets import ListView

from yfetch.config import Config, ConfigManager
from yfetch.tui.app import YFetchApp
from yfetch.tui.widgets import LivePreviewWidget, MenuItem


def test_tui_initialization():
    async def _test():
        app = YFetchApp()
        async with app.run_test() as pilot:
            assert app.current_view == "main"
            list_view = app.query_one("#menu-list", ListView)
            assert len(list_view.children) >= 8

            preview = app.query_one("#preview-content", LivePreviewWidget)
            assert preview is not None
            assert "User" in preview.last_text

    asyncio.run(_test())


def test_tui_module_toggle_with_space():
    async def _test():
        app = YFetchApp()
        async with app.run_test() as pilot:
            app.show_modules_menu()
            assert app.current_view == "modules"

            list_view = app.query_one("#menu-list", ListView)
            # Select first module (index 1, as index 0 is 'back')
            list_view.index = 1
            await pilot.pause()

            mod_id = list_view.highlighted_child.item_key.replace("mod_", "")
            initially_enabled = mod_id in app.cfg.modules.enabled

            # Press space to toggle
            await pilot.press("space")
            await pilot.pause()

            assert (mod_id in app.cfg.modules.enabled) is not initially_enabled

            # Press space again to toggle back
            await pilot.press("space")
            await pilot.pause()

            assert (mod_id in app.cfg.modules.enabled) is initially_enabled

    asyncio.run(_test())


def test_tui_appearance_and_styles(tmp_path):
    async def _test():
        conf_path = tmp_path / "tui_test_config.toml"
        app = YFetchApp(config_path=conf_path)
        async with app.run_test() as pilot:
            # Switch to styles menu
            app.show_styles_menu()
            assert app.current_view == "styles"

            # Select and apply Nord style
            list_view = app.query_one("#menu-list", ListView)
            nord_item = [it for it in list_view.children if getattr(it, "item_key", "") == "style_nord"][0]
            class DummyEvent:
                pass
            ev = DummyEvent()
            ev.item = nord_item
            app.on_list_view_selected(ev)

            assert app.cfg.colors.theme == "nord"

            # Quick save
            app.action_quick_save()
            await pilot.pause()

        # Verify config was saved to disk
        mgr = ConfigManager(conf_path)
        saved_cfg = mgr.load(auto_create=False)
        assert saved_cfg.colors.theme == "nord"

    asyncio.run(_test())
