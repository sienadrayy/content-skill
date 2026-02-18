#!/usr/bin/env python3
"""
Final ComfyUI converter with comprehensive diagnostics.
"""

import json
import requests
from pathlib import Path

def diagnose_workflow(api_wf):
    """Diagnose potential issues in the workflow."""
    issues = []
    
    # Check for required nodes
    has_save_image = any(n.get('class_type') == 'SaveImage' for n in api_wf.values())
    if not has_save_image:
        issues.append("No SaveImage node found")
    
    # Check for dangling references
    node_ids = set(int(k) for k in api_wf.keys())
    
    for node_id, node in api_wf.items():
        for inp_name, inp_val in node.get('inputs', {}).items():
            if isinstance(inp_val, list) and len(inp_val) >= 2:
                ref_node = int(inp_val[0])
                if ref_node not in node_ids:
                    issues.append(f"Node {node_id} references missing node {ref_node}")
    
    return issues

def main():
    print("=" * 70)
    print("ComfyUI Workflow Converter - Final Version")
    print("=" * 70)
    
    # Load original workflow
    wf_path = "\\\\192.168.29.60\\workflows\\image_z_image_turbo.json"
    print(f"\nLoading: {wf_path}")
    
    with open(wf_path) as f:
        wf = json.load(f)
    
    print(f"Workflow has {len(wf['nodes'])} main nodes")
    
    # For now, let's examine what's actually needed
    # The workflow is: node 58 (prompt) -> node 57 (subgraph) -> node 9 (SaveImage)
    
    # Instead of trying to flatten the complex subgraph,
    # let's try submitting the UI format workflow itself to see if the server accepts that
    
    print("\n=== Testing: Submit UI format directly ===")
    
    # Create a minimal wrapper
    ui_format_test = {
        "workflow": wf,
        "ui": wf.get('extra', {})
    }
    
    resp = requests.post(
        "http://192.168.29.60:8188/prompt",
        json=ui_format_test,
        timeout=30
    )
    
    print(f"UI format submission: {resp.status_code}")
    if resp.status_code != 200:
        print(f"Response: {resp.text[:300]}")
    else:
        result = resp.json()
        print(f"SUCCESS! Prompt ID: {result.get('prompt_id')}")
        return 0
    
    # If that didn't work, try with just the workflow part
    print("\n=== Testing: Submit as plain workflow dict ===")
    resp = requests.post(
        "http://192.168.29.60:8188/prompt",
        json=wf,
        timeout=30
    )
    
    print(f"Plain workflow submission: {resp.status_code}")
    if resp.status_code != 200:
        print(f"Response: {resp.text[:300]}")
    else:
        result = resp.json()
        print(f"SUCCESS! Prompt ID: {result.get('prompt_id')}")
        return 0
    
    # Load the previously generated API format
    print("\n=== Testing: Generated API format ===")
    with open("\\\\192.168.29.60\\workflows\\z_image_turbo_api.json") as f:
        api_wf = json.load(f)
    
    if '35' in api_wf:
        del api_wf['35']
    
    # Diagnose
    issues = diagnose_workflow(api_wf)
    if issues:
        print("Potential issues found:")
        for issue in issues:
            print(f"  - {issue}")
    
    # Try with different formats
    print("\nTrying API format with integer keys...")
    api_wf_int = {int(k): v for k, v in api_wf.items()}
    
    resp = requests.post(
        "http://192.168.29.60:8188/prompt",
        json=api_wf_int,
        timeout=30
    )
    
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        result = resp.json()
        print(f"SUCCESS! Prompt ID: {result.get('prompt_id')}")
        return 0
    else:
        print(f"Response: {resp.text[:500]}")
    
    print("\n" + "=" * 70)
    print("All submission methods failed")
    print("=" * 70)
    
    # Save diagnostic info
    with open("C:\\Users\\mohit\\.openclaw\\workspace\\diagnosis.json", 'w') as f:
        json.dump({
            "issues": issues,
            "api_workflow": api_wf,
            "nodes_count": len(api_wf)
        }, f, indent=2)
    
    print("\nDiagnostics saved to diagnosis.json")
    print("\nTroubleshooting steps:")
    print("1. Check if ComfyUI server is running normally")
    print("2. Try submitting via the web UI to see if it works")
    print("3. Check ComfyUI logs for detailed error information")
    print("4. Verify the subgraph definition is being handled correctly")
    
    return 1


if __name__ == "__main__":
    exit(main())
