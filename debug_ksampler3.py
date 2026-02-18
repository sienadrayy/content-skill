import json

with open('\\\\192.168.29.60\\workflows\\image_z_image_turbo.json') as f:
    wf = json.load(f)

sg_def = wf['definitions']['subgraphs'][0]

# Find KSampler
for node in sg_def['nodes']:
    if node['type'] == 'KSampler' and node['id'] == 3:
        print(json.dumps(node, indent=2))
        break
