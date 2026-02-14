# ComfyUI Workflow Runner Skill

Run ComfyUI workflows with dynamic input substitution.

## Setup

1. **Clone the ComfyUI repo** (read-only):
   ```bash
   git clone https://github.com/mohitsoni48/comfy-wf.git
   ```

2. **Ensure ComfyUI server is running** at `http://192.168.29.60:8188`

## Usage

### Option 1: Images Only

```bash
python run_image_workflow.py [--name NAME] [--prompts PROMPTS]
```

**Example:**
```bash
python run_image_workflow.py --name "test" --prompts "Siena is standing in rain"
```

**Parameters:**
- `--name` (optional): Name/prefix for output files (default: "test")
- `--prompts` (optional): Image generation prompts (default: "Siena is standing in rain")

**Output:**
- Images saved to: `ComfyUI/output/{name}/Images/{index}.png`

---

### Option 2: Videos Only

```bash
python run_video_workflow.py [--name NAME] [--prompts PROMPTS]
```

**Example:**
```bash
python run_video_workflow.py --name "test" --prompts "Direct eye contact, confident sensual expression"
```

**Parameters:**
- `--name` (optional): Name/prefix for output files (default: "test")
- `--prompts` (optional): Video generation prompts (default: "Direct eye contact...")

**What happens:**
1. Loads pre-generated images from `ComfyUI/output/{name}/Images/`
2. Converts images to video with motion effects
3. Outputs MP4 video file

**Output:**
- Videos saved to: `ComfyUI/output/{name}/Videos/{index}.mp4`

---

### Option 3: Images + Videos (Dual Run) ⭐ **RECOMMENDED**

```bash
python run_dual_workflow.py [--name NAME] [--image-prompts PROMPTS] [--video-prompts PROMPTS]
```

**Example:**
```bash
python run_dual_workflow.py \
  --name "siena_rain" \
  --image-prompts "Siena is standing in rain" \
  --video-prompts "Direct eye contact, confident sensual expression"
```

**Parameters:**
- `--name` (optional): Name/prefix for output files (default: "test")
- `--image-prompts` (optional): Image generation prompts
- `--video-prompts` (optional): Video generation prompts

**Workflow:**
1. Submit Images workflow
2. Wait 5 seconds
3. Submit Videos workflow
4. Both run in parallel

**Output:**
- Images: `ComfyUI/output/{name}/Images/`
- Videos: `ComfyUI/output/{name}/Videos/`

## Workflow Architecture

### Images Workflow

```
Node 443 (Image Prompts)
    ↓
Node 442 (CreaPrompt List) → Node 444 (StringFromList)
    ↓
Node 505 (For Loop Start) → Node 507 (StringFromList per iteration)
    ↓
Node 499 (Custom Image Generation Pipeline)
    ├─ Qwen Image CLIP: Text encoding
    ├─ Lumina2 CLIP: Additional encoding
    ├─ Z-Image Turbo: Image generation
    ├─ LoRA loaders: Style/detail enhancement
    └─ VAE Decode: Final image output
    ↓
Node 509 (For Loop End) → Batch all generated images
    ↓
Output saved with Node 500 (Name) prefix
```

### Videos Workflow

```
Node 436 (Video Prompts)
    ↓
Node 438 (CreaPrompt List) → Node 439/440 (StringFromList)
    ↓
Node 516 (Load Images For Loop)
    ├─ Reads from: ComfyUI/output/{name}/Images/
    ├─ Loops per image
    └─ Applies video prompts via Node 394:394 (Text Concatenate)
    ↓
Node 394:21 (WanImageToVideo)
    └─ Converts image to 4-second video clip
    ↓
Node 394:16 (RIFE VFI)
    └─ Frame interpolation (2x frames for smoothness)
    ↓
Node 19 (VHS_VideoCombine)
    └─ Combines all clips into final MP4
    ↓
Output saved with Node 500 (Name) prefix
```

## Key Nodes

| Node ID | Type | Purpose | Modifiable |
|---------|------|---------|-----------|
| **443** | PrimitiveStringMultiline | Image prompts | ✅ Yes |
| **436** | PrimitiveStringMultiline | Video prompts | ✅ Yes |
| **500** | PrimitiveStringMultiline | Output name/prefix | ✅ Yes |
| 442/438 | CreaPrompt List | Multiline prompt processor | No |
| 505-509 | easy forLoop* | Batch iteration (images) | No |
| 516 | easy loadImagesForLoop | Batch iteration (videos) | No |
| 499:* | Custom pipeline | Image generation | No |
| 394:* | Custom pipeline | Video generation (Wan2.2, RIFE) | No |

## Status

- ✅ Image generation fully working
- ✅ Video generation fully working
- ✅ Dual-run orchestration working (5-sec gap)
- ⏳ Real-time progress polling (future enhancement)

## File Locations

- Workflows: `C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw/`
  - `Images_workflow.json` - Image generation workflow
  - `Videos_workflow.json` - Video generation workflow
- Scripts: `C:\Users\mohit\.openclaw\workspace/`
  - `run_image_workflow.py` - Image generation
  - `run_video_workflow.py` - Video generation
  - `run_dual_workflow.py` - Orchestrator (recommended)
  - `generate_complete_reel.py` - Master orchestrator with verification
- Git repo: `C:\Users\mohit\.openclaw\workspace\comfy-wf/` (read-only)
- Server: `http://192.168.29.60:8188`

## Master Orchestrator with Verification ⭐ CRITICAL WORKFLOW

**New in production:** `generate_complete_reel.py` chains everything together WITH USER VERIFICATION:

```
Script Generation 
    ↓
[USER VERIFICATION] ← Script shown, waiting for approval/changes
    ↓
I2V Prompt Extraction
    ↓
[USER VERIFICATION] ← Image + Video prompts shown, waiting for approval/changes
    ↓
ComfyUI Dual Workflows (only after approval)
```

**Single Command for Complete Reel:**
```bash
python generate_complete_reel.py --concept "rain" --name "siena_rain_reel"
```

**Parameters:**
- `--concept` (optional): Content concept for script (default: "rain")
- `--name` (optional): Output directory name (default: "siena_reel")
- `--image-prompts` (optional): Skip verification, use provided prompts
- `--video-prompts` (optional): Skip verification, use provided prompts

**Workflow (WITH VERIFICATION):**

1. **STEP 1: Script Generation**
   - Calls sensual-reels skill → Generates 60-sec timeline script
   - Shows script to user
   - User reviews and confirms (Y/N, or provides feedback)
   - If changes needed: Return to sensual-reels or accept edited version

2. **STEP 2: Script Verification Checkpoint**
   - Script displayed in full
   - User must approve before proceeding
   - User can request modifications or regeneration
   - Only on approval: continue to Step 3

3. **STEP 3: Prompt Extraction**
   - Calls i2v-prompt-generator → Extracts image + video prompts from script
   - Creates detailed image prompts (3-10 segments based on script)
   - Creates detailed video prompts (motion-heavy, no cross-refs, standalone)

4. **STEP 4: Prompt Verification Checkpoint**
   - All image prompts displayed in full
   - All video prompts displayed in full
   - User must approve before submitting
   - User can request modifications:
     - More motion detail
     - Different lighting specs
     - Pose adjustments
     - Standalone vs cross-ref fixes
   - Only on approval: continue to Step 5

5. **STEP 5: ComfyUI Submission**
   - Submits to ComfyUI dual workflows (replaces old WhatsApp send)
   - Images workflow submitted first
   - 5-second gap
   - Videos workflow submitted second
   - Both run in parallel
   - Outputs ready in ComfyUI/output/{name}/

**Verification Checkpoint Format:**

```
====================================================================
SCRIPT VERIFICATION CHECKPOINT
====================================================================
[FULL SCRIPT DISPLAYED HERE]

APPROVE? (yes/no/modify)
```

```
====================================================================
PROMPT VERIFICATION CHECKPOINT
====================================================================

IMAGE PROMPTS (total: 3):
[Image 1 full prompt]
[Image 2 full prompt]
[Image 3 full prompt]

VIDEO PROMPTS (total: 3):
[Video 1 full prompt]
[Video 2 full prompt]
[Video 3 full prompt]

APPROVE? (yes/no/modify)
```

**CRITICAL RULES:**
- ❌ Never submit to ComfyUI without user verification
- ❌ Never skip script review checkpoint
- ❌ Never skip prompt review checkpoint
- ✅ Always show full scripts/prompts before proceeding
- ✅ Always wait for explicit user approval
- ✅ Always allow modifications before submission

---

## Direct Script Examples

### Generate images only
```bash
python run_image_workflow.py --name "robe_test" --prompts "Siena wearing burgundy robe"
```

### Generate videos from existing images
```bash
python run_video_workflow.py --name "robe_test" --prompts "Sensual slow motion, confident gaze"
```

### Images + Videos separately
```bash
python run_dual_workflow.py \
  --name "valentine_reel" \
  --image-prompts "Siena in red dress, romantic Valentine setting" \
  --video-prompts "Direct eye contact, sensual slow motion, romantic energy"
```

Monitor both in ComfyUI UI. Videos will be ready after images complete.
