import json
import requests
import uuid

# Load the converted workflow
with open('qwen_z_converted_fixed.json') as f:
    workflow = json.load(f)

# Remove 'Note' nodes and other non-essential nodes
nodes_to_remove = []
for node_id, node in list(workflow.items()):
    if node.get('class_type') == 'Note':
        nodes_to_remove.append(node_id)
        print(f"Removing unused Note node: {node_id}")

for node_id in nodes_to_remove:
    del workflow[node_id]

print(f"\nNodes after cleanup: {len(workflow)}")

# Prepare payload
payload = {
    'prompt': workflow,
    'client_id': str(uuid.uuid4())
}

# Submit
print("\nSubmitting to ComfyUI...")
response = requests.post('http://192.168.29.60:8188/prompt', json=payload)
result = response.json()

if 'prompt_id' in result:
    print(f"\n✓ SUCCESS")
    print(f"Prompt ID: {result['prompt_id']}")
    print(f"\nQwen + Z image workflow is now running on ComfyUI server!")
    print(f"Output will be in: \\\\192.168.29.60\\output\\")
else:
    print(f"\n✗ FAILED")
    err = result.get('error', {})
    print(f"Error: {err.get('message')}")
    if result.get('node_errors'):
        print(f"\nNode errors:")
        for nid, errors in result['node_errors'].items():
            for e in errors.get('errors', []):
                print(f"  Node {nid}: {e.get('message')}")
