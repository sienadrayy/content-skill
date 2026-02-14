#!/usr/bin/env python3
import sys
import json
sys.path.insert(0, r"C:\Users\mohit\.openclaw\workspace\comfyui-workflow-runner\scripts")
from run_workflow import ComfyUIRunner

print("="*80)
print("SIMPLE WORKFLOW TEST")
print("="*80)

runner = ComfyUIRunner("http://192.168.29.60:8188")

# Load simple workflow
print("\n[1] Loading workflow...")
try:
    wf = runner.load_workflow(r"C:\Users\mohit\Downloads\image_z_image_turbo.json")
    print(f"    [OK] Loaded - {type(wf)} with {len(wf)} keys")
except Exception as e:
    print(f"    [ERROR] {e}")
    sys.exit(1)

# Check format
print("\n[2] Checking format...")
if 'nodes' in wf:
    print(f"    [INFO] New format - {len(wf.get('nodes', []))} nodes")
else:
    print(f"    [INFO] Old format")

# Submit directly without substitution
print("\n[3] Submitting workflow...")
prompt_id = runner.submit_workflow(wf)

if prompt_id:
    print(f"    [SUCCESS] Prompt ID: {prompt_id}")
else:
    print(f"    [FAILED]")
