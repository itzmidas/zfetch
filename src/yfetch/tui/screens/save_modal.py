"""Save & exit confirmation modal dialog."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, ListItem, ListView
from rich.text import Text

from yfetch.tui.widgets import MenuItem


class SaveExitModal(ModalScreen[str]):
    """Modal dialog asking user whether to save changes upon exit."""

    DEFAULT_CSS = """
    SaveExitModal {
        align: center middle;
    }

    #save-dialog {
        width: 50;
        height: auto;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }

    #save-title {
        text-align: center;
        margin-bottom: 1;
        font-weight: bold;
    }

    #save-list {
        height: auto;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="save-dialog"):
            yield Label("Save your yfetch configuration?", id="save-title")
            with ListView(id="save-list"):
                yield MenuItem("save", "💾 Save and exit", "Write changes to ~/.config/yfetch/config.toml")
                yield MenuItem("apply", "⚡ Apply once", "Apply changes for this session without saving")
                yield MenuItem("discard", "✕ Exit without saving", "Discard all changes and exit")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if isinstance(event.item, MenuItem):
            self.dismiss(event.item.item_key)

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.dismiss("discard")
