import json

with open('images_wf_api.json') as f:
    w = json.load(f)

print(f"Total nodes: {len(w)}")
print("\nNodes:")
for k in sorted(w.keys(), key=lambda x: int(x) if x.isdigit() else 0):
    print(f"  {k}: {w[k].get('class_type')}")
