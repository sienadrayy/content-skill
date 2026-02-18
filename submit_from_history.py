import requests
import json

# Get a workflow from history
resp = requests.get('http://192.168.29.60:8188/history')
data = resp.json()

if data:
    first_id = list(data.keys())[0]
    first_entry = data[first_id]
    workflow_dict = first_entry['prompt'][2]  # Extract just the nodes dict
    
    print(f"Submitting workflow from history (ID: {first_id[:8]}...)")
    print(f"Nodes in workflow: {len(workflow_dict)}")
    
    # Submit
    response = requests.post('http://192.168.29.60:8188/prompt', json=workflow_dict)
    print(f"\nStatus: {response.status_code}")
    result = response.json()
    if 'prompt_id' in result:
        print(f"✓ SUCCESS - Prompt ID: {result['prompt_id']}")
    else:
        print(f"Response: {json.dumps(result, indent=2)[:500]}")
