import json

with open('videos_run.json') as f:
    api = json.load(f)

if '623' in api:
    print("Node 623 (KSamplerAdvanced):")
    inputs = api['623'].get('inputs', {})
    for k, v in inputs.items():
        print(f"  {k}: {v}")
else:
    print("Node 623 NOT FOUND")
    
# Check what nodes exist
print(f"\nTotal nodes: {len(api)}")
ksampler_nodes = [k for k, v in api.items() if 'KSampler' in v.get('class_type', '')]
print(f"KSampler nodes: {ksampler_nodes}")
