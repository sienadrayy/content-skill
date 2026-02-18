import json
import requests
import uuid

with open('qwen_z_v2.json') as f:
    workflow = json.load(f)

# Remove Note nodes
for nid in list(workflow.keys()):
    if workflow[nid].get('class_type') == 'Note':
        del workflow[nid]
        print(f"Removed Note node: {nid}")

payload = {
    'prompt': workflow,
    'client_id': str(uuid.uuid4())
}

print(f"\nSubmitting {len(workflow)} nodes to ComfyUI...")
response = requests.post('http://192.168.29.60:8188/prompt', json=payload)
result = response.json()

if 'prompt_id' in result:
    print(f"\nSUCCESS!")
    print(f"Prompt ID: {result['prompt_id']}")
else:
    print(f"\nFAILED: {result.get('error', {}).get('message')}")
    if result.get('node_errors'):
        for nid in list(result['node_errors'].keys())[:5]:
            errs = result['node_errors'][nid]['errors']
            print(f"  Node {nid}: {[e['message'] for e in errs[:2]]}")
