import json

with open(r'\\192.168.29.60\workflows\Videos_workflow.json', encoding='utf-8', errors='ignore') as f:
    wf = json.load(f)

subgraphs = wf.get('definitions', {}).get('subgraphs', [])
for sg in subgraphs:
    for node in sg.get('nodes', []):
        if node.get('type') == 'KSamplerAdvanced':
            print(f"KSamplerAdvanced {node['id']}:")
            print(f"  widgets_values ({len(node.get('widgets_values', []))}): {node.get('widgets_values')}")
            print(f"  inputs ({len(node.get('inputs', []))}):")
            for inp in node.get('inputs', []):
                has_link = inp.get('link') is not None
                has_widget = 'widget' in inp
                print(f"    {inp['name']}: link={inp.get('link')}, widget={'yes' if has_widget else 'no'}")
            break
