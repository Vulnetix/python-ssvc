import ssvc

def test_string_inputs():
    result: ssvc.DecisionOutcome = ssvc.Decision(
        exploitation='active',
        automatable='no',
        technical_impact='total',
        mission_wellbeing='high',
    ).outcome
    assert result.impact == ssvc.MissionWellbeingImpact.HIGH, "SSVC decision should be HIGH"
    assert result.action == ssvc.DecisionAction.ACT, "SSVC decision should be ACT"

def test_decision_active_no_total_high():
    result = ssvc.Decision(
        ssvc.ExploitationLevel.ACTIVE,
        ssvc.Automatable.NO,
        ssvc.TechnicalImpact.TOTAL,
        ssvc.MissionWellbeingImpact.HIGH,
    ).outcome
    assert result.impact == ssvc.MissionWellbeingImpact.HIGH, "SSVC decision should be HIGH"
    assert result.action == ssvc.DecisionAction.ACT, "SSVC decision should be ACT"

def test_decision_none_no_total_high():
    result = ssvc.Decision(
        ssvc.ExploitationLevel.NONE,
        ssvc.Automatable.NO,
        ssvc.TechnicalImpact.TOTAL,
        ssvc.MissionWellbeingImpact.HIGH,
    ).outcome
    assert result.impact == ssvc.MissionWellbeingImpact.HIGH, "SSVC decision should be HIGH"
    assert result.action == ssvc.DecisionAction.TRACK_STAR, "SSVC decision should be TRACK_STAR"

def test_decision_poc_no_total_high():
    result = ssvc.Decision(
        ssvc.ExploitationLevel.POC,
        ssvc.Automatable.NO,
        ssvc.TechnicalImpact.TOTAL,
        ssvc.MissionWellbeingImpact.HIGH,
    ).outcome
    assert result.impact == ssvc.MissionWellbeingImpact.HIGH, "SSVC decision should be HIGH"
    assert result.action == ssvc.DecisionAction.ATTEND, "SSVC decision should be ATTEND"

def test_decision_poc_no_partial_high():
    result = ssvc.Decision(
        ssvc.ExploitationLevel.POC,
        ssvc.Automatable.NO,
        ssvc.TechnicalImpact.PARTIAL,
        ssvc.MissionWellbeingImpact.HIGH,
    ).outcome
    assert result.impact == ssvc.MissionWellbeingImpact.HIGH, "SSVC decision should be HIGH"
    assert result.action == ssvc.DecisionAction.TRACK, "SSVC decision should be TRACK"

def test_decision_poc_yes_partial_high():
    result = ssvc.Decision(
        ssvc.ExploitationLevel.POC,
        ssvc.Automatable.YES,
        ssvc.TechnicalImpact.PARTIAL,
        ssvc.MissionWellbeingImpact.HIGH,
    ).outcome
    assert result.impact == ssvc.MissionWellbeingImpact.LOW, "SSVC decision should be LOW"
    assert result.action == ssvc.DecisionAction.TRACK, "SSVC decision should be TRACK"

def test_decision_poc_yes_partial_medium():
    result = ssvc.Decision(
        ssvc.ExploitationLevel.POC,
        ssvc.Automatable.YES,
        ssvc.TechnicalImpact.PARTIAL,
        ssvc.MissionWellbeingImpact.MEDIUM,
    ).outcome
    assert result.impact == ssvc.MissionWellbeingImpact.LOW, "SSVC decision should be LOW"
    assert result.action == ssvc.DecisionAction.TRACK, "SSVC decision should be TRACK"

def test_decision_poc_yes_partial_low():
    result = ssvc.Decision(
        ssvc.ExploitationLevel.POC,
        ssvc.Automatable.YES,
        ssvc.TechnicalImpact.PARTIAL,
        ssvc.MissionWellbeingImpact.LOW,
    ).outcome
    assert result.impact == ssvc.MissionWellbeingImpact.LOW, "SSVC decision should be LOW"
    assert result.action == ssvc.DecisionAction.TRACK, "SSVC decision should be TRACK"
