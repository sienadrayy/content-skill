#!/usr/bin/env python3
"""
Test pipeline: 3-part showering script -> 3 image + 3 video prompts -> ComfyUI

3 Parts = 3 Images (one per 20-second part) + 3 Videos (one per 20-second part)
"""

# 3-Part Showering Script (60 seconds total)
SHOWERING_SCRIPT = """
[PART 1: ANTICIPATION - 0:00-0:20]
Close-up: Water droplets cascading, steam rising. Siena's hand enters frame, 
testing water temperature. Direct eye contact with camera, confident smile. 
Warm lighting glows through shower steam. Sensual anticipation building. 
Professional glamour photography.

[PART 2: SENSATION - 0:20-0:40]
Medium shot: Water flowing over shoulders and body. Hair wet and glistening. 
Confident posture, eyes closed then opening with intensity. Water beads catching light. 
Siena's curves emphasized through water flow. Intimate sensual moment. 
Luxury spa aesthetic. Professional beauty cinematography.

[PART 3: CONFIDENCE - 0:40-1:00]
Full-body reveal: Stepping out of shower frame, reaching for towel. 
Direct camera engagement, knowing smile. Water droplets on skin catching professional lighting. 
Confident power pose. Siena's branding moment @desire.siena. 
Ultimate sensual confidence captured. Cinematic finale photography.
"""

# Image Prompts (3 only - one per part/segment)
IMAGE_PROMPTS = """Close-up of water droplets and steam, Siena's hand testing water, direct eye contact, warm golden shower lighting, anticipation expression, luxury bathroom setting, professional photography
Water flowing over shoulders, hair wet and glossy, confident posture, water beads catching light, sensual energy, intimate moment, luxury spa aesthetic, warm professional lighting, beauty photography
Siena stepping out of shower, reaching for towel, direct camera engagement, knowing smile, water droplets on skin, confident power pose, @desire.siena branding energy, professional finale"""

# Video Prompts (3 only - one per part/segment, 20 seconds each)
VIDEO_PROMPTS = """Water droplets falling, hand testing water, maintain direct eye contact throughout full 20 seconds, slow sensual motion building, warm steam and lighting preserved, anticipation energy held constant, smooth transitions between angles, fade to next segment
Water flowing over shoulders for full 20 seconds, confident posture maintained throughout, eyes intensity building from calm to power, water catching light consistently, sensual curves emphasized through deliberate slow movement, warm professional lighting constant, cut to next
Full 20-second sequence: stepping out of shower, reaching for towel, direct camera engagement growing, confident power energy building, water droplets visible and catching light, branding moment energy present, @desire.siena presence grows, cinematic finale motion maintained"""

def main():
    import subprocess
    import sys
    
    print("=" * 70)
    print("TESTING COMPLETE REEL PIPELINE - 3 PART SHOWERING REEL")
    print("=" * 70)
    print("Structure: 3 Images + 3 Videos (20 seconds each)")
    
    print("\n" + "=" * 70)
    print("PART 1: Generated 3-Part Script (60 seconds)")
    print("=" * 70)
    print(SHOWERING_SCRIPT)
    
    print("\n" + "=" * 70)
    print("PART 2: Extracted Image Prompts (3 IMAGES ONLY)")
    print("=" * 70)
    for i, prompt in enumerate(IMAGE_PROMPTS.split('\n'), 1):
        print(f"Image {i}: {prompt}")
    
    print("\n" + "=" * 70)
    print("PART 3: Extracted Video Prompts (3 VIDEOS, 20 sec each)")
    print("=" * 70)
    for i, prompt in enumerate(VIDEO_PROMPTS.split('\n'), 1):
        print(f"Video {i} (0:{(i-1)*20:02d}-0:{i*20:02d}): {prompt[:80]}...")
    
    print("\n" + "=" * 70)
    print("PART 4: Running ComfyUI Dual Workflows")
    print("=" * 70)
    
    cmd = [
        sys.executable,
        "run_dual_workflow.py",
        "--name", "siena_showering_reel",
        "--image-prompts", IMAGE_PROMPTS,
        "--video-prompts", VIDEO_PROMPTS
    ]
    
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode == 0:
        print("\n" + "=" * 70)
        print("SUCCESS: 3-Part Showering Reel Pipeline Complete!")
        print("=" * 70)
        print("\nGenerated Content:")
        print(f"  Name: siena_showering_reel")
        print(f"  Concept: Showering (3-Part Structure)")
        print(f"  Duration: 60 seconds total")
        print(f"  Images: 3 (one per 20-second part)")
        print(f"  Videos: 3 (one per 20-second part, 20 sec each)")
        print(f"\nParts Breakdown:")
        print(f"  Part 1 [0:00-0:20]: Anticipation")
        print(f"  Part 2 [0:20-0:40]: Sensation")
        print(f"  Part 3 [0:40-1:00]: Confidence")
        print(f"\nMonitor Progress:")
        print(f"  URL: http://192.168.29.60:8188")
        print(f"  Images: ComfyUI/output/siena_showering_reel/Images/")
        print(f"  Videos: ComfyUI/output/siena_showering_reel/Videos/")
        print(f"\nNext: Download and post to Instagram @desire.siena")
        return 0
    else:
        print("\n[ERROR] ComfyUI workflows failed")
        return 1

if __name__ == "__main__":
    exit(main())
