#!/usr/bin/env python3
"""
Download Instagram Reels using yt-dlp
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

def download_instagram_reel(url: str, output_dir: str = "downloads") -> str:
    """
    Download Instagram Reel using yt-dlp
    
    Args:
        url: Instagram Reel URL
        output_dir: Directory to save video
        
    Returns:
        Path to downloaded video file
        
    Raises:
        Exception: If download fails
    """
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"reel_{timestamp}.mp4"
    output_path = os.path.join(output_dir, output_filename)
    
    print(f"📥 Downloading Instagram Reel...")
    print(f"   URL: {url}")
    print(f"   Output: {output_path}")
    
    try:
        # yt-dlp command
        cmd = [
            "yt-dlp",
            "-f", "best[ext=mp4]",  # Best quality MP4
            "-o", output_path,
            "--no-warnings",
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Verify file exists
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Download complete!")
            print(f"   File: {output_path}")
            print(f"   Size: {file_size / (1024*1024):.2f} MB")
            return output_path
        else:
            raise Exception("Downloaded file not found")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Download failed!")
        print(f"   Error: {e.stderr}")
        raise Exception(f"yt-dlp download failed: {e.stderr}")
    except FileNotFoundError:
        print(f"❌ yt-dlp not found!")
        print(f"   Install: pip install yt-dlp")
        raise Exception("yt-dlp not installed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Instagram Reel")
    parser.add_argument("--url", required=True, help="Instagram Reel URL")
    parser.add_argument("--output-dir", default="downloads", help="Output directory")
    
    args = parser.parse_args()
    
    try:
        video_path = download_instagram_reel(args.url, args.output_dir)
        print(f"\n✅ Ready for Wan Animate workflow")
        print(f"   Video: {video_path}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
