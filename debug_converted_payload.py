#!/usr/bin/env python3
import sys
import json
sys.path.insert(0, r"C:\Users\mohit\.openclaw\workspace\comfyui-workflow-runner\scripts")
from run_workflow import ComfyUIRunner

runner = ComfyUIRunner()
wf = runner.load_workflow(r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Images_workflow.json")

# Substitute values
wf = runner.substitute_inputs(wf, {
    "443.value": "siena is standing in rain",
    "436.value": "siena is showering in rain",
    "500.value": "test",
    "519.mode": 0
})

# Convert for submission
if 'nodes' in wf:
    wf = runner._convert_workflow_format(wf)

print("=" * 80)
print("CONVERTED PAYLOAD")
print("=" * 80)

# Check for empty class_type
empty_types = []
for node_id, node_data in wf.items():
    if not node_data.get('class_type'):
        empty_types.append(node_id)
        print(f"\nNODE {node_id} - EMPTY CLASS_TYPE!")
        print(f"  Inputs: {list(node_data.get('inputs', {}).keys())}")
        print(f"  Meta: {node_data.get('_meta')}")

if empty_types:
    print(f"\n[ERROR] {len(empty_types)} nodes with empty class_type: {empty_types[:10]}")
else:
    print("\n[OK] All nodes have class_type")

print(f"\nTotal nodes: {len(wf)}")
print(f"Payload size: {len(json.dumps(wf))} bytes")
