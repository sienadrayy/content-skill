#!/usr/bin/env python3
"""
ComfyUI UI-format to API-format workflow converter.
Properly handles subgraph flattening and reconnection.
"""

import json
import requests
from pathlib import Path
from typing import Dict, List, Any, Tuple

class ComfyUIWorkflowConverter:
    def __init__(self, workflow_path: str):
        """Initialize converter with workflow path."""
        self.workflow_path = Path(workflow_path)
        self.workflow_data = None
        self.subgraph_definitions = {}
        self.next_node_id = 100
        
    def load_workflow(self) -> Dict:
        """Load workflow from JSON file."""
        print(f"Loading workflow from: {self.workflow_path}")
        with open(self.workflow_path, 'r') as f:
            self.workflow_data = json.load(f)
        
        # Extract subgraph definitions
        if 'definitions' in self.workflow_data and 'subgraphs' in self.workflow_data['definitions']:
            for subgraph in self.workflow_data['definitions']['subgraphs']:
                subgraph_id = subgraph['id']
                self.subgraph_definitions[subgraph_id] = subgraph
                print(f"  Found subgraph: {subgraph_id[:8]}...")
        
        return self.workflow_data
    
    def get_available_node_id(self) -> int:
        """Get next available node ID."""
        current_max = max([node['id'] for node in self.workflow_data['nodes']], default=0)
        self.next_node_id = max(self.next_node_id, current_max + 1)
        node_id = self.next_node_id
        self.next_node_id += 1
        return node_id
    
    def flatten_subgraph_with_values(self, subgraph_node: Dict, subgraph_id: str) -> Tuple[List[Dict], Dict, Dict]:
        """
        Flatten subgraph and build remapping for -10 and -20 nodes.
        Returns: (new_nodes, internal_to_global_ids, input_values_map)
        """
        print(f"  Flattening subgraph {subgraph_id[:8]}...")
        
        subgraph_def = self.subgraph_definitions[subgraph_id]
        new_nodes = []
        internal_to_global = {}
        
        # Step 1: Copy all internal nodes with new global IDs
        for node in subgraph_def['nodes']:
            new_node = json.loads(json.dumps(node))
            old_id = node['id']
            new_id = self.get_available_node_id()
            internal_to_global[old_id] = new_id
            new_node['id'] = new_id
            new_nodes.append(new_node)
        
        # Step 2: Build mapping of subgraph inputs to their values
        # input_idx -> (source_node_id, source_slot) or value
        input_sources = {}
        
        for i, subgraph_input in enumerate(subgraph_def.get('inputs', [])):
            # Check if this input has a link
            external_link = None
            for link in self.workflow_data.get('links', []):
                if link[3] == subgraph_node['id'] and link[4] == i:
                    external_link = (link[1], link[2])  # (source_node, source_slot)
                    break
            
            if external_link:
                input_sources[i] = external_link
            else:
                # Use widget value if available
                if i < len(subgraph_node.get('widgets_values', [])):
                    input_sources[i] = subgraph_node['widgets_values'][i]
        
        # Step 3: Remap internal links within the subgraph
        subgraph_links = {link['id']: link for link in subgraph_def.get('links', [])}
        
        for new_node in new_nodes:
            for inp in new_node.get('inputs', []):
                link_id = inp.get('link')
                if link_id and link_id in subgraph_links:
                    link = subgraph_links[link_id]
                    
                    # Check if this link originates from -10 (input node)
                    if link['origin_id'] == -10:
                        # Replace with actual input source
                        input_idx = link['origin_slot']
                        if input_idx in input_sources:
                            source = input_sources[input_idx]
                            if isinstance(source, tuple):
                                # It's a node reference
                                inp['_external_ref'] = source
                            else:
                                # It's a value
                                inp['_value'] = source
                        inp['link'] = None  # Clear the internal link
                    else:
                        # Internal link - remap node ID
                        new_origin_id = internal_to_global.get(link['origin_id'], link['origin_id'])
                        inp['_internal_link'] = (new_origin_id, link['origin_slot'])
                        inp['link'] = None
        
        # Step 4: Find which internal node provides the output
        output_sources = {}
        for i, subgraph_output in enumerate(subgraph_def.get('outputs', [])):
            link_ids = subgraph_output.get('linkIds', [])
            for link_id in link_ids:
                if link_id in subgraph_links:
                    link = subgraph_links[link_id]
                    new_origin_id = internal_to_global.get(link['origin_id'], link['origin_id'])
                    output_sources[i] = (new_origin_id, link['origin_slot'])
        
        return new_nodes, internal_to_global, input_sources, output_sources
    
    def convert_to_api_format(self, update_prompt: str = None) -> Dict:
        """Convert UI workflow to API format."""
        print("\n=== Converting Workflow to API Format ===")
        
        api_workflow = {}
        subgraph_outputs = {}  # Track subgraph output node sources
        
        # Build link map for main workflow
        link_map = {}
        for link in self.workflow_data.get('links', []):
            link_map[link[0]] = link
        
        # Process nodes
        subgraph_node_ids = {}
        for node in self.workflow_data['nodes']:
            if node['type'] in self.subgraph_definitions:
                print(f"  Processing subgraph node {node['id']}")
                subgraph_node_ids[node['id']] = node['type']
                
                # Flatten it
                flattened, id_map, input_srcs, output_srcs = self.flatten_subgraph_with_values(
                    node, node['type']
                )
                subgraph_outputs[node['id']] = output_srcs
                
                # Add flattened nodes to API format
                for flat_node in flattened:
                    self._node_to_api(api_workflow, flat_node, link_map, input_srcs, id_map)
            else:
                # Regular node
                self._node_to_api(api_workflow, node, link_map)
        
        # Step 2: Reconnect external links
        for link in self.workflow_data.get('links', []):
            origin_id = link[1]
            origin_slot = link[2]
            target_id = link[3]
            target_slot = link[4]
            
            # If origin is a subgraph, find its output source
            if origin_id in subgraph_node_ids and origin_id in subgraph_outputs:
                if origin_slot in subgraph_outputs[origin_id]:
                    new_origin_id, new_origin_slot = subgraph_outputs[origin_id][origin_slot]
                    origin_id = new_origin_id
                    origin_slot = new_origin_slot
                else:
                    continue
            
            # Update target node's input
            if target_id not in subgraph_node_ids:
                target_node_str = str(target_id)
                if target_node_str in api_workflow:
                    target_node = api_workflow[target_node_str]
                    
                    # Find the input by slot
                    for orig_node in self.workflow_data['nodes']:
                        if orig_node['id'] == target_id:
                            if target_slot < len(orig_node.get('inputs', [])):
                                inp_item = orig_node['inputs'][target_slot]
                                inp_name = inp_item.get('name')
                                if inp_name:
                                    target_node['inputs'][inp_name] = [str(origin_id), origin_slot]
                            break
        
        # Update prompt
        if update_prompt:
            self._update_prompt_node(api_workflow, update_prompt)
        
        return api_workflow
    
    def _node_to_api(self, api_workflow: Dict, node: Dict, link_map: Dict = None, 
                     input_srcs: Dict = None, internal_id_map: Dict = None):
        """Convert a node to API format."""
        node_id = str(node['id'])
        api_node = {
            "inputs": {},
            "class_type": node['type']
        }
        
        # Add widget values
        if 'widgets_values' in node:
            widget_vals = node['widgets_values']
            widget_idx = 0
            
            for inp in node.get('inputs', []):
                if 'widget' in inp and inp['widget']:
                    if widget_idx < len(widget_vals):
                        inp_name = inp.get('name', f'input_{widget_idx}')
                        api_node['inputs'][inp_name] = widget_vals[widget_idx]
                        widget_idx += 1
            
            # Add remaining widgets
            while widget_idx < len(widget_vals):
                api_node['inputs'][f'widget_{widget_idx}'] = widget_vals[widget_idx]
                widget_idx += 1
        
        # Process inputs with links
        for idx, inp in enumerate(node.get('inputs', [])):
            inp_name = inp.get('name', f'input_{idx}')
            
            # Check for _external_ref (from flattened subgraph)
            if '_external_ref' in inp:
                ext_node, ext_slot = inp['_external_ref']
                api_node['inputs'][inp_name] = [str(ext_node), ext_slot]
            
            # Check for _internal_link (from flattened subgraph)
            elif '_internal_link' in inp:
                int_node, int_slot = inp['_internal_link']
                api_node['inputs'][inp_name] = [str(int_node), int_slot]
            
            # Check for _value (constant from flattened subgraph)
            elif '_value' in inp:
                api_node['inputs'][inp_name] = inp['_value']
            
            # Regular link from workflow
            elif link_map and 'link' in inp and inp['link'] is not None:
                link_id = inp['link']
                if link_id in link_map:
                    link = link_map[link_id]
                    api_node['inputs'][inp_name] = [str(link[1]), link[2]]
        
        api_workflow[node_id] = api_node
        print(f"    Node {node_id}: {node['type']}")
    
    def _update_prompt_node(self, api_workflow: Dict, new_prompt: str):
        """Update prompt node 58."""
        print(f"  Updating prompt node 58")
        if '58' in api_workflow:
            api_workflow['58']['inputs']['value'] = new_prompt
    
    def submit_to_comfyui(self, api_workflow: Dict, server_url: str = "http://192.168.29.60:8188") -> Dict:
        """Submit workflow to ComfyUI API."""
        print(f"\n=== Submitting to ComfyUI ===")
        print(f"  Server: {server_url}")
        
        try:
            response = requests.post(
                f"{server_url}/prompt",
                json=api_workflow,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  [SUCCESS] Workflow submitted!")
                print(f"  Prompt ID: {result.get('prompt_id')}")
                return {
                    'success': True,
                    'prompt_id': result.get('prompt_id'),
                    'response': result
                }
            else:
                print(f"  [ERROR] HTTP {response.status_code}")
                print(f"  Response: {response.text[:300]}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                    'response': response.text
                }
        except Exception as e:
            print(f"  [ERROR] {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def save_api_workflow(self, api_workflow: Dict, output_path: str = None) -> str:
        """Save converted workflow."""
        if output_path is None:
            output_path = self.workflow_path.parent / "z_image_turbo_api.json"
        
        output_path = Path(output_path)
        with open(output_path, 'w') as f:
            json.dump(api_workflow, f, indent=2)
        
        print(f"  Saved to: {output_path}")
        return str(output_path)


def main():
    """Main execution."""
    
    print("=" * 70)
    print("ComfyUI Workflow Converter - UI to API Format")
    print("=" * 70)
    
    try:
        converter = ComfyUIWorkflowConverter(
            "\\\\192.168.29.60\\workflows\\image_z_image_turbo.json"
        )
        
        converter.load_workflow()
        api_wf = converter.convert_to_api_format(update_prompt="Siena is standing in garden")
        converter.save_api_workflow(api_wf)
        result = converter.submit_to_comfyui(api_wf)
        
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        if result['success']:
            print(f"[OK] Success!")
            print(f"     Prompt ID: {result['prompt_id']}")
            return 0
        else:
            print(f"[FAIL] {result.get('error')}")
            return 1
    
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
