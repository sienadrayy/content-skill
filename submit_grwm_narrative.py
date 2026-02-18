#!/usr/bin/env python3
"""
Submit GRWM Narrative Progression Reel to ComfyUI - Images + Videos (6 seconds each)
"""

import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# Image prompts - Scene consistent, narrative states explicit
image_prompts = """Siena at bathroom vanity mirror, fresh face with no makeup visible yet, wearing casual white undershirt, reaching toward makeup drawer with confidence, warm golden bathroom vanity lighting (2700K), bathroom mirror and counter visible in background, anticipation visible in expression, direct eye contact with camera, professional beauty photography
Siena at bathroom vanity mirror, makeup brush visible in motion applying eyeshadow to eyelids, eyeshadow and eyeliner appearing on eyes, eyes gradually gaining definition, same white undershirt, same warm golden bathroom vanity lighting (2700K), focused confident expression, close-up showing makeup application, same bathroom mirror background, professional beauty photography
Siena at bathroom vanity, full face makeup now complete and glowing (eyeshadow visible, eyeliner defined, lips colored), still wearing white undershirt, standing at bathroom mirror, same warm golden lighting (2700K) highlighting makeup glow, turning toward dress hanging nearby, hands lifting dress with anticipation, confident expression building, professional beauty photography
Siena holding dress in both hands at bathroom vanity area, full face makeup complete and visible (glowing finish), white undershirt still worn, dress visible being selected and lifted, same warm golden bathroom vanity lighting (2700K), anticipation and confidence building in expression, ready to begin dress phase, bathroom mirror visible in background, professional beauty photography
Siena with dress sliding over body, motion captured showing dress being worn, full makeup still visible and glowing on face, dress fitting on body showing silhouette beginning to appear, hands adjusting dress fit, same bathroom setting, warm golden lighting (2700K) maintained, breathing visible, confidence and transformation evident, professional body photography
Siena standing at bathroom mirror in complete dressed state, full face makeup glowing (complete eye makeup and lip color visible), complete dress fitted and visible on body, standing in power stance facing mirror, warm golden lighting (2700K) perfect on face and body, hand briefly adjusting final dress detail, confident ownership visible, breathing visible, professional glamorous photography
Siena facing bathroom mirror in final complete look moment, full makeup glowing and complete (eyes, lips, radiant finish), complete dress fitted perfectly on body (showing silhouette and curves), standing in power stance, warm golden bathroom vanity lighting (2700K) consistent throughout, confident powerful expression, direct eye contact in mirror, ready moment evident, professional glamorous photography
Siena turned directly to camera (away from mirror) in final power pose, complete look locked in and visible (full makeup + complete dress), direct camera eye contact intense and confident, bare shoulders visible from dress, warm golden lighting (2700K) perfect on face and outfit, breathing subtly visible, magnetic power energy radiating, confident ownership of complete transformation, freeze on ultimate ready moment, professional photography"""

video_prompts = """Fixed camera on siena at bathroom vanity, RAPID SEQUENCE [6 SECONDS]: reach toward drawer [0.5s motion], open drawer [0.5s motion], grab makeup brush [0.5s], bring brush to eye [0.5s motion], begin applying eyeshadow [remaining time showing transformation starting], warm golden vanity lighting (2700K) constant, anticipation visible growing into focus, hard cut
Fixed camera close-up on siena's eyes at vanity, AGGRESSIVE makeup application [6 SECONDS]: brush applying eyeshadow with visible fast strokes [2s motion], eyes visibly transforming with color appearing, blink and refocus [0.5s], continue defining eyes with eyeliner [2s motion], step back briefly checking look [0.5s], final confident eye contact toward camera, same warm golden vanity lighting (2700K), breathing visible, energy building, hard cut
Fixed camera on siena at bathroom vanity, MULTI-TRANSITION [6 SECONDS]: full makeup now visible and glowing, reach for dress [0.5s motion], grab both sides of dress [0.5s], pull dress up and over head [1.5s rapid motion], dress sliding down body [1s settling motion], quick hand adjustment of dress fit [0.5s], final check in mirror with growing confidence visible, same warm golden bathroom lighting (2700K), breathing evident, hard cut
Fixed camera full-body at bathroom mirror, RAPID BUILD [6 SECONDS]: siena adjusting dress top [0.5s], adjusting dress sides [0.5s], smoothing dress down [0.5s], hands dropping and looking down briefly at complete outfit [0.5s], head lifting up [0.5s], building confident expression as eyes come up, eyes meeting mirror [1s build], small confident head movement [0.5s], breathing visible showing ownership, same warm golden vanity lighting (2700K), hard cut
Fixed camera close-up on siena's face at mirror, POWER BUILD [6 SECONDS]: lips visible (full makeup glowing), slight lip bite showing confidence [0.5s], eyes intensifying with direct gaze into mirror [1s slow build], shoulders visible relaxing into power stance [0.5s], subtle head tilt showing command [0.5s], breathing visibly deeper as confidence peaks [1s], final intense micro-expression showing magnetic ownership [0.5s], freeze on peak confidence, warm golden lighting (2700K) perfect on face, hard cut
Fixed camera on siena turning from mirror TOWARD camera [6 SECONDS]: RAPID transition, siena pivoting from mirror toward camera [1s quick motion], complete outfit and makeup visible during turn, stepping into frame [0.5s motion], positioning into direct camera facing [0.5s], direct eye contact locked with camera [1s intense], breathing visible on chest area showing confidence, expression building from focused to magnetic, warm golden lighting (2700K) maintained throughout, shoulders back power stance evident [remaining time hold], hard cut to black
Fixed camera on siena's final direct camera POWER MOMENT [6 SECONDS]: INTENSE direct eye contact maintained throughout [5s locked], complete makeup glowing and visible on face, complete dress visible on body, slight breathing visible on upper chest showing subtle engagement, shoulders back in command, confident magnetic expression radiating ownership, warm golden lighting (2700K) perfect on face and body, micro-expressions showing final readiness, optional subtle lip movement or eye intensity change at final moment [1s], freeze frame or fade to black on power note"""

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
    print("** GRWM - NARRATIVE PROGRESSION REELS **")
    print("=" * 60)
    
    # Load workflows
    print("\n[*] Loading workflows...")
    images_wf = load_workflow(images_workflow_path)
    videos_wf = load_workflow(videos_workflow_path)
    print("   [OK] Images workflow loaded")
    print("   [OK] Videos workflow loaded")
    
    # Update image workflow
    print("\n[*] STEP 1: Updating Image Workflow")
    name = "grwm_narrative"
    
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
    print("\n[FEATURES]")
    print("   Scene Consistency: Same bathroom throughout")
    print("   Outfit Progression: Fresh face -> Full makeup -> Complete dress")
    print("   Narrative States: 8 explicit states showing clear progress")
    print("   Lighting: Consistent warm golden (2700K) throughout")
    print("\n[TIMING]")
    print("   Images: ~5 minutes")
    print("   Videos: ~15-20 minutes")
    print("   Total: ~25 minutes")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
