import json

# Load the generated API
with open('\\\\192.168.29.60\\workflows\\z_image_turbo_api.json') as f:
    api = json.load(f)

if '35' in api:
    del api['35']

print("Workflow Verification Report")
print("=" * 70)

# Check each node
for node_id_str, node in sorted(api.items(), key=lambda x: int(x[0])):
    node_id = int(node_id_str)
    node_type = node.get('class_type')
    inputs = node.get('inputs', {})
    
    print(f"\nNode {node_id}: {node_type}")
    
    # List all inputs
    if inputs:
        print(f"  Inputs ({len(inputs)}):")
        for inp_name, inp_val in inputs.items():
            if isinstance(inp_val, list):
                print(f"    - {inp_name}: [{inp_val[0]}, {inp_val[1]}]")
            else:
                val_str = str(inp_val)[:50]
                print(f"    - {inp_name}: {val_str}")
    else:
        print(f"  Inputs: NONE")

# Check for all node IDs being referenced
print("\n" + "=" * 70)
print("Reference Check")
print("=" * 70)

node_ids = set(int(k) for k in api.keys())
referenced_ids = set()

for node_id_str, node in api.items():
    for inp_name, inp_val in node.get('inputs', {}).items():
        if isinstance(inp_val, list) and len(inp_val) >= 2:
            ref_id = int(inp_val[0])
            if ref_id not in node_ids:
                print(f"WARNING: Node {node_id_str} references non-existent node {ref_id}")
            else:
                referenced_ids.add(ref_id)

# Check for unused nodes
all_ids = set(int(k) for k in api.keys())
unused = all_ids - referenced_ids
print(f"\nReferenced nodes: {sorted(referenced_ids)}")
print(f"Unreferenced nodes: {sorted(unused)}")

# Specific checks
print("\n" + "=" * 70)
print("Critical Checks")
print("=" * 70)

# Check SaveImage
if '9' in api:
    save_node = api['9']
    if 'images' in save_node['inputs']:
        print(f"SaveImage (9) inputs: {save_node['inputs'].keys()}")
        print(f"  - images source: {save_node['inputs'].get('images')}")
    else:
        print("ERROR: SaveImage has no 'images' input!")
else:
    print("ERROR: No SaveImage node found!")

# Check KSampler
if '115' in api:
    ks = api['115']
    print(f"KSampler (115) inputs: {list(ks['inputs'].keys())}")
    required = ['model', 'positive', 'negative', 'latent_image', 'seed', 'steps', 'cfg']
    for req in required:
        if req in ks['inputs']:
            val = ks['inputs'][req]
            if isinstance(val, list):
                print(f"  - {req}: [node {val[0]}, slot {val[1]}]")
            else:
                print(f"  - {req}: {val}")
        else:
            print(f"  - {req}: MISSING!")
else:
    print("ERROR: No KSampler node found!")
