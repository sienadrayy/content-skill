import json

with open('test_workflow_output.json', 'r', encoding='utf-8') as f:
    workflow = json.load(f)

print('[TEST WORKFLOW VERIFICATION]')
print(f'Format: Valid JSON')
print(f'Total nodes: {len(workflow)}')
print()
print('Injected Prompts:')
node443_val = workflow['443']['inputs']['value']
node500_val = workflow['500']['inputs']['value']
print(f'Node 443 (Images): {node443_val[:60]}...')
print(f'Node 500 (Videos): {node500_val[:60]}...')
print()
print('[OK] Workflow ready for ComfyUI')
print(f'File: test_workflow_output.json')
