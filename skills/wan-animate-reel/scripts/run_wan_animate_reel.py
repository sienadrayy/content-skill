#!/usr/bin/env python3
"""
Main orchestrator for Wan Animate Reel
Downloads Instagram Reel → Submits to Wan Animate workflow → Returns video path
"""

import os
import sys
import argparse
import subprocess
import uuid
from pathlib import Path

# Fix Unicode encoding on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).parent
DOWNLOADS_DIR = SCRIPT_DIR.parent / "downloads"

def run_command(cmd, description: str) -> str:
    """
    Run Python script and return stdout
    
    Args:
        cmd: Command list
        description: What we're doing
        
    Returns:
        Last line of stdout (expected to be the result)
    """
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        # Return last non-empty line
        lines = [l for l in result.stdout.split('\n') if l.strip()]
        return lines[-1] if lines else ""
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        raise Exception(f"{description} failed: {e.stderr}")

def download_instagram_reel(url: str) -> str:
    """Download Instagram Reel and return video path"""
    
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "download_instagram_reel.py"),
        "--url", url,
        "--output-dir", str(DOWNLOADS_DIR)
    ]
    
    output = run_command(cmd, "Downloading Instagram Reel")
    
    # Extract video path from output (last path-like string)
    import re
    paths = re.findall(r'downloads[\\\/]reel_\d{8}_\d{6}\.mp4', output)
    if paths:
        return str(DOWNLOADS_DIR / paths[-1].split('\\')[-1].split('/')[-1])
    
    # Fallback: look for any .mp4 file in last line
    match = re.search(r'([a-zA-Z]:\\[\w\\]+\.mp4)', output)
    if match:
        return match.group(1)
    
    raise Exception("Could not extract video path from download output")

def submit_to_wan_workflow(video_path: str, name: str = None) -> dict:
    """Submit video to Wan Animate dual workflows (Image + Video)"""
    
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "submit_wan_workflow.py"),
        "--video", video_path,
        "--wait"
    ]
    
    if name:
        cmd.extend(["--name", name])
    
    output = run_command(cmd, "Submitting to Wan Animate Dual Workflows (Image + Video)")
    
    # Extract both prompt IDs
    import re
    image_match = re.search(r'Image Prompt ID: ([a-f0-9\-]+)', output)
    video_match = re.search(r'Video Prompt ID: ([a-f0-9\-]+)', output)
    
    return {
        "image_prompt_id": image_match.group(1) if image_match else None,
        "video_prompt_id": video_match.group(1) if video_match else None,
        "output": output
    }

def main():
    parser = argparse.ArgumentParser(
        description="Download Instagram Reel and animate with Wan Video (Image + Video API)"
    )
    parser.add_argument(
        "--url",
        required=True,
        help="Instagram Reel URL (e.g., https://www.instagram.com/reel/ABC123/)"
    )
    
    args = parser.parse_args()
    
    # Generate random UUID for this run
    run_name = str(uuid.uuid4())
    
    try:
        print(f"\n{'='*60}")
        print(f"🎬 WAN ANIMATE REEL ORCHESTRATOR")
        print(f"{'='*60}")
        print(f"URL: {args.url}")
        print(f"Run ID: {run_name}")
        
        # Step 1: Download
        print(f"\n📥 STEP 1: Download Instagram Reel")
        video_path = download_instagram_reel(args.url)
        print(f"✅ Downloaded: {video_path}")
        
        # Step 2: Submit to Dual Workflows (Image + Video)
        print(f"\n🎨 STEP 2: Submit to Wan Animate Dual Workflows")
        result = submit_to_wan_workflow(video_path, run_name)
        
        # Final status
        print(f"\n{'='*60}")
        print(f"🎉 COMPLETE!")
        print(f"{'='*60}")
        print(f"Run ID: {run_name}")
        print(f"📹 Video file: {video_path}")
        print(f"🎬 Workflows: Wan Animate Character Replacement V3 (Image + Video API)")
        print(f"📊 Monitor: http://192.168.29.60:8188")
        print(f"Image Prompt ID: {result.get('image_prompt_id')}")
        print(f"Video Prompt ID: {result.get('video_prompt_id')}")
        print(f"\n💡 Output files will use prefix: {run_name}_")
        
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ FAILED")
        print(f"{'='*60}")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
