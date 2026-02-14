#!/usr/bin/env python3
import sys
import json
sys.path.insert(0, r"C:\Users\mohit\.openclaw\workspace\comfyui-workflow-runner\scripts")
from run_workflow import ComfyUIRunner

runner = ComfyUIRunner()
wf = runner.load_workflow(r"C:\Users\mohit\Downloads\image_z_image_turbo.json")

print("="*80)
print("ORIGINAL NODES")
print("="*80)
if 'nodes' in wf:
    for node in wf['nodes'][:6]:
        print(f"ID {node.get('id')}: {node.get('type')} - {node.get('title', 'NO TITLE')}")

# Convert
print("\n" + "="*80)
print("CONVERTING...")
print("="*80)

converted = runner._convert_workflow_format(wf)

print(f"Original nodes: {len(wf.get('nodes', []))}")
print(f"Converted nodes: {len(converted)}")

print("\n" + "="*80)
print("CONVERTED NODES")
print("="*80)

for node_id in list(converted.keys())[:10]:
    node = converted[node_id]
    print(f"\nNode {node_id}:")
    print(f"  Class: '{node.get('class_type')}'")
    print(f"  Inputs: {list(node.get('inputs', {}).keys())[:3]}")
    if not node.get('class_type'):
        print(f"  [ERROR] EMPTY CLASS_TYPE!")

# Try to submit
print("\n" + "="*80)
print("SUBMISSION ATTEMPT")
print("="*80)

payload = {"prompt": converted}
print(f"Payload size: {len(json.dumps(payload))} bytes")
print(f"Payload (first 500 chars):\n{json.dumps(payload, indent=2)[:500]}")
