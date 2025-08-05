"""
Tests for the new plugin-based SSVC system.
"""

import pytest
import ssvc


def test_list_methodologies():
    """Test that methodologies are properly listed."""
    methodologies = ssvc.list_methodologies()
    assert 'cisa' in methodologies
    assert 'coordinator_triage' in methodologies
    assert len(methodologies) >= 2


def test_get_methodology_info():
    """Test methodology info retrieval."""
    cisa_info = ssvc.get_methodology_info('cisa')
    assert cisa_info is not None
    assert cisa_info['name'] == 'cisa'
    assert 'description' in cisa_info
    
    # Non-existent methodology
    none_info = ssvc.get_methodology_info('nonexistent')
    assert none_info is None


def test_invalid_methodology():
    """Test error handling for invalid methodology."""
    with pytest.raises(ValueError, match="Unknown methodology"):
        ssvc.Decision(methodology='invalid_method')


def test_cisa_methodology_basic():
    """Test basic CISA methodology functionality."""
    decision = ssvc.Decision(
        methodology='cisa',
        exploitation='active',
        automatable='no',
        technical_impact='total',
        mission_wellbeing_impact='high'
    )
    
    assert decision.outcome.action.value == 'act'
    assert decision.outcome.priority.value == 'immediate'


def test_cisa_methodology_incremental():
    """Test incremental input for CISA methodology."""
    decision = ssvc.Decision(methodology='cisa')
    
    # Set attributes incrementally
    decision.exploitation = 'poc'
    decision.automatable = 'yes'
    decision.technical_impact = 'partial'
    decision.mission_wellbeing_impact = 'medium'
    
    # Manual evaluation
    outcome = decision.evaluate()
    assert outcome.action.value == 'track'
    assert outcome.priority.value == 'low'


def test_coordinator_triage_methodology():
    """Test Coordinator Triage methodology."""
    decision = ssvc.Decision(
        methodology='coordinator_triage',
        report_public='no',
        supplier_contacted='yes',
        report_credibility='credible',
        supplier_cardinality='multiple',
        supplier_engagement='active',
        utility='super_effective',
        public_safety_impact='significant'
    )
    
    assert decision.outcome.action.value == 'coordinate'
    assert decision.outcome.priority.value == 'high'


def test_coordinator_triage_decline():
    """Test Coordinator Triage decline path."""
    decision = ssvc.Decision(
        methodology='coordinator_triage',
        report_public='yes',
        supplier_contacted='no',
        report_credibility='not_credible',
        supplier_cardinality='one',
        utility='laborious',
        public_safety_impact='minimal',
        supplier_engagement='active'  # This parameter is required
    )
    
    assert decision.outcome.action.value == 'decline'
    assert decision.outcome.priority.value == 'low'


def test_default_methodology():
    """Test that CISA is the default methodology."""
    decision = ssvc.Decision(
        exploitation='active',
        automatable='yes',
        technical_impact='total',
        mission_wellbeing_impact='high'
    )
    
    assert decision.methodology == 'cisa'
    assert decision.outcome.action.value == 'act'


# Test all CISA decision matrix combinations to ensure comprehensive coverage
class TestCISADecisionMatrix:
    """Comprehensive tests for CISA decision matrix."""
    
    def test_active_yes_total_high(self):
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='active',
            automatable='yes',
            technical_impact='total',
            mission_wellbeing_impact='high'
        )
        assert decision.outcome.action.value == 'act'
        assert decision.outcome.priority.value == 'immediate'
    
    def test_active_yes_total_medium(self):
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='active',
            automatable='yes',
            technical_impact='total',
            mission_wellbeing_impact='medium'
        )
        assert decision.outcome.action.value == 'act'
        assert decision.outcome.priority.value == 'immediate'
    
    def test_active_yes_total_low(self):
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='active',
            automatable='yes',
            technical_impact='total',
            mission_wellbeing_impact='low'
        )
        assert decision.outcome.action.value == 'attend'
        assert decision.outcome.priority.value == 'medium'
    
    def test_active_yes_partial_high(self):
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='active',
            automatable='yes',
            technical_impact='partial',
            mission_wellbeing_impact='high'
        )
        assert decision.outcome.action.value == 'act'
        assert decision.outcome.priority.value == 'immediate'
    
    def test_active_yes_partial_medium(self):
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='active',
            automatable='yes',
            technical_impact='partial',
            mission_wellbeing_impact='medium'
        )
        assert decision.outcome.action.value == 'attend'
        assert decision.outcome.priority.value == 'medium'
    
    def test_active_yes_partial_low(self):
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='active',
            automatable='yes',
            technical_impact='partial',
            mission_wellbeing_impact='low'
        )
        assert decision.outcome.action.value == 'attend'
        assert decision.outcome.priority.value == 'medium'
    
    def test_active_no_total_high(self):
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='active',
            automatable='no',
            technical_impact='total',
            mission_wellbeing_impact='high'
        )
        assert decision.outcome.action.value == 'act'
        assert decision.outcome.priority.value == 'immediate'
    
    def test_active_no_total_medium(self):
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='active',
            automatable='no',
            technical_impact='total',
            mission_wellbeing_impact='medium'
        )
        assert decision.outcome.action.value == 'attend'
        assert decision.outcome.priority.value == 'medium'
    
    def test_active_no_partial_high(self):
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='active',
            automatable='no',
            technical_impact='partial',
            mission_wellbeing_impact='high'
        )
        assert decision.outcome.action.value == 'attend'
        assert decision.outcome.priority.value == 'medium'
    
    def test_poc_yes_total_high(self):
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='poc',
            automatable='yes',
            technical_impact='total',
            mission_wellbeing_impact='high'
        )
        assert decision.outcome.action.value == 'attend'
        assert decision.outcome.priority.value == 'medium'
    
    def test_poc_yes_total_medium(self):
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='poc',
            automatable='yes',
            technical_impact='total',
            mission_wellbeing_impact='medium'
        )
        assert decision.outcome.action.value == 'track_star'
        assert decision.outcome.priority.value == 'medium'
    
    def test_poc_yes_partial_high(self):
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='poc',
            automatable='yes',
            technical_impact='partial',
            mission_wellbeing_impact='high'
        )
        assert decision.outcome.action.value == 'attend'
        assert decision.outcome.priority.value == 'medium'
    
    def test_poc_no_total_high(self):
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='poc',
            automatable='no',
            technical_impact='total',
            mission_wellbeing_impact='high'
        )
        assert decision.outcome.action.value == 'attend'
        assert decision.outcome.priority.value == 'medium'
    
    def test_poc_no_total_medium(self):
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='poc',
            automatable='no',
            technical_impact='total',
            mission_wellbeing_impact='medium'
        )
        assert decision.outcome.action.value == 'track_star'
        assert decision.outcome.priority.value == 'medium'
    
    def test_poc_no_partial_high(self):
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='poc',
            automatable='no',
            technical_impact='partial',
            mission_wellbeing_impact='high'
        )
        assert decision.outcome.action.value == 'track_star'
        assert decision.outcome.priority.value == 'medium'
    
    def test_none_yes_total_high(self):
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='none',
            automatable='yes',
            technical_impact='total',
            mission_wellbeing_impact='high'
        )
        assert decision.outcome.action.value == 'attend'
        assert decision.outcome.priority.value == 'medium'
    
    def test_none_no_total_high(self):
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='none',
            automatable='no',
            technical_impact='total',
            mission_wellbeing_impact='high'
        )
        assert decision.outcome.action.value == 'track_star'
        assert decision.outcome.priority.value == 'medium'
    
    def test_default_track_action(self):
        """Test default action for unmapped paths."""
        decision = ssvc.Decision(
            methodology='cisa',
            exploitation='none',
            automatable='no',
            technical_impact='partial',
            mission_wellbeing_impact='low'
        )
        assert decision.outcome.action.value == 'track'
        assert decision.outcome.priority.value == 'low'


class TestCoordinatorTriageDecisionMatrix:
    """Tests for Coordinator Triage methodology decision patterns."""
    
    def test_coordinate_high_priority(self):
        """Test high-priority coordination scenario."""
        decision = ssvc.Decision(
            methodology='coordinator_triage',
            report_public='no',
            supplier_contacted='yes',
            report_credibility='credible',
            supplier_cardinality='multiple',
            supplier_engagement='active',
            utility='super_effective',
            public_safety_impact='significant'
        )
        assert decision.outcome.action.value == 'coordinate'
        assert decision.outcome.priority.value == 'high'
    
    def test_track_medium_priority(self):
        """Test medium-priority tracking scenario."""
        decision = ssvc.Decision(
            methodology='coordinator_triage',
            report_public='no',
            supplier_contacted='yes',
            report_credibility='credible',
            supplier_cardinality='multiple',
            supplier_engagement='active',
            utility='efficient',
            public_safety_impact='minimal'
        )
        assert decision.outcome.action.value == 'track'
        assert decision.outcome.priority.value == 'medium'
    
    def test_decline_low_priority(self):
        """Test low-priority decline scenario."""
        decision = ssvc.Decision(
            methodology='coordinator_triage',
            report_public='yes',
            supplier_contacted='no',
            report_credibility='not_credible',
            supplier_cardinality='one',
            supplier_engagement='unresponsive',
            utility='laborious',
            public_safety_impact='minimal'
        )
        assert decision.outcome.action.value == 'decline'
        assert decision.outcome.priority.value == 'low'