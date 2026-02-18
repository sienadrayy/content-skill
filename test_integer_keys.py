import requests
import json

# Load the generated API
with open('\\\\192.168.29.60\\workflows\\z_image_turbo_api.json') as f:
    api_wf = json.load(f)

# Remove MarkdownNote
if '35' in api_wf:
    del api_wf['35']

# Convert string keys to integers
api_wf_int = {int(k): v for k, v in api_wf.items()}

# Also convert node references from strings to integers
def convert_refs(obj):
    if isinstance(obj, dict):
        return {k: convert_refs(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        if len(obj) == 2 and isinstance(obj[0], str) and obj[0].isdigit():
            return [int(obj[0]), obj[1]]
        return [convert_refs(v) for v in obj]
    return obj

api_wf_int = convert_refs(api_wf_int)

print(f"Converted to integer keys")
print(f"Nodes: {list(api_wf_int.keys())}")

# Submit
resp = requests.post(
    "http://192.168.29.60:8188/prompt",
    json=api_wf_int,
    timeout=30
)

print(f"\nStatus: {resp.status_code}")
print(f"Response: {resp.text[:500]}")

if resp.status_code == 200:
    print(f"\nSUCCESS!")
    result = resp.json()
    print(f"Prompt ID: {result.get('prompt_id')}")
