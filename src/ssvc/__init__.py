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
    FIRST = "FIRST"
    CISA = "CISA"


priority_map = {
    ActionCISA.TRACK: DecisionPriority.LOW,
    ActionCISA.TRACK_STAR: DecisionPriority.MEDIUM,
    ActionCISA.ATTEND: DecisionPriority.MEDIUM,
    ActionCISA.ACT: DecisionPriority.IMMEDIATE,
}


class OutcomeCISA:
    def __init__(self, action: ActionCISA):
        self.priority: DecisionPriority = priority_map[action]
        self.action: ActionCISA = action


class Decision:
    exploitation: ExploitationLevel
    automatable: Automatable
    technical_impact: TechnicalImpact
    mission_wellbeing: MissionWellbeingImpact
    outcome: OutcomeCISA
    methodology: Methodology = Methodology.CISA

    def __init__(
        self,
        exploitation: ExploitationLevel | str = None,
        automatable: Automatable | str = None,
        technical_impact: TechnicalImpact | str = None,
        mission_wellbeing: MissionWellbeingImpact | str = None,
        methodology: Methodology | str = Methodology.CISA,
    ):
        if isinstance(exploitation, str):
            exploitation = ExploitationLevel(exploitation)
        if isinstance(automatable, str):
            automatable = Automatable(automatable)
        if isinstance(technical_impact, str):
            technical_impact = TechnicalImpact(technical_impact)
        if isinstance(mission_wellbeing, str):
            mission_wellbeing = MissionWellbeingImpact(mission_wellbeing)
        if isinstance(methodology, str):
            methodology = Methodology(methodology)

        self.exploitation = exploitation
        self.automatable = automatable
        self.technical_impact = technical_impact
        self.mission_wellbeing = mission_wellbeing
        self.methodology = methodology
        if all(
            [
                isinstance(self.exploitation, ExploitationLevel),
                isinstance(self.automatable, Automatable),
                isinstance(self.technical_impact, TechnicalImpact),
                isinstance(self.mission_wellbeing, MissionWellbeingImpact),
            ]
        ):
            self.evaluate()

    def evaluate(self) -> OutcomeCISA:
        if self.methodology == Methodology.CISA:
            return self.cisa()

    def cisa(self) -> OutcomeCISA:
        """
        Evaluates the decision based on the provided attributes and returns a OutcomeCISA object.

        Raises:
            AttributeError: If any of the required attributes (exploitation, automatable, technical_impact, mission_wellbeing) are not provided.
        """
        self._validate_cisa()
        decision_matrix = {
            ExploitationLevel.NONE: {
                Automatable.YES: {
                    TechnicalImpact.TOTAL: {
                        MissionWellbeingImpact.HIGH: ActionCISA.ATTEND
                    },
                },
                Automatable.NO: {
                    TechnicalImpact.TOTAL: {
                        MissionWellbeingImpact.HIGH: ActionCISA.TRACK_STAR
                    },
                },
            },
            ExploitationLevel.POC: {
                Automatable.YES: {
                    TechnicalImpact.TOTAL: {
                        MissionWellbeingImpact.MEDIUM: ActionCISA.TRACK_STAR,
                        MissionWellbeingImpact.HIGH: ActionCISA.ATTEND,
                    },
                    TechnicalImpact.PARTIAL: {
                        MissionWellbeingImpact.HIGH: ActionCISA.ATTEND
                    },
                },
                Automatable.NO: {
                    TechnicalImpact.PARTIAL: {
                        MissionWellbeingImpact.HIGH: ActionCISA.TRACK_STAR
                    },
                    TechnicalImpact.TOTAL: {
                        MissionWellbeingImpact.MEDIUM: ActionCISA.TRACK_STAR,
                        MissionWellbeingImpact.HIGH: ActionCISA.ATTEND,
                    },
                },
            },
            ExploitationLevel.ACTIVE: {
                Automatable.YES: {
                    TechnicalImpact.PARTIAL: {
                        MissionWellbeingImpact.LOW: ActionCISA.ATTEND,
                        MissionWellbeingImpact.MEDIUM: ActionCISA.ATTEND,
                        MissionWellbeingImpact.HIGH: ActionCISA.ACT,
                    },
                    TechnicalImpact.TOTAL: {
                        MissionWellbeingImpact.LOW: ActionCISA.ATTEND,
                        MissionWellbeingImpact.MEDIUM: ActionCISA.ACT,
                        MissionWellbeingImpact.HIGH: ActionCISA.ACT,
                    },
                },
                Automatable.NO: {
                    TechnicalImpact.PARTIAL: {
                        MissionWellbeingImpact.HIGH: ActionCISA.ATTEND
                    },
                    TechnicalImpact.TOTAL: {
                        MissionWellbeingImpact.MEDIUM: ActionCISA.ATTEND,
                        MissionWellbeingImpact.HIGH: ActionCISA.ACT,
                    },
                },
            },
        }
        # Lookup decision based on attributes and return outcome
        return OutcomeCISA(
            decision_matrix.get(self.exploitation, {})
            .get(self.automatable, {})
            .get(self.technical_impact, {})
            .get(self.mission_wellbeing, ActionCISA.TRACK)
        )

    def _validate_cisa(self):
        if not isinstance(self.exploitation, ExploitationLevel):
            raise AttributeError("ExploitationLevel has not been provided")
        if not isinstance(self.automatable, Automatable):
            raise AttributeError("Automatable has not been provided")
        if not isinstance(self.technical_impact, TechnicalImpact):
            raise AttributeError("TechnicalImpact has not been provided")
        if not isinstance(self.mission_wellbeing, MissionWellbeingImpact):
            raise AttributeError("MissionWellbeingImpact has not been provided")
