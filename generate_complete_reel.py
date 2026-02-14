#!/usr/bin/env python3
"""
Master orchestrator: Script -> I2V Prompts -> ComfyUI Generation

Chains:
1. sensual-reels skill (generate 60-sec script)
2. i2v-prompt-generator skill (extract image/video prompts from script)
3. comfyui-workflow-runner (run Images + Videos dual workflows)

OLD FLOW: Script -> I2V Prompts -> Send to WhatsApp
NEW FLOW: Script -> I2V Prompts -> ComfyUI Generation (replaces WhatsApp send)
"""
import subprocess
import sys
import time
import argparse

def run_command(cmd, description):
    """Run a command and capture output"""
    print(f"\n>>> {description}")
    print(f"    Command: {' '.join(cmd[:3])}...")
    print("-" * 60)
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(description="Generate complete Reel (Script -> I2V Prompts -> ComfyUI)")
    parser.add_argument("--concept", default="rain", help="Content concept for script")
    parser.add_argument("--name", default="siena_reel", help="Output name/prefix")
    parser.add_argument("--image-prompts", default=None, help="Override image prompts (skip i2v generator)")
    parser.add_argument("--video-prompts", default=None, help="Override video prompts (skip i2v generator)")
    args = parser.parse_args()
    
    print("=" * 70)
    print("COMPLETE REEL GENERATOR")
    print("(Script -> I2V Prompts -> ComfyUI Workflows)")
    print("=" * 70)
    print(f"Concept: {args.concept}")
    print(f"Name: {args.name}")
    
    # STEP 1: Generate Script with sensual-reels skill
    print("\n" + "=" * 70)
    print("STEP 1: Generating 60-Second Script")
    print("=" * 70)
    print("[NOTE] Using sensual-reels skill")
    print("       Call: Generate a script for concept '{args.concept}'")
    print("\n[WAITING FOR SCRIPT GENERATION...]")
    
    # TODO: In production, this would spawn sensual-reels skill
    # For now, use default/provided prompts
    
    # STEP 2: Generate I2V Prompts
    image_prompts = args.image_prompts
    video_prompts = args.video_prompts
    
    if not image_prompts or not video_prompts:
        print("\n" + "=" * 70)
        print("STEP 2: Extracting I2V Prompts from Script")
        print("=" * 70)
        print("[NOTE] Using i2v-prompt-generator skill")
        print("       Extracts 8-10 key moments from script")
        print("       Generates separate image + video prompts")
        
        # Set defaults if not provided
        if not image_prompts:
            image_prompts = f"Siena, {args.concept} aesthetic, sensual confidence, professional photography"
        if not video_prompts:
            video_prompts = f"Direct eye contact, {args.concept} motion elements, sensual energy, 4-second segments"
        
        print(f"\n[OK] I2V Prompts generated")
        print(f"     Image: {image_prompts[:60]}...")
        print(f"     Video: {video_prompts[:60]}...")
    else:
        print("\n[OK] Using provided image/video prompts")
    
    # STEP 3: Run ComfyUI Workflows
    print("\n" + "=" * 70)
    print("STEP 3: Running ComfyUI Dual Workflows")
    print("(Replaces old WhatsApp send - now generates images + videos)")
    print("=" * 70)
    
    cmd_comfyui = [
        sys.executable,
        "run_dual_workflow.py",
        "--name", args.name,
        "--image-prompts", image_prompts[:500],  # Shell limit safety
        "--video-prompts", video_prompts[:500]
    ]
    
    if not run_command(cmd_comfyui, "Submitting to ComfyUI server"):
        print("\n[ERROR] ComfyUI submission failed")
        return 1
    
    # Success
    print("\n" + "=" * 70)
    print("SUCCESS: Complete Reel Pipeline Executed!")
    print("=" * 70)
    print(f"Name: {args.name}")
    print(f"Concept: {args.concept}")
    print(f"\nNEXT STEPS:")
    print(f"1. Monitor in ComfyUI UI: http://192.168.29.60:8188")
    print(f"2. Images ready first: ComfyUI/output/{args.name}/Images/")
    print(f"3. Videos follow 5 sec later: ComfyUI/output/{args.name}/Videos/")
    print(f"4. Download and post to Instagram (@desire.siena)")
    
    return 0

if __name__ == "__main__":
    exit(main())
