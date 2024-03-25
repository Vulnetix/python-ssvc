from enum import Enum

class ExploitationLevel(Enum):
    NONE = 'none'
    POC = 'poc'
    ACTIVE = 'active'

class Automatable(Enum):
    YES = 'yes'
    NO = 'no'

class TechnicalImpact(Enum):
    PARTIAL = 'partial'
    TOTAL = 'total'

class MissionWellbeingImpact(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class DecisionPriority(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    IMMEDIATE = 'immediate'

class DecisionAction(Enum):
    TRACK = 'Track'
    TRACK_STAR = 'Track*'
    ATTEND = 'Attend'
    ACT = 'Act'

priority_map = {
    DecisionAction.TRACK: DecisionPriority.LOW,
    DecisionAction.TRACK_STAR: DecisionPriority.MEDIUM,
    DecisionAction.ATTEND: DecisionPriority.MEDIUM,
    DecisionAction.ACT: DecisionPriority.IMMEDIATE,
}

class DecisionOutcome:
    def __init__(self,
            action: DecisionAction
        ):
        self.priority: DecisionPriority = priority_map[action]
        self.action: DecisionAction = action

class Decision:
    exploitation: ExploitationLevel
    automatable: Automatable
    technical_impact: TechnicalImpact
    mission_wellbeing: MissionWellbeingImpact
    outcome: DecisionOutcome

    def __init__(self,
        exploitation: ExploitationLevel = None,
        automatable: Automatable = None,
        technical_impact: TechnicalImpact = None,
        mission_wellbeing: MissionWellbeingImpact = None
    ):
        if isinstance(exploitation, str):
            exploitation = ExploitationLevel(exploitation)
        if isinstance(automatable, str):
            automatable = Automatable(automatable)
        if isinstance(technical_impact, str):
            technical_impact = TechnicalImpact(technical_impact)
        if isinstance(mission_wellbeing, str):
            mission_wellbeing = MissionWellbeingImpact(mission_wellbeing)

        self.exploitation = exploitation
        self.automatable = automatable
        self.technical_impact = technical_impact
        self.mission_wellbeing = mission_wellbeing
        if all([
            isinstance(self.exploitation, ExploitationLevel),
            isinstance(self.automatable, Automatable),
            isinstance(self.technical_impact, TechnicalImpact),
            isinstance(self.mission_wellbeing, MissionWellbeingImpact)
        ]):
            self.evaluate()

    def evaluate(self) -> DecisionOutcome:
        """
        Evaluates the decision based on the provided attributes and returns a DecisionOutcome object.

        Raises:
            AttributeError: If any of the required attributes (exploitation, automatable, technical_impact, mission_wellbeing) are not provided.
        """
        self._validate_attributes()
        decision_matrix = {
            ExploitationLevel.NONE: {
                Automatable.YES: {
                    TechnicalImpact.TOTAL: {
                        MissionWellbeingImpact.HIGH: DecisionAction.ATTEND
                    },
                },
                Automatable.NO: {
                    TechnicalImpact.TOTAL: {
                        MissionWellbeingImpact.HIGH: DecisionAction.TRACK_STAR
                    },
                }
            },
            ExploitationLevel.POC: {
                Automatable.YES: {
                    TechnicalImpact.TOTAL: {
                        MissionWellbeingImpact.MEDIUM: DecisionAction.TRACK_STAR,
                        MissionWellbeingImpact.HIGH: DecisionAction.ATTEND
                    },
                    TechnicalImpact.PARTIAL: {
                        MissionWellbeingImpact.HIGH: DecisionAction.ATTEND
                    },
                },
                Automatable.NO: {
                    TechnicalImpact.PARTIAL: {
                        MissionWellbeingImpact.HIGH: DecisionAction.TRACK_STAR
                    },
                    TechnicalImpact.TOTAL: {
                        MissionWellbeingImpact.MEDIUM: DecisionAction.TRACK_STAR,
                        MissionWellbeingImpact.HIGH: DecisionAction.ATTEND
                    }
                }
            },
            ExploitationLevel.ACTIVE: {
                Automatable.YES: {
                    TechnicalImpact.PARTIAL: {
                        MissionWellbeingImpact.LOW: DecisionAction.ATTEND,
                        MissionWellbeingImpact.MEDIUM: DecisionAction.ATTEND,
                        MissionWellbeingImpact.HIGH: DecisionAction.ACT
                    },
                    TechnicalImpact.TOTAL: {
                        MissionWellbeingImpact.LOW: DecisionAction.ATTEND,
                        MissionWellbeingImpact.MEDIUM: DecisionAction.ACT,
                        MissionWellbeingImpact.HIGH: DecisionAction.ACT
                    }
                },
                Automatable.NO: {
                    TechnicalImpact.PARTIAL: {
                        MissionWellbeingImpact.HIGH: DecisionAction.ATTEND
                    },
                    TechnicalImpact.TOTAL: {
                        MissionWellbeingImpact.MEDIUM: DecisionAction.ATTEND,
                        MissionWellbeingImpact.HIGH: DecisionAction.ACT
                    }
                }
            }
        }
        # Lookup decision based on attributes and return outcome
        return DecisionOutcome(
            decision_matrix
                .get(self.exploitation, {})
                .get(self.automatable, {})
                .get(self.technical_impact, {})
                .get(self.mission_wellbeing, DecisionAction.TRACK)
        )

    def _validate_attributes(self):
        if not isinstance(self.exploitation, ExploitationLevel):
            raise AttributeError('ExploitationLevel has not been provided')
        if not isinstance(self.automatable, Automatable):
            raise AttributeError('Automatable has not been provided')
        if not isinstance(self.technical_impact, TechnicalImpact):
            raise AttributeError('TechnicalImpact has not been provided')
        if not isinstance(self.mission_wellbeing, MissionWellbeingImpact):
            raise AttributeError('MissionWellbeingImpact has not been provided')
