import json

with open(r'\\192.168.29.60\workflows\Images_workflow.json', encoding='utf-8', errors='ignore') as f:
    ui = json.load(f)

# Find all PrimitiveStringMultiline nodes
print("All PrimitiveStringMultiline nodes:")
for node in ui['nodes']:
    if node.get('type') == 'PrimitiveStringMultiline':
        mode = node.get('mode', 0)
        status = {0: 'ACTIVE', 2: 'muted', 4: 'bypassed'}.get(mode, f'mode={mode}')
        print(f"  Node {node['id']}: {node.get('title', 'untitled')} [{status}]")
        if mode == 0:
            wv = node.get('widgets_values', [])
            if wv:
                text = str(wv[0])[:100]
                print(f"    Content: {text}...")
