"""
Deployer Decision Model Plugin

CERT/CC Deployer Decision Model for prioritizing patch deployment
Generated from YAML configuration.
"""

from enum import Enum
from typing import Dict, Any, Optional


class ExploitationStatus(Enum):
    NONE = "none"
    POC = "poc"
    ACTIVE = "active"

class SystemExposureLevel(Enum):
    SMALL = "small"
    CONTROLLED = "controlled"
    OPEN = "open"

class UtilityLevel(Enum):
    LABORIOUS = "laborious"
    EFFICIENT = "efficient"
    SUPER_EFFECTIVE = "super_effective"

class HumanImpactLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

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


class OutcomeDeployer:
    def __init__(self, action):
        self.priority = priority_map[action]
        self.action = action


class DecisionDeployer:
    def __init__(self, exploitation: ExploitationStatus | str = None, system_exposure: SystemExposureLevel | str = None, utility: UtilityLevel | str = None, human_impact: HumanImpactLevel | str = None):
        if isinstance(exploitation, str):
            exploitation = ExploitationStatus(exploitation)
        if isinstance(system_exposure, str):
            system_exposure = SystemExposureLevel(system_exposure)
        if isinstance(utility, str):
            utility = UtilityLevel(utility)
        if isinstance(human_impact, str):
            human_impact = HumanImpactLevel(human_impact)
        
        self.exploitation = exploitation
        self.system_exposure = system_exposure
        self.utility = utility
        self.human_impact = human_impact
        
        # Always try to evaluate if we have the minimum required parameters
        if all([self.exploitation is not None, self.system_exposure is not None, self.utility is not None, self.human_impact is not None]):
            self.outcome = self.evaluate()

    def evaluate(self) -> OutcomeDeployer:
        action = self._traverse_tree()
        self.outcome = OutcomeDeployer(action)
        return self.outcome

    def _traverse_tree(self):
        """Traverse the decision tree to determine the outcome."""
        if self.exploitation == ExploitationStatus.NONE:
            if self.system_exposure == SystemExposureLevel.SMALL:
                if self.utility == UtilityLevel.LABORIOUS:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.DEFER
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.DEFER
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.DEFER
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.SCHEDULED
                elif self.utility == UtilityLevel.EFFICIENT:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.DEFER
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.DEFER
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.SCHEDULED
                elif self.utility == UtilityLevel.SUPER_EFFECTIVE:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.DEFER
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.OUT_OF_CYCLE
            elif self.system_exposure == SystemExposureLevel.CONTROLLED:
                if self.utility == UtilityLevel.LABORIOUS:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.DEFER
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.DEFER
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.SCHEDULED
                elif self.utility == UtilityLevel.EFFICIENT:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.DEFER
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.OUT_OF_CYCLE
                elif self.utility == UtilityLevel.SUPER_EFFECTIVE:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.OUT_OF_CYCLE
            elif self.system_exposure == SystemExposureLevel.OPEN:
                if self.utility == UtilityLevel.LABORIOUS:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.DEFER
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.OUT_OF_CYCLE
                elif self.utility == UtilityLevel.EFFICIENT:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.OUT_OF_CYCLE
                elif self.utility == UtilityLevel.SUPER_EFFECTIVE:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.IMMEDIATE
        elif self.exploitation == ExploitationStatus.POC:
            if self.system_exposure == SystemExposureLevel.SMALL:
                if self.utility == UtilityLevel.LABORIOUS:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.DEFER
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.DEFER
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.SCHEDULED
                elif self.utility == UtilityLevel.EFFICIENT:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.DEFER
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.OUT_OF_CYCLE
                elif self.utility == UtilityLevel.SUPER_EFFECTIVE:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.OUT_OF_CYCLE
            elif self.system_exposure == SystemExposureLevel.CONTROLLED:
                if self.utility == UtilityLevel.LABORIOUS:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.DEFER
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.OUT_OF_CYCLE
                elif self.utility == UtilityLevel.EFFICIENT:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.OUT_OF_CYCLE
                elif self.utility == UtilityLevel.SUPER_EFFECTIVE:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.IMMEDIATE
            elif self.system_exposure == SystemExposureLevel.OPEN:
                if self.utility == UtilityLevel.LABORIOUS:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.OUT_OF_CYCLE
                elif self.utility == UtilityLevel.EFFICIENT:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.IMMEDIATE
                elif self.utility == UtilityLevel.SUPER_EFFECTIVE:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.IMMEDIATE
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.IMMEDIATE
        elif self.exploitation == ExploitationStatus.ACTIVE:
            if self.system_exposure == SystemExposureLevel.SMALL:
                if self.utility == UtilityLevel.LABORIOUS:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.OUT_OF_CYCLE
                elif self.utility == UtilityLevel.EFFICIENT:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.OUT_OF_CYCLE
                elif self.utility == UtilityLevel.SUPER_EFFECTIVE:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.IMMEDIATE
            elif self.system_exposure == SystemExposureLevel.CONTROLLED:
                if self.utility == UtilityLevel.LABORIOUS:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.OUT_OF_CYCLE
                elif self.utility == UtilityLevel.EFFICIENT:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.IMMEDIATE
                elif self.utility == UtilityLevel.SUPER_EFFECTIVE:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.IMMEDIATE
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.IMMEDIATE
            elif self.system_exposure == SystemExposureLevel.OPEN:
                if self.utility == UtilityLevel.LABORIOUS:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.SCHEDULED
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.IMMEDIATE
                elif self.utility == UtilityLevel.EFFICIENT:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.IMMEDIATE
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.IMMEDIATE
                elif self.utility == UtilityLevel.SUPER_EFFECTIVE:
                    if self.human_impact == HumanImpactLevel.LOW:
                        return ActionType.OUT_OF_CYCLE
                    elif self.human_impact == HumanImpactLevel.MEDIUM:
                        return ActionType.IMMEDIATE
                    elif self.human_impact == HumanImpactLevel.HIGH:
                        return ActionType.IMMEDIATE
                    elif self.human_impact == HumanImpactLevel.VERY_HIGH:
                        return ActionType.IMMEDIATE
        
        # Default action for unmapped paths
        return ActionType.DEFER