import json

with open(r'\\192.168.29.60\workflows\Images_workflow.json', encoding='utf-8', errors='ignore') as f:
    ui = json.load(f)

for node in ui['nodes']:
    wv = node.get('widgets_values')
    if wv is not None and not isinstance(wv, list):
        print(f"Node {node['id']} ({node.get('type')}): widgets_values is {type(wv)}")
        print(f"  Value: {wv}")
