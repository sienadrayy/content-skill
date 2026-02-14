#!/usr/bin/env python3
import json

with open('C:\\Users\\mohit\\.openclaw\\workspace\\Images_workflow_updated.json', 'r') as f:
    wf = json.load(f)

titles_to_find = ['Image Prompts', 'Video Prompts', 'Name', 'Fast group bypasser']

print("=" * 80)
print("SEARCHING FOR KEY NODES IN UPDATED WORKFLOW")
print("=" * 80)

found_nodes = {}

# This workflow uses a "nodes" array format
if isinstance(wf, dict) and 'nodes' in wf:
    nodes_list = wf['nodes']
    for node in nodes_list:
        node_id = node.get('id')
        title = node.get('title', '')
        node_type = node.get('type', '')
        
        if title in titles_to_find:
            found_nodes[title] = node_id
            print(f"\n[FOUND] {title}")
            print(f"  Node ID: {node_id}")
            print(f"  Type: {node_type}")
            
            if 'widgets_values' in node:
                print(f"  Widget Values: {node['widgets_values']}")
            
            if 'size' in node:
                print(f"  Size: {node['size']}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
for title in titles_to_find:
    status = "FOUND" if title in found_nodes else "NOT FOUND"
    node_id = found_nodes.get(title, "N/A")
    print(f"{title:<25} [{status}] Node ID: {node_id}")

# Also list ALL nodes for reference
print("\n" + "=" * 80)
print("ALL NODES")
print("=" * 80)
if isinstance(wf, dict) and 'nodes' in wf:
    for node in wf['nodes']:
        node_id = node.get('id')
        title = node.get('title', 'NO TITLE')
        node_type = node.get('type', 'UNKNOWN')
        print(f"ID: {node_id:<6} | Title: {title:<40} | Type: {node_type}")
