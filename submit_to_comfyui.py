#!/usr/bin/env python3
"""
Submit ComfyUI API-format workflows to the server at 192.168.29.60:8188
"""
import json
import requests
import uuid
import sys
from pathlib import Path

def submit_workflow(workflow_path, client_id=None):
    """Submit a workflow to ComfyUI server"""
    if client_id is None:
        client_id = str(uuid.uuid4())
    
    # Load workflow
    with open(workflow_path) as f:
        workflow = json.load(f)
    
    # Prepare payload
    payload = {
        'prompt': workflow,
        'client_id': client_id
    }
    
    # Submit
    response = requests.post('http://192.168.29.60:8188/prompt', json=payload)
    result = response.json()
    
    if 'prompt_id' in result:
        return {
            'success': True,
            'prompt_id': result['prompt_id'],
            'client_id': client_id
        }
    else:
        return {
            'success': False,
            'error': result.get('error', {}).get('message', 'Unknown error'),
            'errors': result.get('node_errors', {})
        }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python submit_to_comfyui.py <workflow.json>")
        sys.exit(1)
    
    workflow_file = sys.argv[1]
    result = submit_workflow(workflow_file)
    
    if result['success']:
        print(f"SUCCESS")
        print(f"Prompt ID: {result['prompt_id']}")
        print(f"Client ID: {result['client_id']}")
        print(f"\nYour images/videos will be generated on the ComfyUI server")
    else:
        print(f"FAILED")
        print(f"Error: {result['error']}")
        if result['errors']:
            print(f"\nNode errors:")
            for node_id, errs in result['errors'].items():
                print(f"  Node {node_id}: {[e.get('message') for e in errs.get('errors', [])]}")
