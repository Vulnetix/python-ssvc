#!/usr/bin/env python3
"""
SSVC Methodology Validator

Validates YAML methodology files against the JSON schema and performs additional
consistency checks to ensure decision tree integrity.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Union, Any
import yaml
import jsonschema
from jsonschema import validate, ValidationError


class MethodologyValidator:
    """Validates SSVC methodology YAML files against schema and business rules."""
    
    def __init__(self):
        self.schema_path = Path(__file__).parent.parent / "src" / "ssvc" / "methodologies" / "schema.json"
        with open(self.schema_path, 'r') as f:
            self.schema = json.load(f)
    
    def validate_file(self, file_path: Path) -> Dict[str, Union[bool, List[str]]]:
        """Validate a single YAML methodology file."""
        errors = []
        
        try:
            # Load and parse YAML
            with open(file_path, 'r') as f:
                content = f.read()
            methodology = yaml.safe_load(content)
            
            # Validate against JSON schema
            try:
                validate(instance=methodology, schema=self.schema)
            except ValidationError as e:
                # More detailed error reporting
                path = " -> ".join(str(p) for p in e.absolute_path) if e.absolute_path else 'root'
                errors.append(f"Schema error at '{path}': {e.message}")
                if e.instance is not None:
                    errors.append(f"  Problem value: {e.instance} (type: {type(e.instance).__name__})")
            except Exception as e:
                errors.append(f"Schema validation error: {str(e)}")
                
            if not errors:
                # Additional validation checks
                self._validate_tree_depth_consistency(methodology, errors)
                self._validate_enum_usage(methodology, errors)
                self._validate_priority_mapping(methodology, errors)
                self._validate_action_coverage(methodology, errors)
                self._validate_vector_metadata(methodology, errors)
                
            return {"valid": len(errors) == 0, "errors": errors}
            
        except yaml.YAMLError as e:
            errors.append(f"Failed to parse YAML: {str(e)}")
            return {"valid": False, "errors": errors}
        except Exception as e:
            errors.append(f"Unexpected error: {str(e)}")
            return {"valid": False, "errors": errors}
    
    def _validate_tree_depth_consistency(self, methodology: Dict, errors: List[str]) -> None:
        """Ensure all decision paths have consistent depth."""
        depths = self._get_tree_depths(methodology["decisionTree"])
        unique_depths = list(set(depths))
        
        if len(unique_depths) > 1:
            errors.append(f"Inconsistent tree depth: found depths {unique_depths}. "
                         "All paths should have the same depth.")
    
    def _get_tree_depths(self, node: Dict, current_depth: int = 0) -> List[int]:
        """Recursively calculate the depth of all paths in the decision tree."""
        depths = []
        
        for key, child in node["children"].items():
            if isinstance(child, str):
                # This is a leaf action
                depths.append(current_depth + 1)
            else:
                # This is another node, recurse
                depths.extend(self._get_tree_depths(child, current_depth + 1))
        
        return depths
    
    def _validate_enum_usage(self, methodology: Dict, errors: List[str]) -> None:
        """Validate that all declared enums are used and all used enums are declared."""
        declared_enums = set(methodology["enums"].keys())
        used_enums = self._get_used_enum_types(methodology["decisionTree"])
        
        # Special meta-enums used for code generation but not in decision trees
        meta_enums = {"ActionType", "DecisionPriorityLevel"}
        
        # Check that all used enums are declared
        for used in used_enums:
            if used not in declared_enums:
                errors.append(f"Decision tree uses undeclared enum type: {used}")
        
        # Check that all declared enums are used (excluding meta-enums)
        for declared in declared_enums:
            if declared not in used_enums and declared not in meta_enums:
                errors.append(f"Declared enum type is never used: {declared}")
    
    def _get_used_enum_types(self, node: Dict) -> Set[str]:
        """Recursively collect all enum types used in the decision tree."""
        types = {node["type"]}
        
        for child in node["children"].values():
            if isinstance(child, dict):
                types.update(self._get_used_enum_types(child))
        
        return types
    
    def _validate_priority_mapping(self, methodology: Dict, errors: List[str]) -> None:
        """Validate that all actions have priority mappings and vice versa."""
        actions = self._get_leaf_actions(methodology["decisionTree"])
        actions.add(methodology["defaultAction"])
        
        # Check that all actions have priority mappings
        for action in actions:
            if action not in methodology["priorityMap"]:
                errors.append(f"Action '{action}' has no priority mapping")
        
        # Check that all priority mappings have corresponding actions
        for action in methodology["priorityMap"]:
            if action not in actions:
                errors.append(f"Priority mapping exists for unused action: {action}")
    
    def _get_leaf_actions(self, node: Dict) -> Set[str]:
        """Recursively collect all leaf actions from the decision tree."""
        actions = set()
        
        for child in node["children"].values():
            if isinstance(child, str):
                actions.add(child)
            else:
                actions.update(self._get_leaf_actions(child))
        
        return actions
    
    def _validate_action_coverage(self, methodology: Dict, errors: List[str]) -> None:
        """Validate decision tree coverage and warn about sparse trees."""
        enum_types = self._get_decision_path(methodology["decisionTree"])
        total_combinations = 1
        
        for enum_type in enum_types:
            enum_values = methodology["enums"].get(enum_type, [])
            total_combinations *= len(enum_values) if enum_values else 1
        
        covered_paths = self._get_covered_paths(methodology["decisionTree"])
        coverage_percentage = (len(covered_paths) / total_combinations) * 100 if total_combinations > 0 else 0
        
        # Only warn if coverage is extremely low (< 25%) - sparse trees with defaults are valid
        if coverage_percentage < 25:
            print(f"⚠️  Warning: Very low decision coverage ({coverage_percentage:.1f}%) in {methodology['name']}. "
                  f"Ensure default action handles unmapped cases appropriately.")
    
    def _get_decision_path(self, node: Dict) -> List[str]:
        """Get the decision path structure (sequence of enum types)."""
        path = [node["type"]]
        
        # Find the first non-leaf child to continue the path
        for child in node["children"].values():
            if isinstance(child, dict):
                path.extend(self._get_decision_path(child))
                break  # We only need one path to determine the structure
        
        return path
    
    def _get_covered_paths(self, node: Dict, current_path: List[str] = None) -> List[List[str]]:
        """Get all explicitly covered decision paths."""
        if current_path is None:
            current_path = []
        
        paths = []
        
        for value, child in node["children"].items():
            new_path = current_path + [f"{node['type']}:{value}"]
            
            if isinstance(child, str):
                paths.append(new_path + [f"ACTION:{child}"])
            else:
                paths.extend(self._get_covered_paths(child, new_path))
        
        return paths
    
    def _validate_vector_metadata(self, methodology: Dict, errors: List[str]) -> None:
        """Validate vector metadata consistency if present."""
        if "vectorMetadata" not in methodology:
            return
        
        vector_meta = methodology["vectorMetadata"]
        
        # Validate parameter mappings reference valid enum types
        if "parameterMappings" in vector_meta:
            declared_enums = set(methodology["enums"].keys())
            
            for param_name, mapping in vector_meta["parameterMappings"].items():
                if "enumType" in mapping:
                    enum_type = mapping["enumType"]
                    if enum_type not in declared_enums:
                        errors.append(f"Vector metadata parameter '{param_name}' references "
                                    f"undeclared enum type: {enum_type}")
                    
                    # Validate value mappings
                    if "valueMappings" in mapping:
                        enum_values = set(methodology["enums"][enum_type])
                        mapped_values = set(mapping["valueMappings"].keys())
                        
                        # Check for unmapped enum values
                        unmapped = enum_values - mapped_values
                        if unmapped:
                            errors.append(f"Vector metadata parameter '{param_name}' missing "
                                        f"value mappings for: {', '.join(unmapped)}")
                        
                        # Check for mappings to non-existent enum values
                        invalid_mappings = mapped_values - enum_values
                        if invalid_mappings:
                            errors.append(f"Vector metadata parameter '{param_name}' has "
                                        f"mappings for non-existent enum values: {', '.join(invalid_mappings)}")


def main():
    """Main validation function."""
    validator = MethodologyValidator()
    methodologies_dir = Path(__file__).parent.parent / "src" / "ssvc" / "methodologies"
    
    # Get all YAML files
    yaml_files = list(methodologies_dir.glob("*.yaml"))
    
    if not yaml_files:
        print("No YAML files found in methodologies directory")
        sys.exit(1)
    
    has_errors = False
    
    print("🔍 Validating SSVC Methodology Files...\n")
    
    for file_path in yaml_files:
        print(f"Validating {file_path.name}...")
        
        result = validator.validate_file(file_path)
        
        if result["valid"]:
            print(f"✅ {file_path.name} is valid\n")
        else:
            print(f"❌ {file_path.name} has errors:")
            for error in result["errors"]:
                print(f"   • {error}")
            print("")
            has_errors = True
    
    if has_errors:
        print("❌ Validation failed. Please fix the errors above.")
        sys.exit(1)
    else:
        print("✅ All methodology files are valid!")


if __name__ == "__main__":
    main()