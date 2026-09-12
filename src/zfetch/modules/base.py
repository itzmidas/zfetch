"""Base classes and registry for zfetch information modules."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Optional, Type


@dataclass
class ModuleResult:
    """Represents the rendered result of an information module."""

    module_id: str
    label: str
    value: str
    icon: str = ""
    extra: Optional[dict] = None

    def __str__(self) -> str:
        return f"{self.label}: {self.value}"


class BaseModule(ABC):
    """Abstract base class for all system information modules."""

    id: str = ""
    title: str = ""
    description: str = ""
    icon: str = ""
    default_enabled: bool = True
    category: str = "general"

    @abstractmethod
    def fetch(self) -> Optional[ModuleResult]:
        """Fetch system information and return a ModuleResult, or None if unavailable.

        Must never raise exceptions; all errors should be caught and handled gracefully.
        """
        pass


class ModuleRegistry:
    """Registry that manages all available and active information modules."""

    _modules: dict[str, Type[BaseModule]] = {}
    _instances: dict[str, BaseModule] = {}

    @classmethod
    def register(cls, module_cls: Type[BaseModule]) -> Type[BaseModule]:
        """Register a module class in the registry."""
        if not module_cls.id:
            raise ValueError(f"Module class {module_cls.__name__} must define a non-empty 'id'.")
        cls._modules[module_cls.id] = module_cls
        return module_cls

    @classmethod
    def get(cls, module_id: str) -> Optional[BaseModule]:
        """Get an instance of a registered module by its ID."""
        if module_id not in cls._instances:
            module_cls = cls._modules.get(module_id)
            if module_cls:
                cls._instances[module_id] = module_cls()
        return cls._instances.get(module_id)

    @classmethod
    def get_all(cls) -> list[BaseModule]:
        """Return instances of all registered modules in order of registration."""
        for mod_id, mod_cls in cls._modules.items():
            if mod_id not in cls._instances:
                cls._instances[mod_id] = mod_cls()
        return list(cls._instances.values())

    @classmethod
    def get_module_ids(cls) -> list[str]:
        """Return list of all registered module IDs."""
        return list(cls._modules.keys())

    @classmethod
    def clear(cls) -> None:
        """Clear registry (used for tests)."""
        cls._modules.clear()
        cls._instances.clear()


def register_module(cls: Type[BaseModule]) -> Type[BaseModule]:
    """Decorator to register a module class."""
    return ModuleRegistry.register(cls)
