#!/usr/bin/env python3
import sys
sys.path.insert(0, r"C:\Users\mohit\.openclaw\workspace\comfyui-workflow-runner\scripts")
from run_workflow import ComfyUIRunner

runner = ComfyUIRunner("http://192.168.29.60:8188")

print("="*80)
print("IMAGES WORKFLOW - WITH INPUTS")
print("="*80)

# Load Images workflow
print("\n[1] Loading Images_workflow.json...")
wf = runner.load_workflow(r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Images_workflow.json")
print(f"    [OK] Loaded")

# Substitute inputs
print("\n[2] Substituting inputs...")
inputs = {
    "500.value": "test",
    "443.value": "siena is standing in rain"
}
wf = runner.substitute_inputs(wf, inputs)
print(f"    [OK] Inputs substituted")

# Submit
print("\n[3] Submitting workflow...")
prompt_id = runner.submit_workflow(wf)

if prompt_id:
    print(f"\n[SUCCESS] Prompt ID: {prompt_id}")
    sys.exit(0)
else:
    print(f"\n[FAILED] Could not submit")
    sys.exit(1)
