import json
import requests
import uuid

# Load converted workflow
with open('images_wf_api.json') as f:
    workflow = json.load(f)

# Set 2 random prompts in Node 443
prompts = """siena in a luxurious penthouse, wearing a sheer black lace bodysuit, golden hour light streaming through floor-to-ceiling windows, confident pose leaning against marble pillar, sensual yet elegant, cinematic photography
siena on a yacht at sunset, white bikini with gold accents, wind in her hair, Mediterranean sea in background, playful smile, warm orange lighting, professional fashion photography"""

workflow['443']['inputs']['value'] = prompts

# Set output name in Node 500
workflow['500']['inputs']['value'] = "test_converter_run"

print(f"Node 443: 2 prompts set")
print(f"Node 500: test_converter_run")

# Remove unsupported nodes
nodes_to_remove = []
for nid, node in workflow.items():
    class_type = node.get('class_type', '')
    if 'rgthree' in class_type.lower():
        nodes_to_remove.append(nid)
    elif len(class_type) == 36 and class_type.count('-') == 4:  # UUID
        nodes_to_remove.append(nid)

for nid in nodes_to_remove:
    print(f"Removing: {nid} ({workflow[nid].get('class_type')})")
    del workflow[nid]

# Submit
payload = {
    'prompt': workflow,
    'client_id': str(uuid.uuid4())
}

print(f"\nSubmitting {len(workflow)} nodes...")
response = requests.post('http://192.168.29.60:8188/prompt', json=payload)
result = response.json()

if 'prompt_id' in result:
    print(f"\nSUCCESS!")
    print(f"Prompt ID: {result['prompt_id']}")
else:
    print(f"\nFAILED: {result.get('error', {}).get('message')}")
    if result.get('node_errors'):
        for nid, errs in list(result['node_errors'].items())[:5]:
            print(f"  Node {nid}: {[e['message'] for e in errs['errors'][:2]]}")
