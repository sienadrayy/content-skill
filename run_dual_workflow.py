#!/usr/bin/env python3
"""
Run Images and Videos workflows sequentially with 5-second gap
"""
import subprocess
import sys
import time
import argparse

def run_command(cmd, description):
    """Run a command and return result"""
    print(f"\n>>> {description}")
    print(f"    Command: {' '.join(cmd)}")
    print("-" * 60)
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(description="Run both Images and Videos workflows")
    parser.add_argument("--name", default="test", help="Output name/prefix (default: test)")
    parser.add_argument("--image-prompts", default="Siena is standing in rain", help="Image generation prompts")
    parser.add_argument("--video-prompts", default="Direct eye contact, slow blink, confident sensual expression held for 4 seconds", help="Video generation prompts")
    args = parser.parse_args()
    
    print("=" * 60)
    print("ComfyUI Dual Workflow Runner")
    print("=" * 60)
    print(f"Name: {args.name}")
    print(f"Image Prompts: {args.image_prompts}")
    print(f"Video Prompts: {args.video_prompts}")
    
    # Run Images workflow
    print("\n" + "=" * 60)
    print("STEP 1: Running Images Workflow")
    print("=" * 60)
    
    cmd_images = [
        sys.executable,
        "run_image_workflow.py",
        "--name", args.name,
        "--prompts", args.image_prompts
    ]
    
    if not run_command(cmd_images, "Submitting Images Workflow"):
        print("\n[ERROR] Images workflow failed!")
        return 1
    
    # Wait 5 seconds
    print("\n" + "=" * 60)
    print("WAITING 5 SECONDS BEFORE VIDEO WORKFLOW")
    print("=" * 60)
    for i in range(5, 0, -1):
        print(f"  {i}...", end="", flush=True)
        time.sleep(1)
    print(" [OK]")
    
    # Run Videos workflow
    print("\n" + "=" * 60)
    print("STEP 2: Running Videos Workflow")
    print("=" * 60)
    
    cmd_videos = [
        sys.executable,
        "run_video_workflow.py",
        "--name", args.name,
        "--prompts", args.video_prompts
    ]
    
    if not run_command(cmd_videos, "Submitting Videos Workflow"):
        print("\n[ERROR] Videos workflow failed!")
        return 1
    
    # Success
    print("\n" + "=" * 60)
    print("SUCCESS: Both workflows submitted!")
    print("=" * 60)
    print("Monitor both executions in ComfyUI UI")
    print("Images output: ComfyUI/output/{name}/Images/")
    print("Videos output: ComfyUI/output/{name}/Videos/")
    
    return 0

if __name__ == "__main__":
    exit(main())
