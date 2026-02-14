#!/usr/bin/env python3
import json
from pathlib import Path

# Check Images workflow
print("=" * 70)
print("IMAGES WORKFLOW - STRUCTURE CHECK")
print("=" * 70)

images_path = Path("comfy-wf/openclaw/Images_workflow.json")
with open(images_path, encoding='utf-8') as f:
    images_wf = json.load(f)

# Check if old format (flat dict) or new format (has 'nodes' key)
if isinstance(images_wf, dict) and 'nodes' in images_wf:
    print("Format: NEW (nodes array)")
    nodes = {n.get('id'): n.get('type') for n in images_wf.get('nodes', [])}
elif isinstance(images_wf, dict) and all(isinstance(k, str) and k.isdigit() for k in list(images_wf.keys())[:5]):
    print("Format: OLD (flat dict with string node IDs)")
    node_ids = list(images_wf.keys())
    print(f"Total nodes: {len(node_ids)}")
    print(f"Node IDs: {sorted([k for k in node_ids if k.isdigit()])[:10]}")
    
    # Check key nodes
    print("\nKey Nodes (Old Format):")
    print(f"  Node 443 (Image Prompts): {images_wf.get('443', {}).get('class_type', 'NOT FOUND')}")
    print(f"  Node 500 (Name): {images_wf.get('500', {}).get('class_type', 'NOT FOUND')}")
    print(f"  Node 505 (For Loop): {images_wf.get('505', {}).get('class_type', 'NOT FOUND')}")
else:
    print("Format: UNKNOWN")
    print(f"Top-level keys: {list(images_wf.keys())[:5]}")

# Check Videos workflow
print("\n" + "=" * 70)
print("VIDEOS WORKFLOW - STRUCTURE CHECK")
print("=" * 70)

videos_path = Path("comfy-wf/openclaw/Videos_workflow.json")
with open(videos_path, encoding='utf-8') as f:
    videos_wf = json.load(f)

if isinstance(videos_wf, dict) and 'nodes' in videos_wf:
    print("Format: NEW (nodes array)")
    nodes = {n.get('id'): n.get('type') for n in videos_wf.get('nodes', [])}
elif isinstance(videos_wf, dict) and all(isinstance(k, str) and k.isdigit() for k in list(videos_wf.keys())[:5]):
    print("Format: OLD (flat dict with string node IDs)")
    node_ids = list(videos_wf.keys())
    print(f"Total nodes: {len(node_ids)}")
    
    # Check key nodes
    print("\nKey Nodes (Old Format):")
    print(f"  Node 436 (Video Prompts): {videos_wf.get('436', {}).get('class_type', 'NOT FOUND')}")
    print(f"  Node 500 (Name): {videos_wf.get('500', {}).get('class_type', 'NOT FOUND')}")
    print(f"  Node 516 (Load Images): {videos_wf.get('516', {}).get('class_type', 'NOT FOUND')}")
else:
    print("Format: UNKNOWN")
    print(f"Top-level keys: {list(videos_wf.keys())[:5]}")

print("\n" + "=" * 70)
print("CHANGES SUMMARY")
print("=" * 70)
print("\nLatest 3 commits to workflows:")
print("  1. 98ab388 - 'updated video wf api'")
print("     Videos_workflow.json: 342 insertions, 384 deletions")
print("\n  2. e8036fb - 'api wf'")
print("     Major refactor: both workflows significantly changed")
print("     Images: reduced from 12184 lines")
print("     Videos: reduced from 12368 lines")
print("\n  3. 9dd3122 - 'updated openclaw wf'")
print("     Images_workflow.json: 11534 insertions, 681 deletions")
print("\nCRITICAL: Node IDs (443, 436, 500, 505, 516) must remain unchanged")
print("          for comfyui-workflow-runner skill to work!")
