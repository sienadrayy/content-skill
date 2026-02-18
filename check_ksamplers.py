#!/usr/bin/env python3
import json

ui = json.load(open('comfy-wf/image_qwen_image_edit_2509.json'))

ks = [n for n in ui['nodes'] if n['type'] == 'KSampler']
print(f'Found {len(ks)} KSampler nodes\n')
for node in ks:
    print(f"Node {node['id']}: {len(node['widgets_values'])} widget values")
    for i, v in enumerate(node['widgets_values']):
        print(f"  [{i}] {repr(v):40s} ({type(v).__name__})")
    print()
