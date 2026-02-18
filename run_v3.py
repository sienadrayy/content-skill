import json
import requests
import uuid

with open('images_api_v3.json') as f:
    api = json.load(f)

# 2 random prompts
prompts = """siena in a luxurious penthouse, wearing sheer black lace bodysuit, golden hour light, confident pose leaning against marble pillar, cinematic photography
siena on a yacht at sunset, white bikini with gold accents, wind in hair, Mediterranean sea background, warm orange lighting, fashion photography"""

api['443']['inputs']['value'] = prompts
api['500']['inputs']['value'] = "test_v3_run"

print(f"Prompts: 2")
print(f"Name: test_v3_run")
print(f"Nodes: {len(api)}")

payload = {'prompt': api, 'client_id': str(uuid.uuid4())}
response = requests.post('http://192.168.29.60:8188/prompt', json=payload)
result = response.json()

if 'prompt_id' in result:
    print(f"\nSUCCESS! Prompt ID: {result['prompt_id']}")
else:
    print(f"\nFAILED: {result.get('error', {}).get('message')}")
    if result.get('node_errors'):
        for nid, errs in list(result['node_errors'].items())[:10]:
            print(f"  Node {nid}: {[e['message'] for e in errs['errors']]}")
