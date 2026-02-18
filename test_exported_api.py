import json
import requests
import uuid
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Test exported API workflows
workflows = [
    r'\\192.168.29.60\workflows\z_image_turbo_api.json',
    r'\\192.168.29.60\workflows\image_z_image_turbo API.json',
]

for wf_path in workflows:
    try:
        with open(wf_path) as f:
            workflow = json.load(f)
        
        payload = {
            'prompt': workflow,
            'client_id': str(uuid.uuid4())
        }
        
        name = wf_path.split('\\')[-1]
        print(f"\nTesting: {name}")
        print(f"  Nodes: {len(workflow)}")
        
        response = requests.post('http://192.168.29.60:8188/prompt', json=payload)
        result = response.json()
        
        if 'prompt_id' in result:
            prompt_id = result['prompt_id'][:8]
            print(f"  SUCCESS - Prompt ID: {prompt_id}...")
        else:
            err = result.get('error', {})
            msg = err.get('message', 'Unknown')
            print(f"  FAIL - {err.get('type')}: {msg}")
            
    except Exception as e:
        print(f"  ERROR - {str(e)[:100]}")
