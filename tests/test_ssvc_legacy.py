"""
Legacy tests for backward compatibility.
These tests ensure the old API still works but with deprecation warnings.
"""

import pytest
import warnings
import ssvc
from ssvc import (
    ExploitationLevel,
    Automatable,
    TechnicalImpact,
    MissionWellbeingImpact,
    ActionCISA,
    DecisionPriority,
    LegacyDecision,
)


@pytest.mark.xfail(raises=AttributeError)
def test_negative_evaluate_no_attributes():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        decision = LegacyDecision()
        decision.evaluate()


@pytest.mark.xfail(raises=AttributeError)
def test_negative_evaluate_attribute_exploitation():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        decision = LegacyDecision()
        decision.exploitation = ExploitationLevel.POC
        decision.evaluate()


@pytest.mark.xfail(raises=AttributeError)
def test_negative_evaluate_attribute_automatable():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        decision = LegacyDecision()
        decision.exploitation = ExploitationLevel.POC
        decision.automatable = Automatable.YES
        decision.evaluate()


@pytest.mark.xfail(raises=AttributeError)
def test_negative_evaluate_attribute_technical_impact():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        decision = LegacyDecision()
        decision.exploitation = ExploitationLevel.POC
        decision.automatable = Automatable.YES
        decision.technical_impact = TechnicalImpact.TOTAL
        decision.evaluate()


def test_legacy_decision_basic():
    """Test basic legacy decision functionality."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        decision = LegacyDecision(
            ExploitationLevel.ACTIVE,
            Automatable.NO,
            TechnicalImpact.TOTAL,
            MissionWellbeingImpact.HIGH,
        )
        assert decision.outcome.priority == DecisionPriority.IMMEDIATE
        assert decision.outcome.action == ActionCISA.ACT


def test_legacy_string_inputs():
    """Test legacy decision with string inputs."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        decision = LegacyDecision(
            exploitation="active",
            automatable="no",
            technical_impact="total",
            mission_wellbeing="high",
        )
        assert decision.outcome.priority == DecisionPriority.IMMEDIATE
        assert decision.outcome.action == ActionCISA.ACT


def test_deprecation_warning():
    """Test that LegacyDecision raises deprecation warning."""
    with pytest.warns(DeprecationWarning, match="LegacyDecision is deprecated"):
        LegacyDecision(
            ExploitationLevel.ACTIVE,
            Automatable.NO,
            TechnicalImpact.TOTAL,
            MissionWellbeingImpact.HIGH,
        )


def test_legacy_incremental():
    """Test legacy incremental decision setting."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        decision = LegacyDecision()
        decision.exploitation = ExploitationLevel.POC
        decision.automatable = Automatable.YES
        decision.technical_impact = TechnicalImpact.PARTIAL
        decision.mission_wellbeing = MissionWellbeingImpact.MEDIUM
        
        outcome = decision.evaluate()
        assert outcome.priority == DecisionPriority.LOW
        assert outcome.action == ActionCISA.TRACK