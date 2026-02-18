import json

# Check what we're missing
with open('qwen_z_image_api_clean.json') as f:
    api = json.load(f)

# Look at a problematic node - 575 (KSampler)
node575 = api.get('575', {})
print("Node 575 (KSampler) inputs:")
print(json.dumps(node575.get('inputs', {}), indent=2))

print("\n\nWhat we probably need (typical KSampler):")
print("""
{
  "seed": 0,
  "steps": 20,
  "cfg": 7.0,
  "sampler_name": "euler",
  "scheduler": "normal",
  "denoise": 1.0,
  "model": [...],
  "positive": [...],
  "negative": [...],
  "latent_image": [...]
}
""")

# Check the original UI workflow
print("\n\nChecking original UI workflow...")
try:
    with open(r'\\192.168.29.60\workflows\Qwen + Z image.json', encoding='utf-8', errors='ignore') as f:
        ui = json.load(f)
    
    node575_ui = ui.get('575', {})
    print(f"\nNode 575 in UI: type={node575_ui.get('type')}")
    print(f"  Widgets: {list(node575_ui.get('widgets_values', [])[:5])}")
    print(f"  Widget dict: {node575_ui.get('widget_idx')}")
except Exception as e:
    print(f"Error: {e}")
