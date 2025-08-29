# Python implementation of SSVC (Stakeholder-Specific Vulnerability Categorization)

A comprehensive Python library implementing the Stakeholder-Specific Vulnerability Categorization (SSVC) framework with a plugin-based architecture supporting multiple decision methodologies.

The SSVC framework was developed by the CERT/CC Software Engineering Institute at Carnegie Mellon University. More information can be found at https://certcc.github.io/SSVC/

## Installation

### Via Package Managers

```bash
# Using pip
pip install ssvc

# Using uv (recommended)
uv add ssvc

# Using Poetry
poetry add ssvc

# Using Pipenv
pipenv install ssvc

# Using Conda
conda install -c conda-forge ssvc
```

### From Source

```bash
# Clone and install from GitHub
git clone https://github.com/Vulnetix/python-ssvc.git
cd python-ssvc
uv sync
uv run python -m pip install -e .
```

## 🤖 AI Methodology Update Notice

**New AI Methodology Available!** We've recently added support for an AI-specific SSVC methodology designed for vulnerability assessment in artificial intelligence systems. This methodology addresses unique AI security considerations including:

- **Model Exploitation**: Assessment of AI model-specific attack vectors
- **Training Data Impact**: Evaluation of vulnerabilities in training datasets  
- **AI Safety Concerns**: Consideration of AI alignment and safety risks
- **Automated Decision Impact**: Assessment of consequences from AI-driven decisions

The AI methodology is available alongside traditional cybersecurity methodologies and uses the same simple API. See the [AI methodology documentation](docs/ai.md) for complete usage examples and decision trees.

## Available Methodologies

This library supports multiple SSVC methodologies through a plugin-based architecture:

| Methodology | Description | Documentation | Official Source |
|-------------|-------------|---------------|-----------------|
| **AI LLM Triage** | AI-specific vulnerability categorization for ML systems | [docs/ai_llm_triage.md](docs/ai_llm_triage.md) | [NIST AI Risk Management](https://www.nist.gov/ai-risk-management) |
| **CISA** | CISA Stakeholder-Specific Vulnerability Categorization | [docs/cisa.md](docs/cisa.md) | [CISA SSVC](https://www.cisa.gov/stakeholder-specific-vulnerability-categorization-ssvc) |
| **Coordinator Triage** | CERT/CC Coordinator Triage Decision Model | [docs/coordinator_triage.md](docs/coordinator_triage.md) | [CERT/CC Coordinator Triage](https://certcc.github.io/SSVC/howto/coordination_triage_decision/) |
| **Coordinator Publication** | CERT/CC Coordinator Publication Decision Model | [docs/coordinator_publication.md](docs/coordinator_publication.md) | [CERT/CC Publication Decision](https://certcc.github.io/SSVC/howto/publication_decision/) |
| **Supplier** | CERT/CC Supplier Decision Model | [docs/supplier.md](docs/supplier.md) | [CERT/CC Supplier Tree](https://certcc.github.io/SSVC/howto/supplier_tree/) |
| **Deployer** | CERT/CC Deployer Decision Model | [docs/deployer.md](docs/deployer.md) | [CERT/CC Deployer Tree](https://certcc.github.io/SSVC/howto/deployer_tree/) |

## Complete Example

Here's a comprehensive example showing the library's key features:

```python
import ssvc

# 1. List all available methodologies
print("Available SSVC methodologies:")
for methodology in ssvc.list_methodologies():
    print(f"  - {methodology}")

# 2. CISA methodology for enterprise vulnerability management
print("\n=== CISA Enterprise Assessment ===")
cisa_decision = ssvc.Decision(
    methodology='cisa',
    exploitation='active',           # Exploits available in the wild
    automatable='yes',              # Can be automated by attackers
    technical_impact='total',       # Complete system compromise possible
    mission_wellbeing_impact='high' # Significant organizational impact
)

print(f"Decision: {cisa_decision.outcome.action.value}")
print(f"Priority: {cisa_decision.outcome.priority.value}")
print(f"Vector: {cisa_decision.to_vector()}")

# 3. Coordinator triage for vulnerability disclosure
print("\n=== Coordinator Triage Assessment ===")
coord_decision = ssvc.Decision(
    methodology='coordinator_triage',
    report_public='no',              # Report not yet public
    supplier_contacted='yes',        # Vendor has been notified
    report_credibility='credible',   # Report appears legitimate
    supplier_cardinality='multiple', # Affects multiple vendors
    utility='super_effective',       # High exploit utility for attackers
    public_safety_impact='significant' # Could impact public safety
)

print(f"Decision: {coord_decision.outcome.action.value}")
print(f"Priority: {coord_decision.outcome.priority.value}")

# 4. Supplier assessment for patch development prioritization
print("\n=== Supplier Patch Development ===")
supplier_decision = ssvc.Decision(
    methodology='supplier',
    exploitation='poc',              # Proof of concept exists
    utility='efficient',            # Moderately useful to attackers
    technical_impact='partial',     # Limited system access
    public_safety_impact='minimal'  # Low public safety risk
)

print(f"Decision: {supplier_decision.outcome.action.value}")
print(f"Priority: {supplier_decision.outcome.priority.value}")

# 5. Vector string parsing and data exchange
print("\n=== Vector String Operations ===")
vector_string = cisa_decision.to_vector()
print(f"Generated vector: {vector_string}")

# Parse the vector back into a decision
parsed_decision = ssvc.Decision.from_vector(vector_string)
print(f"Parsed action: {parsed_decision.outcome.action.value}")
print(f"Decisions match: {cisa_decision.outcome.action == parsed_decision.outcome.action}")

# 6. Error handling and validation
print("\n=== Input Validation ===")
try:
    invalid_decision = ssvc.Decision('cisa', exploitation='invalid_value')
except ValueError as e:
    print(f"Validation error caught: {e}")

# 7. Case-insensitive input handling
print("\n=== Case-Insensitive Input ===")
flexible_decision = ssvc.Decision(
    methodology='CISA',              # Uppercase methodology
    exploitation='ACTIVE',          # Uppercase parameters
    automatable='No',               # Mixed case
    technical_impact='total',       # Lowercase
    mission_wellbeing_impact='HIGH' # Uppercase
)
print(f"Flexible input result: {flexible_decision.outcome.action.value}")
```

**Output:**
```
Available SSVC methodologies:
  - cisa
  - coordinator_triage
  - coordinator_publication
  - supplier
  - deployer

=== CISA Enterprise Assessment ===
Decision: act
Priority: immediate
Vector: CISAv1/E:A/A:Y/T:T/M:H/2025-08-29T17:53:26.057876/

=== Coordinator Triage Assessment ===
Decision: coordinate
Priority: high

=== Supplier Patch Development ===
Decision: scheduled
Priority: medium

=== Vector String Operations ===
Generated vector: CISAv1/E:A/A:Y/T:T/M:H/2025-08-29T17:53:26.057876/
Parsed action: act
Decisions match: True

=== Input Validation ===
Validation error caught: 'INVALID_VALUE' is not a valid ExploitationStatus

=== Case-Insensitive Input ===
Flexible input result: act
```

## Key Features

### SSVC Vector Strings
All methodologies support vector strings for compact representation:

```python
import ssvc

# Generate vector string
decision = ssvc.Decision('cisa',
    exploitation='active',
    automatable='yes', 
    technical_impact='total',
    mission_wellbeing_impact='high'
)
vector = decision.to_vector()
# Output: CISAv1/E:A/A:Y/T:T/M:H/2024-07-23T20:34:21.000000/

# Parse vector string
parsed = ssvc.Decision.from_vector(vector)
outcome = parsed.evaluate()
```

### Schema Validation
All methodology definitions are validated against a JSON schema:

```python
# Methodologies are defined in YAML and validated against schema.json
# See: src/ssvc/methodologies/schema.json
```

### Plugin System
Create custom methodologies using YAML definitions:

1. Define methodology in YAML format
2. Place in `src/ssvc/methodologies/`
3. Run `python scripts/generate_plugins.py`
4. Generated plugin becomes available via `ssvc.Decision(methodology='custom')`

## Language Implementations

SSVC is available in multiple programming languages:

- **Python**: This library - [python-ssvc](https://github.com/Vulnetix/python-ssvc)
- **TypeScript**: [typescript-ssvc](https://github.com/Vulnetix/typescript-ssvc)
- **Go**: 🚧 In Development

## Contributing

We welcome contributions! To add new methodologies or improve the library:

### Adding New Methodologies

1. **Fork the repository** on [GitHub](https://github.com/Vulnetix/python-ssvc)
2. **Create YAML definition** following the schema structure
3. **Generate plugin** using the built-in generator
4. **Add comprehensive tests** with 100% coverage
5. **Submit Pull Request** with:
   - YAML methodology definition
   - Generated plugin code
   - Complete test suite
   - Documentation updates
   - Links to official methodology sources

### Plugin Development

The plugin system supports extensible methodologies through YAML:

```yaml
name: "Your Methodology"
description: "Description of your methodology"
version: "1.0"
url: "https://example.com/methodology-docs"

enums:
  DecisionPoint:
    - VALUE_ONE
    - VALUE_TWO
  ActionType:
    - ACTION_ONE
    - ACTION_TWO

priorityMap:
  ACTION_ONE: LOW
  ACTION_TWO: HIGH

decisionTree:
  type: DecisionPoint
  children:
    VALUE_ONE: ACTION_ONE
    VALUE_TWO: ACTION_TWO

defaultAction: ACTION_ONE
```

### Development Setup

```bash
git clone https://github.com/Vulnetix/python-ssvc.git
cd python-ssvc
uv sync
uv run python -c "import ssvc; print('SSVC ready for development!')"
```

### Testing

```bash
# Run tests
uv run pytest --cov

# Validate YAML files
uv run python scripts/validate_methodologies.py

# Generate plugins
uv run python scripts/generate_plugins.py
```

## Links

- **Documentation**: [GitHub Repository](https://github.com/Vulnetix/python-ssvc)
- **Issues & Bug Reports**: [GitHub Issues](https://github.com/Vulnetix/python-ssvc/issues)
- **Official SSVC**: [certcc.github.io/SSVC](https://certcc.github.io/SSVC/)

## License

Licensed under the Apache License 2.0. See [LICENSE](./LICENSE) for details.