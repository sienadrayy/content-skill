#!/usr/bin/env python3
import json
import subprocess

result = subprocess.run(
    ["git", "-C", "C:\\Users\\mohit\\.openclaw\\workspace", "show", "comfy-wf/master:openclaw/Images_workflow.json"],
    capture_output=True,
    encoding='utf-8',
    errors='ignore'
)

wf = json.loads(result.stdout)

# Find node 519
for node in wf.get('nodes', []):
    if node.get('id') == 519:
        print("="*80)
        print("NODE 519 - FAST GROUPS BYPASSER")
        print("="*80)
        print(json.dumps(node, indent=2))
        break
