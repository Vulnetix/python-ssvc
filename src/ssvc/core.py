"""
SSVC Core Library with Plugin Support

This module provides the core functionality for SSVC with a plugin-based architecture.
"""

import importlib
import pkgutil
from pathlib import Path
from typing import Dict, Any, Optional, Type
from abc import ABC, abstractmethod


class SSVCPlugin(ABC):
    """Abstract base class for SSVC plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Plugin description."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version."""
        pass

    @abstractmethod
    def create_decision(self, **kwargs) -> Any:
        """Create a decision instance for this plugin."""
        pass


class PluginRegistry:
    """Registry for managing SSVC plugins."""

    def __init__(self):
        self._plugins: Dict[str, SSVCPlugin] = {}
        self._auto_discover_plugins()

    def register(self, plugin: SSVCPlugin):
        """Register a plugin."""
        self._plugins[plugin.name.lower()] = plugin

    def get(self, name: str) -> Optional[SSVCPlugin]:
        """Get a plugin by name."""
        return self._plugins.get(name.lower())

    def list_plugins(self) -> Dict[str, SSVCPlugin]:
        """List all registered plugins."""
        return self._plugins.copy()

    def _auto_discover_plugins(self):
        """Auto-discover plugins from the plugins directory."""
        try:
            import ssvc.plugins

            plugins_path = Path(ssvc.plugins.__file__).parent

            for module_info in pkgutil.iter_modules([str(plugins_path)]):
                try:
                    module = importlib.import_module(f"ssvc.plugins.{module_info.name}")

                    # Look for plugin classes
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (
                            isinstance(attr, type)
                            and attr_name.startswith("Decision")
                            and hasattr(attr, "__init__")
                            and not attr_name.endswith("Level")
                            and not attr_name.endswith("Status")
                        ):
                            # Create a wrapper plugin
                            plugin = BuiltinPlugin(module_info.name, attr, module)
                            self.register(plugin)
                            break  # Only register the first Decision class found

                except ImportError:
                    # Skip modules that can't be imported
                    continue
        except ImportError:
            # No plugins directory found
            pass


class BuiltinPlugin(SSVCPlugin):
    """Wrapper for built-in plugin modules."""

    def __init__(self, name: str, decision_class: Type, module: Any):
        self._name = name
        self._decision_class = decision_class
        self._module = module

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return getattr(self._module, "__doc__", f"{self._name} SSVC plugin").strip()

    @property
    def version(self) -> str:
        return getattr(self._module, "__version__", "1.0.0")

    def create_decision(self, **kwargs):
        return self._decision_class(**kwargs)


# Global plugin registry
registry = PluginRegistry()


class Decision:
    """
    Universal SSVC Decision class that supports multiple methodologies via plugins.

    This class provides backward compatibility with the original API while supporting
    the new plugin-based architecture.
    """

    def __init__(self, methodology: str = "cisa", **kwargs):
        """
        Initialize a decision instance.

        Args:
            methodology: The methodology/plugin to use (default: 'cisa')
            **kwargs: Decision point values specific to the methodology
        """
        self.methodology = methodology.lower()
        self.plugin = registry.get(self.methodology)

        if not self.plugin:
            available = list(registry.list_plugins().keys())
            raise ValueError(
                f"Unknown methodology '{methodology}'. Available: {available}"
            )

        # Create the plugin-specific decision instance
        self._decision_instance = self.plugin.create_decision(**kwargs)

        # Expose the outcome if available
        if hasattr(self._decision_instance, "outcome"):
            self.outcome = self._decision_instance.outcome

    def evaluate(self):
        """Evaluate the decision and return the outcome."""
        if hasattr(self._decision_instance, "evaluate"):
            outcome = self._decision_instance.evaluate()
            self.outcome = outcome
            return outcome
        else:
            # For backward compatibility, return existing outcome
            return getattr(self._decision_instance, "outcome", None)

    def to_vector(self) -> str:
        """Generate SSVC vector string representation."""
        if hasattr(self._decision_instance, "to_vector"):
            return self._decision_instance.to_vector()
        else:
            raise NotImplementedError(
                f"Vector string generation not supported for methodology: {self.methodology}"
            )

    @classmethod
    def from_vector(cls, vector_string: str):
        """Parse SSVC vector string to create decision instance."""
        # Parse the methodology name from vector string
        import re

        match = re.match(r"^([A-Z_]+)v?\d*", vector_string)
        if not match:
            raise ValueError(f"Invalid vector string format: {vector_string}")

        # Extract methodology prefix for debugging if needed
        # methodology_prefix = match.group(1)

        # Find plugin by matching vector prefix
        for plugin_name, plugin in registry.list_plugins().items():
            decision_instance = plugin.create_decision()
            if hasattr(decision_instance, "from_vector"):
                try:
                    parsed_decision = decision_instance.from_vector(vector_string)
                    # Create a Decision wrapper that uses the parsed decision
                    decision = cls(plugin_name)
                    decision._decision_instance = parsed_decision
                    if hasattr(parsed_decision, "outcome"):
                        decision.outcome = parsed_decision.outcome
                    return decision
                except (ValueError, AttributeError):
                    # This plugin can't parse this vector string, try next
                    continue

        raise ValueError(
            f"No plugin found that can parse vector string: {vector_string}"
        )

    def __getattr__(self, name):
        """Delegate attribute access to the plugin-specific decision instance."""
        return getattr(self._decision_instance, name)


def list_methodologies() -> Dict[str, str]:
    """List available methodologies and their descriptions."""
    return {
        name: plugin.description for name, plugin in registry.list_plugins().items()
    }


def get_methodology_info(name: str) -> Optional[Dict[str, str]]:
    """Get information about a specific methodology."""
    plugin = registry.get(name)
    if plugin:
        return {
            "name": plugin.name,
            "description": plugin.description,
            "version": plugin.version,
        }
    return None


# Backward compatibility - expose original classes
# These will be deprecated in future versions
try:
    from ssvc.legacy import (
        ExploitationLevel,
        Automatable,
        TechnicalImpact,
        MissionWellbeingImpact,
        DecisionPriority,
        ActionCISA,
        OutcomeCISA,
        Methodology,
    )
except ImportError:
    # Legacy classes not available, define minimal versions for compatibility
    from enum import Enum

    class ExploitationLevel(Enum):
        NONE = "none"
        POC = "poc"
        ACTIVE = "active"

    class Automatable(Enum):
        YES = "yes"
        NO = "no"

    class TechnicalImpact(Enum):
        PARTIAL = "partial"
        TOTAL = "total"

    class MissionWellbeingImpact(Enum):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    class DecisionPriority(Enum):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"
        IMMEDIATE = "immediate"

    class ActionCISA(Enum):
        TRACK = "Track"
        TRACK_STAR = "Track*"
        ATTEND = "Attend"
        ACT = "Act"

    class Methodology(Enum):
        CISA = "CISA"
        FIRST = "FIRST"

    class OutcomeCISA:
        def __init__(self, action: ActionCISA):
            priority_map = {
                ActionCISA.TRACK: DecisionPriority.LOW,
                ActionCISA.TRACK_STAR: DecisionPriority.MEDIUM,
                ActionCISA.ATTEND: DecisionPriority.MEDIUM,
                ActionCISA.ACT: DecisionPriority.IMMEDIATE,
            }
            self.priority = priority_map[action]
            self.action = action
