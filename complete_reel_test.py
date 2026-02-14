#!/usr/bin/env python3
"""
Complete Reel Test - 3-part script with i2v prompts
"""

import json
from pathlib import Path

# 3-PART SENSUAL SCRIPT
script_name = "siena_valentine_reel_v1"

# Part 1: Hook (0-20s)
part1_images = """Close-up portrait of siena in warm golden bedroom lamp light, confident direct eye contact, bare shoulders visible, champagne silk robe draped elegantly, subtle lip parting, intimate sensual expression, soft golden tones, professional cinematic photography
Medium shot of siena, golden light catching her shoulders, silk robe sliding to reveal collarbone and upper chest, hand tracing shoulder slowly, confident posture, bare skin glowing, luxury bedroom setting, warm champagne lighting, fine art photography"""

part1_videos = """Slow confident eye gaze held directly to camera for 2 seconds, subtle head tilt, lips part and close gently, warm golden rim lighting preserved
Smooth camera pan down from face to shoulders over 3 seconds, siena maintains confident eye contact, warm golden lighting consistent, ends on shoulder reveal"""

# Part 2: Build (20-40s)
part2_images = """Full body of siena seated on edge of bed, champagne silk robe partially open, chest open and confident, golden bedroom light illuminating curves, sensual seated pose, luxury intimate setting, warm golden rim lighting, cinematic photography
Seated siena mid-body-roll, shoulders rotating back, chest fully open, confident direct eye contact maintained, silk robe flowing, curves emphasized through deliberate posing, golden light catching skin, peak sensual moment, professional glamorous photography"""

part2_videos = """Fixed camera, siena transitions from standing to seated position over 2 seconds, then holds confident seated pose for final 2 seconds, warm lighting maintained, chest open throughout
Slow body roll rotation from right to left over 4 seconds, sensual fluid motion, camera stays fixed, curves emphasized, golden lighting catches motion, fade to next"""

# Part 3: Peak (40-60s)
part3_images = """Close-up of siena's face with intense eye contact, hand near neck/collarbone area, confident expression with subtle lip bite, golden warm lighting on face, intimate connection energy, professional beauty photography
Extreme close-up of siena's face, direct to camera, peak confidence expression, eye contact intense and magnetic, warm golden light catching eyes and lips, sensual power moment, intimate yet commanding presence, cinematic portrait"""

part3_videos = """Hold confident gaze for 3 seconds with minimal movement, knowing smile maintained, warm lighting consistent, then subtle head movement for engagement, dissolve to final moment
Hold final power moment pose with zero movement, intense direct eye contact maintained, confident expression frozen, warm golden lighting perfect, fade to black"""

# Combine all parts
all_images = part1_images + "\n" + part2_images + "\n" + part3_images
all_videos = part1_videos + "\n" + part2_videos + "\n" + part3_videos

# Load base workflow
base_wf = Path("comfy-wf/openclaw/Images_workflow.json")
output_wf = Path(f"{script_name}.json")

with open(base_wf, 'r', encoding='utf-8') as f:
    workflow = json.load(f)

# Inject prompts ONLY
workflow['443']['inputs']['value'] = all_images
workflow['500']['inputs']['value'] = all_videos

# Save
with open(output_wf, 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2)

print(f"[OK] Complete reel workflow created: {script_name}.json")
print(f"[OK] Script: 3-part sensual reel (60 seconds)")
print(f"[OK] Part 1 (Hook): 2 image prompts, 2 video prompts")
print(f"[OK] Part 2 (Build): 2 image prompts, 2 video prompts")
print(f"[OK] Part 3 (Peak): 2 image prompts, 2 video prompts")
print(f"[OK] Total: 6 image prompts, 6 video prompts")
print(f"\n[NEXT STEPS]")
print(f"1. Load {script_name}.json in ComfyUI")
print(f"2. Turn ON Images flow, turn OFF Video flow")
print(f"3. Click Run (generates images)")
print(f"4. Turn OFF Images flow, turn ON Video flow")
print(f"5. Click Run (generates videos from images)")
