# Wan Animate Reel Skill

Download Instagram Reels and animate them with Wan Video character motion transfer.

## Setup

1. **Ensure ComfyUI server is running** at `http://192.168.29.60:8188`

2. **Install dependencies** (yt-dlp for Instagram downloads):
   ```bash
   pip install yt-dlp
   ```

3. **ComfyUI must have Wan Video models loaded**
   - Workflow references: `C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Wan Animate character replacement V3 API.json`

## Usage

### Download Instagram Reel & Animate

```bash
python run_wan_animate_reel.py --url "https://www.instagram.com/reel/ABC123def456/"
```

**Parameters:**
- `--url` (required): Full Instagram Reel URL

**What happens:**
1. Downloads Reel video to `./downloads/` locally
2. Uploads video to ComfyUI server via `/upload/image` endpoint
3. Submits Wan Animate workflow with uploaded video filename
4. Extracts first frame and interrogates character
5. Generates new animated video with motion transfer
6. Outputs to ComfyUI's output directory

**Output:**
- Video saved to ComfyUI output folder (path shown after completion)

---

## Workflow Architecture

### Wan Animate Character Replacement V3 API

**Input:**
- Base video file (extracted from Instagram Reel)

**Processing Pipeline:**

```
Load Video (Node 194)
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
- **Node 194** → Input video path (from Instagram download)

**Everything else:** Pre-configured and locked (Siena character, motion transfer, output settings)

## Status

- ✅ Instagram Reel downloader (yt-dlp)
- ✅ ComfyUI workflow submission
- ✅ Motion transfer + character animation
- ✅ Frame interpolation for smoothness
- ⏳ Real-time progress polling (future enhancement)

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
