import json

with open('videos_v6.json') as f:
    api = json.load(f)

for nid in ['508', '546', '549', '568']:
    if nid in api:
        print(f"Node {nid} ({api[nid].get('class_type')}):")
        print(f"  inputs: {api[nid].get('inputs')}")
    else:
        print(f"Node {nid}: NOT IN OUTPUT")
