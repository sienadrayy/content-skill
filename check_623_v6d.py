import json

with open('videos_v6d.json') as f:
    api = json.load(f)

print("Node 623 inputs:")
for k, v in api.get('623', {}).get('inputs', {}).items():
    print(f"  {k}: {v}")
