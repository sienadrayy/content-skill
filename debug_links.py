import json

# Load converted workflow
with open('videos_run.json') as f:
    api = json.load(f)

# Check node 623's expected connections
print("Node 623 inputs (from API):")
for k, v in api.get('623', {}).get('inputs', {}).items():
    print(f"  {k}: {v}")

# Load raw expanded workflow to check links
with open(r'\\192.168.29.60\workflows\Videos_workflow.json', encoding='utf-8', errors='ignore') as f:
    wf = json.load(f)

# Simulate expansion to see what happens
import sys
sys.path.insert(0, 'C:\\Users\\mohit\\.openclaw\\workspace')
from comfyui_export_api_v6 import ComfyUIExporter

exporter = ComfyUIExporter(wf)

# Check if node 623 exists in exporter.nodes
print(f"\nNode 623 in exporter.nodes: {623 in exporter.nodes}")

# Find KSamplerAdvanced nodes
for nid, node in exporter.nodes.items():
    if node.get('type') == 'KSamplerAdvanced':
        print(f"\nNode {nid} (KSamplerAdvanced):")
        for inp in node.get('inputs', []):
            link_id = inp.get('link')
            if link_id:
                link_exists = link_id in exporter.links
                print(f"  {inp['name']}: link={link_id}, exists={link_exists}")
