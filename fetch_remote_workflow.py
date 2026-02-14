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

if result.returncode != 0:
    print(f"Error: {result.stderr}")
    exit(1)

# Parse JSON
try:
    wf = json.loads(result.stdout)
except json.JSONDecodeError as e:
    print(f"JSON Parse Error: {e}")
    print(f"First 500 chars: {result.stdout[:500]}")
    exit(1)

titles_to_find = ['Image Prompts', 'VIdeo Prompts', 'Name', 'Fast Groups Bypasser (rgthree)']

print("=" * 80)
print("SEARCHING FOR KEY NODES IN UPDATED WORKFLOW")
print("=" * 80)

found_nodes = {}

# Check if it's nodes array format or flat object format
if isinstance(wf, dict):
    if 'nodes' in wf:
        # New format with nodes array
        nodes_list = wf['nodes']
        for node in nodes_list:
            node_id = node.get('id')
            title = node.get('title', '')
            node_type = node.get('type', '')
            
            if title in titles_to_find:
                found_nodes[title] = (node_id, node)
                print(f"\n[FOUND] {title}")
                print(f"  Node ID: {node_id}")
                print(f"  Type: {node_type}")
                
                if 'widgets_values' in node:
                    wv = node['widgets_values']
                    if isinstance(wv, list) and len(wv) > 0:
                        val = wv[0]
                        if isinstance(val, str) and len(val) > 100:
                            print(f"  Value: {val[:100]}...")
                        else:
                            print(f"  Value: {val}")
    else:
        # Old format with flat object keys as node IDs
        for node_id, node_data in wf.items():
            title = node_data.get('_meta', {}).get('title', '')
            
            if title in titles_to_find:
                found_nodes[title] = (node_id, node_data)
                print(f"\n[FOUND] {title}")
                print(f"  Node ID: {node_id}")
                
                if 'inputs' in node_data and 'value' in node_data['inputs']:
                    val = node_data['inputs']['value']
                    if isinstance(val, str) and len(val) > 100:
                        print(f"  Value: {val[:100]}...")
                    else:
                        print(f"  Value: {val}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
for title in titles_to_find:
    status = "FOUND" if title in found_nodes else "NOT FOUND"
    node_id = found_nodes.get(title, ("N/A", None))[0]
    print(f"{title:<25} [{status}] Node ID: {node_id}")

print("\n" + "=" * 80)
print("ALL NODES IN WORKFLOW")
print("=" * 80)

# List all node titles for debugging
if isinstance(wf, dict) and 'nodes' in wf:
    nodes_list = wf['nodes']
    for node in nodes_list:
        node_id = node.get('id')
        title = node.get('title', 'NO TITLE')
        node_type = node.get('type', 'UNKNOWN')
        print(f"ID: {node_id:<6} | Title: {title:<40} | Type: {node_type}")
