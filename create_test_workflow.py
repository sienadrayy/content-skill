#!/usr/bin/env python3
"""
Create test workflow with modified prompts only
"""

import json
from pathlib import Path

# Load base workflow
base_wf = Path("comfy-wf/openclaw/Images_workflow.json")
output_wf = Path("siena_test_v1.json")

with open(base_wf, 'r', encoding='utf-8') as f:
    workflow = json.load(f)

# ONLY change the text values - nothing else
image_prompts = """Close-up portrait of siena
Medium shot of siena  
Full body shot of siena"""

video_prompts = """Slow eye gaze
Slow shoulder roll
Slow fluid movement"""

# Modify only the prompt text
workflow['443']['inputs']['value'] = image_prompts
workflow['500']['inputs']['value'] = video_prompts

# Save to new file
with open(output_wf, 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2)

print("[OK] Workflow created: siena_test_v1.json")
print(f"[OK] Node 443 (images): {len(image_prompts.split(chr(10)))} prompts")
print(f"[OK] Node 500 (videos): {len(video_prompts.split(chr(10)))} prompts")
print("[OK] Ready to load in ComfyUI")
