#!/usr/bin/env python3
"""
SSVC Plugin Generator

Generates Python plugin modules from YAML decision tree definitions.
Also generates markdown documentation with mermaid diagrams.
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, List
from textwrap import dedent, indent


class SSVCPluginGenerator:
    def __init__(self, yaml_dir: Path, output_dir: Path, docs_dir: Path):
        self.yaml_dir = yaml_dir
        self.output_dir = output_dir
        self.docs_dir = docs_dir
        
    def generate_all(self):
        """Generate all plugins from YAML files in the methodologies directory."""
        yaml_files = list(self.yaml_dir.glob("*.yaml"))
        
        for yaml_file in yaml_files:
            print(f"Processing {yaml_file.name}...")
            self.generate_plugin(yaml_file)
            
    def generate_plugin(self, yaml_file: Path):
        """Generate a single plugin from a YAML file."""
        with open(yaml_file, 'r') as f:
            config = yaml.safe_load(f)
            
        plugin_name = yaml_file.stem
        
        # Generate Python plugin
        python_code = self._generate_python_plugin(config, plugin_name)
        python_file = self.output_dir / f"{plugin_name}.py"
        with open(python_file, 'w') as f:
            f.write(python_code)
            
        # Generate markdown documentation
        markdown_code = self._generate_markdown_docs(config, plugin_name)
        docs_file = self.docs_dir / f"{plugin_name}.md"
        with open(docs_file, 'w') as f:
            f.write(markdown_code)
            
        print(f"Generated {python_file} and {docs_file}")
        
    def _generate_python_plugin(self, config: Dict[str, Any], plugin_name: str) -> str:
        """Generate Python plugin code from YAML configuration."""
        
        # Generate enum classes
        enums_code = self._generate_enums(config['enums'])
        
        # Generate priority map
        priority_map_code = self._generate_priority_map(config['priorityMap'], config['enums'])
        
        # Generate outcome class
        outcome_class_code = self._generate_outcome_class(plugin_name)
        
        # Generate main decision class
        decision_class_code = self._generate_decision_class(config, plugin_name)
        
        # Combine all parts
        return f'''"""
{config['name']} Plugin

{config['description']}
Generated from YAML configuration.
"""

from enum import Enum
from typing import Dict, Any, Optional


{enums_code}


{priority_map_code}


{outcome_class_code}


{decision_class_code}'''
        
    def _generate_enums(self, enums: Dict[str, List[str]]) -> str:
        """Generate enum class definitions."""
        enum_classes = []
        
        for enum_name, values in enums.items():
            enum_values = []
            for value in values:
                # Handle boolean values and other types that YAML might parse
                if isinstance(value, bool):
                    value_str = "YES" if value else "NO"
                    lower_str = "yes" if value else "no"
                else:
                    value_str = str(value)
                    lower_str = str(value).lower()
                enum_values.append(f'    {value_str} = "{lower_str}"')
                
            enum_class = f"class {enum_name}(Enum):\n" + "\n".join(enum_values)
            enum_classes.append(enum_class)
            
        return "\n\n".join(enum_classes)
        
    def _generate_priority_map(self, priority_map: Dict[str, str], enums: Dict[str, List[str]]) -> str:
        """Generate priority mapping dictionary."""
        
        # Find action and priority enum names
        action_enum = None
        priority_enum = None
        
        for enum_name, values in enums.items():
            if 'ActionType' in enum_name or enum_name == 'ActionType':
                action_enum = enum_name
            elif 'Priority' in enum_name or enum_name.endswith('PriorityLevel'):
                priority_enum = enum_name
                
        if not action_enum or not priority_enum:
            raise ValueError(f"Could not find ActionType and Priority enums. Available enums: {list(enums.keys())}")
            
        mappings = []
        for action, priority in priority_map.items():
            mappings.append(f"    {action_enum}.{action}: {priority_enum}.{priority}")
            
        return f"priority_map = {{\n" + ",\n".join(mappings) + "\n}"
        
    def _generate_outcome_class(self, plugin_name: str) -> str:
        """Generate outcome class."""
        class_name = f"Outcome{plugin_name.title().replace('_', '')}"
        
        return f"""class {class_name}:
    def __init__(self, action):
        self.priority = priority_map[action]
        self.action = action"""
        
    def _generate_decision_class(self, config: Dict[str, Any], plugin_name: str) -> str:
        """Generate main decision class."""
        
        class_name = f"Decision{plugin_name.title().replace('_', '')}"
        outcome_class = f"Outcome{plugin_name.title().replace('_', '')}"
        
        # Get decision point enums (exclude ActionType and Priority)
        decision_enums = []
        for enum_name in config['enums'].keys():
            if 'ActionType' not in enum_name and 'Priority' not in enum_name:
                decision_enums.append(enum_name)
        
        # Generate constructor parameters
        params = []
        type_conversions = []
        attributes = []
        validations = []
        
        for enum_name in decision_enums:
            param_name = self._enum_to_param_name(enum_name)
            params.append(f"{param_name}: {enum_name} | str = None")
            
            type_conversions.append(f"        if isinstance({param_name}, str):")
            type_conversions.append(f"            {param_name} = {enum_name}({param_name})")
            
            attributes.append(f"        self.{param_name} = {param_name}")
            validations.append(f"self.{param_name} is not None")
        
        # Generate decision tree traversal
        tree_method = self._generate_decision_tree_method(config['decisionTree'], config.get('defaultAction', 'TRACK'))
        
        constructor_code = f"""class {class_name}:
    def __init__(self, {", ".join(params)}):
{chr(10).join(type_conversions)}
        
{chr(10).join(attributes)}
        
        # Always try to evaluate if we have the minimum required parameters
        if all([{", ".join(validations)}]):
            self.outcome = self.evaluate()

    def evaluate(self) -> {outcome_class}:
        action = self._traverse_tree()
        self.outcome = {outcome_class}(action)
        return self.outcome

{tree_method}"""
        
        return constructor_code
    
    def _enum_to_param_name(self, enum_name: str) -> str:
        """Convert enum name to parameter name."""
        # Remove common suffixes and convert to snake_case
        param_name = enum_name.replace('Status', '').replace('Level', '').replace('_', '')
        
        # Convert CamelCase to snake_case
        result = []
        for i, char in enumerate(param_name):
            if i > 0 and char.isupper():
                result.append('_')
            result.append(char.lower())
            
        return ''.join(result)
        
    def _generate_decision_tree_method(self, tree: Dict[str, Any], default_action: str) -> str:
        """Generate decision tree traversal method."""
        
        def generate_traversal_code(node: Dict[str, Any], depth: int = 2) -> str:
            indent_str = "    " * depth
            
            if isinstance(node, str):
                # Leaf node - return action
                return f"{indent_str}return ActionType.{node}"
                
            node_type = node['type']
            children = node['children']
            
            param_name = self._enum_to_param_name(node_type)
            
            code_lines = []
            
            for i, (value, child_node) in enumerate(children.items()):
                condition = "if" if i == 0 else "elif" 
                # Handle enum values correctly
                # Convert YAML boolean values to proper enum values
                if isinstance(value, bool):
                    enum_value = "YES" if value else "NO"
                else:
                    enum_value = value
                code_lines.append(f"{indent_str}{condition} self.{param_name} == {node_type}.{enum_value}:")
                
                if isinstance(child_node, str):
                    # Direct action
                    code_lines.append(f"{indent_str}    return ActionType.{child_node}")
                else:
                    # Recursive traversal
                    child_code = generate_traversal_code(child_node, depth + 1)
                    code_lines.append(child_code)
                    
            return "\n".join(code_lines)
            
        traversal_code = generate_traversal_code(tree)
        
        return f"""    def _traverse_tree(self):
        \"\"\"Traverse the decision tree to determine the outcome.\"\"\"
{traversal_code}
        
        # Default action for unmapped paths
        return ActionType.{default_action}"""
        
    def _generate_markdown_docs(self, config: Dict[str, Any], plugin_name: str) -> str:
        """Generate markdown documentation with mermaid diagram."""
        
        # Generate mermaid diagram
        mermaid_code = self._generate_mermaid_diagram(config['decisionTree'])
        
        # Generate enum documentation
        enum_docs = self._generate_enum_docs(config['enums'])
        
        return f"""# {config['name']} Decision Model

{config['description']}

**Version:** {config['version']}  
**Reference:** [{config['url']}]({config['url']})

## Decision Tree

```mermaid
{mermaid_code}
```

## Decision Points

{enum_docs}

## Usage

```python
from ssvc.plugins.{plugin_name} import Decision{plugin_name.title().replace('_', '')}

decision = Decision{plugin_name.title().replace('_', '')}(
    # Set decision point values here
)

outcome = decision.evaluate()
print(f"Action: {{outcome.action}}")
print(f"Priority: {{outcome.priority}}")
```"""
        
    def _generate_mermaid_diagram(self, tree: Dict[str, Any]) -> str:
        """Generate a proper left-to-right mermaid decision tree diagram showing all paths."""
        
        lines = ["flowchart LR"]
        node_counter = 0
        
        def get_node_id(node_type, value=None):
            nonlocal node_counter
            node_counter += 1
            if value is not None:
                # For decision nodes, include the value to make them unique
                return f"{node_type}_{value}_{node_counter}"
            else:
                # For action nodes
                return f"{node_type}_{node_counter}"
        
        def traverse_tree(node, parent_id=None, edge_label=None):
            if isinstance(node, str):
                # Leaf node - action
                action_id = get_node_id(f"Action_{node}")
                lines.append(f"    {action_id}[{node}]")
                if parent_id:
                    lines.append(f"    {parent_id} -->|{edge_label}| {action_id}")
                return action_id
            
            # Decision node
            node_type = node['type']
            children = node['children']
            
            # Create node for this decision point
            decision_id = get_node_id(node_type)
            lines.append(f"    {decision_id}{{{node_type}}}")
            
            # Connect to parent if exists
            if parent_id:
                lines.append(f"    {parent_id} -->|{edge_label}| {decision_id}")
            
            # Process children
            for value, child_node in children.items():
                traverse_tree(child_node, decision_id, value)
            
            return decision_id
        
        # Start traversal from root
        traverse_tree(tree)
        
        return "\n".join(lines)
        
    def _generate_enum_docs(self, enums: Dict[str, List[str]]) -> str:
        """Generate documentation for enums."""
        
        docs = []
        for enum_name, values in enums.items():
            if 'ActionType' in enum_name or 'Priority' in enum_name:
                continue
                
            value_list = ", ".join([f"`{v}`" for v in values])
            docs.append(f"- **{enum_name}**: {value_list}")
            
        return "\n".join(docs)


def main():
    """Main entry point for the generator."""
    
    # Setup paths
    root_dir = Path(__file__).parent.parent
    yaml_dir = root_dir / "src" / "ssvc" / "methodologies"
    output_dir = root_dir / "src" / "ssvc" / "plugins"
    docs_dir = root_dir / "docs"
    
    # Create output directories
    output_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py in plugins directory
    init_file = output_dir / "__init__.py"
    with open(init_file, 'w') as f:
        f.write('"""SSVC Plugins generated from YAML configurations."""\n')
    
    # Generate plugins
    generator = SSVCPluginGenerator(yaml_dir, output_dir, docs_dir)
    generator.generate_all()
    
    print("Plugin generation complete!")


if __name__ == "__main__":
    main()