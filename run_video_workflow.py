#!/usr/bin/env python3
"""
Run the Videos_workflow with modified prompts and name
"""
import json
import urllib.request
import urllib.parse
import time
import sys
import argparse

# ComfyUI server
SERVER_URL = "http://192.168.29.60:8188"

def load_workflow():
    """Load the workflow from file"""
    with open("openclaw/Videos_workflow.json", "r", encoding="utf-8") as f:
        return json.load(f)

def modify_workflow(workflow, name, video_prompts):
    """Modify the workflow with new values"""
    # Modify node 500 (Name)
    workflow["500"]["inputs"]["value"] = name
    print(f"[OK] Modified Node 500 (Name): {name}")
    
    # Modify node 436 (Video Prompts)
    workflow["436"]["inputs"]["value"] = video_prompts
    print(f"[OK] Modified Node 436 (Video Prompts): {video_prompts}")
    
    return workflow

def submit_workflow(workflow):
    """Submit workflow to ComfyUI"""
    payload = {"prompt": workflow}
    
    # Convert to JSON
    json_data = json.dumps(payload).encode('utf-8')
    
    # Create request
    url = f"{SERVER_URL}/prompt"
    req = urllib.request.Request(url, data=json_data)
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            prompt_id = result.get("prompt_id")
            print(f"[OK] Workflow submitted successfully!")
            print(f"     Prompt ID: {prompt_id}")
            return prompt_id
    except Exception as e:
        print(f"[ERROR] Failed to submit workflow: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Run ComfyUI video generation workflow")
    parser.add_argument("--name", default="test", help="Output name/prefix (default: test)")
    parser.add_argument("--prompts", default="Direct eye contact, slow blink, confident sensual expression held for 4 seconds", help="Video generation prompts")
    args = parser.parse_args()
    
    print("=" * 60)
    print("ComfyUI Video Workflow Runner")
    print("=" * 60)
    
    # Load workflow
    print("\n[1] Loading workflow...")
    workflow = load_workflow()
    print(f"[OK] Loaded workflow with {len(workflow)} nodes")
    
    # Modify workflow
    print("\n[2] Modifying workflow...")
    workflow = modify_workflow(workflow, args.name, args.prompts)
    
    # Submit to ComfyUI
    print("\n[3] Submitting to ComfyUI...")
    print(f"    Server: {SERVER_URL}")
    prompt_id = submit_workflow(workflow)
    
    if prompt_id:
        print("\n[OK] Workflow execution started!")
        print(f"     Monitor progress in ComfyUI UI")
        print(f"     Prompt ID: {prompt_id}")
        return 0
    else:
        print("\n[ERROR] Failed to submit workflow")
        return 1

if __name__ == "__main__":
    exit(main())
