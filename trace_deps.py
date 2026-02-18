import json

with open('qwen_z_image_api.json') as f:
    api = json.load(f)

def trace_node(node_id, visited=None, depth=0):
    if visited is None:
        visited = set()
    if node_id in visited:
        return
    visited.add(node_id)
    
    node = api.get(node_id)
    if not node:
        print("  " * depth + f"[{node_id}] NOT FOUND")
        return
    
    print("  " * depth + f"[{node_id}] {node.get('class_type')}")
    
    for key, val in node.get('inputs', {}).items():
        if isinstance(val, list) and len(val) >= 2:
            next_node = str(val[0])
            trace_node(next_node, visited, depth + 1)

print("=== DEPENDENCY CHAIN FROM SaveImage ===")
trace_node('638')

print("\n=== All nodes not in dependency chain ===")
visited = set()
def collect_deps(node_id, visited):
    if node_id in visited:
        return
    visited.add(node_id)
    node = api.get(node_id)
    if node:
        for key, val in node.get('inputs', {}).items():
            if isinstance(val, list) and len(val) >= 2:
                collect_deps(str(val[0]), visited)

collect_deps('638', visited)
for nid in sorted(api.keys()):
    if nid not in visited:
        print(f"  [{nid}] {api[nid].get('class_type')} - UNUSED")
