#!/usr/bin/env python3
"""Submit image_z_image_turbo workflow with custom prompt"""

from comfyui_export_api import graph_to_prompt
import json
import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("ComfyUI Export API - image_z_image_turbo")
print("=" * 70)

# Load workflow
print("\n1. Loading workflow...")
with open(r'\\192.168.29.60\workflows\image_z_image_turbo.json', 'r', encoding='utf-8') as f:
    workflow_ui = json.load(f)
print(f"   Loaded UI-format workflow")

# Store UI node info
ui_nodes_by_id = {str(node['id']): node for node in workflow_ui.get('nodes', [])}

# Convert
print("\n2. Converting to API format...")
workflow, api_prompt = graph_to_prompt(workflow_ui)
print(f"   Converted {len(api_prompt)} nodes")

# Filter invalid nodes
print("\n3. Filtering invalid nodes...")
uuid_pattern = re.compile(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$')
invalid_nodes = set()

for node_id, node_data in api_prompt.items():
    class_type = node_data.get('class_type', '')
    
    if uuid_pattern.match(str(class_type)):
        invalid_nodes.add(node_id)
        print(f"   Removing subgraph node {node_id}")
    elif '(' in str(class_type) and ')' in str(class_type):
        invalid_nodes.add(node_id)
        print(f"   Removing custom node {node_id}")
    elif class_type in ['MarkdownNote', 'Note', 'Reroute']:
        invalid_nodes.add(node_id)
        print(f"   Removing UI-only node {node_id} ({class_type})")

# Remove dependent nodes
max_iterations = 5
iteration = 0
while iteration < max_iterations and invalid_nodes:
    iteration += 1
    new_invalid = set()
    
    for node_id, node_data in api_prompt.items():
        if node_id in invalid_nodes:
            continue
        
        inputs = node_data.get('inputs', {})
        for inp_name, inp_value in inputs.items():
            if isinstance(inp_value, list) and len(inp_value) >= 1:
                ref_node_id = str(inp_value[0])
                if ref_node_id in invalid_nodes:
                    new_invalid.add(node_id)
                    break
    
    invalid_nodes.update(new_invalid)
    if not new_invalid:
        break

for node_id in invalid_nodes:
    del api_prompt[node_id]

print(f"   Remaining nodes: {len(api_prompt)}")

# Populate widget values
print("\n4. Filling widget values...")
for node_id, node_data in api_prompt.items():
    if node_id in ui_nodes_by_id:
        ui_node = ui_nodes_by_id[node_id]
        widget_values = ui_node.get('widgets_values', [])
        ui_inputs = ui_node.get('inputs', [])
        
        if widget_values and isinstance(widget_values, list) and len(ui_inputs) > 0:
            widget_idx = 0
            
            for inp in ui_inputs:
                if not isinstance(inp, dict):
                    continue
                
                inp_name = inp.get('name', '')
                if not inp_name:
                    continue
                
                if 'widget' in inp:
                    if widget_idx < len(widget_values):
                        node_data['inputs'][inp_name] = widget_values[widget_idx]
                        widget_idx += 1

print(f"   Widget values populated")

# Update prompt
print("\n5. Updating prompt...")
for node_id, node_data in api_prompt.items():
    if node_data.get('class_type') == 'PrimitiveStringMultiline':
        if 'value' in node_data.get('inputs', {}):
            node_data['inputs']['value'] = 'Siena is standing in garden'
            print(f"   Updated prompt node {node_id}")
            break

# Save
print("\n6. Saving converted workflow...")
with open('z_image_turbo_converted.json', 'w') as f:
    json.dump(api_prompt, f, indent=2)
print(f"   Saved to: z_image_turbo_converted.json")

# Submit
print("\n7. Submitting to ComfyUI...")
url = 'http://192.168.29.60:8188/prompt'
payload = {"prompt": api_prompt}
req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        prompt_id = result.get('prompt_id')
        print(f"   SUCCESS!")
        print(f"   Prompt ID: {prompt_id}")
        print("\n" + "=" * 70)
        print("SUCCESS - WORKFLOW SUBMITTED")
        print("=" * 70)
except urllib.error.HTTPError as e:
    error_body = e.read().decode('utf-8')
    print(f"   HTTP {e.code}: {e.reason}")
    print(f"   Details: {error_body[:500]}")
    print("\n" + "=" * 70)
    print("SUBMISSION FAILED")
    print("=" * 70)
except Exception as e:
    print(f"   Error: {e}")
