import json

with open(r'\\192.168.29.60\workflows\Qwen + Z image.json', encoding='utf-8', errors='ignore') as f:
    ui = json.load(f)

for node in ui['nodes']:
    if node['id'] == 649:
        print("Node 649:")
        print(f"  Type: {node.get('type')}")
        print(f"  Title: {node.get('title')}")
        print(f"  Mode: {node.get('mode')}")  # 0=normal, 2=muted, 4=bypassed
        print(f"  Widgets: {node.get('widgets_values')}")
        print(f"  Inputs:")
        for inp in node.get('inputs', []):
            print(f"    {inp['name']}: link={inp.get('link')}")
        break
