import json
import requests
import uuid

# Load the converted workflow
with open('qwen_z_converted_fixed.json') as f:
    workflow = json.load(f)

# Remove 'Note' nodes
nodes_to_remove = []
for node_id, node in list(workflow.items()):
    if node.get('class_type') == 'Note':
        nodes_to_remove.append(node_id)
        print(f"Removing Note node: {node_id}")

for node_id in nodes_to_remove:
    del workflow[node_id]

print(f"Nodes after cleanup: {len(workflow)}")

# Prepare payload
payload = {
    'prompt': workflow,
    'client_id': str(uuid.uuid4())
}

# Submit
print("Submitting to ComfyUI...")
response = requests.post('http://192.168.29.60:8188/prompt', json=payload)
result = response.json()

if 'prompt_id' in result:
    prompt_id = result['prompt_id']
    print(f"\nSUCCESS!")
    print(f"Prompt ID: {prompt_id}")
    print(f"\nQwen + Z image workflow is now running!")
else:
    print(f"\nFAILED")
    err = result.get('error', {})
    print(f"Error: {err.get('message')}")
    if result.get('node_errors'):
        print(f"Node errors: {len(result['node_errors'])} nodes")
        for nid in list(result['node_errors'].keys())[:3]:
            errors = result['node_errors'][nid]
            for e in errors.get('errors', [])[:1]:
                print(f"  Node {nid}: {e.get('message')}")
