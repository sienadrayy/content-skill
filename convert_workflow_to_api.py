import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# Read workflow from network
workflow_path = r"\\192.168.29.60\workflows\image_z_image_turbo.json"

with open(workflow_path, 'r') as f:
    ui_workflow = json.load(f)

# Node types that are UI-only and shouldn't be included in API execution
SKIP_TYPES = ['MarkdownNote', 'Note', 'Reroute']

# Convert UI format to API format
api_workflow = {}

if 'nodes' in ui_workflow:
    for node in ui_workflow['nodes']:
        node_id = str(node['id'])
        
        # class_type is in 'type' field for UI format
        class_type = node.get('type') or node.get('class_type')
        
        # Skip non-executable node types
        if class_type in SKIP_TYPES:
            print(f"Skipping UI-only node {node_id} ({class_type})")
            continue
        
        # Skip subgraph nodes (have UUID as class_type)
        if re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', class_type):
            print(f"Skipping subgraph node {node_id} ({class_type})")
            continue
        
        api_node = {
            "inputs": {},
            "class_type": class_type
        }
        
        # Process inputs
        if 'inputs' in node:
            input_list = node['inputs']
            widget_values = node.get('widgets_values', [])
            widget_index = 0
            
            for inp in input_list:
                inp_name = inp.get('name', '')
                
                # If input has a link, use the link reference
                if 'link' in inp and inp['link'] is not None:
                    api_node['inputs'][inp_name] = [str(inp['link']), inp.get('slot_index', 0)]
                # Otherwise use widget value if available
                elif 'widget' in inp and widget_index < len(widget_values):
                    api_node['inputs'][inp_name] = widget_values[widget_index]
                    widget_index += 1
        
        api_workflow[node_id] = api_node

# Update the prompt in node 58
for node_id, node_data in api_workflow.items():
    if 'value' in node_data['inputs']:
        node_data['inputs']['value'] = "Siena is standing in garden"
        print(f"Updated prompt in node {node_id}: 'Siena is standing in garden'")

print(f"Converted {len(api_workflow)} executable nodes to API format")

# Save the converted workflow for inspection
with open('z_image_api_converted.json', 'w') as f:
    json.dump(api_workflow, f, indent=2)
print(f"Saved converted workflow to z_image_api_converted.json")

# Submit to ComfyUI
import urllib.request

url = "http://192.168.29.60:8188/prompt"
payload = {"prompt": api_workflow}
req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(f"\nWorkflow submitted successfully!")
        print(f"Prompt ID: {result.get('prompt_id', 'N/A')}")
except urllib.error.HTTPError as e:
    print(f"\nHTTP Error {e.code}: {e.reason}")
    error_body = e.read().decode('utf-8')
    print(f"Error details: {error_body}")
except Exception as e:
    print(f"Error: {e}")
