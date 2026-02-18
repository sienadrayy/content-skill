import requests
import json

# Test 1: Check if server is alive
try:
    resp = requests.get("http://192.168.29.60:8188", timeout=5)
    print(f"Server alive: {resp.status_code}")
except Exception as e:
    print(f"Server not accessible: {e}")
    exit(1)

# Test 2: Load the generated API
with open('\\\\192.168.29.60\\workflows\\z_image_turbo_api.json') as f:
    api_wf = json.load(f)

# Remove MarkdownNote
if '35' in api_wf:
    del api_wf['35']

print(f"\nWorkflow nodes: {list(api_wf.keys())}")
print(f"Total nodes: {len(api_wf)}")

# Test 3: Try submitting
print("\nSubmitting...")
print(f"Payload size: {len(json.dumps(api_wf))} bytes")

resp = requests.post(
    "http://192.168.29.60:8188/prompt",
    json=api_wf,
    timeout=30
)

print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")

# Parse error if any
if resp.status_code != 200:
    try:
        error_data = resp.json()
        print(f"\nError details:")
        print(json.dumps(error_data, indent=2))
        
        # Check for node_errors
        if 'node_errors' in error_data:
            for node_id, errors in error_data['node_errors'].items():
                print(f"\n  Node {node_id}: {errors}")
    except:
        pass
