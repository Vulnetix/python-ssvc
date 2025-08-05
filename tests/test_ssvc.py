"""
Tests for SSVC functionality using the new plugin-based API.
These tests focus on the new API while maintaining backward compatibility coverage.
"""

import pytest
import ssvc


@pytest.mark.xfail(raises=ValueError)
def test_negative_methodology():
    ssvc.Decision(methodology='noop')


def test_methodology_cisa():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation="active",
        automatable="no",
        technical_impact="total",
        mission_wellbeing_impact="high"
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'immediate', "SSVC priority should be IMMEDIATE"
    assert outcome.action.value == 'act', "SSVC decision should be ACT"


def test_string_inputs():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation="active",
        automatable="no", 
        technical_impact="total",
        mission_wellbeing_impact="high"
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'immediate', "SSVC priority should be IMMEDIATE"
    assert outcome.action.value == 'act', "SSVC decision should be ACT"


def test_decision_active_no_total_high():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='active',
        automatable='no',
        technical_impact='total',
        mission_wellbeing_impact='high'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'immediate', "SSVC priority should be IMMEDIATE"
    assert outcome.action.value == 'act', "SSVC decision should be ACT"


def test_decision_active_no_partial_high():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='active',
        automatable='no',
        technical_impact='partial',
        mission_wellbeing_impact='high'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'medium', "SSVC priority should be MEDIUM"
    assert outcome.action.value == 'attend', "SSVC decision should be ATTEND"


def test_decision_active_no_partial_low():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='active',
        automatable='no',
        technical_impact='partial',
        mission_wellbeing_impact='low'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'low', "SSVC priority should be LOW"
    assert outcome.action.value == 'track', "SSVC decision should be TRACK"


def test_decision_active_no_partial_medium():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='active',
        automatable='no',
        technical_impact='partial',
        mission_wellbeing_impact='medium'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'low', "SSVC priority should be LOW"
    assert outcome.action.value == 'track', "SSVC decision should be TRACK"


def test_decision_active_no_total_medium():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='active',
        automatable='no',
        technical_impact='total',
        mission_wellbeing_impact='medium'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'medium', "SSVC priority should be MEDIUM"
    assert outcome.action.value == 'attend', "SSVC decision should be ATTEND"


def test_decision_active_no_total_low():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='active',
        automatable='no',
        technical_impact='total',
        mission_wellbeing_impact='low'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'low', "SSVC priority should be LOW"
    assert outcome.action.value == 'track', "SSVC decision should be TRACK"


def test_decision_active_yes_total_high():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='active',
        automatable='yes',
        technical_impact='total',
        mission_wellbeing_impact='high'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'immediate', "SSVC priority should be IMMEDIATE"
    assert outcome.action.value == 'act', "SSVC decision should be ACT"


def test_decision_active_yes_total_low():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='active',
        automatable='yes',
        technical_impact='total',
        mission_wellbeing_impact='low'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'medium', "SSVC priority should be MEDIUM"
    assert outcome.action.value == 'attend', "SSVC decision should be ATTEND"


def test_decision_active_yes_partial_low():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='active',
        automatable='yes',
        technical_impact='partial',
        mission_wellbeing_impact='low'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'medium', "SSVC priority should be MEDIUM"
    assert outcome.action.value == 'attend', "SSVC decision should be ATTEND"


def test_decision_active_yes_total_medium():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='active',
        automatable='yes',
        technical_impact='total',
        mission_wellbeing_impact='medium'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'immediate', "SSVC priority should be IMMEDIATE"
    assert outcome.action.value == 'act', "SSVC decision should be ACT"


def test_decision_active_yes_partial_medium():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='active',
        automatable='yes',
        technical_impact='partial',
        mission_wellbeing_impact='medium'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'medium', "SSVC priority should be MEDIUM"
    assert outcome.action.value == 'attend', "SSVC decision should be ATTEND"


def test_decision_none_no_total_high():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='none',
        automatable='no',
        technical_impact='total',
        mission_wellbeing_impact='high'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'medium', "SSVC priority should be MEDIUM"
    assert outcome.action.value == 'track_star', "SSVC decision should be TRACK_STAR"


def test_decision_none_yes_total_high():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='none',
        automatable='yes',
        technical_impact='total',
        mission_wellbeing_impact='high'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'medium', "SSVC priority should be MEDIUM"
    assert outcome.action.value == 'attend', "SSVC decision should be ATTEND"


def test_decision_none_yes_total_low():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='none',
        automatable='yes',
        technical_impact='total',
        mission_wellbeing_impact='low'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'low', "SSVC priority should be LOW"
    assert outcome.action.value == 'track', "SSVC decision should be TRACK"


def test_decision_none_no_partial_high():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='none',
        automatable='no',
        technical_impact='partial',
        mission_wellbeing_impact='high'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'low', "SSVC priority should be LOW"
    assert outcome.action.value == 'track', "SSVC decision should be TRACK"


def test_decision_poc_no_total_high():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='poc',
        automatable='no',
        technical_impact='total',
        mission_wellbeing_impact='high'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'medium', "SSVC priority should be MEDIUM"
    assert outcome.action.value == 'attend', "SSVC decision should be ATTEND"


def test_decision_poc_no_total_medium():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='poc',
        automatable='no',
        technical_impact='total',
        mission_wellbeing_impact='medium'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'medium', "SSVC priority should be MEDIUM"
    assert outcome.action.value == 'track_star', "SSVC decision should be TRACK_STAR"


def test_decision_poc_no_total_low():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='poc',
        automatable='no',
        technical_impact='total',
        mission_wellbeing_impact='low'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'low', "SSVC priority should be LOW"
    assert outcome.action.value == 'track', "SSVC decision should be TRACK"


def test_decision_poc_no_partial_high():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='poc',
        automatable='no',
        technical_impact='partial',
        mission_wellbeing_impact='high'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'medium', "SSVC priority should be MEDIUM"
    assert outcome.action.value == 'track_star', "SSVC decision should be TRACK_STAR"


def test_decision_poc_no_partial_medium():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='poc',
        automatable='no',
        technical_impact='partial',
        mission_wellbeing_impact='medium'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'low', "SSVC priority should be LOW"
    assert outcome.action.value == 'track', "SSVC decision should be TRACK"


def test_decision_poc_yes_partial_high():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='poc',
        automatable='yes',
        technical_impact='partial',
        mission_wellbeing_impact='high'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'medium', "SSVC priority should be MEDIUM"
    assert outcome.action.value == 'attend', "SSVC decision should be ATTEND"


def test_decision_poc_yes_partial_medium():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='poc',
        automatable='yes',
        technical_impact='partial',
        mission_wellbeing_impact='medium'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'low', "SSVC priority should be LOW"
    assert outcome.action.value == 'track', "SSVC decision should be TRACK"


def test_decision_poc_yes_partial_low():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='poc',
        automatable='yes',
        technical_impact='partial',
        mission_wellbeing_impact='low'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'low', "SSVC priority should be LOW"
    assert outcome.action.value == 'track', "SSVC decision should be TRACK"


def test_decision_poc_yes_total_medium():
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='poc',
        automatable='yes',
        technical_impact='total',
        mission_wellbeing_impact='medium'
    )
    outcome = decision.evaluate()
    assert outcome.priority.value == 'medium', "SSVC priority should be MEDIUM"
    assert outcome.action.value == 'track_star', "SSVC decision should be TRACK_STAR"