#!/usr/bin/env python3
import sys
import json
sys.path.insert(0, r"C:\Users\mohit\.openclaw\workspace\comfyui-workflow-runner\scripts")
from run_workflow import ComfyUIRunner

runner = ComfyUIRunner("http://192.168.29.60:8188")

# Load workflow
workflow = runner.load_workflow(r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Images_workflow.json")

print("=" * 80)
print("CONVERTED WORKFLOW (first 5 nodes)")
print("=" * 80)

for i, (node_id, node_data) in enumerate(list(workflow.items())[:5]):
    print(f"\nNode {node_id}:")
    print(f"  Class: {node_data.get('class_type')}")
    print(f"  Title: {node_data.get('_meta', {}).get('title')}")
    print(f"  Inputs: {list(node_data.get('inputs', {}).keys())}")

print("\n" + "=" * 80)
print("Key nodes to test:")
print("=" * 80)
for node_id in ['443', '436', '500', '519']:
    if node_id in workflow:
        print(f"Node {node_id}: OK - {workflow[node_id].get('_meta', {}).get('title')}")
    else:
        print(f"Node {node_id}: NOT FOUND")

print("\n" + "=" * 80)
print("SUBMISSION PAYLOAD (first 500 chars):")
print("=" * 80)
payload = json.dumps(workflow)
print(payload[:500])
print(f"\nTotal payload size: {len(payload)} bytes")
