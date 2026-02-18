import json
import requests
import uuid

with open('images_v5.json') as f:
    api = json.load(f)

if '443' in api:
    api['443']['inputs']['value'] = """siena in red gown at jazz lounge, dramatic lighting, alluring gaze, cinematic
siena in silk robe, morning light, soft warm tones, intimate boudoir, fine art"""
if '500' in api:
    api['500']['inputs']['value'] = "siena_v5_test"

print(f"Nodes: {len(api)}")

payload = {'prompt': api, 'client_id': str(uuid.uuid4())}
r = requests.post('http://192.168.29.60:8188/prompt', json=payload)
result = r.json()

if 'prompt_id' in result:
    print(f"SUCCESS! {result['prompt_id']}")
else:
    print(f"FAILED: {result.get('error', {}).get('message')}")
    for nid, errs in list(result.get('node_errors', {}).items())[:8]:
        print(f"  {nid}: {[e['message'] for e in errs['errors'][:2]]}")
