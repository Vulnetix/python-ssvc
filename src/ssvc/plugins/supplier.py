"""
Supplier Decision Model Plugin

CERT/CC Supplier Decision Model for prioritizing patch creation
Generated from YAML configuration.
"""

from enum import Enum
from typing import Dict, Any, Optional


class ExploitationStatus(Enum):
    NONE = "none"
    POC = "poc"
    ACTIVE = "active"

class UtilityLevel(Enum):
    LABORIOUS = "laborious"
    EFFICIENT = "efficient"
    SUPER_EFFECTIVE = "super_effective"

class TechnicalImpactLevel(Enum):
    PARTIAL = "partial"
    TOTAL = "total"

class PublicSafetyImpactLevel(Enum):
    MINIMAL = "minimal"
    SIGNIFICANT = "significant"

class ActionType(Enum):
    DEFER = "defer"
    SCHEDULED = "scheduled"
    OUT_OF_CYCLE = "out_of_cycle"
    IMMEDIATE = "immediate"

class DecisionPriorityLevel(Enum):
    DEFER = "defer"
    SCHEDULED = "scheduled"
    OUT_OF_CYCLE = "out_of_cycle"
    IMMEDIATE = "immediate"


priority_map = {
    ActionType.DEFER: DecisionPriorityLevel.DEFER,
    ActionType.SCHEDULED: DecisionPriorityLevel.SCHEDULED,
    ActionType.OUT_OF_CYCLE: DecisionPriorityLevel.OUT_OF_CYCLE,
    ActionType.IMMEDIATE: DecisionPriorityLevel.IMMEDIATE
}


class OutcomeSupplier:
    def __init__(self, action):
        self.priority = priority_map[action]
        self.action = action


class DecisionSupplier:
    def __init__(self, exploitation: ExploitationStatus | str = None, utility: UtilityLevel | str = None, technical_impact: TechnicalImpactLevel | str = None, public_safety_impact: PublicSafetyImpactLevel | str = None):
        if isinstance(exploitation, str):
            exploitation = ExploitationStatus(exploitation)
        if isinstance(utility, str):
            utility = UtilityLevel(utility)
        if isinstance(technical_impact, str):
            technical_impact = TechnicalImpactLevel(technical_impact)
        if isinstance(public_safety_impact, str):
            public_safety_impact = PublicSafetyImpactLevel(public_safety_impact)
        
        self.exploitation = exploitation
        self.utility = utility
        self.technical_impact = technical_impact
        self.public_safety_impact = public_safety_impact
        
        # Always try to evaluate if we have the minimum required parameters
        if all([self.exploitation is not None, self.utility is not None, self.technical_impact is not None, self.public_safety_impact is not None]):
            self.outcome = self.evaluate()

    def evaluate(self) -> OutcomeSupplier:
        action = self._traverse_tree()
        self.outcome = OutcomeSupplier(action)
        return self.outcome

    def _traverse_tree(self):
        """Traverse the decision tree to determine the outcome."""
        if self.exploitation == ExploitationStatus.NONE:
            if self.utility == UtilityLevel.LABORIOUS:
                if self.technical_impact == TechnicalImpactLevel.PARTIAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.DEFER
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.DEFER
                elif self.technical_impact == TechnicalImpactLevel.TOTAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.DEFER
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.DEFER
            elif self.utility == UtilityLevel.EFFICIENT:
                if self.technical_impact == TechnicalImpactLevel.PARTIAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.DEFER
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.SCHEDULED
                elif self.technical_impact == TechnicalImpactLevel.TOTAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.SCHEDULED
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.SCHEDULED
            elif self.utility == UtilityLevel.SUPER_EFFECTIVE:
                if self.technical_impact == TechnicalImpactLevel.PARTIAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.SCHEDULED
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.OUT_OF_CYCLE
                elif self.technical_impact == TechnicalImpactLevel.TOTAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.OUT_OF_CYCLE
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.IMMEDIATE
        elif self.exploitation == ExploitationStatus.POC:
            if self.utility == UtilityLevel.LABORIOUS:
                if self.technical_impact == TechnicalImpactLevel.PARTIAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.DEFER
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.DEFER
                elif self.technical_impact == TechnicalImpactLevel.TOTAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.DEFER
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.SCHEDULED
            elif self.utility == UtilityLevel.EFFICIENT:
                if self.technical_impact == TechnicalImpactLevel.PARTIAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.DEFER
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.SCHEDULED
                elif self.technical_impact == TechnicalImpactLevel.TOTAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.SCHEDULED
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.OUT_OF_CYCLE
            elif self.utility == UtilityLevel.SUPER_EFFECTIVE:
                if self.technical_impact == TechnicalImpactLevel.PARTIAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.SCHEDULED
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.OUT_OF_CYCLE
                elif self.technical_impact == TechnicalImpactLevel.TOTAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.OUT_OF_CYCLE
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.IMMEDIATE
        elif self.exploitation == ExploitationStatus.ACTIVE:
            if self.utility == UtilityLevel.LABORIOUS:
                if self.technical_impact == TechnicalImpactLevel.PARTIAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.DEFER
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.SCHEDULED
                elif self.technical_impact == TechnicalImpactLevel.TOTAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.SCHEDULED
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.SCHEDULED
            elif self.utility == UtilityLevel.EFFICIENT:
                if self.technical_impact == TechnicalImpactLevel.PARTIAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.SCHEDULED
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.OUT_OF_CYCLE
                elif self.technical_impact == TechnicalImpactLevel.TOTAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.OUT_OF_CYCLE
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.IMMEDIATE
            elif self.utility == UtilityLevel.SUPER_EFFECTIVE:
                if self.technical_impact == TechnicalImpactLevel.PARTIAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.OUT_OF_CYCLE
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.IMMEDIATE
                elif self.technical_impact == TechnicalImpactLevel.TOTAL:
                    if self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                        return ActionType.IMMEDIATE
                    elif self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                        return ActionType.IMMEDIATE
        
        # Default action for unmapped paths
        return ActionType.DEFER