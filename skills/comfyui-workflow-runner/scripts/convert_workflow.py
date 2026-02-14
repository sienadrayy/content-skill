#!/usr/bin/env python3
"""
Convert ComfyUI workflow from new format to old format (flat prompt format)
New format: {id, nodes[], links[], groups[], ...}
Old format: {node_id: {inputs, class_type, _meta}, ...}
"""

import json
from typing import Dict, Any, Optional


def convert_new_to_old_format(new_workflow: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert new ComfyUI workflow format to old flat format for API submission.
    """
    # Check if it's already in old format
    if 'nodes' not in new_workflow and isinstance(new_workflow, dict):
        # Check if keys are numeric (node IDs)
        first_key = next(iter(new_workflow.keys())) if new_workflow else None
        if first_key and (isinstance(first_key, int) or (isinstance(first_key, str) and first_key.isdigit())):
            # Already in old format
            return new_workflow
    
    # Convert new format to old format
    if 'nodes' in new_workflow:
        old_format = {}
        
        for node in new_workflow.get('nodes', []):
            node_id = str(node.get('id'))
            node_type = node.get('type', 'Unknown')
            title = node.get('title', '')
            
            # Extract inputs from widgets_values or inputs field
            inputs = {}
            
            if 'widgets_values' in node and isinstance(node['widgets_values'], list):
                # New format: widgets_values is a list
                # Map common widget types to field names
                if node_type in ['PrimitiveStringMultiline', 'Text Multiline']:
                    inputs['value'] = node['widgets_values'][0] if node['widgets_values'] else ''
                elif node_type == 'Fast Groups Bypasser (rgthree)':
                    # This is a toggle/switch
                    inputs['mode'] = node.get('mode', 0)
                else:
                    # For other types, store all widget values
                    if len(node['widgets_values']) == 1:
                        inputs['value'] = node['widgets_values'][0]
                    else:
                        for i, val in enumerate(node['widgets_values']):
                            inputs[f'value_{i}'] = val
            
            elif 'inputs' in node:
                # Try to extract from inputs field if it exists
                inputs = node.get('inputs', {})
            
            # Build the old format node entry
            old_format[node_id] = {
                'inputs': inputs,
                'class_type': node_type,
                '_meta': {
                    'title': title
                }
            }
        
        return old_format
    
    return new_workflow


def test_convert():
    """Test the converter"""
    # Load new format
    import subprocess
    
    result = subprocess.run(
        ["git", "-C", "C:\\Users\\mohit\\.openclaw\\workspace", "show", "comfy-wf/master:openclaw/Images_workflow.json"],
        capture_output=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    new_wf = json.loads(result.stdout)
    old_wf = convert_new_to_old_format(new_wf)
    
    print("=" * 80)
    print("CONVERSION TEST")
    print("=" * 80)
    print(f"New format nodes: {len(new_wf.get('nodes', []))}")
    print(f"Old format entries: {len(old_wf)}")
    print("\nSample converted nodes:")
    
    for node_id in ['443', '436', '500', '519']:
        if node_id in old_wf:
            print(f"\nNode {node_id}:")
            print(f"  Class: {old_wf[node_id]['class_type']}")
            print(f"  Inputs: {list(old_wf[node_id]['inputs'].keys())}")
            if 'value' in old_wf[node_id]['inputs']:
                val = old_wf[node_id]['inputs']['value']
                if isinstance(val, str) and len(val) > 50:
                    print(f"  Value: {val[:50]}...")
                else:
                    print(f"  Value: {val}")


if __name__ == "__main__":
    test_convert()
