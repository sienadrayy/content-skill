import json

with open('videos_run.json') as f:
    api = json.load(f)

# Check if source nodes for 623 exist
source_nodes = ['620', '610', '608', '619', '618', '615']
print("Source nodes for 623:")
for nid in source_nodes:
    exists = nid in api
    print(f"  {nid}: {'EXISTS' if exists else 'MISSING'}")

# Check node 623
print(f"\nNode 623 inputs: {api.get('623', {}).get('inputs', {})}")
