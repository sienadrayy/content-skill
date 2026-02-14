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

# Fix Unicode encoding on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

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

def upload_video_to_comfyui(video_path: str) -> str:
    """
    Upload video to ComfyUI server
    
    Args:
        video_path: Path to video file
        
    Returns:
        Filename from ComfyUI (as returned by /upload endpoint)
    """
    if not os.path.exists(video_path):
        raise Exception(f"Video file not found: {video_path}")
    
    print(f"📤 Uploading video to ComfyUI...")
    print(f"   File: {video_path}")
    
    # Read video file
    with open(video_path, 'rb') as f:
        video_data = f.read()
    
    # Prepare multipart upload
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="image"; filename="{os.path.basename(video_path)}"\r\n'
        f'Content-Type: video/mp4\r\n\r\n'
    ).encode() + video_data + f'\r\n--{boundary}--\r\n'.encode()
    
    req = urllib.request.Request(
        f"{COMFYUI_SERVER}/upload/image",
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if "name" not in result:
                raise Exception(f"No filename in upload response: {result}")
            
            filename = result["name"]
            print(f"✅ Upload complete!")
            print(f"   Filename: {filename}")
            return filename
            
    except urllib.error.URLError as e:
        raise Exception(f"Failed to upload to ComfyUI: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid response from ComfyUI: {e}")

def submit_workflow(video_filename: str) -> str:
    """
    Submit workflow to ComfyUI with uploaded video filename
    
    Args:
        video_filename: Filename returned from ComfyUI upload
        
    Returns:
        Prompt ID from ComfyUI
    """
    print(f"📤 Loading Wan Animate workflow...")
    workflow = load_workflow()
    
    # Modify Node 218 (VHS_LoadVideo) with uploaded video filename
    # Node 218 input: "video" field (now expects filename, not path)
    if "218" not in workflow:
        raise Exception("Node 218 not found in workflow")
    
    workflow["218"]["inputs"]["video"] = video_filename
    
    print(f"🎬 Setting video filename: {video_filename}")
    
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
    parser.add_argument("--video", required=True, help="Path to video file (will be uploaded)")
    parser.add_argument("--wait", action="store_true", help="Wait for completion")
    parser.add_argument("--timeout", type=int, default=3600, help="Timeout in seconds")
    
    args = parser.parse_args()
    
    try:
        # Step 1: Upload video
        print(f"\n{'='*60}")
        print(f"STEP 1: Upload Video to ComfyUI")
        print(f"{'='*60}")
        video_filename = upload_video_to_comfyui(args.video)
        
        # Step 2: Submit workflow with uploaded filename
        print(f"\n{'='*60}")
        print(f"STEP 2: Submit Workflow")
        print(f"{'='*60}")
        prompt_id = submit_workflow(video_filename)
        
        if args.wait:
            print(f"\n{'='*60}")
            print(f"STEP 3: Wait for Completion")
            print(f"{'='*60}")
            result = wait_for_completion(prompt_id, args.timeout)
            print(f"\n🎉 Output ready in ComfyUI!")
        else:
            print(f"\n💡 Tip: Use --wait to wait for completion")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
