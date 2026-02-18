import json
import requests

# Try submitting the already-converted API workflow
with open('qwen_z_image_api.json') as f:
    api = json.load(f)

print("=== CONVERTED API WORKFLOW ===")
print(f"Total nodes: {len(api)}")

# Check for SaveImage node
for nid, node in api.items():
    if node.get('class_type') == 'SaveImage':
        print(f"\nFound SaveImage at node {nid}")
        print(f"  Inputs: {node['inputs']}")

# Check for text encoding
for nid, node in api.items():
    if 'Text' in node.get('class_type', ''):
        print(f"\nFound text node {nid}: {node.get('class_type')}")
        print(f"  Inputs: {node['inputs']}")

# Try to submit
print("\n=== SUBMITTING ===")
response = requests.post('http://192.168.29.60:8188/prompt', json=api)
print(f"Status: {response.status_code}")
data = response.json()
print(f"Response: {json.dumps(data, indent=2)}")
