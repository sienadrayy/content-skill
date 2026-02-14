#!/usr/bin/env python3
import sys
sys.path.insert(0, r"C:\Users\mohit\.openclaw\workspace\comfyui-workflow-runner\scripts")
from run_workflow import ComfyUIRunner

runner = ComfyUIRunner("http://192.168.29.60:8188")

print("=" * 80)
print("SIMPLE WORKFLOW - ONE RUN ONLY")
print("=" * 80)

# Load workflow
print("\nLoading: C:\\Users\\mohit\\Downloads\\image_z_image_turbo.json")
wf = runner.load_workflow(r"C:\Users\mohit\Downloads\image_z_image_turbo.json")

# Submit directly
print("Submitting...")
prompt_id = runner.submit_workflow(wf)

if prompt_id:
    print(f"\n[SUCCESS] Prompt ID: {prompt_id}")
else:
    print(f"\n[FAILED] Could not submit")
