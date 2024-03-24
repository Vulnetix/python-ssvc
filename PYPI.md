# Python implementation of SSVC (Stakeholder-Specific Vulnerability Categorization)

## Installation

From pypi.org `pip install ssvc`

From source

```bash
git clone https://github.com/chrisdlangton/py-cisa-ssvc.git
cd py-cisa-ssvc
python3.12 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e '.[dev]'
```

### Example

To use SSVC:
- Determine the exploitation status of the vulnerability
- Assess the technical impact, considering the automatability

```python
from ssvc import Decision, ExploitationLevel, Automatable, TechnicalImpact, MissionWellbeingImpact, DecisionAction
result = Decision(
    ExploitationLevel.POC,
    Automatable.YES,
    TechnicalImpact.PARTIAL,
    MissionWellbeingImpact.MEDIUM,
).outcome
assert result.impact == MissionWellbeingImpact.LOW, "SSVC decision should be LOW"
assert result.action == DecisionAction.TRACK, "SSVC decision should be TRACK"
```

Using strings also works

```python
import ssvc

result: ssvc.DecisionOutcome = ssvc.Decision(
    exploitation='active',
    automatable='no',
    technical_impact='total',
    mission_wellbeing='high',
).outcome
assert result.impact == ssvc.MissionWellbeingImpact.HIGH, "SSVC decision should be HIGH"
assert result.action == ssvc.DecisionAction.ACT, "SSVC decision should be ACT"
```