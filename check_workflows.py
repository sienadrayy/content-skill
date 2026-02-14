#!/usr/bin/env python3
import json

print("="*80)
print("IMAGES WORKFLOW")
print("="*80)
with open(r'C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Images_workflow.json', encoding='utf-8') as f:
    wf = json.load(f)
    if isinstance(wf, dict):
        if 'nodes' in wf:
            print(f'Format: NEW (graph) - {len(wf.get("nodes", []))} nodes')
        else:
            print(f'Format: OLD (flat) - {len(wf)} top-level entries')
        print(f'Keys: {list(wf.keys())[:5]}')

print("\n" + "="*80)
print("VIDEOS WORKFLOW")
print("="*80)
with open(r'C:\Users\mohit\.openclaw\workspace\comfy-wf\openclaw\Videos_workflow.json', encoding='utf-8', errors='ignore') as f:
    wf = json.load(f)
    if isinstance(wf, dict):
        if 'nodes' in wf:
            print(f'Format: NEW (graph) - {len(wf.get("nodes", []))} nodes')
        else:
            print(f'Format: OLD (flat) - {len(wf)} top-level entries')
        print(f'Keys: {list(wf.keys())[:5]}')
