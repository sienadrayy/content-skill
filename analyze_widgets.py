import json

with open(r'\\192.168.29.60\workflows\Qwen + Z image.json', encoding='utf-8', errors='ignore') as f:
    ui = json.load(f)

# Find node 575
for node in ui['nodes']:
    if node['id'] == 575:
        print("Node 575 (KSampler):")
        print(f"  Type: {node.get('type')}")
        print(f"  Widgets values: {node.get('widgets_values')}")
        print(f"  Inputs (slots):")
        for inp in node.get('inputs', []):
            has_link = 'YES' if inp.get('link') else 'NO'
            print(f"    {inp['name']}: link={has_link}")
        break

print("\n" + "="*50)

# Find node 645
for node in ui['nodes']:
    if node['id'] == 645:
        print("\nNode 645 (LoraLoaderModelOnly):")
        print(f"  Type: {node.get('type')}")
        print(f"  Widgets values: {node.get('widgets_values')}")
        print(f"  Inputs (slots):")
        for inp in node.get('inputs', []):
            has_link = 'YES' if inp.get('link') else 'NO'
            print(f"    {inp['name']}: link={has_link}")
        break
