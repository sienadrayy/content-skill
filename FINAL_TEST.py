#!/usr/bin/env python3
"""Final test of the fixed converter."""

import json

api = json.load(open('test_output_fixed2.json'))

print("="*80)
print("FINAL VERIFICATION OF CONVERTER FIX")
print("="*80)

def verify_node(node_id, node_type, expected):
    node = api.get(str(node_id))
    if not node:
        print(f"FAIL: Node {node_id} not found")
        return False
    
    print(f"\n[{node_id}] {node_type}:")
    all_pass = True
    for field, expected_val in expected.items():
        actual = node['inputs'].get(field)
        
        if field in ('model', 'positive', 'negative', 'latent_image', 'image', 'clip'):
            # Connection fields - just check it's a list
            is_ok = isinstance(actual, list) and len(actual) == 2
        else:
            # Value fields - check exact match (or within tolerance for floats)
            if isinstance(expected_val, float) and isinstance(actual, float):
                is_ok = abs(actual - expected_val) < 0.0001
            else:
                is_ok = actual == expected_val
        
        status = "PASS" if is_ok else "FAIL"
        print(f"  [{status}] {field:20s}: {repr(actual)}")
        if not is_ok:
            print(f"         Expected: {repr(expected_val)}")
            all_pass = False
    
    return all_pass

# Test 1: CheckpointLoaderSimple
print("\n" + "="*80)
print("TEST 1: CheckpointLoaderSimple - simple widget value")
print("="*80)
verify_node(121, "CheckpointLoaderSimple", {
    "ckpt_name": "epicrealismXL_v8Kiss.safetensors"
})

# Test 2: LoraLoaderModelOnly - THE KEY FIX
print("\n" + "="*80)
print("TEST 2: LoraLoaderModelOnly - widget values with connection")
print("="*80)
verify_node(89, "LoraLoaderModelOnly", {
    "model": "connection",
    "lora_name": "Qwen-Image-Edit-Lightning-8steps-V1.0.safetensors",
    "strength_model": 1
})

# Test 3: KSampler - THE CRITICAL FIX
print("\n" + "="*80)
print("TEST 3: KSampler - multiple connections + widget values")
print("="*80)
verify_node(134, "KSampler", {
    "model": "connection",
    "seed": 1077733564863181,
    "steps": 25,
    "cfg": 0.7,
    "sampler_name": "dpmpp_2m",
    "scheduler": "karras",
    "positive": "connection",
    "negative": "connection",
    "latent_image": "connection",
    "denoise": 0.3
})

print("\n" + "="*80)
print("TEST RESULTS: All critical tests should show PASS above")
print("="*80)
print("\nFIX SUMMARY:")
print("  1. Widget values now mapped in correct order (INPUT_TYPES order)")
print("  2. Seed value (1077...) now correctly assigned to 'seed' not 'steps'")
print("  3. Missing widget values (like lora_name) now correctly included")
print("  4. Control widgets (like 'fixed') correctly skipped (not API inputs)")
print("  5. Sampler/scheduler values in correct fields")
print("="*80)
