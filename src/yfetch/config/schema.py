"""Configuration schema and defaults for yfetch."""

from dataclasses import asdict, dataclass, field
from typing import Any


DEFAULT_ENABLED_MODULES = [
    "hostname",
    "os",
    "kernel",
    "uptime",
    "packages",
    "shell",
    "resolution",
    "de",
    "wm",
    "gtk_theme",
    "icon_theme",
    "terminal",
    "cpu",
    "gpu",
    "memory",
    "disk",
]


@dataclass
class AsciiConfig:
    """ASCII art options."""

    art: str = "arch"
    color_mode: str = "theme"  # "theme", "single", "gradient", "raw"
    custom_color: str = "cyan"
    gradient_colors: list[str] = field(default_factory=lambda: ["#1793d1", "#00d7ff"])


@dataclass
class ModulesConfig:
    """Module selection and customization."""

    enabled: list[str] = field(default_factory=lambda: list(DEFAULT_ENABLED_MODULES))
    custom_labels: dict[str, str] = field(default_factory=dict)


@dataclass
class AppearanceConfig:
    """Styling and appearance options."""

    preset: str = "classic"  # "classic", "compact", "minimal", "large"
    separator: str = "❯"
    bold_labels: bool = True
    spacing: int = 4
    padding_left: int = 0
    show_color_dots: bool = True
    nerd_fonts: bool = True


@dataclass
class ColorsConfig:
    """Theme and color configuration."""

    theme: str = "default"  # "default", "nord", "dracula", "gruvbox", "tokyo_night", "catppuccin", "monochrome", "cyberpunk", "custom"
    primary: str = "cyan"
    secondary: str = "blue"
    label_color: str = "cyan"
    value_color: str = "white"
    separator_color: str = "dim"


@dataclass
class LayoutConfig:
    """Layout placement options."""

    ascii_position: str = "left"  # "left", "right", "top", "off"


@dataclass
class GeneralConfig:
    """General and advanced options."""

    debug: bool = False
    log_file: str = ""


@dataclass
class Config:
    """Master configuration structure for yfetch."""

    ascii: AsciiConfig = field(default_factory=AsciiConfig)
    modules: ModulesConfig = field(default_factory=ModulesConfig)
    appearance: AppearanceConfig = field(default_factory=AppearanceConfig)
    colors: ColorsConfig = field(default_factory=ColorsConfig)
    layout: LayoutConfig = field(default_factory=LayoutConfig)
    general: GeneralConfig = field(default_factory=GeneralConfig)

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Config":
        """Build Config instance safely from nested dictionary, using defaults for missing fields."""
        cfg = cls()

        if not isinstance(data, dict):
            return cfg

        ascii_data = data.get("ascii")
        if isinstance(ascii_data, dict):
            if "art" in ascii_data:
                cfg.ascii.art = str(ascii_data["art"])
            if "color_mode" in ascii_data:
                cfg.ascii.color_mode = str(ascii_data["color_mode"])
            if "custom_color" in ascii_data:
                cfg.ascii.custom_color = str(ascii_data["custom_color"])
            if "gradient_colors" in ascii_data and isinstance(ascii_data["gradient_colors"], list):
                cfg.ascii.gradient_colors = [str(c) for c in ascii_data["gradient_colors"]]

        mod_data = data.get("modules")
        if isinstance(mod_data, dict):
            if "enabled" in mod_data and isinstance(mod_data["enabled"], list):
                cfg.modules.enabled = [str(m) for m in mod_data["enabled"]]
            if "custom_labels" in mod_data and isinstance(mod_data["custom_labels"], dict):
                cfg.modules.custom_labels = {str(k): str(v) for k, v in mod_data["custom_labels"].items()}

        app_data = data.get("appearance")
        if isinstance(app_data, dict):
            if "preset" in app_data:
                cfg.appearance.preset = str(app_data["preset"])
            if "separator" in app_data:
                cfg.appearance.separator = str(app_data["separator"])
            if "bold_labels" in app_data:
                cfg.appearance.bold_labels = bool(app_data["bold_labels"])
            if "spacing" in app_data and isinstance(app_data["spacing"], int):
                cfg.appearance.spacing = max(0, app_data["spacing"])
            if "padding_left" in app_data and isinstance(app_data["padding_left"], int):
                cfg.appearance.padding_left = max(0, app_data["padding_left"])
            if "show_color_dots" in app_data:
                cfg.appearance.show_color_dots = bool(app_data["show_color_dots"])
            if "nerd_fonts" in app_data:
                cfg.appearance.nerd_fonts = bool(app_data["nerd_fonts"])

        col_data = data.get("colors")
        if isinstance(col_data, dict):
            if "theme" in col_data:
                cfg.colors.theme = str(col_data["theme"])
            if "primary" in col_data:
                cfg.colors.primary = str(col_data["primary"])
            if "secondary" in col_data:
                cfg.colors.secondary = str(col_data["secondary"])
            if "label_color" in col_data:
                cfg.colors.label_color = str(col_data["label_color"])
            if "value_color" in col_data:
                cfg.colors.value_color = str(col_data["value_color"])
            if "separator_color" in col_data:
                cfg.colors.separator_color = str(col_data["separator_color"])

        lay_data = data.get("layout")
        if isinstance(lay_data, dict):
            if "ascii_position" in lay_data:
                cfg.layout.ascii_position = str(lay_data["ascii_position"])

        gen_data = data.get("general")
        if isinstance(gen_data, dict):
            if "debug" in gen_data:
                cfg.general.debug = bool(gen_data["debug"])
            if "log_file" in gen_data:
                cfg.general.log_file = str(gen_data["log_file"])

        return cfg
