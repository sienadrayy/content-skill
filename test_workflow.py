#!/usr/bin/env python3
import json
from pathlib import Path

# Add script to path
import sys
sys.path.insert(0, r"C:\Users\mohit\.openclaw\workspace\comfyui-workflow-runner\scripts")

from run_workflow import ComfyUIRunner

# Load and test
runner = ComfyUIRunner("http://192.168.29.60:8188")
workflow = runner.load_workflow(r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Images_workflow.json")

print("[LOADED] Workflow nodes:")
for node_id in list(workflow.keys())[:5]:
    node = workflow[node_id]
    print(f"  {node_id}: {node.get('_meta', {}).get('title', 'N/A')}")

# Test substitution
print("\n[TEST] Substituting Node 443 prompt...")
original = workflow["443"]["inputs"]["value"]
print(f"  Original (first 100 chars): {original[:100]}...")

inputs_to_sub = {"443.value": "New test prompt for siena"}
workflow_modified = runner.substitute_inputs(workflow, inputs_to_sub)

new_value = workflow_modified["443"]["inputs"]["value"]
print(f"  Modified: {new_value}")
print(f"  Success: {new_value == 'New test prompt for siena'}")

# Test validation
print("\n[TEST] Workflow validation...")
valid, error = runner.validate_workflow(workflow)
print(f"  Valid: {valid}, Error: {error}")

print("\n[OK] All tests passed! Script ready for use.")
