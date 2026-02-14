#!/usr/bin/env python3
"""
Submit Wan Animate workflow to ComfyUI with video path
"""

import os
import sys
import json
import urllib.request
import urllib.error
import time
import argparse
from pathlib import Path

COMFYUI_SERVER = "http://192.168.29.60:8188"
WORKFLOW_PATH = r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Wan Animate character replacement V3 API.json"

def load_workflow() -> dict:
    """Load workflow from file"""
    try:
        with open(WORKFLOW_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception(f"Workflow file not found: {WORKFLOW_PATH}")
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON in workflow: {e}")

def submit_workflow(video_path: str) -> str:
    """
    Submit workflow to ComfyUI with video path
    
    Args:
        video_path: Path to video file
        
    Returns:
        Prompt ID from ComfyUI
    """
    # Verify video exists
    if not os.path.exists(video_path):
        raise Exception(f"Video file not found: {video_path}")
    
    # Convert to absolute path
    abs_video_path = os.path.abspath(video_path)
    
    print(f"📤 Loading Wan Animate workflow...")
    workflow = load_workflow()
    
    # Modify Node 194 (VHS_LoadVideoPath) with video path
    # Node 194 input: "video" field
    if "194" not in workflow:
        raise Exception("Node 194 not found in workflow")
    
    workflow["194"]["inputs"]["video"] = abs_video_path
    
    print(f"🎬 Setting video path: {abs_video_path}")
    
    # Check ComfyUI server availability
    print(f"🔌 Connecting to ComfyUI at {COMFYUI_SERVER}...")
    try:
        urllib.request.urlopen(f"{COMFYUI_SERVER}/system_stats", timeout=5)
        print(f"✅ ComfyUI server ready")
    except urllib.error.URLError:
        raise Exception(f"Cannot reach ComfyUI server at {COMFYUI_SERVER}")
    
    # Submit workflow
    print(f"📤 Submitting workflow to ComfyUI...")
    
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
            
            print(f"✅ Workflow submitted!")
            print(f"   Prompt ID: {prompt_id}")
            return prompt_id
            
    except urllib.error.URLError as e:
        raise Exception(f"Failed to submit to ComfyUI: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid response from ComfyUI: {e}")

def wait_for_completion(prompt_id: str, timeout: int = 3600) -> dict:
    """
    Wait for workflow to complete
    
    Args:
        prompt_id: Prompt ID from submission
        timeout: Maximum seconds to wait
        
    Returns:
        Completion status
    """
    print(f"\n⏳ Waiting for workflow completion (timeout: {timeout}s)...")
    print(f"📊 Monitor progress at: {COMFYUI_SERVER}")
    
    start_time = time.time()
    last_status = {}
    
    while time.time() - start_time < timeout:
        try:
            with urllib.request.urlopen(f"{COMFYUI_SERVER}/history/{prompt_id}") as response:
                history = json.loads(response.read().decode('utf-8'))
                
                if prompt_id in history and history[prompt_id].get("outputs"):
                    print(f"\n✅ Workflow completed!")
                    return history[prompt_id]
                
                # Show progress
                with urllib.request.urlopen(f"{COMFYUI_SERVER}/system_stats") as stats_response:
                    stats = json.loads(stats_response.read().decode('utf-8'))
                    if stats != last_status:
                        last_status = stats
                        print(f"   Running... (system: {stats.get('system', {}).get('cpu_percent', 0):.1f}% CPU)")
                
        except urllib.error.URLError:
            pass  # Server temporarily unavailable, keep waiting
        except json.JSONDecodeError:
            pass  # Invalid response, keep waiting
        
        time.sleep(2)  # Check every 2 seconds
    
    raise Exception(f"Workflow timeout after {timeout}s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Submit Wan Animate workflow")
    parser.add_argument("--video", required=True, help="Path to video file")
    parser.add_argument("--wait", action="store_true", help="Wait for completion")
    parser.add_argument("--timeout", type=int, default=3600, help="Timeout in seconds")
    
    args = parser.parse_args()
    
    try:
        prompt_id = submit_workflow(args.video)
        
        if args.wait:
            result = wait_for_completion(prompt_id, args.timeout)
            print(f"\n🎉 Output ready in ComfyUI!")
        else:
            print(f"\n💡 Tip: Use --wait to wait for completion")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
