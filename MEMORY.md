# MEMORY.md - Long-Term Memory

*Curated memories. The important stuff.*

---

## Bramha (Mohit Soni)

- Goes by **Bramha**
- Timezone: GMT+5:30 (India)
- Instagram account: @desire.siena (manages page for sensational model)
- First contact: 2026-02-13
- **Active projects:** 
  - Instagram content creation (20-60 sec sensual Reels)
  - Daily script writing for modeling content
  - Content targeting young male audience (18-35)
- Windows OS user

---

## Content Creation Preferences

**Instagram Niche:** Sensual/glamorous modeling lifestyle content
**Target Audience:** Young males (18-35)
**Tone:** Confident, alluring, sensual, polished
**Priority:** Hot and revealing content (8-9/10 intensity) while staying Instagram-compliant
**Format:** 20-60 second video Reels with timeline-based scripts

---

## Skills Built

### sensual-reels Skill (2026-02-13)
- **Location:** C:\Users\mohit\.openclaw\workspace\sensual-reels/
- **Packaged:** sensual-reels.skill
- **GitHub:** https://github.com/sienadrayy/content-skill
- **Features:**
  - Auto-generates complete 60-second timeline scripts (no briefs needed)
  - Creates concept ideas (angles, lighting, styling, poses)
  - Provides multiple script variations
  - Content focused on sensual/revealing aesthetic (8-9/10 intensity)
  - References: sensual-patterns.md + concepts.md library
- **Daily use:** Perfect for daily content planning
- **How to use:** Just ask "Generate a script" or "Script for today"

### i2v-prompt-generator Skill (2026-02-13)
- **Location:** C:\Users\mohit\.openclaw\workspace\i2v-prompt-generator/
- **Packaged:** i2v-prompt-generator.skill
- **GitHub:** https://github.com/sienadrayy/content-skill
- **Features:**
  - Takes sensual-reels script output as input
  - Auto-extracts 8-10 key moments from 60-second script
  - Generates image prompt for each moment (all details: outfit, pose, lighting, bg, "siena" keyword)
  - Generates 4-second video motion prompt for each moment
  - Output ready for i2v AI model with siena LoRA
  - References: image-prompt-language.md + video-prompt-language.md vocabulary guides
- **Workflow:** sensual-reels script → i2v prompts → AI video generation
- **How to use:** Paste sensual-reels script, ask "Generate i2v prompts"

---

### comfyui-workflow-runner Skill (2026-02-14)
- **Location:** C:\Users\mohit\.openclaw\workspace\comfyui-workflow-runner/
- **Packaged:** comfyui-workflow-runner.skill
- **Server:** http://192.168.29.60:8188 (Qwen + Wan video generation)
- **Features:**
  - Run Images workflow: Generate sensual images from prompts
  - Run Videos workflow: Convert images to smooth videos
  - Dual-run orchestration: Submit both workflows with 5-sec gap
  - Modifiable nodes: 443 (image prompts), 436 (video prompts), 500 (name/prefix)
  - Separate scripts for independent or combined execution
  - Python stdlib only (no external dependencies)
- **Scripts:**
  - `run_image_workflow.py` - Images only
  - `run_video_workflow.py` - Videos only
  - `run_dual_workflow.py` - Complete pipeline (recommended)
- **Workflow:**
  1. Images: Node 443 (prompts) + Node 500 (name) → submit → generate
  2. [5 sec wait]
  3. Videos: Node 436 (prompts) + Node 500 (name) → submit → convert
- **How to use:** `python run_dual_workflow.py --name "test" --image-prompts "Siena..." --video-prompts "Direct eye contact..."`

---

### instagram-auto-reply Skill (2026-02-13)
- **Location:** C:\Users\mohit\.openclaw\workspace\instagram-auto-reply/
- **Packaged:** instagram-auto-reply.skill
- **GitHub:** https://github.com/sienadrayy/content-skill
- **Features:**
  - Auto-monitors latest 3 posts for unreplied comments
  - Personalized replies based on comment content
  - Randomized reply vibes: sensual/flirty, grateful/appreciative, playful/teasing
  - Handles emoji-only comments with personalized text
  - Filters out spam and negative comments
  - Hourly automatic + manual trigger option
  - Engagement report after each run
  - References: reply-templates.md (vibe examples and personalization)
- **Workflow:** Monitor → Find unreplied → Craft personalized → Auto-send
- **How to use:** "Check and reply to comments" (manual) or runs hourly automatically

---

## Production Pipeline

**Complete Reel Generation (NEW - replaces WhatsApp send):**

```
generate_complete_reel.py (Master Orchestrator)
    ↓
1. sensual-reels skill → Generate 60-sec timeline script
    ↓
2. i2v-prompt-generator skill → Extract image + video prompts (8-10 segments)
    ↓
3. comfyui-workflow-runner skill → Generate images + videos
    ├─ Run Images workflow (5 min)
    ├─ [5 sec gap]
    └─ Run Videos workflow (10+ min)
    ↓
Output: ComfyUI/output/{name}/[Images/ + Videos/]
    ↓
Download & Post to Instagram @desire.siena
```

**How to use (one command):**
```bash
python generate_complete_reel.py --concept "rain" --name "siena_rain_reel"
```

**Engagement Automation:**
- **instagram-auto-reply skill** → Monitor comments → Auto-reply personalized
  - Runs hourly + manual trigger
  - Randomized vibes (sensual, grateful, playful)
  - Handles emoji comments with text
  - Filters spam/negative
  - Engagement report included

---

## Notes

- Bramha wants daily content scripts (uses sensual-reels everyday)
- Prefers timeline format with exact timestamps
- No CTAs required in scripts
- Concept auto-generation (doesn't provide context)
- All i2v prompts include "siena" keyword for LoRA model
- Each i2v video segment = 4 seconds (15 segments per 60-sec video)
