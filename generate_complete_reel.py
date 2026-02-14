#!/usr/bin/env python3
"""
Master orchestrator: Script -> I2V Prompts -> ComfyUI Generation
WITH MANDATORY VERIFICATION CHECKPOINTS

VERIFICATION IS REQUIRED BEFORE ANY WORKFLOW SUBMISSION.

Chains:
1. sensual-reels skill (generate script(s) - single or multi-part)
2. i2v-prompt-generator skill (extract image/video prompts)
3. comfyui-workflow-runner (run Images + Videos dual workflows)

WORKFLOW:
Script Generation → Script Verification → Prompt Extraction → Prompt Verification → ComfyUI Submission
"""
import subprocess
import sys
import json
import argparse

def run_command(cmd, description):
    """Run a command and capture output"""
    print(f"\n>>> {description}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(
        description="Generate complete Reel (Script -> I2V Prompts -> ComfyUI)",
        epilog="VERIFICATION IS MANDATORY. User must approve scripts and prompts before ComfyUI submission."
    )
    parser.add_argument("--concept", required=True, help="Content concept (e.g., 'shower', '3 parts shower')")
    parser.add_argument("--name", required=True, help="Output name/prefix")
    parser.add_argument("--image-prompts", default=None, help="Pre-approved image prompts (skips verification)")
    parser.add_argument("--video-prompts", default=None, help="Pre-approved video prompts (skips verification)")
    args = parser.parse_args()
    
    print("\n" + "=" * 80)
    print("COMPLETE REEL GENERATOR")
    print("Script → I2V Prompts → ComfyUI Workflows")
    print("=" * 80)
    print(f"\n📋 Concept: {args.concept}")
    print(f"📁 Output: {args.name}")
    print(f"✓ Verification: MANDATORY")
    
    # ============================================================================
    # STEP 1: Generate Script(s)
    # ============================================================================
    print("\n" + "=" * 80)
    print("STEP 1: Generating Script(s)")
    print("=" * 80)
    
    # Detect if multi-part (e.g., "3 parts", "2 parts shower")
    parts_count = None
    if any(f"{i} part" in args.concept.lower() for i in range(2, 10)):
        for i in range(2, 10):
            if f"{i} part" in args.concept.lower():
                parts_count = i
                break
    
    if parts_count:
        print(f"\n🎬 Multi-part detected: {parts_count} separate image/video pairs")
    else:
        print(f"\n🎬 Single script detected")
    
    print(f"\n[AWAITING SENSUAL-REELS SKILL TO GENERATE SCRIPT(S)...]")
    print(f"Concept: {args.concept}")
    
    # In production, call sensual-reels skill
    # For now, we'll show a placeholder that the user sees
    scripts = {
        "single": f"[GENERATED SCRIPT]\n60-second timeline for: {args.concept}",
        "parts": [
            f"[PART 1 SCRIPT]\nConcept 1 of {parts_count}: {args.concept}",
            f"[PART 2 SCRIPT]\nConcept 2 of {parts_count}: {args.concept}",
            f"[PART 3 SCRIPT]\nConcept 3 of {parts_count}: {args.concept}",
        ] if parts_count == 3 else []
    }
    
    # ============================================================================
    # VERIFICATION CHECKPOINT 1: SCRIPT APPROVAL
    # ============================================================================
    print("\n" + "=" * 80)
    print("✋ VERIFICATION CHECKPOINT 1: SCRIPT APPROVAL (MANDATORY)")
    print("=" * 80)
    
    if parts_count:
        print(f"\n🎬 Generated {parts_count} separate scripts:\n")
        for i, script in enumerate(scripts["parts"], 1):
            print(f"--- PART {i} ---")
            print(script)
            print()
    else:
        print(f"\n--- SINGLE SCRIPT ---")
        print(scripts["single"])
        print()
    
    print("=" * 80)
    print("User must verify and approve these scripts before proceeding.")
    print("If scripts are not approved, workflow will ABORT.")
    print("=" * 80)
    
    # Return control to user for approval
    print("\n⏸️  AWAITING USER APPROVAL...")
    print("(Scripts printed above. User must review in chat and approve/modify.)")
    
    return 0

if __name__ == "__main__":
    exit(main())
