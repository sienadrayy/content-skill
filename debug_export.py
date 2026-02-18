import json
import sys
sys.path.insert(0, 'C:\\Users\\mohit\\.openclaw\\workspace')

with open(r'\\192.168.29.60\workflows\Videos_workflow.json', encoding='utf-8', errors='ignore') as f:
    wf = json.load(f)

from comfyui_export_api_v6 import ComfyUIExporter
exporter = ComfyUIExporter(wf)

# Manually trace export for node 623
node = exporter.nodes.get(623)
ntype = node.get('type')
print(f"Node 623 type: {ntype}")

inputs = {}
connected = {inp['name'] for inp in node.get('inputs', []) if inp.get('link')}
print(f"Connected inputs: {connected}")

# Process connections
for inp in node.get('inputs', []):
    link_id = inp.get('link')
    if link_id:
        resolved = exporter._resolve_link(link_id)
        print(f"  {inp['name']}: link={link_id}, resolved={resolved}")
        if resolved:
            inputs[inp['name']] = [str(resolved[0]), resolved[1]]

print(f"\nFinal inputs after connections: {inputs}")
