# Wan Animate Reel Skill

**Download Instagram Reels and animate them with Wan Video character motion transfer.**

Complete workflow: Instagram URL → Download → Upload to ComfyUI → Animate → Output video

## ⚠️ IMPORTANT - NOT REEL WORKFLOWS

**This skill uses WAN ANIMATE WORKFLOWS (not Reel workflows):**
- `Wan Animate character replacement V3 - Image API.json` - Extracts character
- `Wan Animate character replacement V3 - Video API.json` - Animates with motion transfer
- **Key Node:** Node 254 "Conept Name" (PrimitiveString)

**Critical Naming Rule:**
- Image API: Node 254 = UUID (plain, no suffix)
- Video API: Node 254 = UUID + "_00001_" (with suffix)
- Example: `bdd183a2-00c2-44ea-8e8a-25af0941fc96` vs `bdd183a2-00c2-44ea-8e8a-25af0941fc96_00001_`
- This is DIFFERENT from Reel workflows (which use same Node 500 for both)

**DO NOT apply Reel workflow Node 500 logic here.**

## Setup

1. **ComfyUI server must be running** at `http://192.168.29.60:8188`
   - Ensure Wan Video 2.2 models are loaded
   - Server must be accessible from this machine

2. **Install dependencies** (if not already installed):
   ```bash
   pip install yt-dlp
   ```

3. **Workflow files** (read-only reference):
   ```
   Image API:
   C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Wan Animate character replacement V3 - Image API.json
   
   Video API:
   C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Wan Animate character replacement V3 - Video API.json
   ```

## Usage

### Download Instagram Reel & Animate (Dual Workflows)

```bash
python run_wan_animate_reel.py --url "https://www.instagram.com/reel/ABC123def456/"
```

**Parameters:**
- `--url` (required): Full Instagram Reel URL

**Output Naming:**
- Each run generates a unique UUID automatically
- **Image output:** Node 254 set to `{uuid}` → Output: `{uuid}_00001_.png`
- **Video output:** Node 254 set to `{uuid}_00001_` → Output: `{uuid}_00001__00001_.mp4`
- Example UUID: `bdd183a2-00c2-44ea-8e8a-25af0941fc96`
  - Image: `bdd183a2-00c2-44ea-8e8a-25af0941fc96_00001_.png`
  - Video: `bdd183a2-00c2-44ea-8e8a-25af0941fc96_00001__00001_.mp4`

**Execution Steps:**

```
0. GENERATE RUN ID
   └─ Create random UUID for this run
   └─ Used as output prefix for consistency

1. DOWNLOAD
   └─ Instagram Reel → Local MP4 file (./downloads/)

2. UPLOAD
   └─ Local MP4 → ComfyUI /upload/image endpoint
   └─ Returns: Filename for both workflows

3. SUBMIT IMAGE API WORKFLOW
   └─ Image API workflow + video + UUID → ComfyUI /prompt endpoint
   └─ Sets Node 254 "Conept Name" to UUID (plain)
   └─ Example: Node 254 = "bdd183a2-00c2-44ea-8e8a-25af0941fc96"
   └─ Returns: Image Prompt ID

4. WAIT 5 SECONDS
   └─ Delay before video workflow submission

5. SUBMIT VIDEO API WORKFLOW
   └─ Video API workflow + video + UUID_00001_ → ComfyUI /prompt endpoint
   └─ Sets Node 254 "Conept Name" to UUID_00001_
   └─ Example: Node 254 = "bdd183a2-00c2-44ea-8e8a-25af0941fc96_00001_"
   └─ Returns: Video Prompt ID
   └─ Both workflows now running in parallel on ComfyUI

6. PROCESS (ComfyUI processes both in parallel)
   IMAGE PIPELINE:
   └─ Load video → Extract frame
   └─ Interrogate character
   └─ Detect pose + face
   └─ Generate character image
   
   VIDEO PIPELINE (starts 5s later):
   └─ Load video
   └─ Transfer animation from generated character
   └─ Interpolate frames (RIFE 2x smoothness)
   └─ Export MP4

7. OUTPUT
   └─ Generated image + animated video saved to ComfyUI output directory
```

**Output Location:**
- Video saved to: `D:\ComfyUI_windows_portable\ComfyUI\output\Animate\` (or configured output dir)
- Filename: Based on workflow settings (Node 118 prefix)

**Monitoring:**
- ComfyUI UI: `http://192.168.29.60:8188` (watch real-time progress)

---

## Workflow Architecture

### Wan Animate Character Replacement V3 - Image API

**Input:**
- `video`: Video filename (uploaded to ComfyUI via /upload/image endpoint)
- `name`: Name/prefix for output

**Processing Pipeline:**

```
Load Video
    ↓
Extract First Frame
    ├─ Resize to 544x960
    └─ Detect pose + face
    ↓
Interrogate Character
    └─ Creates description of who's in frame
    ↓
Generate New Character Image
    ├─ Qwen CLIP encoding
    ├─ Z-Image Turbo generation
    └─ Custom LoRAs applied
    ↓
Save Character Image
    └─ Output image with {name} prefix
```

### Wan Animate Character Replacement V3 - Video API

**Input:**
- `video`: Video filename (same as Image API)
- `name`: Name/prefix for output (same as Image API)

**Processing Pipeline:**

```
Load Video + Generated Character Image
    ↓
Extract Pose + Face from Original Video
    ↓
Encode Character for Animation
    ├─ CLIP Vision embedding
    ├─ Pose embedding (from detected pose)
    └─ Face embedding (from face detection)
    ↓
Wan Video Sampler
    ├─ Model: Wan2.2-Animate-14B-Q6_K.gguf
    ├─ Uses pose + face constraints
    └─ Generates animation frames
    ↓
Decode & Interpolate
    ├─ VAE Decode animation
    └─ RIFE frame interpolation (2x smoothness)
    ↓
Video Export
    └─ MP4 output with H.264 codec
```

**Workflow Execution:**
1. **Image API submits first** → Processes character extraction (takes ~2-5 minutes)
2. **Wait 5 seconds** → Ensures image generation has started
3. **Video API submits second** → Will use generated character image once available
4. **Both run in parallel** on ComfyUI (they don't block each other)

## Key Nodes (Read-Only Reference)

**Both workflows accept dynamic inputs:**
- `video`: Video filename (from ComfyUI upload response)
- `name`: Output name/prefix (auto-generated if not provided)

**Image API Pipeline:**
- Extracts character from first video frame
- Generates character image (for use in Video API)

**Video API Pipeline:**
- Uses extracted character for motion transfer
- Animates with pose-preserving constraints
- Exports MP4 with frame interpolation

**Everything else:** Pre-configured and locked (motion transfer, output settings, interpolation)

## Status

- ✅ Instagram Reel downloader (yt-dlp)
- ✅ ComfyUI video upload handler (/upload/image)
- ✅ Dual workflow support (Image API + Video API)
- ✅ Dynamic node input modification (video + name parameters)
- ✅ 5-second staggered submission
- ✅ Parallel workflow execution on ComfyUI
- ✅ Character extraction + motion transfer
- ✅ Frame interpolation for smoothness
- ✅ Real-time monitoring via ComfyUI UI

## File Locations

- **Workflows** (read-only):
  - Image API: `C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Wan Animate character replacement V3 - Image API.json`
  - Video API: `C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Wan Animate character replacement V3 - Video API.json`
- **Scripts**: `C:\Users\mohit\.openclaw\workspace\skills\wan-animate-reel\scripts\`
  - `run_wan_animate_reel.py` - Main orchestrator
  - `download_instagram_reel.py` - Instagram downloader
  - `submit_wan_workflow.py` - ComfyUI dual-workflow submission
- **Downloads**: `C:\Users\mohit\.openclaw\workspace\skills\wan-animate-reel\downloads\`
- **Server**: `http://192.168.29.60:8188`

## Direct Examples

### Download & animate (UUID auto-generated)
```bash
python run_wan_animate_reel.py --url "https://www.instagram.com/reel/ABC123def456/"
```

**Output will be:**
- Run ID: `bdd183a2-00c2-44ea-8e8a-25af0941fc96` (example)
- Image output: `bdd183a2-00c2-44ea-8e8a-25af0941fc96_00001_.png`
- Video output: `bdd183a2-00c2-44ea-8e8a-25af0941fc96_00001__00001_.mp4`

**Naming explanation:**
- Image uses Node 254 = UUID (plain)
- Video uses Node 254 = UUID + "_00001_" suffix (for proper output naming)

### Check download directory
```bash
Get-ChildItem scripts/../downloads/
```

## Invocation

**When user says:** `/wan <url>` or `wan <url>`

This skill activates. No mixing with other skills.

---

_Standalone Wan Animate Reel processor. Instagram → Motion Transfer → Video._
