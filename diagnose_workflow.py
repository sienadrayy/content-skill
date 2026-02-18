import json

with open('qwen_z_converted_fixed.json') as f:
    workflow = json.load(f)

# Check critical nodes
critical_nodes = ['575', '579', '580', '590', '591', '592', '593', '638']

print("CRITICAL NODE ANALYSIS:\n")
for node_id in critical_nodes:
    node = workflow.get(node_id, {})
    class_type = node.get('class_type', 'NOT FOUND')
    inputs = node.get('inputs', {})
    
    print(f"Node {node_id} - {class_type}")
    for k, v in inputs.items():
        if isinstance(v, list):
            print(f"  {k}: -> [{v[0]}:{v[1]}]")
        else:
            val_str = str(v)[:60] if len(str(v)) > 60 else str(v)
            print(f"  {k}: {val_str}")
    print()

# Check if KSampler has all required inputs
print("\n--- KSampler 575 Required Inputs Check ---")
ksampler = workflow.get('575', {}).get('inputs', {})
required = ['seed', 'steps', 'cfg', 'sampler_name', 'scheduler', 'denoise', 'model', 'positive', 'negative', 'latent_image']
for req in required:
    if req in ksampler:
        print(f"  {req}: OK")
    else:
        print(f"  {req}: MISSING!")
