#!/usr/bin/env python3
import json

with open('C:\\Users\\mohit\\.openclaw\\workspace\\comfy-wf\\openclaw\\Images_workflow.json', 'r') as f:
    wf = json.load(f)

print("=" * 80)
print("ALL NODES IN WORKFLOW")
print("=" * 80)

for node_id, node_data in sorted(wf.items(), key=lambda x: str(x[0])):
    title = node_data.get('_meta', {}).get('title', 'NO TITLE')
    class_type = node_data.get('class_type', 'UNKNOWN')
    print(f"ID: {node_id:<10} | Title: {title:<40} | Type: {class_type}")

print("\n" + "=" * 80)
print("SEARCHING FOR PARTIAL MATCHES")
print("=" * 80)

keywords = ['video', 'bypass', 'switch', 'group']

for node_id, node_data in wf.items():
    title = node_data.get('_meta', {}).get('title', '').lower()
    for keyword in keywords:
        if keyword in title:
            print(f"[MATCH] {keyword.upper()}")
            print(f"  Node ID: {node_id}")
            print(f"  Title: {node_data.get('_meta', {}).get('title', 'N/A')}")
