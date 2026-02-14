#!/usr/bin/env python3
import json

with open(r'C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Images_workflow.json', encoding='utf-8') as f:
    wf = json.load(f)

print("="*80)
print("FINDING INPUT NODES IN IMAGES WORKFLOW")
print("="*80)

if 'nodes' in wf:
    for node in wf['nodes']:
        node_id = node.get('id')
        node_type = node.get('type')
        title = node.get('title', '')
        widgets_values = node.get('widgets_values', [])
        
        # Look for text input nodes
        if node_type in ['PrimitiveStringMultiline', 'Text Multiline']:
            print(f"\nNode {node_id}: {title}")
            print(f"  Type: {node_type}")
            if widgets_values:
                print(f"  Current value: {str(widgets_values[0])[:80]}")
            print(f"  Input: {node_id}.value")
        
        # Look for named nodes
        if 'prompt' in title.lower() or 'name' in title.lower():
            print(f"\nNode {node_id}: {title}")
            print(f"  Type: {node_type}")
            if widgets_values:
                print(f"  Current value: {str(widgets_values[0])[:80]}")
