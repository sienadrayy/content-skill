import json

with open(r'\\192.168.29.60\workflows\Images_workflow.json', encoding='utf-8', errors='ignore') as f:
    ui = json.load(f)

for node in ui['nodes']:
    if node['id'] == 499:
        print(f"Node 499:")
        print(f"  Type: {node.get('type')}")
        print(f"  Title: {node.get('title')}")
        print(f"  Mode: {node.get('mode')}")
        break

# Check if server has this node type
import requests
resp = requests.get('http://192.168.29.60:8188/object_info')
info = resp.json()
uuid_type = "9b294824-0bf9-4ac0-9745-40ad4d129545"
print(f"\nServer has node '{uuid_type}': {uuid_type in info}")
