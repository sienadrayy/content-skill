import json

with open(r'\\192.168.29.60\workflows\Videos_workflow.json', encoding='utf-8', errors='ignore') as f:
    wf = json.load(f)

# Find KSamplerAdvanced in subgraphs
subgraphs = wf.get('definitions', {}).get('subgraphs', [])
for sg in subgraphs:
    for node in sg.get('nodes', []):
        if node.get('type') == 'KSamplerAdvanced':
            print(f"KSamplerAdvanced {node['id']} in subgraph {sg['id'][:8]}:")
            print("  Inputs with links:")
            for inp in node.get('inputs', []):
                if inp.get('link'):
                    print(f"    {inp['name']}: link={inp['link']}")
            
            # Find these links in the subgraph
            print("  Link details:")
            for inp in node.get('inputs', []):
                link_id = inp.get('link')
                if link_id:
                    for link in sg.get('links', []):
                        if isinstance(link, dict) and link['id'] == link_id:
                            print(f"    {inp['name']}: {link['origin_id']} -> {node['id']}")
                            break
            print()
