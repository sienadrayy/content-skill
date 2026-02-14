#!/usr/bin/env python3
import urllib.request
import json

server = "http://192.168.29.60:8188"

# Load the new format workflow
with open(r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Images_workflow.json", 'r') as f:
    workflow = json.load(f)

print(f"Workflow structure type: {type(workflow)}")
print(f"Workflow keys: {list(workflow.keys())[:10]}")

# Try to submit it
workflow_json = json.dumps(workflow).encode('utf-8')
print(f"\nPayload size: {len(workflow_json)} bytes")

req = urllib.request.Request(
    f"{server}/prompt",
    data=workflow_json,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    with urllib.request.urlopen(req, timeout=10) as response:
        response_data = response.read().decode('utf-8')
        print(f"\nResponse (raw): {response_data[:500]}")
        
        try:
            data = json.loads(response_data)
            print(f"\nResponse (parsed):")
            print(json.dumps(data, indent=2))
        except:
            print(f"Could not parse as JSON")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
    error_data = e.read().decode('utf-8')
    print(f"Error response: {error_data}")
except Exception as e:
    print(f"Error: {e}")
