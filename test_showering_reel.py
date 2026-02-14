#!/usr/bin/env python3
"""
Test pipeline: 3-part showering script -> i2v prompts -> ComfyUI generation
"""

# 3-Part Showering Script (60 seconds)
SHOWERING_SCRIPT = """
[PART 1: ANTICIPATION - 0:00-0:20]
Close-up: Water droplets cascading, steam rising. Siena's hand enters frame, testing water temperature. Direct eye contact with camera, confident smile. Warm lighting glows through shower steam. Sensual anticipation building. Professional glamour photography.

[PART 2: SENSATION - 0:20-0:40]
Medium shot: Water flowing over shoulders and body. Hair wet and glistening. Confident posture, eyes closed then opening with intensity. Water beads catching light. Siena's curves emphasized through water flow. Intimate sensual moment. Luxury spa aesthetic. Professional beauty cinematography.

[PART 3: CONFIDENCE - 0:40-1:00]
Full-body reveal: Stepping out of shower frame, reaching for towel. Direct camera engagement, knowing smile. Water droplets on skin catching professional lighting. Confident power pose. Siena's branding moment @desire.siena. Ultimate sensual confidence captured. Cinematic finale photography.
"""

# Image Prompts (extracted from 3-part script - 10 segments)
IMAGE_PROMPTS = """
Close-up of water droplets and steam, Siena's hand testing water, direct eye contact, warm golden shower lighting, anticipation expression, luxury bathroom setting, professional photography
Medium shot Siena under water, hair wet and glossy, shoulders revealed, confident expression building, water catching light, sensual energy, warm professional lighting, beauty photography
Siena's face under water stream, eyes intense and confident, water flowing over features, warm lighting, intimate close-up moment, sensual beauty, professional portrait
Water cascading down body, Siena's torso and shoulders, confident posture maintained, water beads on skin catching light, luxury spa aesthetic, professional body photography
Siena rotating under water, curves emphasized through flowing water, confident energy maintained, warm professional lighting, sensual movement moment, luxury photography
Siena stepping forward, water streaming, direct camera engagement, knowing smile, powerful confident moment, professional photography
Close-up face during water cascade, eyes open with intensity, sensual expression building, warm golden lighting, intimate professional portrait
Siena reaching for towel moment, stepping out of shower, direct camera connection, knowing confident smile, power moment captured, professional photography
Full-body frame, towel in hand, dry skin glistening with water beads, confident power pose, branding moment, @desire.siena energy, professional photography
Final sensual confidence moment, Siena direct to camera, ultimate power expression, warm luxury lighting, cinematic quality, professional finale
"""

# Video Prompts (extracted from 3-part script - 10 segments of 4 seconds each)
VIDEO_PROMPTS = """
Water droplets falling, hand testing water, maintain direct eye contact for full 4 seconds, slow sensual motion, warm steam and lighting preserved, anticipation energy held, fade to next segment
Water flowing over shoulders, head tilts to reveal collarbones, confidence building over 4 seconds, warm lighting constant, sensual fluid motion maintained, cut to next
Extreme close-up of face under water stream, eyes open with intensity building over full 4 seconds, water cascading, direct eye contact maintained where visible, confidence peaks, fade
Body rotation under water over 4 seconds, curves emphasized through deliberate movement, warm light catches body, confident energy sustained, smooth motion to next
Torso and shoulder focus, 4-second slow pan down while water flows, sensual deliberate motion, lighting maintained, intimate moment holds, hard cut to next
Stepping forward motion over 4 seconds, water streaming, body reveals gradually, confidence sustained throughout, direct camera focus maintained, transition smooth
Face close-up 4-second hold, intensity and confidence sustained, water flowing, eye contact powerful and consistent, sensual expression unchanging, dissolve
Full-body motion stepping out over 4 seconds, towel reaching moment, direct camera engagement grows, powerful confident energy building, professional aesthetic held, cut
Standing confident pose held 4 seconds, towel visible, body confident, direct to camera, knowing smile maintained, branding energy present, lighting perfect, continuous
Final power moment frozen 4 seconds, ultimate confidence expression, direct intense eye contact, sensual strength emanates, @desire.siena presence felt, cinematic finale
"""

def main():
    import subprocess
    import sys
    
    print("=" * 70)
    print("TESTING COMPLETE REEL PIPELINE")
    print("Concept: SHOWERING (3-Part Script)")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("PART 1: Generated 3-Part Script")
    print("=" * 70)
    print(SHOWERING_SCRIPT)
    
    print("\n" + "=" * 70)
    print("PART 2: Extracted Image Prompts (10 segments)")
    print("=" * 70)
    print(IMAGE_PROMPTS[:200] + "...")
    
    print("\n" + "=" * 70)
    print("PART 3: Extracted Video Prompts (10 x 4-second segments)")
    print("=" * 70)
    print(VIDEO_PROMPTS[:200] + "...")
    
    print("\n" + "=" * 70)
    print("PART 4: Running ComfyUI Dual Workflows")
    print("=" * 70)
    
    cmd = [
        sys.executable,
        "run_dual_workflow.py",
        "--name", "siena_showering_reel",
        "--image-prompts", IMAGE_PROMPTS[:500],
        "--video-prompts", VIDEO_PROMPTS[:500]
    ]
    
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode == 0:
        print("\n" + "=" * 70)
        print("SUCCESS: Showering Reel Pipeline Complete!")
        print("=" * 70)
        print("\nGenerated Content:")
        print(f"  Name: siena_showering_reel")
        print(f"  Concept: Showering (3-Part)")
        print(f"  Script: 60 seconds, 3 parts")
        print(f"  Image Segments: 10")
        print(f"  Video Segments: 10 x 4-sec")
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
