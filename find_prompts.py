import json

with open('qwen_z_image_api.json') as f:
    api = json.load(f)

for node_id, node in api.items():
    class_type = node.get('class_type', '')
    if 'String' in class_type or 'Prompt' in class_type or 'Text' in class_type:
        print(f'Node {node_id}: {class_type}')
        print(f'  Inputs: {node.get("inputs", {})}')
        print()
