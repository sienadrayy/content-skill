import json

with open(r'\\192.168.29.60\workflows\Images_workflow.json', encoding='utf-8', errors='ignore') as f:
    wf = json.load(f)

subgraphs = wf.get('definitions', {}).get('subgraphs', [])

# Find node 499's subgraph
for sg in subgraphs:
    if sg['id'] == '9b294824-0bf9-4ac0-9745-40ad4d129545':
        print(f"Subgraph for node 499:")
        print(f"  Nodes: {len(sg.get('nodes', []))}")
        print(f"  Links: {len(sg.get('links', []))}")
        
        # Find IO nodes (GraphInput/GraphOutput)
        print("\n  IO Nodes:")
        for n in sg.get('nodes', []):
            if 'Input' in n.get('type', '') or 'Output' in n.get('type', ''):
                print(f"    {n['id']}: {n.get('type')} - {n.get('title')}")
        
        # Check link format
        if sg.get('links'):
            print(f"\n  Link format sample: {sg['links'][0]}")
        
        # Find SaveImage or output nodes
        print("\n  Output nodes:")
        for n in sg.get('nodes', []):
            if 'Save' in n.get('type', '') or 'Preview' in n.get('type', ''):
                print(f"    {n['id']}: {n.get('type')}")
                print(f"      inputs: {n.get('inputs', [])[:2]}")
        break
