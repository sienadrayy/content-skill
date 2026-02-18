import json
import sys
sys.path.insert(0, 'C:\\Users\\mohit\\.openclaw\\workspace')

with open(r'\\192.168.29.60\workflows\Videos_workflow.json', encoding='utf-8', errors='ignore') as f:
    wf = json.load(f)

from comfyui_export_api_v6 import ComfyUIExporter
exporter = ComfyUIExporter(wf)

# Check source nodes
source_nodes = [620, 610, 608, 619, 618, 615]
print("Source node analysis:")
for nid in source_nodes:
    node = exporter.nodes.get(nid)
    if node:
        ntype = node.get('type')
        mode = node.get('mode', 0)
        is_uuid = len(ntype) == 36 and ntype.count('-') == 4 if ntype else False
        in_defs = ntype in exporter.node_defs if ntype else False
        print(f"  {nid}: type={ntype}, mode={mode}, is_uuid={is_uuid}, in_defs={in_defs}")
    else:
        print(f"  {nid}: NOT IN NODES")
