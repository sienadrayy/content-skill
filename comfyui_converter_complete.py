#!/usr/bin/env python3
"""
ComfyUI UI-format to API-format workflow converter.
Complete version with proper widget value handling and subgraph flattening.
"""

import json
import requests
from pathlib import Path
from typing import Dict, List, Tuple, Any

class ComfyUIWorkflowConverter:
    def __init__(self, workflow_path: str):
        """Initialize converter."""
        self.workflow_path = Path(workflow_path)
        self.workflow_data = None
        self.subgraph_defs = {}
        self.next_node_id = 100
        
    def load_workflow(self):
        """Load and parse workflow."""
        print(f"Loading: {self.workflow_path}")
        with open(self.workflow_path) as f:
            self.workflow_data = json.load(f)
        
        # Extract subgraphs
        for sg in self.workflow_data.get('definitions', {}).get('subgraphs', []):
            self.subgraph_defs[sg['id']] = sg
            print(f"  Subgraph: {sg['id'][:8]}...")
    
    def get_node_id(self):
        """Get next available node ID."""
        max_id = max([n['id'] for n in self.workflow_data['nodes']], default=0)
        self.next_node_id = max(self.next_node_id, max_id + 1)
        node_id = self.next_node_id
        self.next_node_id += 1
        return node_id
    
    def convert(self, update_prompt=None) -> Dict:
        """Convert UI workflow to API format."""
        print("\n=== Converting to API Format ===")
        
        api_wf = {}
        sg_node_ids = {}  # Track subgraph nodes
        sg_outputs = {}   # Track their outputs
        
        # Build link map
        links = {link[0]: link for link in self.workflow_data.get('links', [])}
        
        # Process each node
        for node in self.workflow_data['nodes']:
            nid = node['id']
            ntype = node['type']
            
            if ntype in self.subgraph_defs:
                # It's a subgraph - flatten it
                sg_node_ids[nid] = ntype
                sg_def = self.subgraph_defs[ntype]
                
                # Collect external inputs to the subgraph
                sg_inputs = self._collect_sg_inputs(node, sg_def, links)
                
                # Flatten and add nodes
                sg_outputs[nid], internal_id_map = self._flatten_sg(
                    node, sg_def, sg_inputs, api_wf
                )
            else:
                # Regular node
                self._add_node(api_wf, node, links)
        
        # Reconnect external links
        self._reconnect_sg_outputs(api_wf, sg_node_ids, sg_outputs, links)
        
        # Update prompt
        if update_prompt:
            if '58' in api_wf:
                api_wf['58']['inputs']['value'] = update_prompt
                print(f"  Updated prompt node 58")
        
        return api_wf
    
    def _collect_sg_inputs(self, sg_node: Dict, sg_def: Dict, links: Dict) -> Dict:
        """Collect external input values for a subgraph."""
        inputs = {}
        
        for i, sg_input in enumerate(sg_def.get('inputs', [])):
            # Check for external link
            ext_link = None
            for link in self.workflow_data.get('links', []):
                if link[3] == sg_node['id'] and link[4] == i:
                    ext_link = (link[1], link[2])
                    break
            
            if ext_link:
                inputs[i] = ext_link
            elif i < len(sg_node.get('widgets_values', [])):
                inputs[i] = sg_node['widgets_values'][i]
        
        return inputs
    
    def _flatten_sg(self, sg_node: Dict, sg_def: Dict, sg_inputs: Dict, api_wf: Dict) -> Tuple[Dict, Dict]:
        """Flatten a subgraph into nodes."""
        print(f"  Flattening {sg_def['id'][:8]}...")
        
        internal_to_global = {}
        output_sources = {}
        
        # Copy and remap internal nodes
        for node in sg_def['nodes']:
            old_id = node['id']
            new_id = self.get_node_id()
            internal_to_global[old_id] = new_id
            
            new_node = json.loads(json.dumps(node))
            new_node['id'] = new_id
            
            # Mark for later processing
            new_node['_sg_remapping'] = {
                'sg_inputs': sg_inputs,
                'internal_to_global': internal_to_global,
                'sg_def': sg_def
            }
            
            self._add_node(api_wf, new_node, {})
        
        # Find output sources
        for i, sg_output in enumerate(sg_def.get('outputs', [])):
            for link_id in sg_output.get('linkIds', []):
                for link in sg_def.get('links', []):
                    if link['id'] == link_id:
                        new_id = internal_to_global.get(link['origin_id'], link['origin_id'])
                        output_sources[i] = (new_id, link['origin_slot'])
        
        return output_sources, internal_to_global
    
    def _add_node(self, api_wf: Dict, node: Dict, links: Dict):
        """Add a node to API workflow."""
        nid = str(node['id'])
        api_node = {
            'inputs': {},
            'class_type': node['type']
        }
        
        # Process inputs
        sg_remap = node.get('_sg_remapping', {})
        sg_inputs = sg_remap.get('sg_inputs', {})
        sg_def = sg_remap.get('sg_def', {})
        internal_to_global = sg_remap.get('internal_to_global', {})
        
        sg_links = {}
        if sg_def:
            # This is a flattened subgraph node
            sg_links = {link['id']: link for link in sg_def.get('links', [])}
        
        for inp_idx, inp in enumerate(node.get('inputs', [])):
            inp_name = inp.get('name', f'input_{inp_idx}')
            link_id = inp.get('link')
            
            if sg_links and link_id and link_id in sg_links:
                # Internal subgraph link
                link = sg_links[link_id]
                if link['origin_id'] == -10:
                    # From external input
                    src_idx = link['origin_slot']
                    if src_idx in sg_inputs:
                        src = sg_inputs[src_idx]
                        if isinstance(src, tuple):
                            api_node['inputs'][inp_name] = [str(src[0]), src[1]]
                        else:
                            api_node['inputs'][inp_name] = src
                else:
                    # From internal node
                    new_origin = internal_to_global.get(link['origin_id'], link['origin_id'])
                    api_node['inputs'][inp_name] = [str(new_origin), link['origin_slot']]
            elif 'widget' in inp and inp['widget']:
                # Widget input
                widget_idx = self._find_widget_index(node, inp_name)
                if widget_idx is not None and widget_idx < len(node.get('widgets_values', [])):
                    api_node['inputs'][inp_name] = node['widgets_values'][widget_idx]
            elif link_id and link_id in links:
                # External link
                link = links[link_id]
                api_node['inputs'][inp_name] = [str(link[1]), link[2]]
        
        api_wf[nid] = api_node
        print(f"    {nid}: {node['type']}")
    
    def _find_widget_index(self, node: Dict, input_name: str) -> int:
        """Find the index of a widget input in widget_values."""
        widget_idx = 0
        for inp in node.get('inputs', []):
            if 'widget' in inp and inp['widget']:
                if inp.get('name') == input_name:
                    return widget_idx
                widget_idx += 1
        return None
    
    def _reconnect_sg_outputs(self, api_wf: Dict, sg_node_ids: Dict, sg_outputs: Dict, links: Dict):
        """Reconnect subgraph outputs to external nodes."""
        for link in self.workflow_data.get('links', []):
            origin_id = link[1]
            target_id = link[3]
            
            if origin_id in sg_node_ids and origin_id in sg_outputs:
                origin_slot = link[2]
                if origin_slot in sg_outputs[origin_id]:
                    new_origin, new_slot = sg_outputs[origin_id][origin_slot]
                    
                    target_str = str(target_id)
                    if target_str in api_wf:
                        target_node = api_wf[target_str]
                        target_slot = link[4]
                        
                        # Find input name
                        for orig_node in self.workflow_data['nodes']:
                            if orig_node['id'] == target_id:
                                if target_slot < len(orig_node.get('inputs', [])):
                                    inp_item = orig_node['inputs'][target_slot]
                                    inp_name = inp_item.get('name')
                                    if inp_name:
                                        target_node['inputs'][inp_name] = [str(new_origin), new_slot]
                                break
    
    def submit(self, api_wf: Dict, server="http://192.168.29.60:8188") -> Dict:
        """Submit workflow to ComfyUI."""
        print(f"\n=== Submitting to ComfyUI ===")
        print(f"  Server: {server}")
        
        try:
            resp = requests.post(f"{server}/prompt", json=api_wf, timeout=30)
            
            if resp.status_code == 200:
                result = resp.json()
                print(f"  [SUCCESS] Prompt ID: {result.get('prompt_id')}")
                return {'success': True, 'prompt_id': result.get('prompt_id')}
            else:
                print(f"  [ERROR] {resp.status_code}: {resp.text[:200]}")
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
        
        print(f"  Saved: {path}")
        return str(path)


def main():
    print("=" * 70)
    print("ComfyUI Workflow Converter")
    print("=" * 70)
    
    try:
        conv = ComfyUIWorkflowConverter("\\\\192.168.29.60\\workflows\\image_z_image_turbo.json")
        conv.load_workflow()
        
        api_wf = conv.convert(update_prompt="Siena is standing in garden")
        
        # Remove MarkdownNote if present
        if '35' in api_wf and api_wf['35']['class_type'] == 'MarkdownNote':
            del api_wf['35']
        
        conv.save(api_wf)
        result = conv.submit(api_wf)
        
        print("\n" + "=" * 70)
        if result['success']:
            print(f"SUCCESS: Prompt ID {result['prompt_id']}")
            return 0
        else:
            print(f"FAILED: {result['error'][:100]}")
            return 1
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
