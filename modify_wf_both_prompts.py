#!/usr/bin/env python3
"""
Modify Images_workflow.json with both image AND video prompts (3-part script)
"""

import json
from pathlib import Path

# Load base workflow
wf_path = Path("comfy-wf/openclaw/Images_workflow.json")

with open(wf_path, 'r', encoding='utf-8') as f:
    workflow = json.load(f)

# 3-PART IMAGE PROMPTS (6 total)
image_prompts = """Close-up portrait of siena in warm golden bedroom lamp light, confident direct eye contact, bare shoulders visible, champagne silk robe draped elegantly, subtle lip parting, intimate sensual expression, soft golden tones, professional cinematic photography
Medium shot of siena, golden light catching her shoulders, silk robe sliding to reveal collarbone and upper chest, hand tracing shoulder slowly, confident posture, bare skin glowing, luxury bedroom setting, warm champagne lighting, fine art photography
Full body of siena seated on edge of bed, champagne silk robe partially open, chest open and confident, golden bedroom light illuminating curves, sensual seated pose, luxury intimate setting, warm golden rim lighting, cinematic photography
Seated siena mid-body-roll, shoulders rotating back, chest fully open, confident direct eye contact maintained, silk robe flowing, curves emphasized through deliberate posing, golden light catching skin, peak sensual moment, professional glamorous photography
Close-up of siena's face with intense eye contact, hand near neck/collarbone area, confident expression with subtle lip bite, golden warm lighting on face, intimate connection energy, professional beauty photography
Extreme close-up of siena's face, direct to camera, peak confidence expression, eye contact intense and magnetic, warm golden light catching eyes and lips, sensual power moment, intimate yet commanding presence, cinematic portrait"""

# 3-PART VIDEO PROMPTS (6 total)
video_prompts = """Slow confident eye gaze held directly to camera for 2 seconds, subtle head tilt, lips part and close gently, warm golden rim lighting preserved, no body movement, camera fixed, fade to next segment
Smooth camera pan down from face to shoulders over 3 seconds, revealing body gradually, siena maintains confident eye contact as much as visible, warm golden lighting consistent, ends on shoulder reveal, cut to next
Fixed camera, siena transitions from standing/leaning to seated position on bed edge over 2 seconds, then holds confident seated pose for final 2 seconds, warm lighting maintained, chest open throughout, continuous to next
Slow body roll rotation from right side to front to left side over full 4 seconds, sensual fluid motion, camera stays fixed, curves emphasized through deliberate movement, eye contact maintained where visible, golden lighting catches motion, fade to next
Hold confident gaze for 3 seconds with minimal movement, knowing smile maintained, warm lighting consistent, then subtle head movement for engagement, dissolve to final moment
Hold final power moment pose with zero movement, intense direct eye contact maintained, confident expression frozen, warm golden lighting perfect, fade to black"""

# Inject ONLY text values
workflow['443']['inputs']['value'] = image_prompts
workflow['500']['inputs']['value'] = video_prompts

# Save back to the same file
with open(wf_path, 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2)

print("[OK] Images_workflow.json updated:")
print(f"[OK] Node 443 (Image Prompts): 6 prompts injected")
print(f"[OK] Node 500 (Video Prompts): 6 prompts injected")
print(f"[OK] Ready to reload in ComfyUI")
