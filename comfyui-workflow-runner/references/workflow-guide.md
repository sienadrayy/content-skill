# ComfyUI Workflow Runner Guide

## Overview

The ComfyUI Workflow Runner skill allows you to:
1. Load existing ComfyUI workflow JSON files
2. Substitute input parameters (prompts, settings, etc.)
3. Submit to a ComfyUI server for execution
4. Monitor execution status

## Step 1: Pull Latest Workflows from GitHub

Before running workflows, pull the latest versions from your ComfyUI repo:

```bash
# Add the remote if not already added
git remote add comfy-wf https://github.com/mohitsoni48/comfy-wf.git

# Fetch and pull master branch
git fetch comfy-wf master
git pull comfy-wf master --allow-unrelated-histories
```

This ensures you're using the most up-to-date workflow JSON with all recent changes.

## Workflow JSON Structure

Each ComfyUI workflow is a JSON object where keys are **node IDs** (usually numbers as strings):

```json
{
  "443": {
    "inputs": {
      "value": "Close-up portrait of siena"
    },
    "class_type": "PrimitiveStringMultiline",
    "_meta": {
      "title": "Image Prompts"
    }
  },
  "444": {
    "inputs": {
      "index": 0,
      "list_input": ["442", 0]
    },
    "class_type": "StringFromList",
    "_meta": {
      "title": "String From List"
    }
  }
}
```

### Key Concepts

- **Node ID**: The top-level key (e.g., "443", "444") — identifies a node
- **inputs**: A dict of input fields for that node
- **class_type**: The type of node (for reference)
- **_meta.title**: Human-readable name of the node

## Finding Node IDs and Fields

To identify which nodes to modify in your workflow:

1. **Open the workflow in ComfyUI UI** (drag JSON onto interface)
2. **Inspect nodes** in the graph view
3. **Look at the JSON structure** for field names

Example from `siena_test_v1.json`:
- Node 443 has field `value` → stores the main prompt text
- Node 442 has fields `Multi_prompts`, `prefix`, `suffix`
- Node 500 has field `value` → animation instructions

## Substituting Inputs

The script supports two input formats:

### Format 1: `node_id.field` (Recommended)
```
--inputs '{"443.value": "New prompt", "500.value": "New animation"}'
```

### Format 2: Key-value pairs
```
--inputs '443.value="New prompt",500.value="New animation"'
```

Values are parsed as JSON when possible, otherwise treated as strings:
- `"New prompt"` → string
- `"true"` → boolean
- `"42"` → number
- `"[1,2,3]"` → array

## Primary Workflow: Images_workflow.json

**Location**: `comfy-wf/openclaw/Images_workflow.json`

**Purpose**: Generate sensual image sequences for Siena content with video animation support

### The 4 Key Inputs

| Node | Field | Purpose | Type | Example |
|------|-------|---------|------|---------|
| 443 | `value` | Image Prompts | Text | "Close-up portrait of siena..." (6 shots) |
| 436 | `value` | VIdeo Prompts | Text | "Direct eye contact held..." (9 animations) |
| 500 | `value` | Name | Text | "siena_reel_001" (file prefix) |
| 519 | `mode` | Fast Groups Bypasser | Toggle | 0 (enabled) or 1 (disabled) |

### Example Substitution (All 4 Inputs):
```json
{
  "443.value": "Your detailed image prompts here (6 different shots)",
  "436.value": "Your animation descriptions here (9 different movements with timing)",
  "500.value": "my_content_folder_name",
  "519.mode": 0
}
```

### Node Details

- **Node 443 (Image Prompts)**: Contains 6 newline-separated image descriptions
  - Close-up, medium shot, full body, body roll, face detail, extreme close-up
  - Used by Qwen Image generation model
  
- **Node 436 (VIdeo Prompts)**: Contains 9 newline-separated animation descriptions
  - Each has precise timing and camera instructions
  - Used for video generation/animation timing
  
- **Node 500 (Name)**: File/folder naming prefix
  - Used in SaveImage node to organize outputs
  
- **Node 519 (Fast Groups Bypasser)**: Group control toggle
  - 0 = Groups enabled (normal flow)
  - 1 = Groups disabled (bypass)

## Other Workflows

Additional workflows available (in `comfy-wf/`):

| Workflow | Purpose | Key Nodes |
|----------|---------|-----------|
| Reel maker.json | Generic reel creation | Check structure |
| Wan 2.2 variants | Video generation (Wan model) | Video-specific nodes |
| Flux Kontext | Character consistency | Image editing |
| Video Upscale | Upscaling | Input/output images |

**Note**: Each workflow is unique. Check its node structure in ComfyUI UI to identify exact input fields.

## Execution Flow

1. **Load workflow** from JSON file
2. **Substitute inputs** (optional)
3. **Submit to server** (HTTP POST to `/prompt`)
4. **Get prompt_id** back
5. **Monitor status** (poll `/history/{prompt_id}`)
6. **Wait for completion** (optional)

## Server Configuration

Default: `http://192.168.29.60:8188`

Override with `--server`:
```bash
python run_workflow.py siena_test_v1.json --server http://192.168.1.100:8188
```

## API Endpoints Used

- `POST /prompt` — Submit workflow, returns `{prompt_id, number}`
- `GET /history/{prompt_id}` — Check execution results
- `GET /queue` — Check queue status

## Example Usage Patterns

### Simple execution (fire and forget)
```bash
python run_workflow.py comfy-wf/siena_test_v1.json
```

### With input substitution
```bash
python run_workflow.py comfy-wf/siena_test_v1.json \
  --inputs '{"443.value": "Medium shot of siena in sunlight"}'
```

### Wait for completion
```bash
python run_workflow.py comfy-wf/siena_test_v1.json \
  --inputs '{"443.value": "Dynamic pose"}' \
  --wait --timeout 600
```

### Multiple inputs
```bash
python run_workflow.py comfy-wf/siena_valentine_reel_v1.json \
  --inputs '{
    "443.value": "Valentine themed pose",
    "500.value": "Slow romantic movement",
    "401.value": "warm golden lighting"
  }'
```

## Troubleshooting

### "Connection error: Cannot reach ComfyUI"
- Check server is running: `http://192.168.29.60:8188`
- Verify network connectivity
- Check firewall rules

### "Validation error: Workflow must be a JSON object"
- Ensure workflow file is valid JSON
- Check file is readable

### Workflow executes but no visible output
- That's fine! Outputs go to ComfyUI's configured output directory
- The skill focuses on execution, not retrieval
- Check ComfyUI web UI for results

### Node ID not found
- Double-check node_id is a string in the JSON
- Verify the field name is spelled correctly
- Open workflow in ComfyUI UI to inspect nodes

## Advanced: Dynamic Input Lists

Some nodes accept lists of values (for iterating):

```json
"inputs": {
  "list_input": ["node_id", index]
}
```

This references another node's output at a specific index. Keep these intact when substituting.

## Return Values

When executed via the skill system, the script returns:
- **Success (0)**: Workflow submitted/completed
- **Failure (1)**: Connection error, validation error, or timeout

Status messages print to stdout for monitoring.
