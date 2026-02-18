import json
import requests

# Read the generated API
with open('\\\\192.168.29.60\\workflows\\z_image_turbo_api.json') as f:
    api_wf = json.load(f)

# Remove MarkdownNote as it's not a real node
if '35' in api_wf:
    del api_wf['35']

print("Simplified workflow with MarkdownNote removed:")
print(f"Nodes: {list(api_wf.keys())}")

# Try submitting
response = requests.post(
    "http://192.168.29.60:8188/prompt",
    json=api_wf,
    timeout=30
)

print(f"\nStatus: {response.status_code}")
print(f"Response: {response.text[:500]}")
