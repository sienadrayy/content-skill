#!/usr/bin/env python3
"""Debug script to understand widget value ordering."""

import json

# Load UI format
ui = json.load(open('comfy-wf/image_qwen_image_edit_2509.json'))
api = json.load(open('test_output.json'))

def analyze_node(node_id):
    ui_node = [n for n in ui['nodes'] if n['id'] == node_id][0]
    api_node = api.get(str(node_id))
    
    print(f"\n{'='*60}")
    print(f"Node ID: {node_id}, Type: {ui_node['type']}")
    print(f"{'='*60}")
    
    print(f"\nUI Input slots ({len(ui_node['inputs'])}):")
    for i, inp in enumerate(ui_node['inputs']):
        link = inp.get('link', 'None')
        print(f"  [{i}] {inp['name']:15s} - link: {link}")
    
    print(f"\nWidget values ({len(ui_node['widgets_values'])}):")
    for i, val in enumerate(ui_node['widgets_values']):
        print(f"  [{i}] {str(val):40s} ({type(val).__name__})")
    
    if api_node:
        print(f"\nCurrent API output:")
        for name, val in api_node['inputs'].items():
            if isinstance(val, list):
                print(f"  {name:20s}: connection to node {val[0]} slot {val[1]}")
            else:
                print(f"  {name:20s}: {str(val):40s}")
    
    print()

# Analyze key nodes
analyze_node(121)  # CheckpointLoaderSimple - no inputs, 1 widget
analyze_node(89)   # LoraLoaderModelOnly - 1 input (model), 2 widgets
analyze_node(134)  # KSampler - 4 inputs (all connected), 7 widgets
