#!/usr/bin/env python3
"""
Advanced converter: Build old flat format from new graph format including connections
"""

import json
from typing import Dict, Any, List, Tuple


def build_old_format_from_graph(workflow: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert new ComfyUI graph format to old flat prompt format.
    This includes rebuilding node connections.
    """
    if 'nodes' not in workflow:
        return workflow  # Already in old format
    
    old_format = {}
    
    # Step 1: Build basic node structure
    node_id_map = {}  # Map new IDs to string IDs
    
    for node in workflow.get('nodes', []):
        node_id = str(node.get('id'))
        node_id_map[node.get('id')] = node_id
        node_type = node.get('type', 'Unknown')
        title = node.get('title', '')
        
        inputs = {}
        
        # Extract values from widgets or node properties
        if 'Bypasser' in node_type:
            inputs['mode'] = node.get('mode', 0)
        elif 'widgets_values' in node:
            widgets = node['widgets_values']
            if node_type in ['PrimitiveStringMultiline', 'Text Multiline']:
                inputs['value'] = widgets[0] if widgets else ''
            else:
                if len(widgets) == 1:
                    inputs['value'] = widgets[0]
                else:
                    for i, val in enumerate(widgets):
                        inputs[f'widget_{i}'] = val
        
        old_format[node_id] = {
            'inputs': inputs,
            'class_type': node_type,
            '_meta': {'title': title}
        }
    
    # Step 2: Process links to build input references
    for link in workflow.get('links', []):
        # Link format: [link_id, source_node, output_index, target_node, input_index, data_type]
        source_node_id = str(link[1])
        output_idx = link[2]
        target_node_id = str(link[3])
        input_idx = link[4]
        
        # Find target node type to determine input field name
        target_node = None
        for node in workflow.get('nodes', []):
            if str(node.get('id')) == target_node_id:
                target_node = node
                break
        
        if not target_node:
            continue
        
        # Get the input name from the target node's inputs
        if 'inputs' in target_node and isinstance(target_node['inputs'], list):
            if input_idx < len(target_node['inputs']):
                input_name = target_node['inputs'][input_idx].get('name', f'input_{input_idx}')
            else:
                input_name = f'input_{input_idx}'
        else:
            input_name = f'input_{input_idx}'
        
        # Set the reference in old format
        if target_node_id not in old_format:
            old_format[target_node_id] = {'inputs': {}, 'class_type': '', '_meta': {}}
        
        old_format[target_node_id]['inputs'][input_name] = [source_node_id, output_idx]
    
    return old_format


def test_converter():
    with open(r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Images_workflow.json", 'r') as f:
        wf = json.load(f)
    
    old_fmt = build_old_format_from_graph(wf)
    
    print("="*80)
    print("CONVERTED TO OLD FORMAT")
    print("="*80)
    print(f"Nodes: {len(old_fmt)}")
    
    # Show key nodes
    for node_id in ['443', '436', '500', '519']:
        if node_id in old_fmt:
            node = old_fmt[node_id]
            print(f"\nNode {node_id}:")
            print(f"  Type: {node.get('class_type')}")
            print(f"  Inputs: {node.get('inputs')}")


if __name__ == "__main__":
    test_converter()
