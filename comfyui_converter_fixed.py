#!/usr/bin/env python3
"""
ComfyUI Converter - FIXED version with correct widget value mapping.
"""

import json
import requests
from pathlib import Path
from typing import Dict, List, Tuple, Any

class ComfyUIConverter:
    def __init__(self, workflow_path: str):
        self.workflow_path = Path(workflow_path)
        with open(self.workflow_path) as f:
            self.wf = json.load(f)
        self.subgraphs = {}
        for sg in self.wf.get('definitions', {}).get('subgraphs', []):
            self.subgraphs[sg['id']] = sg
        self.next_id = 100
        
    def get_id(self):
        """Get next available node ID."""
        max_id = max([n['id'] for n in self.wf['nodes']], default=0)
        self.next_id = max(self.next_id, max_id + 1)
        node_id = self.next_id
        self.next_id += 1
        return node_id
    
    def _get_widget_index(self, node: Dict, input_name: str) -> int:
        """Get the widget index for a given input name."""
        widget_idx = 0
        for inp in node.get('inputs', []):
            if 'widget' in inp and inp['widget']:
                if inp.get('name') == input_name:
                    return widget_idx
                widget_idx += 1
        return -1
    
    def convert(self, prompt_text=None) -> Dict:
        """Convert workflow to API format."""
        print("\n=== Converting to API Format ===")
        
        api = {}
        sg_info = {}
        links = {link[0]: link for link in self.wf.get('links', [])}
        
        # First pass: Process all non-subgraph nodes
        for node in self.wf['nodes']:
            if node['type'] not in self.subgraphs:
                self._add_node(api, node, links, use_orig_node=node)
        
        # Second pass: Flatten subgraph nodes
        for node in self.wf['nodes']:
            if node['type'] in self.subgraphs:
                print(f"  Flattening subgraph node {node['id']}")
                sg_def = self.subgraphs[node['type']]
                
                # Collect external inputs
                ext_inputs = {}
                for i in range(len(sg_def.get('inputs', []))):
                    for link in self.wf.get('links', []):
                        if link[3] == node['id'] and link[4] == i:
                            ext_inputs[i] = (link[1], link[2])
                            break
                    if i not in ext_inputs and i < len(node.get('widgets_values', [])):
                        ext_inputs[i] = node['widgets_values'][i]
                
                # Flatten subgraph
                output_map = self._flatten_sg(api, sg_def, ext_inputs)
                sg_info[node['id']] = output_map
        
        # Third pass: Update external connections
        for link in self.wf.get('links', []):
            origin_id, origin_slot, target_id, target_slot = link[1], link[2], link[3], link[4]
            
            # If origin is a subgraph output
            if origin_id in sg_info and origin_slot in sg_info[origin_id]:
                new_origin, new_slot = sg_info[origin_id][origin_slot]
                
                # Update target node's input
                target_str = str(target_id)
                if target_str in api:
                    target = api[target_str]
                    for orig_node in self.wf['nodes']:
                        if orig_node['id'] == target_id:
                            if target_slot < len(orig_node.get('inputs', [])):
                                inp_name = orig_node['inputs'][target_slot].get('name')
                                if inp_name:
                                    target['inputs'][inp_name] = [str(new_origin), new_slot]
                            break
        
        # Update prompt
        if prompt_text and '58' in api:
            api['58']['inputs']['value'] = prompt_text
            print(f"  Updated prompt node 58")
        
        return api
    
    def _add_node(self, api: Dict, node: Dict, links: Dict, use_orig_node: Dict = None):
        """Add a node to API."""
        nid = str(node['id'])
        orig_node = use_orig_node or node
        
        api_node = {
            'inputs': {},
            'class_type': node['type']
        }
        
        # Process widget values with CORRECT mapping
        for inp in node.get('inputs', []):
            if 'widget' in inp and inp['widget']:
                inp_name = inp.get('name')
                widget_idx = self._get_widget_index(orig_node, inp_name)
                
                if widget_idx >= 0 and widget_idx < len(orig_node.get('widgets_values', [])):
                    api_node['inputs'][inp_name] = orig_node['widgets_values'][widget_idx]
        
        # Process links
        for inp_idx, inp in enumerate(node.get('inputs', [])):
            if 'link' in inp and inp['link'] is not None:
                link_id = inp['link']
                if link_id in links:
                    link = links[link_id]
                    inp_name = inp.get('name')
                    api_node['inputs'][inp_name] = [str(link[1]), link[2]]
        
        api[nid] = api_node
        print(f"    {nid}: {node['type']}")
    
    def _flatten_sg(self, api: Dict, sg_def: Dict, ext_inputs: Dict) -> Dict:
        """Flatten a subgraph."""
        
        sg_links = {link['id']: link for link in sg_def.get('links', [])}
        
        # Build ID map
        internal_to_new = {}
        for node in sg_def['nodes']:
            old_id = node['id']
            new_id = self.get_id()
            internal_to_new[old_id] = new_id
        
        # Create nodes with correct widget mapping
        for orig_node in sg_def['nodes']:
            old_id = orig_node['id']
            new_id = internal_to_new[old_id]
            nid_str = str(new_id)
            
            api_node = {
                'inputs': {},
                'class_type': orig_node['type']
            }
            
            # Process widget values with CORRECT input name mapping
            for inp in orig_node.get('inputs', []):
                if 'widget' in inp and inp['widget']:
                    inp_name = inp.get('name')
                    # Find this input's position in widget inputs
                    widget_idx = self._get_widget_index(orig_node, inp_name)
                    
                    if widget_idx >= 0 and widget_idx < len(orig_node.get('widgets_values', [])):
                        api_node['inputs'][inp_name] = orig_node['widgets_values'][widget_idx]
            
            # Process links with remapping
            for inp_idx, inp in enumerate(orig_node.get('inputs', [])):
                link_id = inp.get('link')
                if link_id and link_id in sg_links:
                    link = sg_links[link_id]
                    inp_name = inp.get('name')
                    
                    if link['origin_id'] == -10:
                        # External input
                        src_idx = link['origin_slot']
                        if src_idx in ext_inputs:
                            src = ext_inputs[src_idx]
                            if isinstance(src, tuple):
                                api_node['inputs'][inp_name] = [str(src[0]), src[1]]
                            else:
                                api_node['inputs'][inp_name] = src
                    else:
                        # Internal link - remap node ID
                        new_origin = internal_to_new.get(link['origin_id'], link['origin_id'])
                        api_node['inputs'][inp_name] = [str(new_origin), link['origin_slot']]
            
            api[nid_str] = api_node
            print(f"    {nid_str}: {orig_node['type']}")
        
        # Find output mappings
        output_map = {}
        for out_idx, sg_output in enumerate(sg_def.get('outputs', [])):
            for link_id in sg_output.get('linkIds', []):
                if link_id in sg_links:
                    link = sg_links[link_id]
                    new_id = internal_to_new.get(link['origin_id'], link['origin_id'])
                    output_map[out_idx] = (new_id, link['origin_slot'])
        
        return output_map
    
    def submit(self, api_wf: Dict, server="http://192.168.29.60:8188"):
        """Submit to ComfyUI."""
        print(f"\n=== Submitting to ComfyUI ===")
        print(f"  Server: {server}")
        print(f"  Nodes: {len(api_wf)}")
        
        # Remove MarkdownNote
        if '35' in api_wf:
            del api_wf['35']
        
        try:
            resp = requests.post(f"{server}/prompt", json=api_wf, timeout=30)
            
            if resp.status_code == 200:
                result = resp.json()
                prompt_id = result.get('prompt_id')
                print(f"  [SUCCESS] Prompt ID: {prompt_id}")
                return {'success': True, 'prompt_id': prompt_id}
            else:
                print(f"  [ERROR] {resp.status_code}")
                try:
                    err = resp.json()
                    if err.get('node_errors'):
                        for nid, errs in err['node_errors'].items():
                            print(f"    Node {nid}: {errs}")
                except:
                    pass
                return {'success': False, 'error': resp.text}
        except Exception as e:
            print(f"  [ERROR] {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def save(self, api_wf: Dict, path=None) -> str:
        """Save converted workflow."""
        if not path:
            path = self.workflow_path.parent / "z_image_turbo_api.json"
        
        path = Path(path)
        with open(path, 'w') as f:
            json.dump(api_wf, f, indent=2)
        
        print(f"  Saved to: {path}")
        return str(path)


def main():
    print("=" * 70)
    print("ComfyUI Workflow Converter - FIXED Widget Mapping")
    print("=" * 70)
    
    try:
        conv = ComfyUIConverter("\\\\192.168.29.60\\workflows\\image_z_image_turbo.json")
        api_wf = conv.convert(prompt_text="Siena is standing in garden")
        conv.save(api_wf)
        result = conv.submit(api_wf)
        
        print("\n" + "=" * 70)
        if result['success']:
            print(f"[SUCCESS] Prompt ID: {result['prompt_id']}")
            return 0
        else:
            print(f"[FAILED] Error: {result['error'][:150]}")
            return 1
    
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
