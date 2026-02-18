import requests
import json

history = requests.get('http://192.168.29.60:8188/history').json()
prompt_id = 'd1a4920e-10a3-47b0-ad31-c6258b87547e'

if prompt_id in history:
    entry = history[prompt_id]
    outputs = entry.get('outputs', {})
    print('Outputs:')
    for node_id, output in outputs.items():
        print(f'\nNode {node_id}:')
        print(json.dumps(output, indent=2)[:500])
    
    # Check what node 612 is in the original workflow
    prompt_data = entry.get('prompt', [])
    if len(prompt_data) >= 3:
        workflow = prompt_data[2]
        print(f'\n\nNode 612 class: {workflow.get("612", {}).get("class_type")}')
        print(f'Node 638 class: {workflow.get("638", {}).get("class_type")}')
