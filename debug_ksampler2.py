import json

with open('\\\\192.168.29.60\\workflows\\image_z_image_turbo.json') as f:
    wf = json.load(f)

sg_def = wf['definitions']['subgraphs'][0]

# Find KSampler
for node in sg_def['nodes']:
    if node['type'] == 'KSampler':
        print(f"KSampler node {node['id']}:")
        print(f"  Total inputs: {len(node.get('inputs', []))}")
        print(f"  Widget values count: {len(node['widgets_values'])}")
        print(f"  Widget values: {node['widgets_values']}")
        
        # Count inputs that have widgets
        widget_count = sum(1 for inp in node.get('inputs', []) if 'widget' in inp and inp['widget'])
        print(f"  Inputs with widgets: {widget_count}")
        
        # List all inputs with their widget status
        for i, inp in enumerate(node.get('inputs', [])):
            has_widget = 'widget' in inp and inp['widget']
            print(f"    [{i}] {inp.get('name')}: widget={has_widget}")
        break
