import json

with open(r'\\192.168.29.60\workflows\Images_workflow.json', encoding='utf-8', errors='ignore') as f:
    ui = json.load(f)

for node in ui['nodes']:
    if node['id'] == 443:
        print(f"Node 443:")
        print(f"  Type: {node.get('type')}")
        print(f"  Mode: {node.get('mode')} (0=normal, 2=muted, 4=bypassed)")
        print(f"  Title: {node.get('title')}")
        break
else:
    print("Node 443 not found in UI workflow!")
