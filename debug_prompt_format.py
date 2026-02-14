#!/usr/bin/env python3
import json
import urllib.request
import urllib.error

# Get workflow
with open(r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Images_workflow.json", 'r') as f:
    wf_new = json.load(f)

print(f"Workflow type: {type(wf_new)}")
print(f"Has 'nodes': {'nodes' in wf_new}")

# Try submitting as-is (new format)
print("\n" + "="*80)
print("ATTEMPT 1: Send new format directly")
print("="*80)

payload = json.dumps(wf_new).encode('utf-8')
print(f"Payload size: {len(payload)} bytes")

req = urllib.request.Request(
    "http://192.168.29.60:8188/prompt",
    data=payload,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    with urllib.request.urlopen(req, timeout=10) as response:
        print(f"SUCCESS: {response.status}")
        print(response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    error_data = e.read().decode('utf-8')
    print(f"ERROR {e.code}: {error_data[:300]}")
