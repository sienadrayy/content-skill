#!/usr/bin/env python3
"""Test the ComfyUI Export API replica with actual workflow"""

from comfyui_export_api import graph_to_prompt
import json
import urllib.request

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

# Update prompt
print("\n3. Updating prompt...")
for node_id, node_data in api_prompt.items():
    if node_data.get('class_type') == 'PrimitiveStringMultiline':
        if 'value' in node_data.get('inputs', {}):
            node_data['inputs']['value'] = 'Siena is standing in garden'
            print(f"   Updated node {node_id}")
            break

# Save converted workflow
print("\n4. Saving converted workflow...")
with open('Images_workflow_api_export.json', 'w') as f:
    json.dump(api_prompt, f, indent=2)
print(f"   Saved to: Images_workflow_api_export.json")

# Submit to ComfyUI
print("\n5. Submitting to ComfyUI...")
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
        print("✅ WORKFLOW SUBMITTED SUCCESSFULLY")
        print("=" * 70)
except urllib.error.HTTPError as e:
    error_body = e.read().decode('utf-8')
    print(f"   HTTP {e.code}: {e.reason}")
    print(f"   Details: {error_body}")
except Exception as e:
    print(f"   Error: {e}")
