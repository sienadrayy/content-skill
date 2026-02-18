# ComfyUI Workflow Converter - Bypass Node Fix

## Problem Statement

When converting ComfyUI workflows from UI format to API format, the converter was removing bypassed nodes (mode=4) but leaving dangling references. This caused validation errors when submitting the converted workflow to the ComfyUI server.

**Example of the bug:**
- Node 645 expected input from node 649
- Node 649 was bypassed (mode=4) and removed
- Result: Node 645 referenced a non-existent node 649

## Solution

Implemented a bypass resolution system that:

1. **Builds a bypass map** - Identifies all bypassed nodes and their input/output connections
2. **Traces input sources** - For each bypassed node's output, determines what its actual input source is
3. **Re-routes connections** - Updates all links that reference bypassed nodes to point to their actual sources instead

## Implementation Details

### New Methods Added

#### `_build_bypass_map()`
- Scans all nodes to identify those with `mode=4` (BYPASS)
- For each bypassed node, maps its output slots to the actual source of its input
- Stores output redirects as: `(bypassed_node_id, output_slot) -> (source_node_id, source_slot)`

#### `_resolve_node_source(node_id, slot)`
- Recursively resolves the actual source of a connection
- Traces through bypass redirects to find the ultimate source node
- Returns `(node_id, slot)` or `None` if unresolvable

### Modified Sections

#### `convert_to_api_format()`
- When processing input connections, calls `_resolve_node_source()` to handle bypassed nodes
- Skips connections that resolve to `None` (bypassed nodes with no valid input)
- Also skips "Note" nodes (documentation-only, not executable)

## Test Results

### Original Workflow (Qwen + Z image.json)
- **Total nodes:** 54
- **Total links:** 61
- **Bypassed nodes:** 18
- **Links to bypassed nodes:** 24
- **Links from bypassed nodes:** 22

### Converted Workflow
- **Total nodes:** 34 (removed 18 bypassed + 2 Note nodes)
- **Dangling references:** 0
- **Status:** ✓ Ready for submission

## Testing

The fix was validated with the test workflow: `\\192.168.29.60\workflows\Qwen + Z image.json`

```
Test Results:
- No bypassed nodes remain in converted output
- All 34 nodes have valid input references
- Workflow successfully submits to http://192.168.29.60:8188/prompt
```

## Code Changes

File: `comfyui_workflow_converter_v2.py`

**Changes:**
1. Added `_build_bypass_map()` method to `__init__()`
2. Added `_build_bypass_map()` method implementation
3. Added `_resolve_node_source()` helper method
4. Modified `convert_to_api_format()` to use `_resolve_node_source()`
5. Added skipping of "Note" nodes
6. Added `Set` to type imports

## Bypass Semantics

In ComfyUI, a bypassed node (mode=4):
- Is not executed during rendering
- Acts as a "pass-through" node
- Its output is re-routed to one of its inputs (typically the first connected input)

The converter now properly handles this by:
1. Removing the bypassed node from the API output
2. Re-routing all connections that would go to/through the bypassed node to its actual input source

## Success Criteria Met

✓ Workflow submits to http://192.168.29.60:8188/prompt without bypass-related errors
✓ No dangling references in converted output
✓ All nodes have valid input sources
✓ Bypassed nodes are properly traced and removed
