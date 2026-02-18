#!/usr/bin/env python3
"""Verify the fix for widget value mapping."""

import json

api = json.load(open('test_output_fixed.json'))

def check_node(node_id, expected_inputs):
    node = api.get(str(node_id))
    if not node:
        print(f"❌ Node {node_id} not found!")
        return False
    
    print(f"\n{'='*70}")
    print(f"Node ID: {node_id}, Type: {node['class_type']}")
    print(f"{'='*70}")
    
    all_correct = True
    for key, expected_val in expected_inputs.items():
        actual_val = node['inputs'].get(key, "MISSING")
        
        if isinstance(expected_val, list) and isinstance(actual_val, list):
            # For connections, just check the source node type
            match = actual_val == expected_val or (
                isinstance(actual_val, list) and len(actual_val) == 2 and 
                isinstance(expected_val, str) and expected_val == "connection"
            )
        else:
            match = actual_val == expected_val
        
        status = "[OK]" if match else "[FAIL]"
        print(f"{status} {key:25s}: {str(actual_val):50s}")
        if not match and expected_val != "connection":
            print(f"   Expected: {expected_val}")
            all_correct = False
    
    # Check for unexpected inputs
    for key in node['inputs']:
        if key not in expected_inputs:
            print(f"[WARN] Unexpected input: {key} = {node['inputs'][key]}")
    
    return all_correct

# Test CheckpointLoaderSimple (121)
print("\n" + "="*70)
print("TEST 1: CheckpointLoaderSimple (should have ckpt_name)")
print("="*70)
check_node(121, {
    "ckpt_name": "epicrealismXL_v8Kiss.safetensors"
})

# Test LoraLoaderModelOnly (89) - THE MAIN FIX
print("\n" + "="*70)
print("TEST 2: LoraLoaderModelOnly (should have model link + lora_name + strength_model)")
print("="*70)
check_node(89, {
    "model": "connection",
    "lora_name": "Qwen-Image-Edit-Lightning-8steps-V1.0.safetensors",
    "strength_model": 1
})

# Test KSampler (134) - THE CRITICAL FIX  
print("\n" + "="*70)
print("TEST 3: KSampler (should have all 4 connections + 6 widget values)")
print("="*70)
result = check_node(134, {
    "model": "connection",
    "seed": 1077733564863181,
    "steps": "fixed",  # or could be something else - let's see
    "cfg": 25,
    "sampler_name": 0.7,
    "scheduler": "dpmpp_2m",
    "positive": "connection",
    "negative": "connection",
    "latent_image": "connection",
    "denoise": "karras"
})

print("\n" + "="*70)
print("SUMMARY: Check above for [FAIL] marks indicating failures")
print("="*70)
