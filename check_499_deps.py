import json

with open('images_run.json') as f:
    api = json.load(f)

print("Nodes referencing 499:")
for nid, node in api.items():
    for inp_name, inp_val in node.get('inputs', {}).items():
        if isinstance(inp_val, list) and len(inp_val) == 2:
            if inp_val[0] == '499':
                print(f"  Node {nid} ({node.get('class_type')}): {inp_name} -> 499")
