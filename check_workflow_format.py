#!/usr/bin/env python3
import json

# Load from git remote 
import subprocess

result = subprocess.run(
    ["git", "-C", "C:\\Users\\mohit\\.openclaw\\workspace", "show", "comfy-wf/master:openclaw/Images_workflow.json"],
    capture_output=True,
    encoding='utf-8',
    errors='ignore'
)

wf = json.loads(result.stdout)

print("=" * 80)
print("WORKFLOW STRUCTURE")
print("=" * 80)
print(f"Type: {type(wf)}")
print(f"Top-level keys: {list(wf.keys())}")

if isinstance(wf, dict):
    # Check if it's old format (node IDs as keys) or new format (has 'nodes' key)
    if 'nodes' in wf:
        print("\n[NEW FORMAT] Workflow has 'nodes' array")
        print(f"Total nodes: {len(wf['nodes'])}")
        print(f"Other keys: {[k for k in wf.keys() if k != 'nodes']}")
    else:
        print("\n[OLD FORMAT] Workflow has node IDs as keys")
        print(f"Sample keys (first 5): {list(wf.keys())[:5]}")

print("\n" + "=" * 80)
print("FIRST 500 chars of JSON:")
print("=" * 80)
print(json.dumps(wf, indent=2)[:500])
