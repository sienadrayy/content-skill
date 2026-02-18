import json

with open(r'\\192.168.29.60\workflows\Images_workflow.json', encoding='utf-8', errors='ignore') as f:
    wf = json.load(f)

# Find node 499
for n in wf['nodes']:
    if n['id'] == 499:
        print("Node 499:")
        print(f"  Type: {n.get('type')}")
        print(f"  Inputs: {len(n.get('inputs', []))}")
        for inp in n.get('inputs', []):
            print(f"    {inp.get('name')}: link={inp.get('link')}")
        print(f"  Outputs: {len(n.get('outputs', []))}")
        for out in n.get('outputs', []):
            print(f"    {out.get('name')}: links={out.get('links')}")
        break

# What feeds into 499?
print("\nLinks TO node 499:")
for link in wf['links']:
    if link[3] == 499:  # target_node == 499
        print(f"  Link {link[0]}: node {link[1]} slot {link[2]} -> slot {link[4]}")

# What does 499 feed?
print("\nLinks FROM node 499:")
for link in wf['links']:
    if link[1] == 499:  # source_node == 499
        print(f"  Link {link[0]}: slot {link[2]} -> node {link[3]} slot {link[4]}")
