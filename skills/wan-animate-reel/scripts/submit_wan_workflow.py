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
import uuid
from pathlib import Path

# Fix Unicode encoding on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

COMFYUI_SERVER = "http://192.168.29.60:8188"
WORKFLOWS_DIR = r"\\192.168.29.60\workflows"
WORKFLOW_IMAGE_PATH = f"{WORKFLOWS_DIR}\\Wan Animate character replacement V3 - Image API.json"
WORKFLOW_VIDEO_PATH = f"{WORKFLOWS_DIR}\\Wan Animate character replacement V3 - Video API.json"

def load_workflow(workflow_path: str) -> dict:
    """Load workflow from file"""
    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception(f"Workflow file not found: {workflow_path}")
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON in workflow: {e}")

def generate_random_name() -> str:
    """Generate a random UUID for this run"""
    return str(uuid.uuid4())

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

def submit_workflow(video_filename: str, name: str, workflow_type: str) -> str:
    """
    Submit workflow to ComfyUI with uploaded video filename and UUID
    
    Args:
        video_filename: Filename returned from ComfyUI upload
        name: UUID for this run (sets Node 254 "Conept Name")
        workflow_type: "image" or "video"
        
    Node 254 "Conept Name" values:
        - Image workflow: Node 254 = {name} (plain UUID)
        - Video workflow: Node 254 = {name}_00001_ (UUID with suffix)
        
    Returns:
        Prompt ID from ComfyUI
    """
    workflow_path = WORKFLOW_IMAGE_PATH if workflow_type == "image" else WORKFLOW_VIDEO_PATH
    
    print(f"📤 Loading Wan Animate {workflow_type.upper()} workflow...")
    workflow = load_workflow(workflow_path)
    
    # Find and modify nodes with "video" input and concept name
    video_set = False
    concept_name_set = False
    
    for node_id, node_data in workflow.items():
        if isinstance(node_data, dict) and "inputs" in node_data:
            inputs = node_data["inputs"]
            
            # Set video if this node has a video input
            if "video" in inputs:
                inputs["video"] = video_filename
                video_set = True
                print(f"🎬 Setting video in node {node_id}: {video_filename}")
            
            # Set concept name (PrimitiveString with "value" field)
            if node_data.get("class_type") == "PrimitiveString" and node_data.get("_meta", {}).get("title") == "Conept Name":
                # For video workflow, append _00001_ suffix
                concept_value = f"{name}_00001_" if workflow_type == "video" else name
                inputs["value"] = concept_value
                concept_name_set = True
                print(f"📝 Setting concept name in node {node_id}: {concept_value}")
    
    if not video_set:
        print(f"⚠️  Warning: No 'video' input found in {workflow_type} workflow")
    if not concept_name_set:
        print(f"⚠️  Warning: No 'Conept Name' node found in {workflow_type} workflow")
    
    # Check ComfyUI server availability
    print(f"🔌 Connecting to ComfyUI at {COMFYUI_SERVER}...")
    try:
        urllib.request.urlopen(f"{COMFYUI_SERVER}/system_stats", timeout=5)
        print(f"✅ ComfyUI server ready")
    except urllib.error.URLError:
        raise Exception(f"Cannot reach ComfyUI server at {COMFYUI_SERVER}")
    
    # Submit workflow
    print(f"📤 Submitting {workflow_type.upper()} workflow to ComfyUI...")
    
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
            
            print(f"✅ {workflow_type.upper()} workflow submitted!")
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
    parser = argparse.ArgumentParser(description="Submit Wan Animate dual workflows (Image + Video)")
    parser.add_argument("--video", required=True, help="Path to video file (will be uploaded)")
    parser.add_argument("--name", help="Name/prefix for output (optional, defaults to UUID)")
    parser.add_argument("--wait", action="store_true", help="Wait for completion")
    parser.add_argument("--timeout", type=int, default=3600, help="Timeout in seconds")
    
    args = parser.parse_args()
    
    try:
        # Use provided name or generate random UUID
        name = args.name if args.name else generate_random_name()
        print(f"\n📝 Using run ID: {name}")
        
        # Step 1: Upload video
        print(f"\n{'='*60}")
        print(f"STEP 1: Upload Video to ComfyUI")
        print(f"{'='*60}")
        video_filename = upload_video_to_comfyui(args.video)
        
        # Step 2: Submit Image API workflow
        print(f"\n{'='*60}")
        print(f"STEP 2: Submit Image API Workflow")
        print(f"{'='*60}")
        image_prompt_id = submit_workflow(video_filename, name, "image")
        
        # Step 3: Wait 5 seconds
        print(f"\n⏳ Waiting 5 seconds before submitting Video API...")
        time.sleep(5)
        
        # Step 4: Submit Video API workflow
        print(f"\n{'='*60}")
        print(f"STEP 3: Submit Video API Workflow")
        print(f"{'='*60}")
        video_prompt_id = submit_workflow(video_filename, name, "video")
        
        # Step 5: Summary
        print(f"\n{'='*60}")
        print(f"WORKFLOWS SUBMITTED")
        print(f"{'='*60}")
        print(f"Run ID: {name}")
        print(f"Image Prompt ID: {image_prompt_id}")
        print(f"Video Prompt ID: {video_prompt_id}")
        print(f"📊 Monitor: {COMFYUI_SERVER}")
        
        if args.wait:
            print(f"\n{'='*60}")
            print(f"STEP 5: Wait for Completion")
            print(f"{'='*60}")
            print(f"⏳ Waiting for both Image and Video workflows to complete...")
            
            # Wait for both
            image_result = wait_for_completion(image_prompt_id, args.timeout)
            video_result = wait_for_completion(video_prompt_id, args.timeout)
            
            print(f"\n🎉 Both workflows complete!")
            print(f"✅ Image output ready")
            print(f"✅ Video output ready")
        else:
            print(f"\n💡 Both workflows running in parallel on ComfyUI")
            print(f"💡 Output prefix: {name}_")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
