"""
CISA Plugin

CISA Stakeholder-Specific Vulnerability Categorization
Generated from YAML configuration.
"""

from enum import Enum
from typing import Dict, Any, Optional


class ExploitationStatus(Enum):
    NONE = "none"
    POC = "poc"
    ACTIVE = "active"

class AutomatableStatus(Enum):
    YES = "yes"
    NO = "no"

class TechnicalImpactLevel(Enum):
    PARTIAL = "partial"
    TOTAL = "total"

class MissionWellbeingImpactLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class DecisionPriorityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    IMMEDIATE = "immediate"

class ActionType(Enum):
    TRACK = "track"
    TRACK_STAR = "track_star"
    ATTEND = "attend"
    ACT = "act"


priority_map = {
    ActionType.TRACK: DecisionPriorityLevel.LOW,
    ActionType.TRACK_STAR: DecisionPriorityLevel.MEDIUM,
    ActionType.ATTEND: DecisionPriorityLevel.MEDIUM,
    ActionType.ACT: DecisionPriorityLevel.IMMEDIATE
}


class OutcomeCisa:
    def __init__(self, action):
        self.priority = priority_map[action]
        self.action = action


class DecisionCisa:
    def __init__(self, exploitation: ExploitationStatus | str = None, automatable: AutomatableStatus | str = None, technical_impact: TechnicalImpactLevel | str = None, mission_wellbeing_impact: MissionWellbeingImpactLevel | str = None):
        if isinstance(exploitation, str):
            exploitation = ExploitationStatus(exploitation)
        if isinstance(automatable, str):
            automatable = AutomatableStatus(automatable)
        if isinstance(technical_impact, str):
            technical_impact = TechnicalImpactLevel(technical_impact)
        if isinstance(mission_wellbeing_impact, str):
            mission_wellbeing_impact = MissionWellbeingImpactLevel(mission_wellbeing_impact)
        
        self.exploitation = exploitation
        self.automatable = automatable
        self.technical_impact = technical_impact
        self.mission_wellbeing_impact = mission_wellbeing_impact
        
        # Always try to evaluate if we have the minimum required parameters
        if all([self.exploitation is not None, self.automatable is not None, self.technical_impact is not None, self.mission_wellbeing_impact is not None]):
            self.outcome = self.evaluate()

    def evaluate(self) -> OutcomeCisa:
        action = self._traverse_tree()
        self.outcome = OutcomeCisa(action)
        return self.outcome

    def _traverse_tree(self):
        """Traverse the decision tree to determine the outcome."""
        if self.exploitation == ExploitationStatus.NONE:
            if self.automatable == AutomatableStatus.YES:
                if self.technical_impact == TechnicalImpactLevel.TOTAL:
                    if self.mission_wellbeing_impact == MissionWellbeingImpactLevel.HIGH:
                        return ActionType.ATTEND
            elif self.automatable == AutomatableStatus.NO:
                if self.technical_impact == TechnicalImpactLevel.TOTAL:
                    if self.mission_wellbeing_impact == MissionWellbeingImpactLevel.HIGH:
                        return ActionType.TRACK_STAR
        elif self.exploitation == ExploitationStatus.POC:
            if self.automatable == AutomatableStatus.YES:
                if self.technical_impact == TechnicalImpactLevel.TOTAL:
                    if self.mission_wellbeing_impact == MissionWellbeingImpactLevel.MEDIUM:
                        return ActionType.TRACK_STAR
                    elif self.mission_wellbeing_impact == MissionWellbeingImpactLevel.HIGH:
                        return ActionType.ATTEND
                elif self.technical_impact == TechnicalImpactLevel.PARTIAL:
                    if self.mission_wellbeing_impact == MissionWellbeingImpactLevel.HIGH:
                        return ActionType.ATTEND
            elif self.automatable == AutomatableStatus.NO:
                if self.technical_impact == TechnicalImpactLevel.PARTIAL:
                    if self.mission_wellbeing_impact == MissionWellbeingImpactLevel.HIGH:
                        return ActionType.TRACK_STAR
                elif self.technical_impact == TechnicalImpactLevel.TOTAL:
                    if self.mission_wellbeing_impact == MissionWellbeingImpactLevel.MEDIUM:
                        return ActionType.TRACK_STAR
                    elif self.mission_wellbeing_impact == MissionWellbeingImpactLevel.HIGH:
                        return ActionType.ATTEND
        elif self.exploitation == ExploitationStatus.ACTIVE:
            if self.automatable == AutomatableStatus.YES:
                if self.technical_impact == TechnicalImpactLevel.PARTIAL:
                    if self.mission_wellbeing_impact == MissionWellbeingImpactLevel.LOW:
                        return ActionType.ATTEND
                    elif self.mission_wellbeing_impact == MissionWellbeingImpactLevel.MEDIUM:
                        return ActionType.ATTEND
                    elif self.mission_wellbeing_impact == MissionWellbeingImpactLevel.HIGH:
                        return ActionType.ACT
                elif self.technical_impact == TechnicalImpactLevel.TOTAL:
                    if self.mission_wellbeing_impact == MissionWellbeingImpactLevel.LOW:
                        return ActionType.ATTEND
                    elif self.mission_wellbeing_impact == MissionWellbeingImpactLevel.MEDIUM:
                        return ActionType.ACT
                    elif self.mission_wellbeing_impact == MissionWellbeingImpactLevel.HIGH:
                        return ActionType.ACT
            elif self.automatable == AutomatableStatus.NO:
                if self.technical_impact == TechnicalImpactLevel.PARTIAL:
                    if self.mission_wellbeing_impact == MissionWellbeingImpactLevel.HIGH:
                        return ActionType.ATTEND
                elif self.technical_impact == TechnicalImpactLevel.TOTAL:
                    if self.mission_wellbeing_impact == MissionWellbeingImpactLevel.MEDIUM:
                        return ActionType.ATTEND
                    elif self.mission_wellbeing_impact == MissionWellbeingImpactLevel.HIGH:
                        return ActionType.ACT
        
        # Default action for unmapped paths
        return ActionType.TRACK