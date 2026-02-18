import json

with open(r'\\192.168.29.60\workflows\Qwen + Z image.json', encoding='utf-8', errors='ignore') as f:
    ui = json.load(f)

node594 = ui.get('594', {})
print('Node 594 in UI workflow:')
print(f'  Type: {node594.get("type")}')
print(f'  Title: {node594.get("title")}')
print(f'  Class name: {node594.get("class_name")}')
print(f'  Full node: {json.dumps(node594, indent=2)[:500]}')

# Check what the converter puts out
with open('qwen_z_image_api_clean.json') as f:
    api = json.load(f)
    
node594_api = api.get('594', {})
print('\n\nNode 594 in converted API workflow:')
print(f'  Class type: {node594_api.get("class_type")}')
print(f'  Inputs: {node594_api.get("inputs")}')
