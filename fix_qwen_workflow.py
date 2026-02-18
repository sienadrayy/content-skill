import json

with open('qwen_z_image_api.json') as f:
    api = json.load(f)

# Fix node 592 - connect text from node 594
api['592']['inputs']['text'] = ['594', 0]

# Remove unused nodes
unused = ['576', '581', '612', '634', '639', '642', '643', '644', '646']
for nid in unused:
    if nid in api:
        del api[nid]

# Save fixed version
with open('qwen_z_image_api_clean.json', 'w') as f:
    json.dump(api, f, indent=2)

print("Fixed workflow saved to qwen_z_image_api_clean.json")
print(f"Removed {len(unused)} unused nodes")
print(f"Fixed node 592: added text input from node 594")

# Try submit
import requests
response = requests.post('http://192.168.29.60:8188/prompt', json=api)
print(f"\nSubmit status: {response.status_code}")
result = response.json()
if 'prompt_id' in result:
    print(f"✓ SUCCESS - Prompt ID: {result['prompt_id']}")
else:
    print(f"Error: {result.get('error', {}).get('message', 'Unknown')}")
    if result.get('node_errors'):
        print(f"Node errors: {result['node_errors']}")
