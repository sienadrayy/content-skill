import json

with open('\\\\192.168.29.60\\workflows\\image_z_image_turbo.json') as f:
    wf = json.load(f)
    sg_def = wf['definitions']['subgraphs'][0]
    
    # Check subgraph input 1 (width)
    print("Subgraph input 1 (width):")
    inp1 = sg_def['inputs'][1]
    print(f"  Name: {inp1['name']}")
    print(f"  LinkIds: {inp1.get('linkIds')}")
    
    # Find the links with those IDs
    for link_id in inp1.get('linkIds', []):
        for link in sg_def.get('links', []):
            if link['id'] == link_id:
                print(f"  Link {link_id}: from node {link['origin_id']} slot {link['origin_slot']} -> to node {link['target_id']} slot {link['target_slot']}")
    
    # Now check the subgraph node's widget values
    sg_node = [n for n in wf['nodes'] if n['id'] == 57][0]
    print(f"\nSubgraph node 57 widgets: {sg_node['widgets_values']}")
    
    # The widget values should map to the inputs like this:
    # Input 0 (text): widget value at index 0 (empty string, but overridden by link 63)
    # Input 1 (width): widget value at index 1 (1536)
    # Input 2 (height): widget value at index 2 (2048)
    
    print("\nFor flattening:")
    print("  Input 0 (text): comes from link 63 (node 58 slot 0)")
    print("  Input 1 (width): widget value 1536")
    print("  Input 2 (height): widget value 2048")
    
    # These widget values need to be passed to the internal nodes
    # Let's find which internal nodes use them
    print("\nInternal nodes consuming -10:")
    for link in sg_def.get('links', []):
        if link['origin_id'] == -10:
            print(f"  Link {link['id']}: -10 slot {link['origin_slot']} -> node {link['target_id']} slot {link['target_slot']}")
