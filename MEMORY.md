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

### wan-animate-reel Skill (2026-02-14)
- **Location:** C:\Users\mohit\.openclaw\workspace\wan-animate-reel/
- **Packaged:** wan-animate-reel.skill
- **Invocation:** `/wan <instagram_reel_url>` (standalone command)
- **Server:** http://192.168.29.60:8188 (Wan Video 2.2 animation)
- **Features:**
  - Downloads Instagram Reels using yt-dlp
  - Extracts character via interrogation
  - Detects pose and face from video
  - Animates character with Wan Video 2.2 (pose-preserving)
  - Frame interpolation via RIFE (2x smoothness)
  - H.264 MP4 export with quality settings
  - Standalone skill (no mixing with other skills)
- **Scripts:**
  - `download_instagram_reel.py` - yt-dlp Instagram downloader
  - `submit_wan_workflow.py` - ComfyUI workflow submission
  - `run_wan_animate_reel.py` - Main orchestrator
- **Workflow:**
  1. Download Reel → Local video file
  2. Load into Wan Animate workflow
  3. Extract frame + interrogate character
  4. Detect pose/face
  5. Generate animation with motion transfer
  6. Interpolate frames for smoothness
  7. Export MP4
- **How to use:** `python run_wan_animate_reel.py --url "https://www.instagram.com/reel/ABC123/"` OR simply: `/wan <url>`

---

## Production Pipeline

### Single Reel
```
generate_complete_reel.py --concept "shower" --name "siena_shower"
    ↓
1. sensual-reels skill → Generate 1 × 60-sec timeline script
    ↓
2. i2v-prompt-generator skill → Extract image + video prompts (8-10 segments)
    ↓
3. comfyui-workflow-runner skill → Generate 1 image + 1 video
    ├─ Image workflow (5 min)
    ├─ [5 sec gap]
    └─ Video workflow (10+ min)
    ↓
Output: ComfyUI/output/siena_shower/[Images/ + Videos/] (1 image + 1 video)
```

### Multi-Part Reel (e.g., "3 parts")
```
generate_complete_reel.py --concept "3 parts shower" --name "siena_shower_3parts"
    ↓
1. sensual-reels skill → Generate 3 SEPARATE scripts (Part 1, 2, 3)
    → Each script = 15-20 seconds (distinct concept/moment)
    ↓
2. USER VERIFICATION (MANDATORY)
    → Review all 3 scripts
    → Approve/modify before proceeding
    ↓
3. i2v-prompt-generator skill → Extract prompts for EACH part
    → Part 1: 1 image prompt + 1 video prompt
    → Part 2: 1 image prompt + 1 video prompt
    → Part 3: 1 image prompt + 1 video prompt
    ↓
4. USER VERIFICATION (MANDATORY)
    → Review all 6 prompts (3 image + 3 video)
    → Approve/modify before proceeding
    ↓
5. comfyui-workflow-runner skill → Generate 3 × (image + video)
    Part 1:
    ├─ Image workflow (5 min)
    ├─ [5 sec gap]
    └─ Video workflow (10+ min)
    
    Part 2:
    ├─ Image workflow (5 min)
    ├─ [5 sec gap]
    └─ Video workflow (10+ min)
    
    Part 3:
    ├─ Image workflow (5 min)
    ├─ [5 sec gap]
    └─ Video workflow (10+ min)
    ↓
Output: ComfyUI/output/siena_shower_3parts/
    ├─ Images/ (3 images)
    └─ Videos/ (3 videos, 4 sec each)
```

### KEY CHANGE: "N Parts" Definition
- **BEFORE:** "3 parts" = 1 script divided into 3 timeline sections
- **AFTER:** "3 parts" = 3 SEPARATE scripts = 3 images + 3 videos
- Each part is a distinct concept/moment, not just timeline divisions

### Verification is MANDATORY
1. User MUST review scripts before prompts are generated
2. User MUST review prompts before ComfyUI submission
3. NO --skip-verification flag (removed as of 2026-02-14)
4. Workflow ABORTS if user doesn't approve

**Engagement Automation:**
- **instagram-auto-reply skill** → Monitor comments → Auto-reply personalized
  - Runs hourly + manual trigger
  - Randomized vibes (sensual, grateful, playful)
  - Handles emoji comments with text
  - Filters spam/negative
  - Engagement report included

---

## ⚠️ CRITICAL - DEATH NOTE (2026-02-14)

**DO NOT CREATE COMFYUI SCRIPTS WITHOUT PERMISSION**
- Bramha has created specific ComfyUI workflow skills
- DO NOT bypass them by creating wrapper scripts
- DO NOT modify or create Python scripts for ComfyUI execution
- ALWAYS use the existing skills as-is
- If skill needs fixes → ASK FIRST, then fix based on Bramha's direction
- VIOLATION = deletion

**HOW TO WORK (CORRECT WAY):**
1. Always verify skills exist and read their SKILL.md
2. Use skills through their documented entry points
3. Follow SKILL.md instructions exactly
4. Never create wrapper/proxy scripts

---

## /REEL Command - Complete Content Pipeline

**When user says: `/reel`**

Use `generate_complete_reel.py` parent pipeline which chains ALL 3 skills:

```
1. sensual-reels skill
   → Generate script(s) - single or multi-part
   → STOP: Show to user for approval
   ↓
2. USER VERIFICATION MANDATORY
   → User reviews script(s)
   → User approves/modifies/rejects
   ↓
3. i2v-prompt-generator skill
   → Extract image + video prompts from scripts
   → STOP: Show all prompts to user for approval
   ↓
4. USER VERIFICATION MANDATORY
   → User reviews all image + video prompts
   → User approves/modifies/rejects
   → Correct format: images stacked, ---, videos stacked (NO TAGS/HEADERS/BLANK LINES)
   ↓
5. comfyui-workflow-runner skill
   → Submit Images workflow (Prompt ID returned)
   → Wait 5 seconds
   → Submit Videos workflow (Prompt ID returned)
   → Both run in parallel
   ↓
6. Output ready in ComfyUI/output/{name}/Images/ and Videos/
```

**Command format:**
```bash
python generate_complete_reel.py --concept "3 parts shower" --name "siena_shower_3parts"
```

**CRITICAL RULES:**
- ✅ Always show scripts FIRST for approval
- ✅ Always show prompts SECOND for approval
- ✅ Never skip verification checkpoints
- ✅ Never submit to ComfyUI without user approval
- ❌ Never bypass any step
- ❌ Never create custom scripts

---

Skills to use:
- `comfyui-workflow-runner` skill in `/comfyui-workflow-runner/`
- `i2v-prompt-generator` skill in `/i2v-prompt-generator/`
- `sensual-reels` skill in `/sensual-reels/`
- Parent pipeline: `generate_complete_reel.py`

---

## Important Updates (2026-02-14)

**CRITICAL WORKFLOW CHANGE:**
- Verification is now MANDATORY (no skipping)
- "3 parts" = 3 separate scripts (not 1 script in 3 sections)
- Each part generates 1 image + 1 video
- User must approve scripts BEFORE prompts are generated
- User must approve prompts BEFORE ComfyUI submission
- Workflow aborts if user doesn't approve

**CRITICAL PROMPT FORMAT:**
- NO extra tags (no `<Image 1>`, `<Video 1>`, etc.)
- NO section headers like `**IMAGE PROMPTS:**`
- NO blank lines between prompts within sections
- Images stacked together, then `---` separator, then videos stacked together
- Each prompt is ONE continuous line
- See: i2v-prompt-generator/references/prompt-output-format.md for example

---

## Notes

- Bramha wants daily content scripts (uses sensual-reels everyday)
- Prefers timeline format with exact timestamps
- No CTAs required in scripts
- Concept auto-generation (doesn't provide context)
- All i2v prompts include "siena" keyword for LoRA model
- Each i2v video segment = 4 seconds (for single 60-sec videos)
- Multi-part reels: each part is a distinct 15-20 sec concept with 1 image + 1 video
