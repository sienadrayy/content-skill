import json

with open('\\\\192.168.29.60\\workflows\\z_image_turbo_api.json') as f:
    api_wf = json.load(f)

if '35' in api_wf:
    del api_wf['35']

print("Checking workflow structure:\n")

for node_id, node in sorted(api_wf.items(), key=lambda x: int(x[0])):
    print(f"Node {node_id}: {node['class_type']}")
    print(f"  Inputs: {list(node.get('inputs', {}).keys())}")
    
    # Check for missing/invalid references
    for inp_name, inp_val in node.get('inputs', {}).items():
        if isinstance(inp_val, list) and len(inp_val) >= 2:
            ref_node = inp_val[0]
            print(f"    {inp_name} -> node {ref_node}")
            if ref_node not in api_wf and ref_node not in ['-10', '-20']:
                print(f"      WARNING: node {ref_node} not found!")
    print()
