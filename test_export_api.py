#!/usr/bin/env python3
"""Test the ComfyUI Export API replica with actual workflow"""

from comfyui_export_api import graph_to_prompt
import json
import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("ComfyUI Export API - Real Workflow Test")
print("=" * 70)

# Load workflow
print("\n1. Loading workflow...")
with open(r'\\192.168.29.60\workflows\Images_workflow.json', 'r', encoding='utf-8') as f:
    workflow_ui = json.load(f)
print(f"   Loaded UI-format workflow")

# Convert using ComfyUI's exact algorithm
print("\n2. Converting to API format (using ComfyUI's exact algorithm)...")
workflow, api_prompt = graph_to_prompt(workflow_ui)
print(f"   Converted {len(api_prompt)} nodes")

# Filter out subgraph nodes (UUID-based class_type), custom nodes, and nodes that depend on them
print("\n3. Filtering subgraph and invalid nodes...")
uuid_pattern = re.compile(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$')
invalid_nodes = set()

# Find subgraph nodes and custom extension nodes
for node_id, node_data in api_prompt.items():
    class_type = node_data.get('class_type', '')
    
    # Skip subgraph nodes (UUID)
    if uuid_pattern.match(str(class_type)):
        invalid_nodes.add(node_id)
        print(f"   Removing subgraph node {node_id} ({class_type})")
    # Skip custom extension nodes (have parentheses like "Custom Node (author)")
    elif '(' in str(class_type) and ')' in str(class_type):
        invalid_nodes.add(node_id)
        print(f"   Removing custom node {node_id} ({class_type})")

# Find nodes that depend on invalid nodes
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
                    print(f"   Removing node {node_id} (depends on {ref_node_id})")
                    break
    
    invalid_nodes.update(new_invalid)
    if not new_invalid:
        break

# Remove invalid nodes
for node_id in invalid_nodes:
    del api_prompt[node_id]

print(f"   Remaining nodes: {len(api_prompt)}")

# Update prompt
print("\n4. Updating prompt...")
found_prompt = False
for node_id, node_data in api_prompt.items():
    if node_data.get('class_type') == 'PrimitiveStringMultiline':
        if 'value' in node_data.get('inputs', {}):
            node_data['inputs']['value'] = 'Siena is standing in garden'
            print(f"   Updated node {node_id}")
            found_prompt = True
            break

if not found_prompt:
    print("   WARNING: No prompt node found")

# Save converted workflow
print("\n5. Saving converted workflow...")
with open('Images_workflow_api_export.json', 'w') as f:
    json.dump(api_prompt, f, indent=2)
print(f"   Saved to: Images_workflow_api_export.json")

# Submit to ComfyUI
print("\n6. Submitting to ComfyUI...")
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
    print(f"   Details: {error_body}")
    print("\n" + "=" * 70)
    print("SUBMISSION FAILED")
    print("=" * 70)
except Exception as e:
    print(f"   Error: {e}")
