"""
SSVC: Stakeholder-Specific Vulnerability Categorization

A Python implementation of the SSVC framework with plugin support for different methodologies.
"""

# Import the new core functionality
from .core import Decision, list_methodologies, get_methodology_info

# Import legacy classes for backward compatibility (with deprecation warnings)
from .legacy import (
    ExploitationLevel,
    Automatable,
    TechnicalImpact,
    MissionWellbeingImpact,
    DecisionPriority,
    ActionCISA,
    OutcomeCISA,
    Methodology,
    LegacyDecision,
)

# For backward compatibility, expose the old Decision class as well
# Users should migrate to the new Decision class
__all__ = [
    # New API
    "Decision",
    "list_methodologies",
    "get_methodology_info",
    # Legacy API (deprecated)
    "ExploitationLevel",
    "Automatable",
    "TechnicalImpact",
    "MissionWellbeingImpact",
    "DecisionPriority",
    "ActionCISA",
    "OutcomeCISA",
    "Methodology",
    "LegacyDecision",
]
