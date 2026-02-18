#!/usr/bin/env python3
"""
Submit Video Workflow Only to ComfyUI
"""

import sys
import json
import urllib.request
import urllib.error
import argparse

# Fix UTF-8 encoding on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

COMFYUI_SERVER = "http://192.168.29.60:8188"
WORKFLOW_VIDEO_PATH = r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Videos_workflow.json"

def load_workflow(workflow_path: str) -> dict:
    """Load workflow from file"""
    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception(f"Workflow file not found: {workflow_path}")
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON in workflow: {e}")

def submit_video_workflow(video_prompts: str, output_name: str, seconds: int = 6) -> str:
    """Submit Video workflow"""
    print(f"📤 Loading Video workflow...")
    workflow = load_workflow(WORKFLOW_VIDEO_PATH)
    
    # Set inputs
    workflow["436"]["inputs"]["value"] = video_prompts
    workflow["500"]["inputs"]["value"] = output_name
    workflow["394:396"]["inputs"]["Number"] = str(seconds)
    
    print(f"🎬 Setting video prompts, output name: {output_name}, seconds: {seconds}")
    
    # Check server
    print(f"🔌 Connecting to ComfyUI at {COMFYUI_SERVER}...")
    try:
        urllib.request.urlopen(f"{COMFYUI_SERVER}/system_stats", timeout=5)
        print(f"✅ ComfyUI server ready")
    except urllib.error.URLError:
        raise Exception(f"Cannot reach ComfyUI server at {COMFYUI_SERVER}")
    
    # Submit
    print(f"📤 Submitting Video workflow to ComfyUI...")
    payload = json.dumps({"prompt": workflow}).encode('utf-8')
    req = urllib.request.Request(
        f"{COMFYUI_SERVER}/prompt",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            prompt_id = result.get("prompt_id")
            
            if not prompt_id:
                raise Exception("No prompt_id returned from ComfyUI")
            
            print(f"✅ Video workflow submitted!")
            print(f"   Prompt ID: {prompt_id}")
            return prompt_id
            
    except urllib.error.URLError as e:
        raise Exception(f"Failed to submit to ComfyUI: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid response from ComfyUI: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Submit Video Workflow Only to ComfyUI")
    parser.add_argument("--name", required=True, help="Output name/prefix")
    parser.add_argument("--video-prompts", required=True, help="Video prompts (newline-separated)")
    parser.add_argument("--seconds", type=int, default=6, help="Seconds per video segment (default: 6)")
    
    args = parser.parse_args()
    
    try:
        print(f"\n{'='*60}")
        print(f"🎬 VIDEO WORKFLOW SUBMISSION")
        print(f"{'='*60}")
        print(f"Output Name: {args.name}")
        print(f"Seconds: {args.seconds}")
        
        # Submit Video
        print(f"\n{'='*60}")
        print(f"Submit Video Workflow")
        print(f"{'='*60}")
        video_prompt_id = submit_video_workflow(args.video_prompts, args.name, args.seconds)
        
        # Summary
        print(f"\n{'='*60}")
        print(f"🎉 VIDEO WORKFLOW SUBMITTED!")
        print(f"{'='*60}")
        print(f"Output Name: {args.name}")
        print(f"Video Prompt ID: {video_prompt_id}")
        print(f"Video Seconds: {args.seconds}")
        print(f"📊 Monitor: {COMFYUI_SERVER}")
        
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ Error")
        print(f"{'='*60}")
        print(f"Error: {e}")
        sys.exit(1)
