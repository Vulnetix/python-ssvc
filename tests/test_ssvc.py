import pytest
from ssvc import Decision, ExploitationLevel, Automatable, TechnicalImpact, MissionWellbeingImpact, DecisionAction, DecisionPriority

@pytest.mark.xfail(raises=AttributeError)
def test_negative_evaluate_no_attributes():
    decision = Decision()
    decision.evaluate()

@pytest.mark.xfail(raises=AttributeError)
def test_negative_evaluate_attribute_exploitation():
    decision = Decision()
    decision.exploitation = ExploitationLevel.POC
    decision.evaluate()

@pytest.mark.xfail(raises=AttributeError)
def test_negative_evaluate_attribute_automatable():
    decision = Decision()
    decision.exploitation = ExploitationLevel.POC
    decision.automatable = Automatable.YES
    decision.evaluate()

@pytest.mark.xfail(raises=AttributeError)
def test_negative_evaluate_attribute_technical_impact():
    decision = Decision()
    decision.exploitation = ExploitationLevel.POC
    decision.automatable = Automatable.YES
    decision.technical_impact = TechnicalImpact.TOTAL
    decision.evaluate()

def test_string_inputs():
    outcome = Decision(
        exploitation='active',
        automatable='no',
        technical_impact='total',
        mission_wellbeing='high',
    ).evaluate()
    assert outcome.priority == DecisionPriority.IMMEDIATE, "SSVC priority should be IMMEDIATE"
    assert outcome.action == DecisionAction.ACT, "SSVC decision should be ACT"

def test_decision_active_no_total_high():
    outcome = Decision(
        ExploitationLevel.ACTIVE,
        Automatable.NO,
        TechnicalImpact.TOTAL,
        MissionWellbeingImpact.HIGH,
    ).evaluate()
    assert outcome.priority == DecisionPriority.IMMEDIATE, "SSVC priority should be IMMEDIATE"
    assert outcome.action == DecisionAction.ACT, "SSVC decision should be ACT"

def test_decision_active_no_partial_high():
    outcome = Decision(
        ExploitationLevel.ACTIVE,
        Automatable.NO,
        TechnicalImpact.PARTIAL,
        MissionWellbeingImpact.HIGH,
    ).evaluate()
    assert outcome.priority == DecisionPriority.MEDIUM, "SSVC priority should be MEDIUM"
    assert outcome.action == DecisionAction.ATTEND, "SSVC decision should be ATTEND"

def test_decision_active_no_partial_low():
    outcome = Decision(
        ExploitationLevel.ACTIVE,
        Automatable.NO,
        TechnicalImpact.PARTIAL,
        MissionWellbeingImpact.LOW,
    ).evaluate()
    assert outcome.priority == DecisionPriority.LOW, "SSVC priority should be LOW"
    assert outcome.action == DecisionAction.TRACK, "SSVC decision should be TRACK"

def test_decision_active_no_partial_medium():
    outcome = Decision(
        ExploitationLevel.ACTIVE,
        Automatable.NO,
        TechnicalImpact.PARTIAL,
        MissionWellbeingImpact.MEDIUM,
    ).evaluate()
    assert outcome.priority == DecisionPriority.LOW, "SSVC priority should be LOW"
    assert outcome.action == DecisionAction.TRACK, "SSVC decision should be TRACK"

def test_decision_active_no_total_medium():
    outcome = Decision(
        ExploitationLevel.ACTIVE,
        Automatable.NO,
        TechnicalImpact.TOTAL,
        MissionWellbeingImpact.MEDIUM,
    ).evaluate()
    assert outcome.priority == DecisionPriority.MEDIUM, "SSVC priority should be MEDIUM"
    assert outcome.action == DecisionAction.ATTEND, "SSVC decision should be ATTEND"

def test_decision_active_no_total_low():
    outcome = Decision(
        ExploitationLevel.ACTIVE,
        Automatable.NO,
        TechnicalImpact.TOTAL,
        MissionWellbeingImpact.LOW,
    ).evaluate()
    assert outcome.priority == DecisionPriority.LOW, "SSVC priority should be LOW"
    assert outcome.action == DecisionAction.TRACK, "SSVC decision should be TRACK"

def test_decision_active_yes_total_high():
    outcome = Decision(
        ExploitationLevel.ACTIVE,
        Automatable.YES,
        TechnicalImpact.TOTAL,
        MissionWellbeingImpact.HIGH,
    ).evaluate()
    assert outcome.priority == DecisionPriority.IMMEDIATE, "SSVC priority should be IMMEDIATE"
    assert outcome.action == DecisionAction.ACT, "SSVC decision should be ACT"

def test_decision_active_yes_total_low():
    outcome = Decision(
        ExploitationLevel.ACTIVE,
        Automatable.YES,
        TechnicalImpact.TOTAL,
        MissionWellbeingImpact.LOW,
    ).evaluate()
    assert outcome.priority == DecisionPriority.MEDIUM, "SSVC priority should be MEDIUM"
    assert outcome.action == DecisionAction.ATTEND, "SSVC decision should be ATTEND"

def test_decision_active_yes_partial_low():
    outcome = Decision(
        ExploitationLevel.ACTIVE,
        Automatable.YES,
        TechnicalImpact.PARTIAL,
        MissionWellbeingImpact.LOW,
    ).evaluate()
    assert outcome.priority == DecisionPriority.MEDIUM, "SSVC priority should be MEDIUM"
    assert outcome.action == DecisionAction.ATTEND, "SSVC decision should be ATTEND"

def test_decision_active_yes_total_medium():
    outcome = Decision(
        ExploitationLevel.ACTIVE,
        Automatable.YES,
        TechnicalImpact.TOTAL,
        MissionWellbeingImpact.MEDIUM,
    ).evaluate()
    assert outcome.priority == DecisionPriority.IMMEDIATE, "SSVC priority should be IMMEDIATE"
    assert outcome.action == DecisionAction.ACT, "SSVC decision should be ACT"

def test_decision_active_yes_partial_medium():
    outcome = Decision(
        ExploitationLevel.ACTIVE,
        Automatable.YES,
        TechnicalImpact.PARTIAL,
        MissionWellbeingImpact.MEDIUM,
    ).evaluate()
    assert outcome.priority == DecisionPriority.MEDIUM, "SSVC priority should be MEDIUM"
    assert outcome.action == DecisionAction.ATTEND, "SSVC decision should be ATTEND"

def test_decision_none_no_total_high():
    outcome = Decision(
        ExploitationLevel.NONE,
        Automatable.NO,
        TechnicalImpact.TOTAL,
        MissionWellbeingImpact.HIGH,
    ).evaluate()
    assert outcome.priority == DecisionPriority.MEDIUM, "SSVC priority should be MEDIUM"
    assert outcome.action == DecisionAction.TRACK_STAR, "SSVC decision should be TRACK_STAR"

def test_decision_none_yes_total_high():
    outcome = Decision(
        ExploitationLevel.NONE,
        Automatable.YES,
        TechnicalImpact.TOTAL,
        MissionWellbeingImpact.HIGH,
    ).evaluate()
    assert outcome.priority == DecisionPriority.MEDIUM, "SSVC priority should be MEDIUM"
    assert outcome.action == DecisionAction.ATTEND, "SSVC decision should be ATTEND"

def test_decision_none_yes_total_low():
    outcome = Decision(
        ExploitationLevel.NONE,
        Automatable.YES,
        TechnicalImpact.TOTAL,
        MissionWellbeingImpact.LOW,
    ).evaluate()
    assert outcome.priority == DecisionPriority.LOW, "SSVC priority should be LOW"
    assert outcome.action == DecisionAction.TRACK, "SSVC decision should be TRACK"

def test_decision_none_no_partial_high():
    outcome = Decision(
        ExploitationLevel.NONE,
        Automatable.NO,
        TechnicalImpact.PARTIAL,
        MissionWellbeingImpact.HIGH,
    ).evaluate()
    assert outcome.priority == DecisionPriority.LOW, "SSVC priority should be LOW"
    assert outcome.action == DecisionAction.TRACK, "SSVC decision should be TRACK"

def test_decision_poc_no_total_high():
    outcome = Decision(
        ExploitationLevel.POC,
        Automatable.NO,
        TechnicalImpact.TOTAL,
        MissionWellbeingImpact.HIGH,
    ).evaluate()
    assert outcome.priority == DecisionPriority.MEDIUM, "SSVC priority should be MEDIUM"
    assert outcome.action == DecisionAction.ATTEND, "SSVC decision should be ATTEND"

def test_decision_poc_no_total_medium():
    outcome = Decision(
        ExploitationLevel.POC,
        Automatable.NO,
        TechnicalImpact.TOTAL,
        MissionWellbeingImpact.MEDIUM,
    ).evaluate()
    assert outcome.priority == DecisionPriority.MEDIUM, "SSVC priority should be MEDIUM"
    assert outcome.action == DecisionAction.TRACK_STAR, "SSVC decision should be TRACK_STAR"

def test_decision_poc_no_total_low():
    outcome = Decision(
        ExploitationLevel.POC,
        Automatable.NO,
        TechnicalImpact.TOTAL,
        MissionWellbeingImpact.LOW,
    ).evaluate()
    assert outcome.priority == DecisionPriority.LOW, "SSVC priority should be LOW"
    assert outcome.action == DecisionAction.TRACK, "SSVC decision should be TRACK"

def test_decision_poc_no_partial_high():
    outcome = Decision(
        ExploitationLevel.POC,
        Automatable.NO,
        TechnicalImpact.PARTIAL,
        MissionWellbeingImpact.HIGH,
    ).evaluate()
    assert outcome.priority == DecisionPriority.MEDIUM, "SSVC priority should be MEDIUM"
    assert outcome.action == DecisionAction.TRACK_STAR, "SSVC decision should be TRACK_STAR"

def test_decision_poc_no_partial_medium():
    outcome = Decision(
        ExploitationLevel.POC,
        Automatable.NO,
        TechnicalImpact.PARTIAL,
        MissionWellbeingImpact.MEDIUM,
    ).evaluate()
    assert outcome.priority == DecisionPriority.LOW, "SSVC priority should be LOW"
    assert outcome.action == DecisionAction.TRACK, "SSVC decision should be TRACK"

def test_decision_poc_yes_partial_high():
    outcome = Decision(
        ExploitationLevel.POC,
        Automatable.YES,
        TechnicalImpact.PARTIAL,
        MissionWellbeingImpact.HIGH,
    ).evaluate()
    assert outcome.priority == DecisionPriority.MEDIUM, "SSVC priority should be MEDIUM"
    assert outcome.action == DecisionAction.ATTEND, "SSVC decision should be ATTEND"

def test_decision_poc_yes_partial_medium():
    outcome = Decision(
        ExploitationLevel.POC,
        Automatable.YES,
        TechnicalImpact.PARTIAL,
        MissionWellbeingImpact.MEDIUM,
    ).evaluate()
    assert outcome.priority == DecisionPriority.LOW, "SSVC priority should be LOW"
    assert outcome.action == DecisionAction.TRACK, "SSVC decision should be TRACK"

def test_decision_poc_yes_partial_low():
    outcome = Decision(
        ExploitationLevel.POC,
        Automatable.YES,
        TechnicalImpact.PARTIAL,
        MissionWellbeingImpact.LOW,
    ).evaluate()
    assert outcome.priority == DecisionPriority.LOW, "SSVC priority should be LOW"
    assert outcome.action == DecisionAction.TRACK, "SSVC decision should be TRACK"

def test_decision_poc_yes_total_medium():
    outcome = Decision(
        ExploitationLevel.POC,
        Automatable.YES,
        TechnicalImpact.TOTAL,
        MissionWellbeingImpact.MEDIUM,
    ).evaluate()
    assert outcome.priority == DecisionPriority.MEDIUM, "SSVC priority should be MEDIUM"
    assert outcome.action == DecisionAction.TRACK_STAR, "SSVC decision should be TRACK_STAR"
