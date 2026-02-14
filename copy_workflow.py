#!/usr/bin/env python3
import subprocess
import json

# Get the remote workflow
result = subprocess.run(
    ["git", "-C", "C:\\Users\\mohit\\.openclaw\\workspace", "show", "comfy-wf/master:openclaw/Images_workflow.json"],
    capture_output=True,
    encoding='utf-8',
    errors='ignore'
)

wf = json.loads(result.stdout)

# Write it locally
with open(r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Images_workflow.json", 'w') as f:
    json.dump(wf, f, indent=2)

print(f"[OK] Copied workflow with {len(wf.get('nodes', []))} nodes")
