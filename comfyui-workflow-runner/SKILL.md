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

- Workflows: `C:\Users\mohit\.openclaw\workspace\openclaw/`
- Scripts: `C:\Users\mohit\.openclaw\workspace/`
  - `run_image_workflow.py` - Image generation
  - `run_video_workflow.py` - Video generation
  - `run_dual_workflow.py` - Orchestrator (recommended)
- Git repo: `C:\Users\mohit\.openclaw\workspace\comfy-wf/` (read-only)
- Server: `http://192.168.29.60:8188`

## Master Orchestrator

**New in production:** `generate_complete_reel.py` chains everything together:

```
Script Generation → I2V Prompt Extraction → ComfyUI Workflows
(sensual-reels)    (i2v-prompt-generator)   (comfyui-runner)
```

**Single Command for Complete Reel:**
```bash
python generate_complete_reel.py --concept "rain" --name "siena_rain_reel"
```

**Parameters:**
- `--concept` (optional): Content concept for script (default: "rain")
- `--name` (optional): Output directory name (default: "siena_reel")
- `--image-prompts` (optional): Override image prompts (skip generator)
- `--video-prompts` (optional): Override video prompts (skip generator)

**What it does:**
1. Calls sensual-reels skill → Generates 60-sec timeline script
2. Calls i2v-prompt-generator → Extracts image + video prompts from script
3. Submits to ComfyUI dual workflows (replaces old WhatsApp send)
4. Images generated first, videos follow with 5-sec gap
5. Outputs ready in ComfyUI/output/{name}/

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
