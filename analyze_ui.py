#!/usr/bin/env python3
import json

ui = json.load(open('comfy-wf/image_qwen_image_edit_2509.json'))

# LoraLoaderModelOnly
print('=== LoraLoaderModelOnly Node (ID 89) ===')
node = [n for n in ui['nodes'] if n['id'] == 89][0]
print(f'Number of inputs array items: {len(node["inputs"])}')
for i, inp in enumerate(node['inputs']):
    print(f'  Input {i}: name={inp["name"]}, link={inp.get("link", None)}')
print(f'Number of widgets_values: {len(node["widgets_values"])}')
print(f'Widgets values: {node["widgets_values"]}')
print()

# KSampler
print('=== KSampler Node (ID 134) ===')
node = [n for n in ui['nodes'] if n['id'] == 134][0]
print(f'Number of inputs array items: {len(node["inputs"])}')
for i, inp in enumerate(node['inputs']):
    print(f'  Input {i}: name={inp["name"]}, link={inp.get("link", None)}')
print(f'Number of widgets_values: {len(node["widgets_values"])}')
print(f'Widgets values: {node["widgets_values"]}')
print()

# CheckpointLoaderSimple
print('=== CheckpointLoaderSimple Node (ID 121) ===')
node = [n for n in ui['nodes'] if n['id'] == 121][0]
print(f'Number of inputs array items: {len(node["inputs"])}')
for i, inp in enumerate(node['inputs']):
    print(f'  Input {i}: name={inp["name"]}, link={inp.get("link", None)}')
print(f'Number of widgets_values: {len(node["widgets_values"])}')
print(f'Widgets values: {node["widgets_values"]}')
