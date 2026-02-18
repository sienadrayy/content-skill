import json

with open(r'\\192.168.29.60\workflows\Videos_workflow.json', encoding='utf-8', errors='ignore') as f:
    wf = json.load(f)

# Find KSamplerAdvanced in subgraph
subgraphs = wf.get('definitions', {}).get('subgraphs', [])
for sg in subgraphs:
    for node in sg.get('nodes', []):
        if node.get('type') == 'KSamplerAdvanced':
            print(f"KSamplerAdvanced node {node['id']} in subgraph {sg['id'][:8]}:")
            print(f"  widgets_values: {node.get('widgets_values')}")
            print(f"  inputs: {[i['name'] for i in node.get('inputs', [])]}")
            break
