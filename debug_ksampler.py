import json

with open('\\\\192.168.29.60\\workflows\\image_z_image_turbo.json') as f:
    wf = json.load(f)

sg_def = wf['definitions']['subgraphs'][0]

# Find KSampler in the subgraph
for node in sg_def['nodes']:
    if node['type'] == 'KSampler':
        print(f"KSampler node {node['id']}:")
        print(f"  Widget values: {node['widgets_values']}")
        print(f"  Inputs:")
        for i, inp in enumerate(node.get('inputs', [])):
            has_widget = 'widget' in inp and inp['widget']
            has_link = 'link' in inp and inp['link'] is not None
            print(f"    [{i}] {inp.get('name')}: widget={has_widget}, link={has_link}")
        break
