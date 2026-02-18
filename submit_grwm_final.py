#!/usr/bin/env python3
"""
Submit GRWM Reel to ComfyUI - Images + Videos (6 seconds each)
"""

import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# Image and video prompts
image_prompts = """Extreme close-up of siena's face, topless or minimal bikini top, direct INTENSE eye contact locked with camera, confident lip bite visible at 1-second moment, bare shoulders and collarbone fully exposed, warm golden bathroom vanity lighting (2700K), subtle breathing visible, peak confidence energy, professional intimate beauty photography, 9/10 intensity
Siena in bathroom, bikini top strap pulled down partially, expose more upper chest and ribs visible, body at 20-degree angle showing side profile curves, hand trailing from collarbone downward sensually, confident eye contact maintained, warm golden lighting catching exposed skin and curves, professional body photography, 8.5/10 intensity
Siena adjusting bikini bottom to show more hip and upper thigh exposure, standing power pose with confidence, minimal coverage bikini fully visible, direct camera engagement intensifying, hand positioned on hip showing ownership, lighting hits body definition and curves, breathing visible on chest, professional glamorous photography, 8.5/10 intensity
Siena at 45-degree angle showing full side profile, back slightly arched emphasizing back curves and shoulder blades, minimal bikini coverage, hand on own hip, confident posture, warm golden lighting catching entire body silhouette and curves, direct eye contact from profile angle, professional photography, 9/10 intensity
Siena mid-body-roll rotation visible, minimal bikini coverage throughout, hand tracing from collarbone sensually down toward hip, direct intense eye contact, confident expression at peak, breathing subtly visible on exposed chest, golden lighting emphasizing curves through body position, professional photography, 9/10 intensity
Siena facing camera in power pose, minimal bikini/lingerie fully visible on body, hand positioned on own collarbone/hip area confident and unapologetic, INTENSE direct eye contact locked with camera, knowing confident smile, warm golden lighting on face and exposed skin, magnetic dominating energy, professional glamorous photography, 9/10 intensity
Siena with hand pulling hair back to expose neck and collarbone fully, minimal bikini visible on body, bare neck and shoulders emphasized, eye contact intense and deepening, subtle breathing visible, expression showing peak confidence and sexuality, warm golden bathroom lighting throughout, professional beauty photography, 9/10 intensity
Siena in strongest confident power stance, direct camera INTENSE eye contact, minimal coverage bikini frozen in place on body, breathing subtly visible on chest, expression peak confident and magnetic, bare shoulders and upper body fully exposed, warm golden lighting perfect on face and skin, ultimate sensual power moment, professional photography, 9/10 intensity"""

video_prompts = """Extreme close-up camera on siena's face, INTENSE direct eye contact locked with camera throughout, lip bite visible at 1-second mark, hold intense stare for remaining 3 seconds, confident expression, warm golden bathroom lighting (2700K) on face, breathing subtly visible, magnetic commanding energy, hard cut to next
Quick camera adjustment from face to shoulders, bikini strap pull motion visible, fast 2-second motion revealing more upper chest, warm golden lighting maintained, eye contact follows as body adjusts, breathing becomes visible on exposed chest, hard cut to next
Fixed camera, fast bikini bottom adjustment over 2 seconds showing hip/thigh exposure, confident energy building, direct camera engagement, hand movement purposeful and sensual, minimal coverage visible, lighting hits new exposed areas, eye contact maintained, hard cut to next
Fixed camera, smooth body rotation to 45-degree side profile over 3.5 seconds, back arch maintained emphasizing curves, warm golden lighting catches silhouette and body definition throughout motion, eye contact where visible from profile, confident expression, hard cut to next
Fixed camera, slow confident body roll from side to front over 3.5 seconds, hand traces collarbone to hip with sensual intentional motion, direct intense eye contact when facing camera, minimal bikini throughout motion, breathing visible, golden light catches curves emphasized by rotation, hard cut to next
Freeze on siena's face and upper body, INTENSE direct eye contact for full 4 seconds, confident power pose, hand near collarbone area, knowing confident smile building, minimal coverage visible, breathing visible on exposed chest, warm golden lighting perfect, magnetic dominating presence, hard cut to next
Quick hand movement pulling hair back over 2 seconds, expose neck and collarbone fully, direct eye contact INTENSE throughout motion and hold, expression deepening in confidence, breathing visible on chest, bare shoulders emphasized, warm golden lighting highlights exposed areas, hard cut to next
Freeze on strongest power pose facing camera, INTENSE direct eye contact held for 4 seconds, confident commanding expression, minimal bikini visible on body, breathing subtly visible on chest, expression shows peak sexuality and confidence, warm golden lighting perfect on face and exposed skin, magnetic presence, hard cut to black or fade"""

# Configuration
VIDEO_DURATION_SECONDS = 6  # Seconds per video segment

# Paths
images_workflow_path = Path(r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Images_workflow.json")
videos_workflow_path = Path(r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Videos_workflow.json")

def load_workflow(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def submit_to_comfyui(workflow, server_url="http://192.168.29.60:8188"):
    """Submit workflow directly to ComfyUI API"""
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
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            prompt_id = data.get("prompt_id")
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
            print(f"   [HTTP {e.code}] {error_data}")
        return None
    except urllib.error.URLError as e:
        print(f"   [ERROR] Cannot reach ComfyUI at {server_url}")
        return None
    except Exception as e:
        print(f"   [ERROR] {e}")
        return None

def main():
    print("** GRWM - SENSUAL HEAT REELS **")
    print("=" * 60)
    
    # Load workflows
    print("\n[*] Loading workflows...")
    images_wf = load_workflow(images_workflow_path)
    videos_wf = load_workflow(videos_workflow_path)
    print("   [OK] Images workflow loaded")
    print("   [OK] Videos workflow loaded")
    
    # Update image workflow
    print("\n[*] STEP 1: Updating Image Workflow")
    name = "grwm_sensual"
    
    if "443" in images_wf:
        images_wf["443"]["inputs"]["value"] = image_prompts
        print(f"   [OK] Updated node 443 (image prompts): {len(image_prompts)} chars")
    else:
        print("   [!] Node 443 not found")
        return False
    
    if "500" in images_wf:
        images_wf["500"]["inputs"]["value"] = name
        print(f"   [OK] Updated node 500 (output name): {name}")
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
        videos_wf["436"]["inputs"]["value"] = video_prompts
        print(f"   [OK] Updated node 436 (video prompts): {len(video_prompts)} chars")
    else:
        print("   [!] Node 436 not found")
        return False
    
    if "500" in videos_wf:
        videos_wf["500"]["inputs"]["value"] = name
        print(f"   [OK] Updated node 500 (output name): {name}")
    else:
        print("   [!] Node 500 not found")
        return False
    
    if "394:396" in videos_wf:
        videos_wf["394:396"]["inputs"]["Number"] = str(VIDEO_DURATION_SECONDS)
        print(f"   [OK] Updated node 394:396 (seconds): {VIDEO_DURATION_SECONDS}")
    else:
        print("   [!] Node 394:396 not found")
        return False
    
    # Submit videos workflow
    print("\n[*] Submitting Videos Workflow...")
    videos_prompt_id = submit_to_comfyui(videos_wf)
    if not videos_prompt_id:
        print("[!] Failed to submit videos workflow")
        return False
    
    # Summary
    print("\n" + "=" * 60)
    print("[SUCCESS] BOTH WORKFLOWS SUBMITTED!")
    print("\n[IDS]")
    print(f"   Images: {images_prompt_id}")
    print(f"   Videos: {videos_prompt_id}")
    print("\n[STATUS]")
    print(f"   Output: ComfyUI/output/{name}/")
    print(f"   Images: {name}/Images/")
    print(f"   Videos: {name}/Videos/ (6 seconds each)")
    print("\n[TIMING]")
    print("   Images: ~5 minutes")
    print("   Videos: ~15-20 minutes")
    print("   Total: ~25 minutes")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
