#!/usr/bin/env python3
"""
Enhance video prompts with more specific details and change name to concept-based
"""

import json
from pathlib import Path

# Load workflow
wf_path = Path("comfy-wf/openclaw/Images_workflow.json")

with open(wf_path, 'r', encoding='utf-8') as f:
    workflow = json.load(f)

# ENHANCED VIDEO PROMPTS - MORE DETAILED & SPECIFIC (6 total)
enhanced_video_prompts = """Direct confident eye contact held for full 4 seconds, slow blink at 1.5 second mark, subtle head tilt, lips part and close with intention, warm golden rim lighting preserved, no body movement, camera fixed on face, smooth fade to next segment

Slow controlled camera pan down from face to shoulders over exactly 3 seconds, revealing skin gradually, siena maintains confident eye contact as much as visible, warm golden lighting stays consistent, pan ends on shoulder and collarbone reveal, hard cut to next

Fixed wide camera, siena transitions from standing/leaning to seated position on bed edge over exactly 2 seconds, smooth deliberate motion, then holds confident seated pose for final 2 seconds, warm lighting maintained constant, chest fully open throughout, seamless continuous to next

Slow full-body rotation from right side profile to front-facing to left side profile over exactly 4 seconds, sensual fluid motion that emphasizes curves, camera stays locked fixed position, golden light catches body as it moves, eye contact maintained where visible, dramatic fade to next moment

Hand traces from shoulder down toward collarbone with sensual intention over 2 seconds, deliberate slow motion, siena's facial expression intensifies with confidence, then returns to pose for final 2 seconds with enhanced direct eye contact, warm light preserved, smooth natural transition

Hold confident over-shoulder back glance pose for exactly 3 seconds with minimal movement, knowing smile maintained, subtle natural hair shift/adjustment, warm golden lighting consistent, in final second add slight head movement for subtle engagement, dissolve smoothly to next

Slow controlled zoom into extreme close-up of face over 2 seconds, maintain direct eye contact throughout zoom, final 2 seconds hold intense gaze with confidence building, warm light on face intensifies, eye contact deepens with intent, hard cut to power moment

Return to forward-facing pose from over-shoulder position with smooth transition over 1 second, hold confident centered pose for remaining 3 seconds, direct camera engagement with intensity, warm golden lighting constant, subtle breathing visible, seamless continuous flow

Hold final power moment pose with zero movement for full 4 seconds, intense direct eye contact maintained constantly, confident expression frozen perfectly, warm golden lighting perfect, no dissolve, hard cut to black"""

# CONCEPT-BASED NAME
concept_name = "golden_hour_confidence"

# Update workflow
workflow['500']['inputs']['value'] = enhanced_video_prompts

# Save
with open(wf_path, 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2)

print(f"[OK] Enhanced video prompts (9 detailed segments)")
print(f"[OK] Concept name ready: {concept_name}")
print(f"[OK] Ready to reload and toggle controls in ComfyUI")
