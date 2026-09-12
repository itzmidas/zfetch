"""Custom widgets for zfetch TUI configurator."""

from rich.text import Text
from textual.widgets import Label, ListItem, Static


class MenuItem(ListItem):
    """List item representing a menu entry with an icon, title, and gray hint."""

    def __init__(self, key: str, title: str, description: str = "", icon: str = "") -> None:
        super().__init__()
        self.item_key = key
        self.item_title = title
        self.item_description = description
        self.item_icon = icon

    def compose(self):
        title_text = f"{self.item_icon}  {self.item_title}".strip() if self.item_icon else self.item_title
        yield Label(Text(title_text, style="bold"))
        if self.item_description:
            yield Label(Text(self.item_description, style="dim #888888"))


class LivePreviewWidget(Static):
    """Widget that renders the fetch output with real-time updates."""

    last_text: str = ""

    DEFAULT_CSS = """
    LivePreviewWidget {
        width: 100%;
        height: 100%;
        padding: 1 2;
        overflow-y: auto;
        overflow-x: auto;
    }
    """

    def update(self, renderable="") -> None:
        self.last_text = str(renderable)
        super().update(renderable)
