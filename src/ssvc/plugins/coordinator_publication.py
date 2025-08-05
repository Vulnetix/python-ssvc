"""
Coordinator Publication Decision Model Plugin

CERT/CC Coordinator Publication Decision Model for determining vulnerability disclosure
Generated from YAML configuration.
"""

from enum import Enum
from typing import Dict, Any, Optional


class SupplierInvolvement(Enum):
    FIX_READY = "fix_ready"
    COOPERATIVE = "cooperative"
    UNCOOPERATIVE_UNRESPONSIVE = "uncooperative_unresponsive"

class ExploitationStatus(Enum):
    NONE = "none"
    PUBLIC_POC = "public_poc"
    ACTIVE = "active"

class PublicValueAdded(Enum):
    LIMITED = "limited"
    AMPLIATIVE = "ampliative"
    PRECEDENCE = "precedence"

class ActionType(Enum):
    PUBLISH = "publish"
    DO_NOT_PUBLISH = "do_not_publish"

class DecisionPriorityLevel(Enum):
    PUBLISH = "publish"
    DO_NOT_PUBLISH = "do_not_publish"


priority_map = {
    ActionType.PUBLISH: DecisionPriorityLevel.PUBLISH,
    ActionType.DO_NOT_PUBLISH: DecisionPriorityLevel.DO_NOT_PUBLISH
}


class OutcomeCoordinatorPublication:
    def __init__(self, action):
        self.priority = priority_map[action]
        self.action = action


class DecisionCoordinatorPublication:
    def __init__(self, supplier_involvement: SupplierInvolvement | str = None, exploitation: ExploitationStatus | str = None, public_value_added: PublicValueAdded | str = None):
        if isinstance(supplier_involvement, str):
            supplier_involvement = SupplierInvolvement(supplier_involvement)
        if isinstance(exploitation, str):
            exploitation = ExploitationStatus(exploitation)
        if isinstance(public_value_added, str):
            public_value_added = PublicValueAdded(public_value_added)
        
        self.supplier_involvement = supplier_involvement
        self.exploitation = exploitation
        self.public_value_added = public_value_added
        
        # Always try to evaluate if we have the minimum required parameters
        if all([self.supplier_involvement is not None, self.exploitation is not None, self.public_value_added is not None]):
            self.outcome = self.evaluate()

    def evaluate(self) -> OutcomeCoordinatorPublication:
        action = self._traverse_tree()
        self.outcome = OutcomeCoordinatorPublication(action)
        return self.outcome

    def _traverse_tree(self):
        """Traverse the decision tree to determine the outcome."""
        if self.supplier_involvement == SupplierInvolvement.FIX_READY:
            if self.exploitation == ExploitationStatus.NONE:
                if self.public_value_added == PublicValueAdded.LIMITED:
                    return ActionType.DO_NOT_PUBLISH
                elif self.public_value_added == PublicValueAdded.AMPLIATIVE:
                    return ActionType.DO_NOT_PUBLISH
                elif self.public_value_added == PublicValueAdded.PRECEDENCE:
                    return ActionType.PUBLISH
            elif self.exploitation == ExploitationStatus.PUBLIC_POC:
                if self.public_value_added == PublicValueAdded.LIMITED:
                    return ActionType.DO_NOT_PUBLISH
                elif self.public_value_added == PublicValueAdded.AMPLIATIVE:
                    return ActionType.PUBLISH
                elif self.public_value_added == PublicValueAdded.PRECEDENCE:
                    return ActionType.PUBLISH
            elif self.exploitation == ExploitationStatus.ACTIVE:
                if self.public_value_added == PublicValueAdded.LIMITED:
                    return ActionType.PUBLISH
                elif self.public_value_added == PublicValueAdded.AMPLIATIVE:
                    return ActionType.PUBLISH
                elif self.public_value_added == PublicValueAdded.PRECEDENCE:
                    return ActionType.PUBLISH
        elif self.supplier_involvement == SupplierInvolvement.COOPERATIVE:
            if self.exploitation == ExploitationStatus.NONE:
                if self.public_value_added == PublicValueAdded.LIMITED:
                    return ActionType.DO_NOT_PUBLISH
                elif self.public_value_added == PublicValueAdded.AMPLIATIVE:
                    return ActionType.DO_NOT_PUBLISH
                elif self.public_value_added == PublicValueAdded.PRECEDENCE:
                    return ActionType.PUBLISH
            elif self.exploitation == ExploitationStatus.PUBLIC_POC:
                if self.public_value_added == PublicValueAdded.LIMITED:
                    return ActionType.DO_NOT_PUBLISH
                elif self.public_value_added == PublicValueAdded.AMPLIATIVE:
                    return ActionType.PUBLISH
                elif self.public_value_added == PublicValueAdded.PRECEDENCE:
                    return ActionType.PUBLISH
            elif self.exploitation == ExploitationStatus.ACTIVE:
                if self.public_value_added == PublicValueAdded.LIMITED:
                    return ActionType.PUBLISH
                elif self.public_value_added == PublicValueAdded.AMPLIATIVE:
                    return ActionType.PUBLISH
                elif self.public_value_added == PublicValueAdded.PRECEDENCE:
                    return ActionType.PUBLISH
        elif self.supplier_involvement == SupplierInvolvement.UNCOOPERATIVE_UNRESPONSIVE:
            if self.exploitation == ExploitationStatus.NONE:
                if self.public_value_added == PublicValueAdded.LIMITED:
                    return ActionType.PUBLISH
                elif self.public_value_added == PublicValueAdded.AMPLIATIVE:
                    return ActionType.PUBLISH
                elif self.public_value_added == PublicValueAdded.PRECEDENCE:
                    return ActionType.PUBLISH
            elif self.exploitation == ExploitationStatus.PUBLIC_POC:
                if self.public_value_added == PublicValueAdded.LIMITED:
                    return ActionType.PUBLISH
                elif self.public_value_added == PublicValueAdded.AMPLIATIVE:
                    return ActionType.PUBLISH
                elif self.public_value_added == PublicValueAdded.PRECEDENCE:
                    return ActionType.PUBLISH
            elif self.exploitation == ExploitationStatus.ACTIVE:
                if self.public_value_added == PublicValueAdded.LIMITED:
                    return ActionType.PUBLISH
                elif self.public_value_added == PublicValueAdded.AMPLIATIVE:
                    return ActionType.PUBLISH
                elif self.public_value_added == PublicValueAdded.PRECEDENCE:
                    return ActionType.PUBLISH
        
        # Default action for unmapped paths
        return ActionType.DO_NOT_PUBLISH