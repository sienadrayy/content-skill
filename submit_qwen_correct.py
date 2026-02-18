import json
import requests
import uuid

# Load the Qwen workflow
with open('qwen_z_image_api_clean.json') as f:
    workflow = json.load(f)

client_id = str(uuid.uuid4())

# Wrap in the correct format
payload = {
    'prompt': workflow,
    'client_id': client_id
}

print(f"Submitting Qwen + Z image workflow")
print(f"  Nodes: {len(workflow)}")
print(f"  Client ID: {client_id}")

response = requests.post('http://192.168.29.60:8188/prompt', json=payload)
print(f"\nStatus: {response.status_code}")
result = response.json()

if 'prompt_id' in result:
    print(f"\n✓ SUCCESS!")
    print(f"  Prompt ID: {result['prompt_id']}")
    print(f"  Output will be in: ComfyUI/output/")
else:
    print(f"\nError: {result.get('error', {}).get('message', 'Unknown error')}")
    if result.get('node_errors'):
        print(f"\nNode errors:")
        for node_id, errors in result['node_errors'].items():
            print(f"  Node {node_id}:")
            for err in errors.get('errors', []):
                print(f"    - {err.get('message')}")
