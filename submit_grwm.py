#!/usr/bin/env python3
"""
Submit GRWM Reel to ComfyUI - Images + Videos
"""

import json
import sys
import time
import subprocess
from pathlib import Path

# Image and video prompts
image_prompts = """Close-up portrait of siena in bathroom mirror, topless or minimal bikini top, direct intense eye contact with camera, lip bite confidence, bare shoulders and collarbone fully exposed, warm golden bathroom vanity lighting (2700K), soft light catching skin, subtle knowing expression building, bare-shouldered power pose, bathroom mirror reflection visible behind, professional sensual beauty photography, 9/10 intensity
Siena in bathroom mirror medium shot, minimal bikini or lingerie top showing bare shoulders, collarbone, and defined upper body, hand slowly trailing down from collarbone toward hip, body turned slight 20-degree angle, warm golden bathroom lighting (2700K), direct eye contact with camera, confident sensual expression, bare skin emphasizing curves, professional body photography, 8.5/10 intensity
Siena in bathroom mirror, full-body side profile at 90-degree angle, minimal bikini top and bottoms, back slightly arched showing defined back and shoulder blades, hair flowing down back, warm golden bathroom lighting (2700K) catching curves and skin definition, confident powerful stance, visible collarbone and back curves emphasized by lighting, professional glamorous photography, 9/10 intensity, cinematic sensuality
Siena in bathroom mirror rotating toward camera, 45-degree body angle captured mid-turn, minimal coverage bikini visible, direct eye contact beginning to focus on camera, both shoulders visible, upper body skin emphasis, warm golden lighting (2700K) catching shoulders and curves, confident expression intensifying, professional body photography, sensual motion captured, 8.5/10 intensity
Extreme close-up of sienas face and upper chest, direct intense eye contact with camera, minimal bikini top visible at frame edge showing bare shoulders and upper collarbone, warm golden bathroom lighting (2700K), confident knowing smile building, expression showing peak allure, water-like skin appearance suggesting shower setting, professional intimate beauty photography, breathing visible, 9/10 intensity
Siena medium shot, body positioned mid-roll rotation visible, minimal bikini coverage, hand placed sensually on own collarbone/upper chest area, direct intense eye contact with camera, confident sensual expression, bare shoulders and upper body fully visible, warm golden lighting (2700K) catching skin and curves, professional body photography, peak sensuality moment, 9/10 intensity, cinematic
Siena extreme close-up face focused, hand running through hair and pulling back to expose neck and collarbone more, direct locked eye contact with camera, sensual confident expression, breathing visible with subtle chest movement, bare shoulders and neck fully exposed, warm golden bathroom lighting (2700K), intimate vulnerable-yet-powerful expression, professional beauty photography, 9/10 intensity
Siena full body shot, stepping or rotating position showing minimal bikini coverage, hands briefly placed on own body (collarbone/hip area), direct confident stare at camera, bare shoulders, back, sides fully visible, warm golden lighting (2700K) throughout, powerful confident stance, peak intensity moment, professional glamorous photography, 9/10 intensity, unapologetic sensuality"""

video_prompts = """Close-up fixed camera on sienas face in mirror, warm golden bathroom lighting (2700K), direct eye contact locked with camera throughout, subtle lip bite moment mid-sequence, slight head tilt 10 degrees, confident expression builds from neutral to alluring, minimal micro-movements of eyes deepening intensity, water-like moisture visible on skin suggesting shower context, fade to next moment
Siena visible in bathroom mirror from shoulders up, hand entering frame from collarbone slowly trailing downward over 4 seconds with sensual deliberate motion, warm golden vanity lighting (2700K) maintained throughout, head maintains slight angle toward camera, eyes track downward with hand movement then return to camera eye contact, breathing subtly visible on chest, soft steady motion, fade to next segment
Siena in mirror slow rotation from 90-degree side profile to 45-degree angle over 4 seconds, warm golden bathroom lighting (2700K) throughout, back arch maintained emphasizing curves, hair movement visible with slow turn, body curves catch and reflect light, camera fixed on mirror showing full body rotation, confident expression maintained in profile, smooth continuous motion, transition fade
Siena in mirror completing 90-degree rotation from side profile toward front-facing over 4 seconds, minimal coverage clothing visible throughout, warm golden bathroom lighting (2700K) maintained, shoulders rotate smoothly with body, eye contact shifts from profile gaze to direct camera lock, confident expression builds with rotation, lighting catches new angles of body, smooth controlled continuous motion
Close-up camera on sienas face transitioning to include upper chest, warm golden bathroom lighting (2700K) focused on face and shoulders, direct eye contact locked and intensifying over 4 seconds, subtle head movement slight 5-degree tilt, confident expression deepens with micro-movements of eyes and lips, minimal breathing visible on chest, soft water droplet effects visible, fade to wider shot
Siena medium shot camera, slow deliberate body roll over 4 seconds from side to front position, minimal coverage bikini throughout motion, hand movement tracing sensually from collarbone downward along upper body with slow intentional motion, warm golden lighting (2700K) follows body through roll, direct eye contact maintained during rotation, confident expression throughout, light catches curves emphasized by body roll motion, continuous smooth fade
Extreme close-up on sienas face and neck, hand entering frame from side slowly running through hair and pulling back over 3 seconds with sensual motion, warm golden bathroom lighting (2700K) highlights exposed neck and collarbone as hand moves, direct eye contact locked with camera throughout, subtle breathing visible on chest, expression shifts to knowing confident smile, head movement follows hand motion smoothly, fade to next moment
Siena full-body camera angle, slow rotation 180 degrees over 4 seconds showing full body and minimal coverage from multiple angles, hands moving sensually across own collarbone and hip area with confident slow motion, warm golden bathroom lighting (2700K) maintained, direct eye contact locked with camera throughout rotation, confident powerful expression, lighting catches body curves and skin throughout motion, ends on power pose facing camera directly"""

# Configuration
VIDEO_DURATION_SECONDS = 6  # Seconds per video segment

# Paths
skill_dir = Path(r"C:\Users\mohit\.openclaw\workspace\skills\comfyui-workflow-runner")
images_workflow = Path(r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Images_workflow.json")
videos_workflow = Path(r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Videos_workflow.json")
run_script = skill_dir / "scripts" / "run_workflow.py"

def load_workflow(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_workflow(workflow, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2)

def submit_workflow(workflow_path, inputs):
    """Submit workflow via run_workflow.py"""
    input_json = json.dumps(inputs)
    cmd = [
        sys.executable,
        str(run_script),
        str(workflow_path),
        "--inputs", input_json,
        "--server", "http://192.168.29.60:8188"
    ]
    
    print(f"\n[SUBMIT] {workflow_path.name}")
    print(f"   Command: {' '.join(cmd[:3])} ...")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0

def main():
    print("** GRWM HEAT REEL - ComfyUI Submission **")
    print("=" * 60)
    
    # Load workflows
    print("\n[*] Loading workflows...")
    images_wf = load_workflow(images_workflow)
    videos_wf = load_workflow(videos_workflow)
    print("   [OK] Images workflow loaded")
    print("   [OK] Videos workflow loaded")
    
    # Prepare inputs
    name = "grwm_heat"
    
    # Image inputs (node ID: value)
    image_inputs = {
        "443.value": image_prompts,  # Image prompts
        "500.value": name             # Output name
    }
    
    # Video inputs
    video_inputs = {
        "436.value": video_prompts,   # Video prompts
        "500.value": name             # Output name (same directory)
    }
    
    # Submit images workflow
    print("\n[*] STEP 1: Submitting Images Workflow")
    if not submit_workflow(images_workflow, image_inputs):
        print("[!] Failed to submit images workflow")
        return False
    
    images_prompt_id = "waiting..."
    print(f"   Images prompt_id: {images_prompt_id}")
    
    # Wait 5 seconds
    print("\n[*] Waiting 5 seconds before submitting videos...")
    for i in range(5, 0, -1):
        print(f"   {i}...", end=" ", flush=True)
        time.sleep(1)
    print("[OK]")
    
    # Submit videos workflow
    print("\n[*] STEP 2: Submitting Videos Workflow")
    if not submit_workflow(videos_workflow, video_inputs):
        print("[!] Failed to submit videos workflow")
        return False
    
    videos_prompt_id = "waiting..."
    print(f"   Videos prompt_id: {videos_prompt_id}")
    
    # Summary
    print("\n" + "=" * 60)
    print("[SUCCESS] BOTH WORKFLOWS SUBMITTED!")
    print("\n[STATUS]")
    print(f"   Output directory: ComfyUI/output/{name}/")
    print(f"   Images: {name}/Images/")
    print(f"   Videos: {name}/Videos/")
    print(f"   Server: http://192.168.29.60:8188")
    print("\n[INFO] Check ComfyUI UI for progress:")
    print("   http://192.168.29.60:8188/")
    print("\n[TIMING]")
    print("   Images: ~5 minutes")
    print("   Videos: ~10-15 minutes")
    print("   Total: ~20 minutes")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
