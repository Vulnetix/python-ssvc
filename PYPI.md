# Python implementation of SSVC (Stakeholder-Specific Vulnerability Categorization)

## Installation

From pypi.org `pip install ssvc`

### Example

To use SSVC:
- Determine the exploitation status of the vulnerability
- Assess the technical impact, considering the automatability

```python
from ssvc import Decision, ExploitationLevel, Automatable, TechnicalImpact, MissionWellbeingImpact, ActionCISA, DecisionPriority
decision = Decision(
    ExploitationLevel.POC,
    Automatable.YES,
    TechnicalImpact.PARTIAL,
    MissionWellbeingImpact.MEDIUM,
)
assert decision.outcome.priority == DecisionPriority.LOW, "SSVC priority should be LOW"
assert decision.outcome.action == ActionCISA.TRACK, "SSVC decision should be TRACK"
```

Using strings also works

```python
import ssvc

decision = ssvc.Decision(
    exploitation='active',
    automatable='no',
    technical_impact='total',
    mission_wellbeing='high',
)
assert decision.outcome.priority == ssvc.DecisionPriority.HIGH, "SSVC priority should be HIGH"
assert decision.outcome.action == ssvc.ActionCISA.ACT, "SSVC decision should be ACT"
```

Input incrementally and control how to handle decisions

```python
from ssvc import Decision, ExploitationLevel, Automatable, TechnicalImpact, MissionWellbeingImpact, ActionCISA, DecisionPriority
decision = Decision()
# what is the ExploitationLevel?
decision.exploitation = ExploitationLevel.POC
# is it Automatable?
decision.automatable = Automatable.YES
# figure out the technical impact
decision.technical_impact = TechnicalImpact.PARTIAL
# Wha't our impact?
decision.mission_wellbeing = MissionWellbeingImpact.MEDIUM

# Get a decision outcome
outcome = decision.evaluate()

# decisions are return and available as a new variable
assert outcome.priority == DecisionPriority.LOW, "SSVC priority should be LOW"
# or use the `decision.outcome` like before
assert decision.outcome.action == ActionCISA.TRACK, "SSVC decision should be TRACK"
```
