# MEMORY.md - Long-Term Memory

*Curated memories. The important stuff.*

---

## Bramha (Mohit Soni)

- Goes by **Bramha** | Timezone: GMT+5:30 (India)
- Instagram: @desire.siena (sensual modeling content)
- First contact: 2026-02-13 | Windows OS user
- **Active:** Instagram Reels (20-60s), daily scripts, target audience 18-35 male
- **Preferences:** Hot & revealing (8-9/10 intensity), timeline format, no CTAs, specific timed actions

---

## Skills Overview

| Skill | Location | Purpose |
|-------|----------|---------|
| **sensual-reels** | `/sensual-reels/` | Generates 60s timeline scripts (progressive narrative, specific actions) |
| **i2v-prompt-generator** | `/i2v-prompt-generator/` | Extracts image + video prompts from scripts (8-10 segments, includes "siena" LoRA keyword) |
| **comfyui-workflow-runner** | `/comfyui-workflow-runner/` | Dual workflow submission to ComfyUI (Image + Video, 5s gap, locked sequence) |
| **wan-animate-reel** | `/skills/wan-animate-reel/` | Downloads Instagram Reels, applies Wan Animate motion transfer (UUID naming, Node 254) |
| **instagram-auto-reply** | `/instagram-auto-reply/` | Auto-replies to comments (hourly + manual, randomized vibes) |

---

## FakeLocation App - COMPLETE (2026-02-18)

**PROJECT STATUS: ✅ 100% COMPLETE - BUILD VERIFIED & SUCCESSFUL**

**All 10 Tasks Delivered:**
- T1: DirectionsService ✅ | T2: PolylineInterpolator ✅
- T3: RouteSimulatorService ✅ | T4: RouteConfigurationScreen ✅
- T5: SimulationMapScreen ✅ | T6-T8: RouteHistory & Persistence ✅
- T7: RouteSimulationState ✅ | T9: ToastManager ✅
- T10: CreditTracker ✅ | T11: ViewModel Integration ✅

**Build Output:**
- Debug: `app-debug.apk` ✅
- Release: `app-release-unsigned.apk` ✅
- Zero compilation errors after 3 targeted fixes

**Branch:** t11-viewmodel-integration (ready for merge to main)

**Next:** Device deployment & E2E testing

---

## /REEL Command Pipeline (LOCKED)

**When user says `/reel`:**

1. ✅ sensual-reels skill → Generate script(s) → SHOW FOR APPROVAL
2. ✅ USER VERIFICATION → Review & approve/modify scripts
3. ✅ i2v-prompt-generator skill → Extract prompts → SHOW FOR APPROVAL
4. ✅ USER VERIFICATION → Review & approve prompts (format: images stacked, `---`, videos stacked, NO TAGS/HEADERS)
5. ✅ comfyui-workflow-runner skill → Submit Image → Wait 5s → Submit Video → Parallel execution
6. ✅ Output in ComfyUI/output/{name}/

**Format for ComfyUI:**
```bash
python submit_dual_workflow.py \
  --name "siena_concept_name" \
  --image-prompts "prompt1\nprompt2\n..." \
  --video-prompts "prompt1\nprompt2\n..." \
  --seconds 6
```

**Critical Rules:**
- ✅ Always show scripts & prompts for approval
- ✅ Pass prompts as newline-separated strings  
- ✅ Use submit_dual_workflow.py (generic, never create reel-specific scripts)
- ❌ Never skip verification | Never mix Node 254 logic into Node 500 | Never reverse workflow order

---

## Workflow Preference: Detailed Descriptions (2026-02-16)

**If Bramha sends detailed visual description in reel context:**
- Treat as **FIRST IMAGE PROMPT** (skip sensual-reels)
- Proceed to i2v-prompt-generator with description as base
- Generate remaining prompts (video for that segment + additional images/videos if multi-part)
- Allows fast-track when Bramha has specific visual direction

---

## Key Workflow Distinctions

### System A: Wan Animate (wan-animate-reel skill)
- **Node:** 254 "Concept Name" (PrimitiveString)
- **Naming:** Image = UUID plain | Video = UUID_00001_ (with suffix)
- **Output:** `{uuid}_00001_.png` + `{uuid}_00001__00001_.mp4`
- **Use:** Downloaded Instagram Reels with motion transfer

### System B: Reel Generation (comfyui-workflow-runner skill)
- **Nodes:** Image (443) + Video (436), both use Node 500 for output name
- **Rule:** Node 500 IDENTICAL for both workflows
- **Output:** `{name}_00001_.png` + `{name}_00001_.mp4`
- **Use:** Generated content from scripts

⚠️ **NEVER mix these patterns — they are completely different.**

---

## Recent Skill Improvements (2026-02-14)

**sensual-reels:** Complete rebuild focused on NARRATIVE PROGRESSION
- Added `narrative-progression.md` guide
- Rebuilt `sensual-patterns.md` (Setup → Progression → Climax → Finale)
- Specific 60s breakdown: Hook [0-2s], First Reveal [2-8s], Escalation [8-25s], Peak [25-45s], Engagement [45-55s], Exit [55-60s]
- Script checklist validates 20+ quality gates
- Result: Fast, engaging, progressive scripts (not vague filler)

**i2v-prompt-generator:** Updated for fast/aggressive pacing
- Removed "slow/gentle/subtle" language
- Added "QUICK/FAST/INTENSE/COMMANDING" focus
- 8 aggressive prompt examples
- Video prompts escalate to match script intensity
- Result: Fast, intense videos matched to scripts

---

## Multi-Part Reels

**"3 parts" = 3 SEPARATE scripts (not 1 script in 3 sections)**
- Each part: 15-20s distinct concept
- Each part: 1 image + 1 video
- User verification MANDATORY after scripts AND after prompts
- Workflow aborts if user doesn't approve

---

## Network Access

**ComfyUI Output:** `\\192.168.29.60\output\`
- Read/Write access ✅
- Structure: siena_luxury_lingerie/ | LoraNew/ | ComfyUI/ | Animate/
- SMB network share (direct file access)

---

## Constraints & Critical Rules

⚠️ **DEATH NOTE:**
- DO NOT create ComfyUI scripts without permission
- Always use existing skills (read SKILL.md first)
- If skill needs fixes → ASK FIRST
- VIOLATION = deletion

⚠️ **Reel Generation Rules:**
- Verification is MANDATORY (no skip-verification flag)
- Prompt format: NO extra tags, NO headers, NO blank lines within sections
- Images stacked → `---` → Videos stacked (each prompt = ONE line)
- See: i2v-prompt-generator/references/prompt-output-format.md

⚠️ **ComfyUI Workflow (System B):**
- Image Workflow FIRST, Video Workflow SECOND (5s gap, NEVER reverse)
- Node 500 identical for both
- Video gets --seconds parameter (default 6)

---

## Notes

- Concept auto-generation (no context needed)
- i2v video segment = 4s (single 60s video) | 1-2s (multi-part)
- All prompts include "siena" keyword (LoRA model)
- Timeline format with exact timestamps preferred
- Generated content for Instagram posting via network share
