import json
import requests

# Try the z_image_turbo_api.json that was exported from ComfyUI
with open(r'\\192.168.29.60\workflows\z_image_turbo_api.json') as f:
    api = json.load(f)

print(f"Submitting z_image_turbo_api.json ({len(api)} nodes)...")
response = requests.post('http://192.168.29.60:8188/prompt', json=api)
print(f"Status: {response.status_code}")
result = response.json()
if 'prompt_id' in result:
    print(f"✓ SUCCESS - Prompt ID: {result['prompt_id']}")
else:
    print(f"Response: {json.dumps(result, indent=2)}")
