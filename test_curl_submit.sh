#!/bin/bash

# Export the converted workflow to JSON
python3 << 'EOF'
import json
import sys
sys.path.insert(0, r"C:\Users\mohit\.openclaw\workspace\comfyui-workflow-runner\scripts"
from run_workflow import ComfyUIRunner

runner = ComfyUIRunner()
wf = runner.load_workflow(r"C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Images_workflow.json")

# Save the converted workflow
with open('/tmp/workflow_converted.json', 'w') as f:
    json.dump(wf, f)

print("Converted workflow saved")
EOF

# Submit via curl
curl -X POST \
  -H "Content-Type: application/json" \
  -d @/tmp/workflow_converted.json \
  http://192.168.29.60:8188/prompt
