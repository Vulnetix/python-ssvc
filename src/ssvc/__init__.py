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
        if not isinstance(self.exploitation, ExploitationLevel):
            raise AttributeError('ExploitationLevel has not been provided')
        if not isinstance(self.automatable, Automatable):
            raise AttributeError('Automatable has not been provided')
        if not isinstance(self.technical_impact, TechnicalImpact):
            raise AttributeError('TechnicalImpact has not been provided')
        if not isinstance(self.mission_wellbeing, MissionWellbeingImpact):
            raise AttributeError('MissionWellbeingImpact has not been provided')

        if self.exploitation == ExploitationLevel.NONE:
            if self.automatable == Automatable.YES:
                if self.mission_wellbeing == MissionWellbeingImpact.HIGH: # TechnicalImpact.TOTAL or TechnicalImpact.PARTIAL
                    self.outcome = DecisionOutcome(DecisionAction.ATTEND)
                else: # MissionWellbeingImpact.LOW MissionWellbeingImpact.MEDIUM and TechnicalImpact.TOTAL or TechnicalImpact.PARTIAL
                    self.outcome = DecisionOutcome(DecisionAction.TRACK)
            else: # Automatable.NO
                if self.technical_impact == TechnicalImpact.TOTAL and self.mission_wellbeing == MissionWellbeingImpact.HIGH:
                    self.outcome = DecisionOutcome(DecisionAction.TRACK_STAR)
                else:  # TechnicalImpact.PARTIAL (all) or TechnicalImpact.TOTAL (low & medium)
                    self.outcome = DecisionOutcome(DecisionAction.TRACK)

        elif self.exploitation == ExploitationLevel.POC:
            if self.mission_wellbeing == MissionWellbeingImpact.LOW: # Automatable.NO or Automatable.YES and TechnicalImpact.TOTAL or TechnicalImpact.PARTIAL
                self.outcome = DecisionOutcome(DecisionAction.TRACK)

            elif self.automatable == Automatable.YES:
                if self.mission_wellbeing == MissionWellbeingImpact.HIGH: # TechnicalImpact.TOTAL or TechnicalImpact.PARTIAL
                    self.outcome = DecisionOutcome(DecisionAction.ATTEND)
                elif self.mission_wellbeing == MissionWellbeingImpact.MEDIUM:
                    if self.technical_impact == TechnicalImpact.PARTIAL:
                        self.outcome = DecisionOutcome(DecisionAction.TRACK)
                    else: # TechnicalImpact.TOTAL
                        self.outcome = DecisionOutcome(DecisionAction.TRACK_STAR)
            else: # Automatable.NO
                if self.technical_impact == TechnicalImpact.PARTIAL:
                    if self.mission_wellbeing == MissionWellbeingImpact.HIGH:
                        self.outcome = DecisionOutcome(DecisionAction.TRACK_STAR)
                    else: # MissionWellbeingImpact.MEDIUM
                        self.outcome = DecisionOutcome(DecisionAction.TRACK)
                else: # TechnicalImpact.TOTAL
                    if self.mission_wellbeing == MissionWellbeingImpact.MEDIUM:
                        self.outcome = DecisionOutcome(DecisionAction.TRACK_STAR)
                    else: # MissionWellbeingImpact.HIGH:
                        self.outcome = DecisionOutcome(DecisionAction.ATTEND)

        else: # ExploitationLevel.ACTIVE
            if self.automatable == Automatable.YES:
                if self.mission_wellbeing == MissionWellbeingImpact.LOW: # TechnicalImpact.TOTAL or TechnicalImpact.PARTIAL
                    self.outcome = DecisionOutcome(DecisionAction.ATTEND)
                elif self.mission_wellbeing == MissionWellbeingImpact.HIGH: # TechnicalImpact.TOTAL or TechnicalImpact.PARTIAL
                    self.outcome = DecisionOutcome(DecisionAction.ACT)
                else: # MissionWellbeingImpact.MEDIUM
                    if self.technical_impact == TechnicalImpact.PARTIAL:
                        self.outcome = DecisionOutcome(DecisionAction.ATTEND)
                    else: # TechnicalImpact.TOTAL
                        self.outcome = DecisionOutcome(DecisionAction.ACT)

            else: # Automatable.NO
                if self.mission_wellbeing == MissionWellbeingImpact.LOW: # TechnicalImpact.TOTAL or TechnicalImpact.PARTIAL
                    self.outcome = DecisionOutcome(DecisionAction.TRACK)
                elif self.technical_impact == TechnicalImpact.PARTIAL:
                    if self.mission_wellbeing == MissionWellbeingImpact.MEDIUM:
                        self.outcome = DecisionOutcome(DecisionAction.TRACK)
                    else: # MissionWellbeingImpact.HIGH
                        self.outcome = DecisionOutcome(DecisionAction.ATTEND)
                else: # TechnicalImpact.TOTAL
                    if self.mission_wellbeing == MissionWellbeingImpact.MEDIUM:
                        self.outcome = DecisionOutcome(DecisionAction.ATTEND)
                    else: # MissionWellbeingImpact.HIGH
                        self.outcome = DecisionOutcome(DecisionAction.ACT)
        return self.outcome
