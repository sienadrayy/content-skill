import json

with open('videos_v6c.json') as f:
    api = json.load(f)

for nid, node in api.items():
    if node.get('class_type') == 'KSamplerAdvanced':
        print(f"Node {nid}:")
        inputs = node.get('inputs', {})
        for k in ['sampler_name', 'scheduler', 'steps', 'cfg', 'start_at_step', 'end_at_step']:
            print(f"  {k}: {inputs.get(k, 'MISSING')}")
        print()
