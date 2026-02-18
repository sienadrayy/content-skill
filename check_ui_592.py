import json

with open(r'\\192.168.29.60\workflows\Qwen + Z image.json', encoding='utf-8', errors='ignore') as f:
    ui = json.load(f)

node592 = ui.get('592', {})
print('Node 592 in UI workflow:')
print(f'  Type: {node592.get("type")}')
print(f'  Title: {node592.get("title")}')
print(f'  Widget inputs:')
for name, inp in node592.get('inputs', {}).items():
    print(f'    {name}: {inp}')

# Check links
print('\nLinks involving node 592:')
link_count = 0
for link in ui.get('links', []):
    if link[1] == 592 or link[3] == 592:
        print(f'  {link}')
        link_count += 1
if link_count == 0:
    print('  (none found)')
