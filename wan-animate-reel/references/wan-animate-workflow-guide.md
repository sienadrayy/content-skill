# Wan Animate Character Replacement V3 API - Workflow Guide

## Overview

This workflow takes a video input and uses Wan Video (version 2.2) to re-animate the video while preserving character motion transfer via pose and face detection.

**Input:** Video file path  
**Output:** MP4 video with character animation and motion transfer

---

## Processing Pipeline

### 1. Video Loading (Node 194)
**Type:** VHS_LoadVideoPath  
**Input:** Video file path (modified at runtime)  
**Output:** Video frames

```
Video file → Load → Extract frames (16 fps by default)
```

### 2. Frame Extraction & Interrogation (Nodes 217, 197)
**Purpose:** Understand the character in the first frame

```
Node 217 (ImageFromBatch) → Get first frame
     ↓
Node 197 (easy imageInterrogator) → Describe character
     ↓
Output: Character description text
```

**Example output:** "A young woman with long hair, wearing a red dress, looking at camera..."

### 3. Pose & Face Detection (Nodes 148, 151)
**Purpose:** Extract movement skeleton from video

```
Node 148 (PoseAndFaceDetection)
     ├─ Uses YOLO for body detection
     ├─ Uses ViTPose for skeleton points
     └─ Outputs: Pose keypoints, face keypoints

Node 151 (DrawViTPose) → Visualize skeleton overlay
```

**Output:** Pose skeleton coordinates for each frame

### 4. Image Resizing & Preprocessing (Nodes 123, 208)
**Purpose:** Prepare frames for animation model

```
Node 123: Resize to 544×960 (Wan Video native resolution)
Node 208: Resize by longer edge to 2048px (for image generation)
```

### 5. Character Image Generation (Nodes 199-214)
**Purpose:** Generate a new character image matching the description

**Pipeline:**

```
Node 216 (Character Prompt Input)
     ├─ Prompt: "amateur photo image taken using iphone of a young 
     │             beautiful white woman named siena without any makeup"
     └─ Text Concatenate with interrogation output (Node 215)
          ↓
Node 201 (Load CLIP - Qwen)
     ↓
Node 199 (CLIP Text Encode) → Text embeddings
     ↓
Node 209 (VAE Encode) → Encode resized image
     ↓
Node 214 (KSamplerAdvanced) → Z-Image Turbo generation
     ├─ Model: z_image_turbo_bf16.safetensors
     ├─ LoRAs applied:
     │  - deedee_amateur_photography (0.3 strength)
     │  - z-image-desire_copy (1.0 strength)
     └─ Steps: 10, CFG: 1.2
          ↓
Node 202 (VAE Decode) → Decode to image
     ↓
Output: Generated character image
```

### 6. Animation Embedding Creation (Node 180)
**Purpose:** Create motion embeddings from pose data

```
Node 180 (WanVideoAnimateEmbeds)
     ├─ Input: Generated image
     ├─ Pose data from Node 151 (skeleton)
     ├─ Face data from Node 148 (face keypoints)
     ├─ CLIP Vision encoding (Node 112)
     └─ Creates: Image + pose + face embeddings for animation
          ↓
Output: Multi-modal embeddings for video generation
```

### 7. Video Generation - Wan Sampler (Node 126)
**Purpose:** Generate video frames preserving pose/motion

```
Node 126 (WanVideoSampler)
     ├─ Model: Wan2.2-Animate-14B-Q6_K.gguf
     ├─ Image embeddings (from Node 180)
     ├─ Pose embeddings (from Node 180)
     ├─ Text embeddings (negative prompt in Chinese - quality penalties)
     ├─ Context options (Node 188):
     │  - Frame window: 77 frames
     │  - Context stride: 4
     │  - Freenoise: enabled
     └─ Generates: Latent video representation
          ↓
Output: Latent video (compressed representation)
```

### 8. Video Decoding (Node 131)
**Purpose:** Convert latents to actual frames

```
Node 131 (WanVideoDecode)
     ├─ VAE: wan_2.1_vae_fp32.safetensors
     ├─ Tiling enabled (efficient VRAM usage)
     └─ Decodes latents → Video frames
          ↓
Output: Decoded video frames (high quality)
```

### 9. Frame Interpolation (Node 196)
**Purpose:** Smooth motion by interpolating between frames

```
Node 196 (RIFE VFI)
     ├─ Model: rife47.pth
     ├─ Multiplier: 2x (double frame count)
     ├─ Fast mode: enabled
     └─ Smooths motion between generated frames
          ↓
Output: Interpolated frames (smoother playback)
```

### 10. Video Export (Node 118)
**Purpose:** Combine frames into MP4

```
Node 118 (VHS_VideoCombine)
     ├─ Frame rate: 32 fps
     ├─ Format: video/h264-mp4
     ├─ Codec: H.264
     ├─ CRF: 19 (quality)
     └─ Outputs to ComfyUI output directory
          ↓
Final Output: Animated MP4 video
```

---

## Key Configuration Values

### Resolution
- **Animation model (Wan):** 544 × 960 px (Node 123)
- **Image generation:** 2048 px longer edge (Node 208)

### Video Settings
- **Input frame rate:** 16 fps (Node 194)
- **Output frame rate:** 32 fps (Node 118)
- **Video codec:** H.264 MP4
- **Quality (CRF):** 19 (lower = better, 0-51 range)

### Model Settings
- **Wan model:** Wan2.2-Animate-14B-Q6_K.gguf (quantized)
- **Image model:** z_image_turbo_bf16.safetensors
- **CLIP:** qwen_3_4b.safetensors (text encoding)
- **VAE:** wan_2.1_vae_fp32.safetensors (video) + ae.safetensors (image)

### LoRAs Applied
1. WanAnimate_relight_lora (1.5x) - Lighting enhancement
2. low_noise_model (1.0x) - Noise reduction
3. FastWan_T2V_14B_480p (1.0x) - Fast generation
4. Wan22_PusaV1 (1.0x) - Quality enhancement
5. Wan2.2-Fun-A14B (0.5x) - Fun/stylization

### Character Prompt
```
amateur photo image taken using iphone of a young beautiful white woman 
named siena without any makeup
```

### Negative Prompt (Chinese)
```
色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，
静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，
多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，
形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，
背景人很多，倒着走
```

---

## Runtime Modification

**Only Node 194 is modified at runtime:**

```json
"194": {
  "inputs": {
    "video": "<VIDEO_PATH_HERE>",
    "force_rate": 16,
    "format": "AnimateDiff"
  }
}
```

All other nodes remain locked with their pre-configured values.

---

## Performance Notes

- **Execution time:** ~15-20 minutes (depends on video length)
- **GPU requirement:** High-end GPU recommended (Wan2.2 is heavy)
- **VRAM tiling:** Enabled for efficiency
- **Block swapping:** Enabled to manage VRAM
- **Offloading:** CPU offloading enabled for models

---

## Dependencies

- ComfyUI with Wan Video extension
- yt-dlp (for Instagram download)
- Python 3.7+
