#!/usr/bin/env python3
import zipfile
import os
from pathlib import Path

def package_skill(skill_dir, output_dir):
    """Package a skill directory into a .skill file"""
    skill_dir = Path(skill_dir)
    output_dir = Path(output_dir)
    skill_name = skill_dir.name
    output_file = output_dir / f"{skill_name}.skill"
    
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(skill_dir.parent)
                zf.write(file_path, arcname)
    
    print(f"[OK] Packaged: {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python package_skill.py <skill_dir> [output_dir]")
        sys.exit(1)
    
    skill_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    package_skill(skill_dir, output_dir)
