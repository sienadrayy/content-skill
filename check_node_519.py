#!/usr/bin/env python3
import subprocess
import json

# Fetch the file from remote
result = subprocess.run(
    ["git", "-C", "C:\\Users\\mohit\\.openclaw\\workspace", "show", "comfy-wf/master:openclaw/Images_workflow.json"],
    capture_output=True,
    encoding='utf-8',
    errors='ignore'
)

wf = json.loads(result.stdout)

# Find node 519
if 'nodes' in wf:
    for node in wf['nodes']:
        if node.get('id') == 519:
            print("=" * 80)
            print(f"NODE 519 - FULL DETAILS")
            print("=" * 80)
            print(json.dumps(node, indent=2)[:1000])
