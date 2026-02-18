import json

with open(r'\\192.168.29.60\workflows\Images_workflow.json', encoding='utf-8', errors='ignore') as f:
    wf = json.load(f)

subgraphs = wf.get('definitions', {}).get('subgraphs', [])

for sg in subgraphs:
    if sg['id'] == '9b294824-0bf9-4ac0-9745-40ad4d129545':
        print("Subgraph keys:", list(sg.keys()))
        
        # Check for external connections info
        if 'external_connections' in sg:
            print("\nExternal connections:", sg['external_connections'])
        
        if 'inputs' in sg:
            print("\nSubgraph inputs:", sg['inputs'])
        
        if 'outputs' in sg:
            print("\nSubgraph outputs:", sg['outputs'])
        
        # Check for linkMapping or similar
        for key in sg.keys():
            if key not in ['nodes', 'links', 'id']:
                print(f"\n{key}: {sg[key]}")
        
        # Find nodes with no input links (they might receive external input)
        print("\n\nNodes with missing input links:")
        inner_link_sources = set()
        for link in sg.get('links', []):
            if isinstance(link, dict):
                inner_link_sources.add(link['origin_id'])
        
        for n in sg.get('nodes', []):
            for inp in n.get('inputs', []):
                link_id = inp.get('link')
                if link_id is not None:
                    # Check if this link exists in inner links
                    link_exists = any(
                        (isinstance(l, dict) and l['id'] == link_id) or 
                        (isinstance(l, list) and l[0] == link_id)
                        for l in sg.get('links', [])
                    )
                    if not link_exists:
                        print(f"  Node {n['id']} ({n.get('type')}): input '{inp.get('name')}' has link {link_id} NOT in subgraph")
        break
