#!/usr/bin/env python3
"""
Generic ComfyUI Workflow Submitter - works with any UI or API format workflow
"""

import json
import sys
import urllib.request
import urllib.error
import argparse
import traceback

sys.stdout.reconfigure(encoding='utf-8')

def load_and_convert_workflow(workflow_path):
    """Load workflow and convert UI format to API format if needed"""
    import re
    
    with open(workflow_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check if it's UI format (has 'nodes' key with list of node objects)
    if isinstance(data, dict) and 'nodes' in data and isinstance(data.get('nodes'), list):
        print("  Converting UI format to API format...")
        api_workflow = {}
        
        # UUID pattern for detecting subgraph nodes
        uuid_pattern = re.compile(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$')
        
        for node in data['nodes']:
            try:
                if not isinstance(node, dict) or 'id' not in node:
                    continue
                
                node_id = str(node['id'])
                node_type = node.get('type') or node.get('class_type', 'Unknown')
                
                # Skip subgraph nodes (have UUID as class_type)
                if uuid_pattern.match(str(node_type)):
                    print(f"  Skipping subgraph node {node_id} ({node_type})")
                    continue
                
                # Skip UI-only nodes
                if node_type in ['MarkdownNote', 'Note', 'Reroute']:
                    continue
                
                # Skip custom extension nodes (contain parentheses like "Custom Node (author)")
                if '(' in str(node_type) and ')' in str(node_type):
                    print(f"  Skipping custom node {node_id} ({node_type})")
                    continue
                
                # Skip preview/debug nodes
                if node_type in ['PreviewImage', 'PreviewAny', 'easy showAnything', 'easy XYInputs', 'easy dynamicCast']:
                    print(f"  Skipping preview node {node_id} ({node_type})")
                    continue
                
                api_node = {
                    "inputs": {},
                    "class_type": node_type
                }
                
                # Process inputs
                if 'inputs' in node and isinstance(node['inputs'], list):
                    widget_values = node.get('widgets_values', [])
                    widget_idx = 0
                    
                    for inp in node['inputs']:
                        if not isinstance(inp, dict):
                            continue
                        
                        inp_name = inp.get('name', '')
                        if not inp_name:
                            continue
                        
                        # If input has a link to another node
                        if 'link' in inp and inp['link'] is not None:
                            api_node['inputs'][inp_name] = [str(inp['link']), inp.get('slot_index', 0)]
                        # Otherwise use widget value
                        elif 'widget' in inp:
                            if widget_idx < len(widget_values):
                                api_node['inputs'][inp_name] = widget_values[widget_idx]
                                widget_idx += 1
                
                api_workflow[node_id] = api_node
            except Exception as e:
                print(f"  Warning: Error processing node {node.get('id')}: {e}")
                continue
        
        return api_workflow
    
    # Otherwise assume it's already API format
    elif isinstance(data, dict):
        if 'prompt' in data:
            return data['prompt']
        # If keys are all numeric (node IDs), it's API format
        if all(str(k).isdigit() for k in data.keys()):
            return data
        return data
    
    return data

def find_and_update_prompt(workflow, prompt_text, node_id=None, input_key=None):
    """Find and update prompt node"""
    
    # If specific node/key provided, use it
    if node_id and input_key:
        node_id = str(node_id)
        if node_id in workflow and input_key in workflow[node_id].get('inputs', {}):
            workflow[node_id]['inputs'][input_key] = prompt_text
            print(f"  Updated node {node_id}/{input_key}")
            return True
        else:
            print(f"  ERROR: Node {node_id} or key {input_key} not found")
            return False
    
    # Otherwise auto-find prompt node (prioritize PrimitiveStringMultiline with 'value')
    candidates = []
    for nid, ndata in workflow.items():
        if not isinstance(ndata, dict) or 'inputs' not in ndata:
            continue
        
        inputs = ndata.get('inputs', {})
        if not isinstance(inputs, dict):
            continue
        
        class_type = ndata.get('class_type', '')
        
        # Highest priority: PrimitiveStringMultiline with value
        if class_type == 'PrimitiveStringMultiline' and 'value' in inputs:
            candidates.append((0, nid, 'value'))  # priority 0 (highest)
        # Medium priority: other string inputs
        elif any(k in inputs for k in ['text', 'prompt']):
            for k in ['text', 'prompt']:
                if k in inputs:
                    candidates.append((1, nid, k))
    
    if candidates:
        candidates.sort()  # Sort by priority
        _, best_node_id, best_key = candidates[0]
        workflow[str(best_node_id)]['inputs'][best_key] = prompt_text
        print(f"  Updated node {best_node_id}/{best_key}")
        return True
    
    print(f"  ERROR: Could not find any prompt node")
    return False

def submit_workflow(workflow, server_url):
    """Submit workflow to ComfyUI"""
    url = f"{server_url}/prompt"
    
    payload = {"prompt": workflow}
    payload_str = json.dumps(payload)
    
    req = urllib.request.Request(
        url,
        data=payload_str.encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            prompt_id = result.get('prompt_id')
            if prompt_id:
                print(f"  Prompt ID: {prompt_id}")
                return prompt_id
            else:
                print(f"  ERROR: {result}")
                return None
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"  Details: {error_body}")
        except:
            pass
        return None
    except Exception as e:
        print(f"  ERROR: {e}")
        traceback.print_exc()
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Submit ComfyUI workflow with custom prompt',
        epilog="""
Examples:
  python submit_workflow_with_prompt.py \\\\192.168.29.60\\workflows\\Images_workflow.json "Siena standing in a garden"
  python submit_workflow_with_prompt.py \\\\192.168.29.60\\workflows\\Videos_workflow.json "Woman dancing" --node-id 436 --input-key value
        """
    )
    
    parser.add_argument('workflow', help='Workflow JSON path (local or UNC)')
    parser.add_argument('prompt', help='Prompt text to use')
    parser.add_argument('--server', default='http://192.168.29.60:8188', help='ComfyUI server URL')
    parser.add_argument('--node-id', help='Specific node ID for prompt')
    parser.add_argument('--input-key', help='Specific input key (default: auto-detect)')
    
    args = parser.parse_args()
    
    print("\n" + "=" * 75)
    print("ComfyUI Workflow Submitter")
    print("=" * 75)
    
    try:
        # Load
        print(f"\n1. Loading workflow...")
        workflow = load_and_convert_workflow(args.workflow)
        print(f"   {len(workflow)} nodes loaded")
        
        # Update prompt
        print(f"\n2. Updating prompt...")
        if not find_and_update_prompt(workflow, args.prompt, args.node_id, args.input_key):
            return 1
        
        # Submit
        print(f"\n3. Submitting to {args.server}...")
        prompt_id = submit_workflow(workflow, args.server)
        
        print("\n" + "=" * 75)
        if prompt_id:
            print("SUCCESS")
            return 0
        else:
            print("FAILED")
            return 1
    
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
