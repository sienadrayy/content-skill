import json
import requests

# Try the image_z_image_turbo API.json (the one mentioned as working)
with open(r'\\192.168.29.60\workflows\image_z_image_turbo API.json') as f:
    api = json.load(f)

print(f"Submitting 'image_z_image_turbo API.json' ({len(api)} nodes)...")

# Check structure
print(f"Root keys: {list(api.keys())}")
print(f"First node sample: {list(api.values())[0]}")

response = requests.post('http://192.168.29.60:8188/prompt', json=api)
print(f"\nStatus: {response.status_code}")
result = response.json()
if 'prompt_id' in result:
    print(f"✓ SUCCESS - Prompt ID: {result['prompt_id']}")
else:
    print(f"Error: {json.dumps(result, indent=2)}")
