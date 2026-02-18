import requests
import json

# Check queue
queue = requests.get('http://192.168.29.60:8188/queue').json()
print('Queue running:', len(queue.get('queue_running', [])))
print('Queue pending:', len(queue.get('queue_pending', [])))

# Check history for our prompt
history = requests.get('http://192.168.29.60:8188/history').json()
prompt_id = 'd1a4920e-10a3-47b0-ad31-c6258b87547e'

if prompt_id in history:
    entry = history[prompt_id]
    print(f'\nPrompt {prompt_id[:8]}...')
    status = entry.get('status', {})
    print(f'Status completed: {status.get("completed", False)}')
    print(f'Status messages: {status.get("status_str", "N/A")}')
    if 'outputs' in entry:
        print(f'Outputs: {list(entry["outputs"].keys())}')
    if status.get('messages'):
        for msg in status['messages'][:3]:
            print(f'  Message: {msg}')
else:
    print(f'\nPrompt {prompt_id[:8]}... NOT found in history')
    print('Last 3 history IDs:')
    for pid in list(history.keys())[:3]:
        entry = history[pid]
        status = entry.get('status', {})
        print(f'  {pid[:12]}... completed={status.get("completed")}')
