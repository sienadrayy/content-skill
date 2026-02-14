#!/usr/bin/env python3
"""
Test script: Run Images_workflow.json twice with different group configurations
- First run: Enable Images, disable Videos
- Second run: Disable Images, enable Videos
- 5 second delay between runs
"""

import sys
import time
import subprocess
import json

sys.path.insert(0, r"C:\Users\mohit\.openclaw\workspace\comfyui-workflow-runner\scripts")
from run_workflow import ComfyUIRunner

def run_workflow(name, image_prompts, video_prompts, mode_value):
    """Run workflow with specified inputs"""
    print("\n" + "="*80)
    print(f"RUNNING WORKFLOW: {name}")
    print("="*80)
    print(f"Name: {name}")
    print(f"Image Prompts: {image_prompts[:50]}...")
    print(f"Video Prompts: {video_prompts[:50]}...")
    print(f"Mode (Group Control): {mode_value}")
    print("-"*80)
    
    runner = ComfyUIRunner("http://192.168.29.60:8188")
    
    # Load workflow
    workflow = runner.load_workflow(r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Images_workflow.json")
    
    # Substitute inputs
    inputs = {
        "500.value": name,
        "443.value": image_prompts,
        "436.value": video_prompts,
        "519.mode": mode_value
    }
    workflow = runner.substitute_inputs(workflow, inputs)
    
    # Submit
    prompt_id = runner.submit_workflow(workflow)
    
    if prompt_id:
        print(f"SUCCESS: Workflow submitted with Prompt ID: {prompt_id}")
        return prompt_id
    else:
        print(f"FAILED: Could not submit workflow")
        return None

def main():
    print("\n" + "#"*80)
    print("# COMFYUI WORKFLOW TEST - DUAL RUN WITH GROUP SWITCHING")
    print("#"*80)
    
    # Test values
    test_name = "test"
    image_prompts = "siena is standing in rain"
    video_prompts = "siena is showering in rain"
    
    # Run 1: Enable Images, Disable Videos (mode 0 typically means "enabled" or "default")
    print("\n[RUN 1] Enable Images Group (Disable Videos)")
    prompt_id_1 = run_workflow(
        name=test_name,
        image_prompts=image_prompts,
        video_prompts=video_prompts,
        mode_value=0  # Enable Images, disable rest
    )
    
    # Wait 5 seconds
    print("\n[WAIT] Waiting 5 seconds before second run...")
    for i in range(5, 0, -1):
        print(f"  {i}...", end=" ", flush=True)
        time.sleep(1)
    print("\n")
    
    # Run 2: Disable Images, Enable Videos (mode 1 typically means "disabled/alternate")
    print("\n[RUN 2] Enable Videos Group (Disable Images)")
    prompt_id_2 = run_workflow(
        name=test_name,
        image_prompts=image_prompts,
        video_prompts=video_prompts,
        mode_value=1  # Disable Images, enable Videos
    )
    
    # Summary
    print("\n" + "#"*80)
    print("# TEST SUMMARY")
    print("#"*80)
    print(f"Run 1 (Images Enabled): {'SUCCESS' if prompt_id_1 else 'FAILED'} - ID: {prompt_id_1}")
    print(f"Run 2 (Videos Enabled): {'SUCCESS' if prompt_id_2 else 'FAILED'} - ID: {prompt_id_2}")
    print(f"Delay: 5 seconds")
    print("#"*80)
    
    if prompt_id_1 and prompt_id_2:
        print("\n[OK] Both workflows submitted successfully!")
        return 0
    else:
        print("\n[ERROR] One or both workflows failed to submit")
        return 1

if __name__ == "__main__":
    sys.exit(main())
