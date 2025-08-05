# Python implementation of SSVC (Stakeholder-Specific Vulnerability Categorization)

This library now supports multiple SSVC methodologies through a plugin-based architecture. You can use the built-in methodologies or create your own.

The SSVC framework was developed by the CERT/CC Software Engineering Institute at Carnegie Mellon University. More information can be found at https://certcc.github.io/SSVC/

## Installation

From pypi.org `pip install ssvc`

### Available Methodologies

- **CISA**: The CISA Stakeholder-Specific Vulnerability Categorization methodology
- **Coordinator Triage**: The CERT/CC Coordinator Triage Decision Model
- **Supplier Decision Model**: The CERT/CC Supplier Decision Model for prioritizing patch creation
- **Deployer Decision Model**: The CERT/CC Deployer Decision Model for prioritizing patch deployment
- **Coordinator Publication Decision Model**: The CERT/CC Coordinator Publication Decision Model for determining vulnerability disclosure

### Quick Start

```python
import ssvc

# List available methodologies
print("Available methodologies:", ssvc.list_methodologies())

# Use CISA methodology (default)
decision = ssvc.Decision(
    methodology='cisa',  # or omit for default
    exploitation='active',
    automatable='no',
    technical_impact='total',
    mission_wellbeing_impact='high'
)
print(f"CISA Decision: {decision.outcome.action.value} (Priority: {decision.outcome.priority.value})")

# Use Coordinator Triage methodology
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
print(f"Coordinator Triage Decision: {decision.outcome.action.value} (Priority: {decision.outcome.priority.value})")

# Use Supplier Decision Model
decision = ssvc.Decision(
    methodology='supplier',
    exploitation='active',
    utility='super_effective',
    technical_impact='total',
    public_safety_impact='significant'
)
print(f"Supplier Decision: {decision.outcome.action.value} (Priority: {decision.outcome.priority.value})")

# Use Deployer Decision Model
decision = ssvc.Decision(
    methodology='deployer',
    exploitation='active',
    system_exposure='open',
    utility='super_effective',
    human_impact='very_high'
)
print(f"Deployer Decision: {decision.outcome.action.value} (Priority: {decision.outcome.priority.value})")

# Use Coordinator Publication Decision Model
decision = ssvc.Decision(
    methodology='coordinator_publication',
    supplier_involvement='uncooperative_unresponsive',
    exploitation='active',
    public_value_added='precedence'
)
print(f"Coordinator Publication Decision: {decision.outcome.action.value} (Priority: {decision.outcome.priority.value})")
```

### CISA Methodology Examples

The CISA methodology follows these steps:
1. Determine the exploitation status of the vulnerability
2. Assess the technical impact, considering the automatability, mission prevalence, and public well-being impact  
3. Navigate through the decision tree to arrive at a decision point: Track, Track*, Attend, or Act

```python
import ssvc

# Using enum-style values
decision = ssvc.Decision(
    methodology='cisa',
    exploitation='poc',
    automatable='yes', 
    technical_impact='partial',
    mission_wellbeing_impact='medium'
)
assert decision.outcome.action.value == 'track'
assert decision.outcome.priority.value == 'low'

# Incremental input 
decision = ssvc.Decision(methodology='cisa')
decision.exploitation = 'active'
decision.automatable = 'yes'
decision.technical_impact = 'total' 
decision.mission_wellbeing_impact = 'high'

outcome = decision.evaluate()
assert outcome.action.value == 'act'
assert outcome.priority.value == 'immediate'
```

### Coordinator Triage Methodology Examples

The Coordinator Triage methodology evaluates whether a vulnerability coordination center should coordinate disclosure:

```python
import ssvc

# High-priority coordination case
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

# Low-priority decline case
decision = ssvc.Decision(
    methodology='coordinator_triage', 
    report_public='yes',
    supplier_contacted='no',
    report_credibility='not_credible',
    supplier_cardinality='one',
    utility='laborious',
    public_safety_impact='minimal'
)
assert decision.outcome.action.value == 'decline'
assert decision.outcome.priority.value == 'low'
```

## Creating New Methodologies

This library supports extensible methodologies through a YAML-based plugin system. You can create your own decision methodologies by defining them in YAML format and generating Python plugins.

### YAML Methodology Structure

Each methodology is defined in a YAML file with the following structure:

```yaml
name: "Your Methodology Name"
description: "Description of your methodology"
version: "1.0"
url: "https://example.com/methodology-docs"

enums:
  DecisionPointName:
    - VALUE_ONE
    - VALUE_TWO
    - VALUE_THREE
  AnotherDecisionPoint:
    - OPTION_A
    - OPTION_B
  ActionType:
    - ACTION_ONE
    - ACTION_TWO
    - ACTION_THREE
  DecisionPriorityLevel:
    - LOW
    - MEDIUM
    - HIGH

priorityMap:
  ACTION_ONE: LOW
  ACTION_TWO: MEDIUM
  ACTION_THREE: HIGH

decisionTree:
  type: DecisionPointName
  children:
    VALUE_ONE:
      type: AnotherDecisionPoint
      children:
        OPTION_A: ACTION_ONE
        OPTION_B: ACTION_TWO
    VALUE_TWO: ACTION_THREE
    VALUE_THREE:
      type: AnotherDecisionPoint
      children:
        OPTION_A: ACTION_TWO
        OPTION_B: ACTION_THREE

defaultAction: ACTION_ONE
```

### Required YAML Elements

1. **Metadata Fields**:
   - `name`: Human-readable name for the methodology
   - `description`: Brief description of the methodology's purpose  
   - `version`: Version string (e.g., "1.0")
   - `url`: Reference URL for methodology documentation

2. **enums Section**:
   - Define all decision points as enum classes
   - Must include `ActionType` enum for possible actions
   - Must include a priority enum (ending with "PriorityLevel")
   - Use UPPERCASE values for enum entries
   - Quote boolean-like values: `"YES"` and `"NO"` instead of `YES` and `NO`

3. **priorityMap Section**:
   - Maps each action to a priority level
   - Keys must match `ActionType` enum values
   - Values must match the priority enum values

4. **decisionTree Section**:
   - Defines the decision tree structure
   - Each node has a `type` (enum name) and `children` (possible values)
   - Leaf nodes contain action names directly
   - Non-leaf nodes contain nested decision structures

5. **defaultAction**:
   - Fallback action for unmapped decision paths
   - Must match an `ActionType` enum value

### Example: Custom Risk Assessment Methodology

```yaml
name: "Custom Risk Assessment"
description: "A simplified risk-based vulnerability assessment methodology"
version: "1.0"
url: "https://example.com/custom-risk-methodology"

enums:
  SeverityLevel:
    - LOW
    - MEDIUM
    - HIGH
    - CRITICAL
  ExposureLevel:
    - INTERNAL
    - EXTERNAL
  BusinessImpactLevel:
    - MINIMAL
    - MODERATE
    - SIGNIFICANT
  ActionType:
    - MONITOR
    - SCHEDULE
    - EXPEDITE
    - EMERGENCY
  DecisionPriorityLevel:
    - LOW
    - MEDIUM
    - HIGH
    - CRITICAL

priorityMap:
  MONITOR: LOW
  SCHEDULE: MEDIUM
  EXPEDITE: HIGH
  EMERGENCY: CRITICAL

decisionTree:
  type: SeverityLevel
  children:
    CRITICAL:
      type: ExposureLevel
      children:
        EXTERNAL: EMERGENCY
        INTERNAL:
          type: BusinessImpactLevel
          children:
            SIGNIFICANT: EMERGENCY
            MODERATE: EXPEDITE
            MINIMAL: SCHEDULE
    HIGH:
      type: ExposureLevel
      children:
        EXTERNAL:
          type: BusinessImpactLevel
          children:
            SIGNIFICANT: EXPEDITE
            MODERATE: SCHEDULE
            MINIMAL: SCHEDULE
        INTERNAL: SCHEDULE
    MEDIUM: SCHEDULE
    LOW: MONITOR

defaultAction: MONITOR
```

### Generating Plugins from YAML

1. **Place YAML files** in `src/ssvc/methodologies/`
2. **Run the generator**:
   ```bash
   python scripts/generate_plugins.py
   ```
3. **Generated files**:
   - Python plugin: `src/ssvc/plugins/{methodology_name}.py`
   - Documentation: `docs/{methodology_name}.md`

The generator creates:
- Enum classes for all decision points
- Priority mapping dictionary
- Outcome class with priority/action mapping
- Decision class with parameter validation
- Decision tree traversal logic
- Markdown documentation with mermaid diagrams

### Plugin Registration

Plugins are automatically discovered and registered when the library loads. The plugin system:

1. **Auto-discovery**: Scans the `src/ssvc/plugins/` directory
2. **Registration**: Registers Decision classes found in plugin modules
3. **Usage**: Access via `ssvc.Decision(methodology='plugin_name')`
