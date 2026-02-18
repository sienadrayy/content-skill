import json

with open('videos_v6.json') as f:
    api = json.load(f)

print("SaveImage/PreviewImage nodes:")
for nid, node in api.items():
    ct = node.get('class_type', '')
    if 'Save' in ct or 'Preview' in ct or 'Purge' in ct:
        inputs = node.get('inputs', {})
        has_images = 'images' in inputs or 'anything' in inputs
        print(f"  {nid} ({ct}): {'OK' if has_images else 'MISSING INPUT'}")
        if not has_images:
            print(f"    inputs: {inputs}")
