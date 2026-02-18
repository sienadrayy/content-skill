import json
import requests
import uuid

with open('images_run.json') as f:
    api = json.load(f)

prompts = """siena in elegant red evening gown, standing by grand piano in dimly lit jazz lounge, dramatic side lighting, confident alluring gaze, luxury ambiance, cinematic photography
siena lounging on velvet chaise in silk robe, morning light through sheer curtains, relaxed sensual pose, soft warm tones, intimate boudoir setting, fine art photography"""

api['443']['inputs']['value'] = prompts
api['500']['inputs']['value'] = "siena_elegance"

payload = {'prompt': api, 'client_id': str(uuid.uuid4())}
response = requests.post('http://192.168.29.60:8188/prompt', json=payload)
result = response.json()

if 'prompt_id' in result:
    print(f"SUCCESS! Prompt ID: {result['prompt_id']}")
    print(f"Output: \\\\192.168.29.60\\output\\siena_elegance\\")
else:
    print(f"FAILED: {result.get('error', {}).get('message')}")
    if result.get('node_errors'):
        for nid, errs in list(result['node_errors'].items())[:5]:
            print(f"  Node {nid}: {[e['message'] for e in errs['errors'][:2]]}")
