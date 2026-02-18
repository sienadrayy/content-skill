import json
import requests
import uuid

with open('qwen_api_v3.json') as f:
    api = json.load(f)

# Remove Note nodes
for nid in list(api.keys()):
    if api[nid].get('class_type') == 'Note':
        del api[nid]

print(f"Submitting {len(api)} nodes...")

payload = {'prompt': api, 'client_id': str(uuid.uuid4())}
response = requests.post('http://192.168.29.60:8188/prompt', json=payload)
result = response.json()

if 'prompt_id' in result:
    print(f"SUCCESS! Prompt ID: {result['prompt_id']}")
else:
    print(f"FAILED: {result.get('error', {}).get('message')}")
    if result.get('node_errors'):
        for nid, errs in list(result['node_errors'].items())[:5]:
            print(f"  Node {nid}: {[e['message'] for e in errs['errors'][:2]]}")
