#!/usr/bin/env python3
"""
Submit Dual Workflow (Images + Videos) to ComfyUI

Loads UI-format workflows from network drive, converts to API format,
updates prompt nodes, and submits to ComfyUI.
"""

import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
import argparse

# Import the converter
from comfyui_export_api_v6 import ComfyUIExporter

# Network drive paths (shared workflows)
WORKFLOWS_DIR = Path(r"\\192.168.29.60\workflows")
COMFYUI_SERVER = "http://192.168.29.60:8188"


def load_and_convert_workflow(path):
    """Load UI-format workflow and convert to API format"""
    with open(path, 'r', encoding='utf-8') as f:
        wf = json.load(f)
    
    exporter = ComfyUIExporter(wf, COMFYUI_SERVER)
    api = exporter.export()
    
    # Filter out unsupported nodes (rgthree, etc.)
    to_remove = [k for k, v in api.items() if 'rgthree' in v.get('class_type', '').lower()]
    for k in to_remove:
        del api[k]
    
    return api


def submit_to_comfyui(workflow, server_url=COMFYUI_SERVER):
    """Submit API-format workflow to ComfyUI"""
    endpoint = f"{server_url}/prompt"
    
    try:
        payload = {"prompt": workflow}
        payload_json = json.dumps(payload).encode('utf-8')
        
        req = urllib.request.Request(
            endpoint,
            data=payload_json,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            prompt_id = data.get("prompt_id")
            errors = data.get("node_errors", {})
            
            if errors:
                print(f"   [WARN] Node errors: {list(errors.keys())}")
            
            if prompt_id:
                print(f"   [OK] Submitted. Prompt ID: {prompt_id}")
                return prompt_id
            else:
                print(f"   [ERROR] Response: {data}")
                return None
    
    except urllib.error.HTTPError as e:
        error_data = e.read().decode('utf-8')
        try:
            error_json = json.loads(error_data)
            print(f"   [HTTP {e.code}] {error_json.get('error', {}).get('message', e.reason)}")
        except:
            print(f"   [HTTP {e.code}] {error_data[:500]}")
        return None
    except urllib.error.URLError as e:
        print(f"   [ERROR] Cannot reach ComfyUI at {server_url}")
        return None
    except Exception as e:
        print(f"   [ERROR] {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='Submit dual workflow to ComfyUI')
    parser.add_argument('--name', required=True, help='Output name/prefix')
    parser.add_argument('--image-prompts', required=True, help='Image prompts (newline-separated)')
    parser.add_argument('--video-prompts', required=True, help='Video prompts (newline-separated)')
    parser.add_argument('--seconds', type=int, default=6, help='Seconds per video segment')
    
    args = parser.parse_args()
    
    print("** DUAL WORKFLOW SUBMISSION **")
    print("=" * 60)
    print(f"Name: {args.name}")
    print(f"Duration: {args.seconds}s per segment")
    print(f"Source: {WORKFLOWS_DIR}")
    print("=" * 60)
    
    # Load and convert workflows
    print("\n[*] Loading & converting workflows...")
    
    images_path = WORKFLOWS_DIR / "Images_workflow.json"
    videos_path = WORKFLOWS_DIR / "Videos_workflow.json"
    
    images_wf = load_and_convert_workflow(images_path)
    print(f"   [OK] Images workflow: {len(images_wf)} nodes")
    
    videos_wf = load_and_convert_workflow(videos_path)
    print(f"   [OK] Videos workflow: {len(videos_wf)} nodes")
    
    # Update image workflow
    print("\n[*] STEP 1: Updating Image Workflow")
    
    if "443" in images_wf:
        images_wf["443"]["inputs"]["value"] = args.image_prompts
        print(f"   [OK] Updated node 443 (image prompts): {len(args.image_prompts)} chars")
    else:
        print("   [!] Node 443 not found")
        return False
    
    if "500" in images_wf:
        images_wf["500"]["inputs"]["value"] = args.name
        print(f"   [OK] Updated node 500 (output name): {args.name}")
    else:
        print("   [!] Node 500 not found")
        return False
    
    # Submit images workflow
    print("\n[*] Submitting Images Workflow...")
    images_prompt_id = submit_to_comfyui(images_wf)
    if not images_prompt_id:
        print("[!] Failed to submit images workflow")
        return False
    
    # Wait 5 seconds
    print("\n[*] Waiting 5 seconds before submitting videos...")
    for i in range(5, 0, -1):
        print(f"   {i}...", end=" ", flush=True)
        time.sleep(1)
    print("[OK]")
    
    # Update video workflow
    print("\n[*] STEP 2: Updating Video Workflow")
    
    if "436" in videos_wf:
        videos_wf["436"]["inputs"]["value"] = args.video_prompts
        print(f"   [OK] Updated node 436 (video prompts): {len(args.video_prompts)} chars")
    else:
        print("   [!] Node 436 not found")
        return False
    
    if "500" in videos_wf:
        videos_wf["500"]["inputs"]["value"] = args.name
        print(f"   [OK] Updated node 500 (output name): {args.name}")
    else:
        print("   [!] Node 500 not found")
        return False
    
    # Try to find and set seconds parameter
    for node_id, node_data in videos_wf.items():
        if isinstance(node_data, dict) and "inputs" in node_data:
            if "seconds" in node_data["inputs"]:
                node_data["inputs"]["seconds"] = args.seconds
                print(f"   [OK] Updated node {node_id} (seconds): {args.seconds}")
                break
    
    # Submit videos workflow
    print("\n[*] Submitting Videos Workflow...")
    videos_prompt_id = submit_to_comfyui(videos_wf)
    if not videos_prompt_id:
        print("[!] Failed to submit videos workflow")
        return False
    
    # Success
    print("\n[*] SUBMISSION COMPLETE")
    print("=" * 60)
    print(f"Images Prompt ID: {images_prompt_id}")
    print(f"Videos Prompt ID: {videos_prompt_id}")
    print(f"Output: \\\\192.168.29.60\\output\\{args.name}\\")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
