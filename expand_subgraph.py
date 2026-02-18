import json

with open(r'\\192.168.29.60\workflows\Images_workflow.json', encoding='utf-8', errors='ignore') as f:
    wf = json.load(f)

# Find node 499
node_499 = None
for node in wf['nodes']:
    if node['id'] == 499:
        node_499 = node
        break

print("Node 499:")
print(f"  Type: {node_499.get('type')}")
print(f"  Title: {node_499.get('title')}")

# Check subgraphs
subgraphs = wf.get('definitions', {}).get('subgraphs', [])
print(f"\nSubgraphs: {len(subgraphs)}")

for sg in subgraphs:
    sg_id = sg.get('id')
    print(f"\n  Subgraph ID: {sg_id}")
    print(f"  Nodes: {len(sg.get('nodes', []))}")
    if sg.get('nodes'):
        for n in sg['nodes'][:5]:
            print(f"    - {n.get('id')}: {n.get('type')}")
    
    # Check if this matches node 499's type
    if node_499 and sg_id == node_499.get('type'):
        print("  ^ THIS IS NODE 499's DEFINITION!")
