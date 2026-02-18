import json
import sys
sys.path.insert(0, 'C:\\Users\\mohit\\.openclaw\\workspace')

with open(r'\\192.168.29.60\workflows\Videos_workflow.json', encoding='utf-8', errors='ignore') as f:
    wf = json.load(f)

from comfyui_export_api_v6 import ComfyUIExporter
exporter = ComfyUIExporter(wf)

# Find node 623 and check its links
node_623 = exporter.nodes.get(623)
if node_623:
    print("Node 623 link resolution:")
    for inp in node_623.get('inputs', []):
        link_id = inp.get('link')
        if link_id:
            link = exporter.links.get(link_id)
            if link:
                src_node = link[1]
                src_slot = link[2]
                src_in_nodes = src_node in exporter.nodes
                src_bypassed = src_node in exporter.bypassed
                print(f"  {inp['name']}: link={link_id}, src={src_node}:{src_slot}, in_nodes={src_in_nodes}, bypassed={src_bypassed}")
            else:
                print(f"  {inp['name']}: link={link_id} NOT FOUND")
