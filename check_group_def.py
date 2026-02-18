import json

with open(r'\\192.168.29.60\workflows\Images_workflow.json', encoding='utf-8', errors='ignore') as f:
    wf = json.load(f)

print("Top-level keys:", list(wf.keys()))

if 'extra' in wf:
    print("\nextra keys:", list(wf['extra'].keys()) if isinstance(wf['extra'], dict) else wf['extra'])
    if 'groupNodes' in wf.get('extra', {}):
        print("\nGroup nodes found!")
        for name, definition in wf['extra']['groupNodes'].items():
            print(f"  {name}:")
            if 'nodes' in definition:
                print(f"    Inner nodes: {len(definition['nodes'])}")
                for n in definition['nodes'][:3]:
                    print(f"      - {n.get('type')}")

if 'definitions' in wf:
    print("\ndefinitions:", list(wf['definitions'].keys()) if isinstance(wf['definitions'], dict) else "exists")
