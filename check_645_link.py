import json

with open(r'\\192.168.29.60\workflows\Qwen + Z image.json', encoding='utf-8', errors='ignore') as f:
    ui = json.load(f)

# Find node 645's model link
for node in ui['nodes']:
    if node['id'] == 645:
        print("Node 645 inputs:")
        for inp in node.get('inputs', []):
            print(f"  {inp['name']}: link_id={inp.get('link')}")
        
        # Find the actual link
        model_link_id = None
        for inp in node.get('inputs', []):
            if inp['name'] == 'model':
                model_link_id = inp.get('link')
                break
        
        if model_link_id:
            # Find link in links array
            for link in ui['links']:
                if link[0] == model_link_id:
                    print(f"\nLink {model_link_id}:")
                    print(f"  Source node: {link[1]}, slot: {link[2]}")
                    print(f"  Target node: {link[3]}, slot: {link[4]}")
                    print(f"  Type: {link[5]}")
        break
