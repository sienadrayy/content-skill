import json
import requests
import uuid

with open('qwen_z_final.json') as f:
    workflow = json.load(f)

# Remove Note nodes
for nid in list(workflow.keys()):
    if workflow[nid].get('class_type') == 'Note':
        del workflow[nid]
        print(f"Removed Note: {nid}")

payload = {
    'prompt': workflow,
    'client_id': str(uuid.uuid4())
}

print(f"Submitting {len(workflow)} nodes...")
response = requests.post('http://192.168.29.60:8188/prompt', json=payload)
result = response.json()

if 'prompt_id' in result:
    print(f"\nSUCCESS! Prompt ID: {result['prompt_id']}")
else:
    print(f"\nFAILED: {result.get('error', {}).get('message')}")
    if result.get('node_errors'):
        for nid, errs in list(result['node_errors'].items())[:5]:
            print(f"  Node {nid}: {[e['message'] for e in errs['errors'][:2]]}")
