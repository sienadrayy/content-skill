#!/usr/bin/env python3
import json
import urllib.request
import urllib.error

# Try sending via comfy-cli instead
import subprocess

print("="*80)
print("Testing comfy-cli approach")
print("="*80)

# Check if comfy-cli is installed
result = subprocess.run(["comfy", "--version"], capture_output=True, text=True)
if result.returncode == 0:
    print(f"comfy-cli found: {result.stdout}")
else:
    print("comfy-cli not found, trying pip install...")
    subprocess.run(["pip", "install", "comfy-cli"], capture_output=True)

# Try to submit workflow via comfy-cli
print("\nAttempting to submit via comfy-cli...")
result = subprocess.run(
    ["comfy", "run", "--server", "192.168.29.60:8188", 
     r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Images_workflow.json"],
    capture_output=True,
    text=True,
    timeout=30
)

print(f"Return code: {result.returncode}")
print(f"Output: {result.stdout[:500] if result.stdout else 'None'}")
print(f"Error: {result.stderr[:500] if result.stderr else 'None'}")
