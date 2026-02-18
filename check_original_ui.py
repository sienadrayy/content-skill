import json

with open(r'\\192.168.29.60\workflows\Qwen + Z image.json', encoding='utf-8', errors='ignore') as f:
    ui = json.load(f)

# Check if it's a nested structure (common ComfyUI format)
if 'nodes' in ui:
    print("UI workflow has 'nodes' key - standard LiteGraph format")
    nodes = ui['nodes']
    links = ui.get('links', [])
    
    # Find nodes 579 and 594
    for node in nodes:
        if node.get('id') in [579, 594]:
            print(f"\nNode {node.get('id')} - {node.get('type')}")
            print(f"  Title: {node.get('title')}")
            print(f"  Widgets values: {node.get('widgets_values', [])[:3]}")
            print(f"  Inputs: {node.get('inputs', [])}")
            print(f"  Outputs: {node.get('outputs', [])[:2]}")
else:
    print("UI workflow is flat dict format")
    print(f"Keys sample: {list(ui.keys())[:5]}")
