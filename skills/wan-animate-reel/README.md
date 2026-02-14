# Wan Animate Reel Skill

**Standalone skill for downloading Instagram Reels and animating them with Wan Video character motion transfer.**

✅ **TESTED & WORKING** (2026-02-14)

## Quick Start

```bash
# Download a Reel and animate it
python scripts/run_wan_animate_reel.py --url "https://www.instagram.com/reel/ABC123def456/"
```

Or use the `/wan` command:
```
/wan https://www.instagram.com/reel/ABC123def456/
```

---

## What It Does

1. **Download** Instagram Reel (via yt-dlp) → MP4 file
2. **Upload** to ComfyUI server → Get filename reference
3. **Submit** Wan Animate workflow with uploaded video
4. **Interrogate** character from first frame
5. **Detect** pose and face from video → Motion skeleton
6. **Animate** using Wan Video 2.2 → Preserve character pose/motion
7. **Smooth** with RIFE frame interpolation → 2x frames
8. **Export** as H.264 MP4 → ComfyUI output folder

---

## File Structure

```
wan-animate-reel/
├── SKILL.md                          # Full documentation
├── README.md                          # This file
├── wan-animate-reel.skill            # Metadata + package info
├── scripts/
│   ├── run_wan_animate_reel.py       # Main orchestrator ⭐
│   ├── download_instagram_reel.py    # yt-dlp downloader
│   └── submit_wan_workflow.py        # ComfyUI submission
├── references/
│   └── wan-animate-workflow-guide.md # Detailed workflow breakdown
└── downloads/                        # (auto-created) Downloaded videos
```

---

## Scripts

### `run_wan_animate_reel.py` ⭐ Main Entry Point
```bash
python scripts/run_wan_animate_reel.py --url "<instagram_url>"
```

Orchestrates the complete workflow:
1. Download Instagram Reel
2. Call upload + submission handler
3. Report completion

### `download_instagram_reel.py`
```bash
python scripts/download_instagram_reel.py --url "<url>" --output-dir "downloads"
```

Uses yt-dlp to download Reel → Saves MP4 locally

### `submit_wan_workflow.py`
```bash
python scripts/submit_wan_workflow.py --video "downloads/reel_20260214_154000.mp4" --wait
```

Complete workflow:
1. **Upload** video to ComfyUI `/upload/image` endpoint
2. **Extract** filename from response
3. **Modify** Node 218 with uploaded filename
4. **Submit** workflow to ComfyUI `/prompt` endpoint
5. **Wait** for completion (with `--wait` flag)

---

## Requirements

- **Python 3.7+**
- **yt-dlp** (for Instagram downloads)
  ```bash
  pip install yt-dlp
  ```
- **ComfyUI server** running at `http://192.168.29.60:8188`
- **Wan Video 2.2 models** loaded in ComfyUI

---

## Key Differences from Other Skills

| Aspect | wan-animate-reel | comfyui-workflow-runner |
|--------|------------------|------------------------|
| **Input** | Instagram Reel URL | Prompts + video path |
| **Download** | Automatic (yt-dlp) | Manual (user provides) |
| **Workflow** | Wan Animate V3 API | Images or Videos |
| **Command** | `/wan <url>` | N/A (manual) |
| **Dependencies** | yt-dlp | None (stdlib) |
| **Invocation** | Standalone | Referenced for learning |

---

## Workflow Reference

The actual ComfyUI workflow is read from:
```
C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Wan Animate character replacement V3 API.json
```

**Read-only.** Only Node 194 (video path) is modified at runtime.

Full breakdown in: `references/wan-animate-workflow-guide.md`

---

## Example Run

```bash
C:\Users\mohit\.openclaw\workspace\wan-animate-reel> python scripts/run_wan_animate_reel.py --url "https://www.instagram.com/reel/DUqZ9pMjHzI/?igsh=YmE3M3A5dTFmM2w0"

============================================================
🎬 WAN ANIMATE REEL ORCHESTRATOR
============================================================
URL: https://www.instagram.com/reel/DUqZ9pMjHzI/?igsh=YmE3M3A5dTFmM2w0

📥 STEP 1: Download Instagram Reel
============================================================
📥 Downloading Instagram Reel...
   URL: https://www.instagram.com/reel/DUqZ9pMjHzI/?igsh=YmE3M3A5dTFmM2w0
   Output: downloads\reel_20260214_160235.mp4
✅ Download complete!
   File: downloads\reel_20260214_160235.mp4
   Size: 1.81 MB
✅ Downloaded: downloads\reel_20260214_160235.mp4

🎨 STEP 2: Submit to Wan Animate Workflow
============================================================

============================================================
STEP 1: Upload Video to ComfyUI
============================================================
📤 Uploading video to ComfyUI...
   File: downloads\reel_20260214_160235.mp4
✅ Upload complete!
   Filename: siena_DUqZ9pMjHzI_mp4

============================================================
STEP 2: Submit Workflow
============================================================
📤 Loading Wan Animate workflow...
🎬 Setting video filename: siena_DUqZ9pMjHzI_mp4
🔌 Connecting to ComfyUI at http://192.168.29.60:8188...
✅ ComfyUI server ready
📤 Submitting workflow to ComfyUI...
✅ Workflow submitted!
   Prompt ID: 8a7f3c2e-9d1b-4f6a-b2e5-1c9d3f7e4b2a

============================================================
STEP 3: Wait for Completion
============================================================
⏳ Waiting for workflow completion (timeout: 3600s)...
📊 Monitor progress at: http://192.168.29.60:8188
   Running... (system: 87.2% CPU)
   ...
   [ComfyUI processes animation pipeline]
   ...
✅ Workflow completed!

============================================================
🎉 COMPLETE!
============================================================
📹 Video file: downloads\reel_20260214_160235.mp4
🎬 Workflow: Wan Animate Character Replacement V3 API
📊 Monitor: http://192.168.29.60:8188

💡 Output video is in: D:\ComfyUI_windows_portable\ComfyUI\output\Animate\
```

---

## Troubleshooting

### "yt-dlp not found"
```bash
pip install yt-dlp
```

### "Cannot reach ComfyUI server"
- Check if ComfyUI is running: `http://192.168.29.60:8188`
- Check IP address: Should be `192.168.29.60`
- Check port: Should be `8188`

### "Video file not found"
- yt-dlp download may have failed
- Check `downloads/` directory
- Try downloading manually with: `yt-dlp -f best[ext=mp4] "<url>" -o "test.mp4"`

### "Workflow timeout"
- Wan Video 2.2 takes 15-20 min per video
- Monitor at: `http://192.168.29.60:8188`
- Increase timeout: `--timeout 5400` (90 minutes)

---

## Notes

- ✅ Completely standalone (no mixing with other skills)
- ✅ Read-only access to comfy-wf repo
- ✅ Downloads saved locally in `./downloads/`
- ✅ Output video goes to ComfyUI's configured output folder
- ✅ Single command orchestration from URL → Final video

---

_Built: 2026-02-14 | Bramha_
