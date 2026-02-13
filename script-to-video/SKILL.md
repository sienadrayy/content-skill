---
name: script-to-video
description: End-to-end content pipeline orchestrator. Generate complete Instagram Reel content in one go from concept to i2v prompts. Automatically runs sensual-reels skill to generate 60-second script, presents it for your verification and approval, then runs i2v-prompt-generator skill to create image and video prompts ready for AI generation. Single command generates complete production assets. Use when: (1) Creating new Instagram Reel content from scratch, (2) Need both script and i2v prompts in one workflow, (3) Want verification step between script generation and prompt creation, (4) Daily content planning with full pipeline.
---

# Script to Video 🎬 → 🎥

Complete content pipeline in one skill. Generate script → verify → convert to i2v prompts → ready to film.

## How It Works

**One command does everything:**

```
Generate complete reel content
```

**The workflow:**

1️⃣ **Generate Script** 
   - Runs sensual-reels skill
   - Creates 60-second timeline script + concept

2️⃣ **Present for Verification**
   - Shows you the complete script
   - Asks: Approve? Modify? Regenerate?
   - Waits for your feedback

3️⃣ **Convert to i2v Prompts**
   - Once approved, runs i2v-prompt-generator
   - Extracts 8-10 key moments
   - Generates image + video prompts
   - All with "siena" keyword

4️⃣ **Deliver Final Output**
   - Script (approved)
   - i2v prompts (8-10 pairs)
   - Ready to shoot and generate

---

## Quick Start

**Just say:**
```
Generate complete reel content
```

**You'll get:**
1. Script with timeline and concept
2. Request for approval ("Ready to proceed?")
3. i2v prompts (image + video for 8-10 moments)
4. Full production-ready output

---

## The Verification Step

After script generation, you see:

```
GENERATED SCRIPT
[Full 60-second timeline]

CONCEPT
[Styling, angles, lighting, poses, vibe]

---
✅ Does this work for you? 
- "Yes, proceed with i2v prompts"
- "Modify: [your request]"
- "Regenerate: [new concept]"
```

**You control quality** before moving to AI generation. No wasted prompts on scripts you don't like!

---

## Output Format

**Step 1 - Script Verification:**
```
TIMELINE SCRIPT
[0-2s] HOOK: [description]
[2-15s] BUILD: [description]
... etc ...

CONCEPT
[Full concept details]

> Awaiting your approval...
```

**Step 2 - i2v Prompts (After Approval):**
```
SCRIPT APPROVED ✅

Image Prompts

<Image 1>
[detailed description with siena]

<Image 2>
[detailed description with siena]
... (8-10 total)

Video Prompts

<Video 1>
[4-second motion description]

<Video 2>
[4-second motion description]
... (8-10 total)

READY FOR i2v MODEL → siena LoRA
```

---

## Workflow Variations

### Option 1: Full Auto (Recommended Daily)
```
"Generate complete reel content"
→ Approve → Get i2v prompts
```

### Option 2: Script First, Review Later
```
"Generate script only"
→ Review script
→ "Convert this script to i2v prompts"
```

### Option 3: Specific Concept
```
"Generate reel for: [your concept idea]"
→ Gets script with your concept
→ Approve or modify
→ Convert to i2v prompts
```

---

## Dependencies

This skill requires:
- ✅ **sensual-reels skill** (generates script)
- ✅ **i2v-prompt-generator skill** (generates prompts)

Both must be available in your OpenClaw setup.

---

## Perfect For

✅ **Daily workflow** - One command for complete content  
✅ **Quality control** - Verify before AI generation  
✅ **Time savings** - Skip switching between skills  
✅ **Batch production** - Generate multiple complete assets at once  
✅ **Content planning** - Script + prompts in one go  

---

## Pro Tips

1. **Use daily** - "Generate complete reel content" → get approved script + i2v prompts in minutes
2. **Batch mode** - Ask for 3 complete reels in one session, modify those you want
3. **Save the scripts** - Each approved script becomes reference for future content
4. **Track themes** - Monitor which concepts/vibes get most engagement
5. **Iterate quickly** - If script doesn't work, regenerate immediately without losing i2v prompts

---

## What Happens Behind the Scenes

1. Skill triggers sensual-reels
2. sensual-reels generates script + concept
3. Output presented to you
4. Waits for "yes" / "modify" / "regenerate"
5. Once approved, triggers i2v-prompt-generator with exact script
6. i2v-generator extracts moments and creates prompts
7. All output delivered to you
8. Ready to shoot and use i2v model

**Total time:** 2-3 minutes from request to ready-to-shoot prompts!
