"""
Coordinator Triage Plugin

CERT/CC Coordinator Triage Decision Model
Generated from YAML configuration.
"""

from enum import Enum
from typing import Dict, Any, Optional


class ReportPublicStatus(Enum):
    YES = "yes"
    NO = "no"

class SupplierContactedStatus(Enum):
    YES = "yes"
    NO = "no"

class ReportCredibilityLevel(Enum):
    CREDIBLE = "credible"
    NOT_CREDIBLE = "not_credible"

class SupplierCardinalityLevel(Enum):
    ONE = "one"
    MULTIPLE = "multiple"

class SupplierEngagementLevel(Enum):
    ACTIVE = "active"
    UNRESPONSIVE = "unresponsive"

class UtilityLevel(Enum):
    LABORIOUS = "laborious"
    EFFICIENT = "efficient"
    SUPER_EFFECTIVE = "super_effective"

class PublicSafetyImpactLevel(Enum):
    MINIMAL = "minimal"
    SIGNIFICANT = "significant"

class ActionType(Enum):
    DECLINE = "decline"
    TRACK = "track"
    COORDINATE = "coordinate"

class DecisionPriorityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


priority_map = {
    ActionType.DECLINE: DecisionPriorityLevel.LOW,
    ActionType.TRACK: DecisionPriorityLevel.MEDIUM,
    ActionType.COORDINATE: DecisionPriorityLevel.HIGH
}


class OutcomeCoordinatorTriage:
    def __init__(self, action):
        self.priority = priority_map[action]
        self.action = action


class DecisionCoordinatorTriage:
    def __init__(self, report_public: ReportPublicStatus | str = None, supplier_contacted: SupplierContactedStatus | str = None, report_credibility: ReportCredibilityLevel | str = None, supplier_cardinality: SupplierCardinalityLevel | str = None, supplier_engagement: SupplierEngagementLevel | str = None, utility: UtilityLevel | str = None, public_safety_impact: PublicSafetyImpactLevel | str = None):
        if isinstance(report_public, str):
            report_public = ReportPublicStatus(report_public)
        if isinstance(supplier_contacted, str):
            supplier_contacted = SupplierContactedStatus(supplier_contacted)
        if isinstance(report_credibility, str):
            report_credibility = ReportCredibilityLevel(report_credibility)
        if isinstance(supplier_cardinality, str):
            supplier_cardinality = SupplierCardinalityLevel(supplier_cardinality)
        if isinstance(supplier_engagement, str):
            supplier_engagement = SupplierEngagementLevel(supplier_engagement)
        if isinstance(utility, str):
            utility = UtilityLevel(utility)
        if isinstance(public_safety_impact, str):
            public_safety_impact = PublicSafetyImpactLevel(public_safety_impact)
        
        self.report_public = report_public
        self.supplier_contacted = supplier_contacted
        self.report_credibility = report_credibility
        self.supplier_cardinality = supplier_cardinality
        self.supplier_engagement = supplier_engagement
        self.utility = utility
        self.public_safety_impact = public_safety_impact
        
        # Always try to evaluate if we have the minimum required parameters
        if all([self.report_public is not None, self.supplier_contacted is not None, self.report_credibility is not None, self.supplier_cardinality is not None, self.supplier_engagement is not None, self.utility is not None, self.public_safety_impact is not None]):
            self.outcome = self.evaluate()

    def evaluate(self) -> OutcomeCoordinatorTriage:
        action = self._traverse_tree()
        self.outcome = OutcomeCoordinatorTriage(action)
        return self.outcome

    def _traverse_tree(self):
        """Traverse the decision tree to determine the outcome."""
        if self.report_public == ReportPublicStatus.YES:
            if self.supplier_contacted == SupplierContactedStatus.YES:
                if self.report_credibility == ReportCredibilityLevel.CREDIBLE:
                    if self.supplier_cardinality == SupplierCardinalityLevel.MULTIPLE:
                        if self.utility == UtilityLevel.SUPER_EFFECTIVE:
                            if self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                                return ActionType.COORDINATE
                            elif self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                                return ActionType.TRACK
                        elif self.utility == UtilityLevel.EFFICIENT:
                            if self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                                return ActionType.TRACK
                            elif self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                                return ActionType.DECLINE
                        elif self.utility == UtilityLevel.LABORIOUS:
                            return ActionType.DECLINE
                    elif self.supplier_cardinality == SupplierCardinalityLevel.ONE:
                        if self.utility == UtilityLevel.SUPER_EFFECTIVE:
                            if self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                                return ActionType.TRACK
                            elif self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                                return ActionType.DECLINE
                        elif self.utility == UtilityLevel.EFFICIENT:
                            return ActionType.DECLINE
                        elif self.utility == UtilityLevel.LABORIOUS:
                            return ActionType.DECLINE
                elif self.report_credibility == ReportCredibilityLevel.NOT_CREDIBLE:
                    return ActionType.DECLINE
            elif self.supplier_contacted == SupplierContactedStatus.NO:
                if self.supplier_cardinality == SupplierCardinalityLevel.MULTIPLE:
                    if self.utility == UtilityLevel.SUPER_EFFECTIVE:
                        if self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                            return ActionType.COORDINATE
                        elif self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                            return ActionType.TRACK
                    elif self.utility == UtilityLevel.EFFICIENT:
                        return ActionType.DECLINE
                    elif self.utility == UtilityLevel.LABORIOUS:
                        return ActionType.DECLINE
                elif self.supplier_cardinality == SupplierCardinalityLevel.ONE:
                    return ActionType.DECLINE
        elif self.report_public == ReportPublicStatus.NO:
            if self.supplier_contacted == SupplierContactedStatus.YES:
                if self.report_credibility == ReportCredibilityLevel.CREDIBLE:
                    if self.supplier_cardinality == SupplierCardinalityLevel.MULTIPLE:
                        if self.supplier_engagement == SupplierEngagementLevel.ACTIVE:
                            if self.utility == UtilityLevel.SUPER_EFFECTIVE:
                                if self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                                    return ActionType.COORDINATE
                                elif self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                                    return ActionType.TRACK
                            elif self.utility == UtilityLevel.EFFICIENT:
                                if self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                                    return ActionType.TRACK
                                elif self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                                    return ActionType.TRACK
                            elif self.utility == UtilityLevel.LABORIOUS:
                                return ActionType.TRACK
                        elif self.supplier_engagement == SupplierEngagementLevel.UNRESPONSIVE:
                            if self.utility == UtilityLevel.SUPER_EFFECTIVE:
                                if self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                                    return ActionType.COORDINATE
                                elif self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                                    return ActionType.TRACK
                            elif self.utility == UtilityLevel.EFFICIENT:
                                return ActionType.TRACK
                            elif self.utility == UtilityLevel.LABORIOUS:
                                return ActionType.DECLINE
                    elif self.supplier_cardinality == SupplierCardinalityLevel.ONE:
                        if self.supplier_engagement == SupplierEngagementLevel.ACTIVE:
                            if self.utility == UtilityLevel.SUPER_EFFECTIVE:
                                if self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                                    return ActionType.TRACK
                                elif self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                                    return ActionType.TRACK
                            elif self.utility == UtilityLevel.EFFICIENT:
                                return ActionType.TRACK
                            elif self.utility == UtilityLevel.LABORIOUS:
                                return ActionType.DECLINE
                        elif self.supplier_engagement == SupplierEngagementLevel.UNRESPONSIVE:
                            return ActionType.DECLINE
                elif self.report_credibility == ReportCredibilityLevel.NOT_CREDIBLE:
                    return ActionType.DECLINE
            elif self.supplier_contacted == SupplierContactedStatus.NO:
                if self.supplier_cardinality == SupplierCardinalityLevel.MULTIPLE:
                    if self.utility == UtilityLevel.SUPER_EFFECTIVE:
                        if self.public_safety_impact == PublicSafetyImpactLevel.SIGNIFICANT:
                            return ActionType.COORDINATE
                        elif self.public_safety_impact == PublicSafetyImpactLevel.MINIMAL:
                            return ActionType.TRACK
                    elif self.utility == UtilityLevel.EFFICIENT:
                        return ActionType.DECLINE
                    elif self.utility == UtilityLevel.LABORIOUS:
                        return ActionType.DECLINE
                elif self.supplier_cardinality == SupplierCardinalityLevel.ONE:
                    return ActionType.DECLINE
        
        # Default action for unmapped paths
        return ActionType.DECLINE