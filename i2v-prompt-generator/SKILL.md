---
name: i2v-prompt-generator
description: Convert sensual-reels scripts into image-to-video (i2v) model prompts. Automatically extracts 8-10 key moments from a 60-second timeline script, generates detailed image prompts with outfit, pose, lighting, expression and background details (including "siena" keyword), and corresponding 4-second video motion prompts. Output format optimized for i2v AI generation with LoRA model. Use when: (1) Converting sensual-reels script to i2v prompts, (2) Generating image+video prompt pairs for AI video generation, (3) Creating structured prompts for multi-clip sensual video content.

**⚠️ CRITICAL:** See `references/prompt-output-format.md` for EXACT output format before showing prompts to user. NO tags, NO headers, NO blank lines between prompts.
---

# i2v Prompt Generator 🎬

Convert sensual-reels scripts into AI-ready image and video prompts. Extracts key moments, generates detailed visual descriptions with sensuality optimized for i2v models with LoRA fine-tuning.

## How It Works

**Input:** sensual-reels timeline script (60 seconds)

**Process:**
1. Auto-identify 8-10 key moments from the script
2. For each moment: generate image + video prompt pair
3. Each 4-second segment = 1 image prompt + 1 video motion prompt
4. Always include "siena" keyword + LoRA trigger

**Output:** 
```
Image Prompts

<Image 1>
[detailed image description]

<Image 2>
[detailed image description]

...

Video Prompts

<Video 1>
[4-second motion description]

<Video 2>
[4-second motion description]

...
```

## Quick Start

**Just paste your sensual-reels script:**

```
I have this script:
[0-2s] HOOK: Close-up face, confident eye contact...
[2-15s] BUILD: Pan down shoulder, minimal clothing...
[15-45s] MAIN: Body roll, sensual movement...
etc.

Generate i2v prompts.
```

**You'll get:**
- 8-10 auto-selected key moments
- Image prompt for each (all details: outfit, pose, bg, lighting, "siena")
- Video prompt for each (4-sec motion description)

## Image Prompt Structure - DETAILED & STANDALONE

Each image prompt is **COMPLETE AND STANDALONE** - no references to other prompts, no "same as", no consistency cross-references.

**MANDATORY ELEMENTS:**

1. **Subject:**
   - Siena (always include name)
   - Body position/pose (standing, stepping, reaching, angle, degree positioning)

2. **Outfit/Clothing/Wetness State:**
   - Specific materials (silk, water, etc.)
   - Coverage level (bare shoulders, exposed collarbone, full-body, etc.)
   - Colors (golden, champagne, bronze tones, etc.)
   - Wetness state (dripping, slicked back, wet throughout, water flowing, etc.)

3. **Pose & Body Details:**
   - Exact positioning (standing, stepping forward, reaching, body angle)
   - Visible body parts (shoulders, collarbones, chest, legs, curves)
   - Hand positions (at side, reaching, testing, holding)
   - Angle of body (45-degree turn, direct facing, profile, etc.)
   - Movement implied in pose (stepping, rotating, reaching motion)

4. **Expression & Eyes:**
   - Eye contact (direct to camera, intense, locked)
   - Expression (confident, knowing smile, power, anticipation, sensual)
   - Facial details (lip parting, smile type, eye intensity)

5. **Lighting:**
   - EXACT COLOR TEMP (2700K warm golden, 5600K daylight, etc.)
   - Direction (front-lit, back-lit, side-lit, overhead, diffused)
   - Quality (soft, dramatic, glowing, catching light, sparkling)
   - Effect on skin/water (highlighting, shadows, reflections)

6. **Background:**
   - Location (bathroom, bedroom, outdoor, etc.)
   - Details (tile wall, towel rack, nature, etc.)
   - Focus (sharp, soft-focused, bokeh, out of focus)

7. **Water/Elements:**
   - Water state (droplets on skin, flowing, cascading, sparkling)
   - Visible water movement
   - Water catching light and sparkle effects

8. **Hair:**
   - State (wet, dripping, slicked back, flowing, wet strands visible)
   - Movement/styling (loose, pulled back, cascading)

9. **Overall Style/Quality:**
   - "professional beauty photography", "professional body photography", "cinematic photography"

**CRITICAL RULES:**
- ❌ NO CROSS-REFERENCES ("same as Image 1", "consistent with previous")
- ❌ NO BRANDING or @ mentions
- ❌ NO TIME REFERENCES
- ✅ EACH PROMPT COMPLETE DESCRIPTION
- ✅ DETAILED LIGHTING SPECS
- ✅ DETAILED BODY/POSE SPECS
- ✅ EXPLICIT WETNESS/CLOTHING STATE

**Example:**
```
<Image 1>
Close-up of Siena's face, wet hair dripping down shoulders, bare shoulders visible, direct eye contact with camera, 
confident anticipation expression, warm golden shower steam lighting (2700K), bathroom tile wall soft-focused background, 
water droplets on face and neck, slight knowing smile, hands testing water stream at shoulder level, 
professional beauty photography, razor-sharp focus on face, soft bokeh background

<Image 2>
Siena medium shot, shoulders and upper body exposed, hair wet and slicked back, water actively flowing down shoulders and collarbone, 
body turned 45-degrees angle, intense eye contact with camera, expression showing calm-to-power transition, 
water beads catching light and sparkling, visible collarbones and shoulder definition, luxury bathroom background, 
skin glowing with water droplets, warm golden lighting (2700K) throughout scene, professional body photography

<Image 3>
Siena full-body standing, stepping forward in motion, reaching right hand toward towel rack, left hand at side, 
direct forward-facing camera engagement, knowing confident smile, water droplets visible across entire body catching and reflecting light, 
warm golden shower lighting (2700K), towel visible in frame, professional powerful confident stance, 
expression showing peak confidence and power, bathroom setting visible in background, professional finale photography
```

**NOT:**
```
Siena in shower, water flowing, confident expression, golden lighting, professional photography.
```

## Video Prompt Structure - MOTION FOCUSED ⭐ CRITICAL

Each video prompt MUST include DETAILED MOTION DESCRIPTIONS. Each prompt is **STANDALONE** - no cross-references, no "same as", no "consistent with previous", each prompt complete.

**MANDATORY ELEMENTS:**

1. **Camera Setup:**
   - Camera angle (close-up, medium shot, full-body, static, etc.)
   - Camera movement (fixed, tracking, panning, zoom, etc.)

2. **Motion Details - EXPLICIT:**
   - Head movements (tilts, turns, degree angles, speed)
   - Eye movements (opening, closing, pupils dilating, intensity progression)
   - Hand movements (reaching, tracing, spreading, curling, speed, path)
   - Body movements (rotation degrees, stepping, swaying, side-to-side, speed)
   - Hair movements (falling, floating, cascading, motion descriptions)
   - Arm movements (raising, lowering, positioning, speed)

3. **Water/Element Dynamics:**
   - Water flowing (continuous, cascading, streaming, direction)
   - Water droplets (falling, rolling, visible motion, speed)
   - Sparkle and light reflection (when visible, intensity)
   - Dripping motion (location, speed, frequency)

4. **Expression/Eyes Progression:**
   - Starting state (neutral, calm, closed)
   - Transition (building, deepening, intensifying)
   - Final state (power, confident, locked intensity)
   - Micro-movements (pupil dilation, eyelid lowering, lip parting)

5. **Breathing/Subtle Motion:**
   - Visible chest movement
   - Shoulder rise/fall
   - Natural breathing visible in frame

6. **Transition:**
   - How video ends (fade, cut, hard cut, freeze)

7. **Lighting/Sound:**
   - Exact color temp (2700K, 5600K, etc.)
   - Sound (water sounds, silence, etc.)

**CRITICAL RULES:**
- ❌ NO TIME MARKERS ("Seconds 0-5", "0-2s", "first half", "then")
- ❌ NO REFERENCES TO OTHER PROMPTS ("same as Video 1", "consistent with Image 2")
- ❌ NO BRANDING (@desire.siena, usernames, tags)
- ❌ NO VAGUE DESCRIPTIONS ("sensual motion", "confident energy")
- ✅ EXPLICIT MOTION ("hand reaching 45 degrees slowly over 5 hand movements")
- ✅ SPECIFIC ANGLES AND DEGREES ("180-degree rotation", "15 degree head tilt")
- ✅ SPEED DESCRIPTORS ("slow", "deliberate", "smooth" + duration context)
- ✅ EVERY MOVEMENT DESCRIBED in detail

**Example:**
```
<Video 1>
Close-up static camera on Siena's face, warm golden shower steam lighting (2700K). 
Water droplets begin falling from top, slow continuous cascade throughout. 
Hand enters frame from left side, fingers moving deliberately to test water temperature, 
slow sensual testing motion repeated 2-3 times. 
Head tilts slowly right 15 degrees, direct eye contact locked with camera. 
Confident smile builds gradually from neutral to knowing expression. 
Eyes deepen in intensity with micro-movements (pupils dilating, eyelids lowering slightly). 
Slight lip parting occurs, single water droplet rolling slowly down left cheek from temple. 
Hair strands drip steadily, occasional strand falling across shoulder with slow floating motion. 
Facial breathing becomes visible, subtle chest rise/fall. 
Water stream sound present. 
Entire body remains still, only head and hands move. 
Motion ends with slow fade to black.
```

**NOT:**
```
Water droplets fall, hand testing temperature, eye contact maintained, smile builds, 
eyes deepen, lip parts, same warm lighting, fade to black.
```

## Prompt Language Reference

See `references/image-prompt-language.md` for:
- Pose terminology (recline patterns, standing poses, angles, etc.)
- Outfit/material descriptions (silk, mesh, sheer, minimal, etc.)
- Lighting language (golden hour, moody, dramatic, warm, etc.)
- Expression vocabulary (confident, mysterious, alluring, etc.)

See `references/video-prompt-language.md` for:
- Motion types (pan, zoom, rotation, roll, fade, cut, etc.)
- Camera movements (tracking, fixed, overhead, etc.)
- Transition terminology (cut, fade, dissolve, continuous, etc.)

## Moment Selection Strategy

The skill auto-selects moments by:
1. **Hook moment** (0-3s) - Peak attention grab
2. **Reveal moments** (2-3 key transitions showing more)
3. **Main sensual peaks** (2-3 maximum impact moments)
4. **Engagement moments** (1-2 direct camera/connection moments)
5. **Transitions** (1-2 smooth connecting moments)

Result: 8-10 total moments distributed across the 60-second script for maximum visual impact.

## LoRA Integration

All prompts automatically include:
- ✅ "siena" keyword (your LoRA trigger)
- ✅ Reference to sensual aesthetic matching LoRA training
- ✅ Consistent visual style throughout prompts
- ✅ Details that maximize LoRA model recognition

## Generation Requirements ⭐ MANDATORY

When generating prompts:

1. **Each Prompt is STANDALONE:**
   - ❌ NO references to other prompts ("same as Video 1", "consistent with Image 2")
   - ❌ NO cross-references within descriptions
   - ✅ Each prompt complete, detailed, independent

2. **Detailed Over Generic:**
   - ❌ Don't: "sensual water flowing"
   - ✅ Do: "water actively flowing down shoulders and collarbone, water beads catching light and sparkling, visible collarbones and shoulder definition, body turned 45-degrees angle"

3. **Explicit Motion in Videos:**
   - ❌ Don't: "steps forward"
   - ✅ Do: "stepping forward with deliberate slow motion, 2-3 steps taken over several seconds, hand extending toward towel rack with sensual reaching motion, arm movements smooth and controlled"

4. **Specific Angles & Speeds:**
   - ✅ "15 degree head tilt"
   - ✅ "180-degree body rotation"
   - ✅ "slow deliberate motion"
   - ✅ "repeated 2-3 times"

5. **Lighting Specifications:**
   - ALWAYS specify exact color temp: "2700K warm golden", "5600K daylight", etc.
   - Describe where light hits (catching light, highlighting, sparkling, etc.)
   - NO vague "golden lighting"

6. **No Time Markers:**
   - ❌ Don't: "Seconds 0-5: water falls..."
   - ❌ Don't: "First 10 seconds..."
   - ✅ Describe motion as continuous narrative flow

7. **No Branding/Tags:**
   - ❌ NO @desire.siena, usernames, hashtags in prompts
   - Prompts are pure visual descriptions only

8. **Motion Vocabulary (Videos):**
   - Use precise verbs: cascading, streaming, rolling, tilting, rotating, rising, floating, swaying, rippling, sparkling
   - Combine with speed: "slow continuous cascade", "deliberate slow motion", "smooth slow rotation"
   - Add repetition: "repeated 2-3 times", "2-3 steps", "occasional strand falling"

## Pro Tips

- **Standalone Prompts = Better Results:** AI models generate cleaner content when each prompt is complete
- **Detail Prevents Artifacts:** Explicit motion descriptions prevent AI from creating still frames or glitches
- **Motion Commands Clarity:** More detailed motion = more reliable video generation
- **Lighting Locks Quality:** Exact color temps ensure visual quality across all images/videos
- **Duration Implicit:** Never mention duration in prompts - let the i2v model handle timing based on motion description
