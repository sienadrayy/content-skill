# Wan Animate Reel Skill

**Download Instagram Reels and animate them with Wan Video character motion transfer.**

Complete workflow: Instagram URL → Download → Upload to ComfyUI → Animate → Output video

## Setup

1. **ComfyUI server must be running** at `http://192.168.29.60:8188`
   - Ensure Wan Video 2.2 models are loaded
   - Server must be accessible from this machine

2. **Install dependencies** (if not already installed):
   ```bash
   pip install yt-dlp
   ```

3. **Workflow file** (read-only reference):
   ```
   C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Wan Animate character replacement V3 API.json
   ```

## Usage

### Download Instagram Reel & Animate

```bash
python run_wan_animate_reel.py --url "https://www.instagram.com/reel/ABC123def456/"
```

**Parameters:**
- `--url` (required): Full Instagram Reel URL

**Execution Steps:**

```
1. DOWNLOAD
   └─ Instagram Reel → Local MP4 file (./downloads/)

2. UPLOAD
   └─ Local MP4 → ComfyUI /upload/image endpoint
   └─ Returns: Filename for workflow

3. SUBMIT
   └─ Workflow + uploaded filename → ComfyUI /prompt endpoint
   └─ Returns: Prompt ID for tracking

4. ANIMATE (ComfyUI processes)
   └─ Load video → Extract frame
   └─ Interrogate character
   └─ Detect pose + face
   └─ Generate animation with motion transfer
   └─ Interpolate frames (RIFE 2x smoothness)
   └─ Export MP4

5. OUTPUT
   └─ Animated video saved to ComfyUI output directory
```

**Output Location:**
- Video saved to: `D:\ComfyUI_windows_portable\ComfyUI\output\Animate\` (or configured output dir)
- Filename: Based on workflow settings (Node 118 prefix)

**Monitoring:**
- ComfyUI UI: `http://192.168.29.60:8188` (watch real-time progress)

---

## Workflow Architecture

### Wan Animate Character Replacement V3 API

**Input:**
- Video filename (uploaded to ComfyUI via /upload/image endpoint)

**Processing Pipeline:**

```
Load Video (Node 218)
    ↓
Extract First Frame (Node 217)
    ├─ Resize to 544x960 (Node 123)
    └─ Detect pose + face (Node 148, 151)
    ↓
Interrogate Character (Node 197)
    └─ Creates description of who's in frame
    ↓
Generate New Character Image (Node 208-214)
    ├─ Qwen CLIP encoding
    ├─ Z-Image Turbo generation
    └─ Custom LoRAs applied
    ↓
Encode Character for Animation (Node 180)
    ├─ CLIP Vision embedding
    ├─ Pose embedding (from detected pose)
    └─ Face embedding (from face detection)
    ↓
Wan Video Sampler (Node 126)
    ├─ Model: Wan2.2-Animate-14B-Q6_K.gguf
    ├─ Uses pose + face constraints
    └─ Generates animation frames
    ↓
Decode & Interpolate (Node 131, 196)
    ├─ VAE Decode animation
    └─ RIFE frame interpolation (2x smoothness)
    ↓
Video Export (Node 118)
    └─ MP4 output with H.264 codec
```

## Key Nodes (Read-Only Reference)

| Node ID | Type | Purpose |
|---------|------|---------|
| **218** | VHS_LoadVideo | Input video path (runtime modified) |
| 217 | ImageFromBatch | Extract first frame |
| 123 | ImageResizeKJv2 | Resize to 544x960 |
| 148 | PoseAndFaceDetection | Detect body/face pose |
| 151 | DrawViTPose | Visualize pose skeleton |
| 197 | easy imageInterrogator | Describe character in frame |
| 208-214 | Custom pipeline | Generate new character image |
| 180 | WanVideoAnimateEmbeds | Create animation embeddings |
| 126 | WanVideoSampler | Generate video frames |
| 131 | WanVideoDecode | Decode latents to video |
| 196 | RIFE VFI | Frame interpolation (2x) |
| 118 | VHS_VideoCombine | Export MP4 |

## Workflow Flow

**What gets modified at runtime:**
- **Node 218** → Video filename (from ComfyUI upload response)

**Everything else:** Pre-configured and locked (Siena character, motion transfer, output settings)

**Runtime Sequence:**
1. Local video file downloaded
2. Uploaded to ComfyUI `/upload/image` endpoint
3. Returned filename inserted into Node 218
4. Workflow submitted to ComfyUI
5. ComfyUI processes entire animation pipeline
6. Output saved to configured directory

## Status

- ✅ Instagram Reel downloader (yt-dlp)
- ✅ ComfyUI video upload handler (/upload/image)
- ✅ Dynamic workflow node modification
- ✅ Workflow submission & execution
- ✅ Motion transfer + character animation
- ✅ Frame interpolation for smoothness
- ✅ Real-time monitoring via ComfyUI UI

## File Locations

- Workflow (read-only): `C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Wan Animate character replacement V3 API.json`
- Scripts: `C:\Users\mohit\.openclaw\workspace\wan-animate-reel\scripts\`
  - `run_wan_animate_reel.py` - Main orchestrator
  - `download_instagram_reel.py` - Instagram downloader
  - `submit_wan_workflow.py` - ComfyUI submission
- Downloads: `C:\Users\mohit\.openclaw\workspace\wan-animate-reel\downloads\`
- Server: `http://192.168.29.60:8188`

## Direct Examples

### Simple reel download & animate
```bash
python run_wan_animate_reel.py --url "https://www.instagram.com/reel/ABC123def456/"
```

### Check download directory
```bash
ls downloads/
```

## Invocation

**When user says:** `/wan <url>` or `wan <url>`

This skill activates. No mixing with other skills.

---

_Standalone Wan Animate Reel processor. Instagram → Motion Transfer → Video._
