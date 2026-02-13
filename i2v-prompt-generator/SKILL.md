---
name: i2v-prompt-generator
description: Convert sensual-reels scripts into image-to-video (i2v) model prompts. Automatically extracts 8-10 key moments from a 60-second timeline script, generates detailed image prompts with outfit, pose, lighting, expression and background details (including "siena" keyword), and corresponding 4-second video motion prompts. Output format optimized for i2v AI generation with LoRA model. Use when: (1) Converting sensual-reels script to i2v prompts, (2) Generating image+video prompt pairs for AI video generation, (3) Creating structured prompts for multi-clip sensual video content.
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

## Image Prompt Structure

Each image prompt includes:
- **Subject:** "siena" (always included)
- **Outfit/Clothing:** Specific materials, coverage, colors (minimal, silk, etc.)
- **Pose/Body Position:** Exact positioning (recline, seated, standing, angle)
- **Expression/Eyes:** Eye contact, expression (confident, mysterious, engaged)
- **Background:** Location (bedroom, bathroom, outdoor, etc.)
- **Lighting:** Mood and direction (golden hour, warm lamp, soft shadows, etc.)
- **Style:** "professional photography", "cinematic", etc.

**Example:**
```
<Image 1>
Close-up portrait of siena in golden bedroom light, confident direct eye contact, bare shoulders visible, silk robe draped elegantly, intimate and sensual expression, warm champagne tones, professional cinematic photography
```

## Video Prompt Structure

Each video prompt includes:
- **Primary Motion:** What moves (face, camera, body, etc.)
- **Movement Type:** Type of motion (pan, roll, rotation, fade, etc.)
- **Speed:** Pace (slow, deliberate, smooth, etc.)
- **Duration:** 4 seconds (standard for each segment)
- **Transition:** How it connects to next (cut, fade, continuous, etc.)

**Example:**
```
<Video 1>
Slow blink with confident eye gaze held for 4 seconds, soft golden lighting preserved, no body movement, direct to camera, fade to next segment
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

## Pro Tips

- **Use with sensual-reels:** Feed this skill the exact script from sensual-reels for perfect alignment
- **Consistency:** All 8-10 prompts maintain the same "siena" visual identity
- **4-second timing:** Each video prompt is optimized for ~4 sec i2v generation
- **Clip assembly:** Generated clips will stitch together smoothly for final 60-sec video
