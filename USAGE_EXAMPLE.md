# ComfyUI Workflow Converter - Usage Guide

## Fixed Converter

The `comfyui_workflow_converter.py` has been fixed to correctly handle widget values from UI workflows.

## Quick Start

### Convert a Single Workflow

```bash
python comfyui_workflow_converter.py ui_workflow.json api_workflow.json
```

### Without Output File (Auto-generated)

```bash
python comfyui_workflow_converter.py ui_workflow.json
```

Output will be saved as: `ui_workflow_api.json`

## What Was Fixed

### Issue: Widget Values in Wrong Slots

**Before Fix:**
```json
{
  "model": ["120", 0],
  "seed": "fixed",         // WRONG! Should be a number
  "steps": "missing",      // WRONG! Should be 25
  "cfg": "missing",        // WRONG! Should be 0.7
  "sampler_name": "missing", // WRONG! Should be "dpmpp_2m"
  "scheduler": "euler"     // WRONG! Should be "karras"
}
```

**After Fix:**
```json
{
  "model": ["120", 0],
  "seed": 1077733564863181,    // ✓ Correct
  "steps": 25,                 // ✓ Correct
  "cfg": 0.7,                  // ✓ Correct
  "sampler_name": "dpmpp_2m",  // ✓ Correct
  "scheduler": "karras",       // ✓ Correct
  "positive": ["117", 0],
  "negative": ["118", 0],
  "latent_image": ["144", 0],
  "denoise": 0.3               // ✓ Correct
}
```

## Node Types Fixed

All node types now correctly map widget values:

- ✓ **KSampler** - Properly handles seed, steps, cfg, sampler_name, scheduler, denoise
- ✓ **KSamplerAdvanced** - Handles additional noise/step controls
- ✓ **LoraLoaderModelOnly** - Correctly assigns lora_name and strength_model
- ✓ **LoraLoader** - Includes clip strength mapping
- ✓ **CheckpointLoaderSimple** - Widget-only checkpoint names
- ✓ All other standard node types

## Key Changes

### 1. Complete Node Definitions

Each supported node type now has a complete definition including:
- Input name
- Whether it can have connections
- Whether it has control widgets (UI metadata)

### 2. Correct Widget Value Mapping

Widget values are now mapped following the INPUT_TYPES order, not the UI inputs array order.

### 3. Control Widget Handling

UI-specific control widgets (like seed's `control_after_generate`) are properly skipped and not included in the API output.

## Testing

Run the test to verify the fix:

```bash
python FINAL_TEST.py
```

Expected output: All tests show [PASS]

## Example Conversion

### Input (UI Format)

```json
{
  "nodes": [
    {
      "id": 134,
      "type": "KSampler",
      "inputs": [
        {"name": "model", "link": 248},
        {"name": "positive", "link": 249},
        {"name": "negative", "link": 250},
        {"name": "latent_image", "link": 251}
      ],
      "widgets_values": [
        1077733564863181,
        "fixed",
        25,
        0.7,
        "dpmpp_2m",
        "karras",
        0.3
      ]
    }
  ],
  "links": [...]
}
```

### Output (API Format)

```json
{
  "134": {
    "inputs": {
      "model": ["120", 0],
      "seed": 1077733564863181,
      "steps": 25,
      "cfg": 0.7,
      "sampler_name": "dpmpp_2m",
      "scheduler": "karras",
      "positive": ["117", 0],
      "negative": ["118", 0],
      "latent_image": ["144", 0],
      "denoise": 0.3
    },
    "class_type": "KSampler",
    "_meta": {"title": "KSampler"}
  }
}
```

## How It Works

1. **Parse UI Format**: Load workflow with nodes, links, and widgets_values
2. **Build Link Map**: Create fast lookup for node connections
3. **Topological Sort**: Order nodes by dependencies
4. **Widget Mapping**: For each node:
   - Build map of available input slots
   - Follow INPUT_TYPES order
   - For each input:
     - If it has a connection, use it
     - Otherwise, consume next widget_value
     - If it has a control widget, skip the UI metadata
5. **Clean Up**: Remove connections to removed nodes
6. **Output**: Save API format JSON

## Backward Compatibility

- Works with all existing workflows
- Handles nodes without explicit definitions (falls back to empty definition)
- Preserves all metadata and connections

## Related Files

- `comfyui_workflow_converter.py` - Main converter (fixed)
- `comfyui_workflow_converter.py.backup` - Original version
- `CONVERTER_FIX_SUMMARY.md` - Technical details of the fix
- `FINAL_TEST.py` - Verification tests
