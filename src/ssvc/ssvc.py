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

class DecisionAction(Enum):
    TRACK = 'Track'
    TRACK_STAR = 'Track*'
    ATTEND = 'Attend'
    ACT = 'Act'

class DecisionOutcome:
    def __init__(self,
            impact: TechnicalImpact|MissionWellbeingImpact,
            action: DecisionAction
        ):
        self.impact: TechnicalImpact|MissionWellbeingImpact = impact
        self.action: DecisionAction = action

class Decision:
    outcome: DecisionOutcome
    def __init__(self,
        exploitation: ExploitationLevel,
        automatable: Automatable,
        technical_impact: TechnicalImpact,
        mission_wellbeing: MissionWellbeingImpact
    ):
        if isinstance(exploitation, str):
            exploitation = ExploitationLevel(exploitation)
        if isinstance(automatable, str):
            automatable = Automatable(automatable)
        if isinstance(technical_impact, str):
            technical_impact = TechnicalImpact(technical_impact)
        if isinstance(mission_wellbeing, str):
            mission_wellbeing = MissionWellbeingImpact(mission_wellbeing)

        if exploitation == ExploitationLevel.NONE:
            if automatable == Automatable.YES:
                self.outcome = DecisionOutcome(MissionWellbeingImpact.LOW, DecisionAction.TRACK)
            else: # Automatable.NO
                if technical_impact == TechnicalImpact.PARTIAL:
                    self.outcome = DecisionOutcome(mission_wellbeing, DecisionAction.TRACK)
                else: # TechnicalImpact.TOTAL
                    self.outcome = DecisionOutcome(mission_wellbeing, DecisionAction.TRACK_STAR)
        elif exploitation == ExploitationLevel.POC:
            if automatable == Automatable.YES:
                self.outcome = DecisionOutcome(MissionWellbeingImpact.LOW, DecisionAction.TRACK)
            else: # Automatable.NO
                if technical_impact == TechnicalImpact.PARTIAL:
                    self.outcome = DecisionOutcome(mission_wellbeing, DecisionAction.TRACK)
                else: # TechnicalImpact.TOTAL
                    if mission_wellbeing == MissionWellbeingImpact.LOW:
                        self.outcome = DecisionOutcome(mission_wellbeing, DecisionAction.ATTEND)
                    else: # MissionWellbeingImpact.MEDIUM or HIGH
                        self.outcome = DecisionOutcome(mission_wellbeing, DecisionAction.ATTEND)
        else: # ExploitationLevel.ACTIVE
            if automatable == Automatable.YES:
                self.outcome = DecisionOutcome(MissionWellbeingImpact.LOW, DecisionAction.TRACK)
            else: # Automatable.NO
                if technical_impact == TechnicalImpact.PARTIAL:
                    if mission_wellbeing == MissionWellbeingImpact.LOW:
                        self.outcome = DecisionOutcome(mission_wellbeing, DecisionAction.TRACK)
                    elif mission_wellbeing == MissionWellbeingImpact.MEDIUM:
                        self.outcome = DecisionOutcome(mission_wellbeing, DecisionAction.ATTEND)
                    else: # MissionWellbeingImpact.HIGH
                        self.outcome = DecisionOutcome(mission_wellbeing, DecisionAction.ATTEND)
                else: # TechnicalImpact.TOTAL
                    if mission_wellbeing == MissionWellbeingImpact.LOW:
                        self.outcome = DecisionOutcome(mission_wellbeing, DecisionAction.ATTEND)
                    elif mission_wellbeing == MissionWellbeingImpact.MEDIUM:
                        self.outcome = DecisionOutcome(mission_wellbeing, DecisionAction.ACT)
                    else: # MissionWellbeingImpact.HIGH
                        self.outcome = DecisionOutcome(mission_wellbeing, DecisionAction.ACT)
