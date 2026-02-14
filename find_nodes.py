#!/usr/bin/env python3
import json

with open('C:\\Users\\mohit\\.openclaw\\workspace\\comfy-wf\\openclaw\\Images_workflow.json', 'r') as f:
    wf = json.load(f)

titles_to_find = ['Image Prompts', 'Video Prompts', 'Name', 'Fast group bypasser']

print("=" * 80)
print("SEARCHING FOR KEY NODES")
print("=" * 80)

found_nodes = {}

for node_id, node_data in wf.items():
    title = node_data.get('_meta', {}).get('title', '')
    if title in titles_to_find:
        found_nodes[title] = node_id
        print(f"\n[FOUND] {title}")
        print(f"  Node ID: {node_id}")
        print(f"  Class Type: {node_data.get('class_type', 'N/A')}")
        print(f"  Input Fields: {list(node_data.get('inputs', {}).keys())}")
        
        inputs = node_data.get('inputs', {})
        for field_name, field_value in inputs.items():
            if field_name == 'value' and isinstance(field_value, str):
                if len(field_value) > 120:
                    print(f"  {field_name}: {field_value[:120]}...")
                else:
                    print(f"  {field_name}: {field_value}")
            else:
                print(f"  {field_name}: {field_value}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
for title in titles_to_find:
    status = "FOUND" if title in found_nodes else "NOT FOUND"
    node_id = found_nodes.get(title, "N/A")
    print(f"{title:<25} [{status}] Node ID: {node_id}")
