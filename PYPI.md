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

## Available Methodologies

This library supports multiple SSVC methodologies through a plugin-based architecture:

| Methodology | Description | Documentation | Official Source |
|-------------|-------------|---------------|-----------------|
| **CISA** | CISA Stakeholder-Specific Vulnerability Categorization | [docs/cisa.md](https://github.com/Vulnetix/python-ssvc/blob/main/docs/cisa.md) | [CISA SSVC](https://www.cisa.gov/stakeholder-specific-vulnerability-categorization-ssvc) |
| **Coordinator Triage** | CERT/CC Coordinator Triage Decision Model | [docs/coordinator_triage.md](https://github.com/Vulnetix/python-ssvc/blob/main/docs/coordinator_triage.md) | [CERT/CC Coordinator Triage](https://certcc.github.io/SSVC/howto/coordination_triage_decision/) |
| **Coordinator Publication** | CERT/CC Coordinator Publication Decision Model | [docs/coordinator_publication.md](https://github.com/Vulnetix/python-ssvc/blob/main/docs/coordinator_publication.md) | [CERT/CC Publication Decision](https://certcc.github.io/SSVC/howto/publication_decision/) |
| **Supplier** | CERT/CC Supplier Decision Model | [docs/supplier.md](https://github.com/Vulnetix/python-ssvc/blob/main/docs/supplier.md) | [CERT/CC Supplier Tree](https://certcc.github.io/SSVC/howto/supplier_tree/) |
| **Deployer** | CERT/CC Deployer Decision Model | [docs/deployer.md](https://github.com/Vulnetix/python-ssvc/blob/main/docs/deployer.md) | [CERT/CC Deployer Tree](https://certcc.github.io/SSVC/howto/deployer_tree/) |

## Quick Start

```python
import ssvc

# List available methodologies
print("Available methodologies:", ssvc.list_methodologies())

# Use CISA methodology
decision = ssvc.Decision(
    methodology='cisa',
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
    utility='super_effective',
    public_safety_impact='significant'
)
print(f"Coordinator Triage Decision: {decision.outcome.action.value} (Priority: {decision.outcome.priority.value})")
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

Licensed under the Apache License 2.0. See [LICENSE](https://github.com/Vulnetix/python-ssvc/blob/main/LICENSE) for details.