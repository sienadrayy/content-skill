import json
import requests
import uuid

with open('images_v4.json') as f:
    api = json.load(f)

# Set prompts and name
if '443' in api:
    api['443']['inputs']['value'] = """siena in red evening gown at jazz lounge, dramatic side lighting, confident alluring gaze, cinematic
siena lounging in silk robe, morning light through curtains, soft warm tones, intimate boudoir, fine art"""
if '500' in api:
    api['500']['inputs']['value'] = "siena_v4_test"

# Remove unsupported nodes
to_remove = [nid for nid, n in api.items() if 'rgthree' in n.get('class_type', '').lower()]
for nid in to_remove:
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
