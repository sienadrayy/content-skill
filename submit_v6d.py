import json
import requests
import uuid

with open('videos_v6d.json') as f:
    api = json.load(f)

api['436']['inputs']['value'] = """slow confident movement, direct eye contact, warm golden lighting, cinematic
graceful body roll, silk fabric flowing, dramatic shadows, sensual energy"""
api['500']['inputs']['value'] = "siena_video_test"

payload = {'prompt': api, 'client_id': str(uuid.uuid4())}
r = requests.post('http://192.168.29.60:8188/prompt', json=payload)
result = r.json()

if 'prompt_id' in result:
    print(f"SUCCESS! {result['prompt_id']}")
else:
    print(f"FAILED: {result.get('error', {}).get('message')}")
    for nid, errs in list(result.get('node_errors', {}).items())[:5]:
        print(f"  {nid}: {[e['message'] for e in errs['errors'][:3]]}")
