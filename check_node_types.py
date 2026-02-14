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

print("=" * 80)
print("CHECKING NODE TYPES")
print("=" * 80)

for node in wf.get('nodes', []):
    node_id = node.get('id')
    node_type = node.get('type', '')
    title = node.get('title', '')
    
    if node_type and (node_type.startswith('{') or '-' in node_type):
        print(f"\nNode {node_id}: {node_type[:60]}")
        print(f"  Title: {title}")
        print(f"  Full type: {node_type}")
