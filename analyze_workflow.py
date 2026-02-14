#!/usr/bin/env python3
import json

with open(r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Images_workflow.json", 'r') as f:
    wf = json.load(f)

print("="*80)
print("WORKFLOW ANALYSIS")
print("="*80)
print(f"ID: {wf.get('id')}")
print(f"Nodes: {len(wf.get('nodes', []))}")
print(f"Links: {len(wf.get('links', []))}")
print(f"Groups: {len(wf.get('groups', []))}")

# Find nodes with "SaveImage" or final outputs
print("\n" + "="*80)
print("OUTPUT NODES")
print("="*80)

for node in wf.get('nodes', []):
    node_type = node.get('type', '')
    if 'Save' in node_type or 'Preview' in node_type or 'VideoC ombine' in node_type:
        print(f"Node {node.get('id')}: {node_type} - {node.get('title', '')}")

# Print ALL links to understand dependencies
print("\n" + "="*80)
print("LINKS (connections)")
print("="*80)
for i, link in enumerate(wf.get('links', [])[:10]):
    print(f"Link {i}: {link}")
print(f"... (total {len(wf.get('links', []))} links)")

# Find which node has outputs
print("\n" + "="*80)
print("NODES WITH OUTPUTS")
print("="*80)
for node in wf.get('nodes', []):
    if node.get('outputs'):
        print(f"Node {node.get('id')}: {node.get('type')} - outputs: {len(node.get('outputs', []))}")
