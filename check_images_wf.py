import json

with open(r'\\192.168.29.60\workflows\Images_workflow.json', encoding='utf-8', errors='ignore') as f:
    ui = json.load(f)

print(f"Keys: {list(ui.keys())[:5]}")
print(f"Has 'nodes': {'nodes' in ui}")

if 'nodes' in ui:
    # Find node 443
    for node in ui['nodes']:
        if node['id'] == 443:
            print(f"\nNode 443:")
            print(f"  Type: {node.get('type')}")
            print(f"  widgets_values type: {type(node.get('widgets_values'))}")
            print(f"  widgets_values: {node.get('widgets_values')}")
            break
