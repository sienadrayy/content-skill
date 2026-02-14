#!/usr/bin/env python3
import json

with open(r'C:\Users\mohit\Downloads\image_z_image_turbo.json') as f:
    wf = json.load(f)

print("Top-level keys:", list(wf.keys()))

if 'definitions' in wf:
    print(f"\nDefinitions found: {len(wf['definitions'])} entries")
    for key in list(wf['definitions'].keys())[:5]:
        print(f"  {key}: {wf['definitions'][key]}")
else:
    print("\nNo 'definitions' key")

# Check node 57
print("\n" + "="*80)
print("NODE 57 DETAILS")
print("="*80)

for node in wf.get('nodes', []):
    if node.get('id') == 57:
        print(json.dumps(node, indent=2)[:800])
