#!/usr/bin/env python3
"""
ComfyUI UI-format to API-format workflow converter.
Properly handles subgraph flattening and API submission.
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
        self.node_id_map = {}  # Maps old node IDs to new ones
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
                print(f"  Found subgraph: {subgraph_id}")
        
        return self.workflow_data
    
    def get_available_node_id(self) -> int:
        """Get next available node ID."""
        current_max = max([node['id'] for node in self.workflow_data['nodes']], default=0)
        self.next_node_id = max(self.next_node_id, current_max + 1)
        node_id = self.next_node_id
        self.next_node_id += 1
        return node_id
    
    def _find_link_for_subgraph_input(self, subgraph_def: Dict, input_index: int) -> Tuple[int, int, int, int]:
        """
        Find the internal node that connects to a subgraph input.
        Returns: (origin_id, origin_slot, target_id, target_slot)
        """
        if input_index >= len(subgraph_def.get('inputs', [])):
            return None
        
        input_def = subgraph_def['inputs'][input_index]
        link_ids = input_def.get('linkIds', [])
        
        # Find the first link connected to this input
        for link_id in link_ids:
            for link in subgraph_def.get('links', []):
                if link['id'] == link_id:
                    return link
        return None
    
    def _find_output_connection(self, subgraph_def: Dict, output_index: int) -> Dict:
        """
        Find which internal node feeds the subgraph output.
        """
        if output_index >= len(subgraph_def.get('outputs', [])):
            return None
        
        output_def = subgraph_def['outputs'][output_index]
        link_ids = output_def.get('linkIds', [])
        
        # Find the first link connected to this output
        for link_id in link_ids:
            for link in subgraph_def.get('links', []):
                if link['id'] == link_id:
                    return link
        return None
    
    def flatten_subgraph(self, subgraph_node: Dict, subgraph_id: str) -> Tuple[List[Dict], Dict]:
        """
        Flatten a subgraph into individual nodes.
        Returns: (new_nodes, internal_node_id_map)
        """
        print(f"\n  Flattening subgraph {subgraph_id[:8]}...")
        
        if subgraph_id not in self.subgraph_definitions:
            raise ValueError(f"Subgraph {subgraph_id} not found in definitions")
        
        subgraph_def = self.subgraph_definitions[subgraph_id]
        new_nodes = []
        internal_to_global = {}  # Map internal node IDs to new global IDs
        
        # Step 1: Copy all nodes and assign new IDs
        for node in subgraph_def['nodes']:
            new_node = json.loads(json.dumps(node))  # Deep copy
            old_id = node['id']
            new_id = self.get_available_node_id()
            internal_to_global[old_id] = new_id
            new_node['id'] = new_id
            new_nodes.append(new_node)
        
        # Step 2: Build a map of links within the subgraph
        subgraph_links = {link['id']: link for link in subgraph_def.get('links', [])}
        
        # Step 3: Update links in nodes
        for new_node in new_nodes:
            if 'inputs' in new_node:
                for input_item in new_node.get('inputs', []):
                    if 'link' in input_item and input_item['link'] is not None:
                        link_id = input_item['link']
                        if link_id in subgraph_links:
                            link = subgraph_links[link_id]
                            # Remap the origin node ID
                            old_origin_id = link['origin_id']
                            new_origin_id = internal_to_global.get(old_origin_id, old_origin_id)
                            # Store as reference for later
                            input_item['_link_ref'] = (new_origin_id, link['origin_slot'])
        
        # Step 4: Connect external inputs to internal nodes
        for i, subgraph_input in enumerate(subgraph_def.get('inputs', [])):
            link_ids = subgraph_input.get('linkIds', [])
            for link_id in link_ids:
                if link_id in subgraph_links:
                    link = subgraph_links[link_id]
                    target_node_id = link['target_id']
                    target_input_slot = link['target_slot']
                    global_target_id = internal_to_global.get(target_node_id)
                    
                    # Find the target node and input
                    for new_node in new_nodes:
                        if new_node['id'] == global_target_id:
                            inputs = new_node.get('inputs', [])
                            if target_input_slot < len(inputs):
                                # Mark this input for external connection
                                inputs[target_input_slot]['_external_source'] = (
                                    subgraph_node['id'], i
                                )
        
        print(f"    Created {len(new_nodes)} nodes")
        return new_nodes, internal_to_global
    
    def convert_to_api_format(self, update_prompt: str = None) -> Dict:
        """Convert UI workflow to API format."""
        print("\n=== Converting Workflow to API Format ===")
        
        api_workflow = {}
        
        # Build link map for main workflow
        link_map = {}
        for link in self.workflow_data.get('links', []):
            link_map[link[0]] = link  # link[0] is the ID
        
        # Track which nodes need to be replaced (subgraphs)
        subgraph_node_ids = {}
        subgraph_output_mappings = {}
        subgraph_input_mappings = {}  # Map subgraph node ID -> (input_node_id, node_type)
        
        # Process all nodes
        for node in self.workflow_data['nodes']:
            node_id = node['id']
            node_type = node['type']
            
            # Check if this is a subgraph node
            if node_type in self.subgraph_definitions:
                print(f"  Processing subgraph node {node_id}")
                subgraph_node_ids[node_id] = node_type
                
                # Flatten it
                flattened_nodes, id_map = self.flatten_subgraph(node, node_type)
                subgraph_info = {
                    'nodes': flattened_nodes,
                    'id_map': id_map,
                    'subgraph_def': self.subgraph_definitions[node_type],
                    'subgraph_node': node
                }
                subgraph_output_mappings[node_id] = subgraph_info
                subgraph_input_mappings[node_id] = node_type
                
                # Add flattened nodes
                for flat_node in flattened_nodes:
                    self._add_node_to_api(api_workflow, flat_node, link_map, subgraph_info)
            else:
                # Regular node
                self._add_node_to_api(api_workflow, node, link_map)
        
        # Step 2: Remap internal subgraph node references
        # Replace -10 (input node) with actual external input
        # Replace -20 (output node) with actual consumer
        for subgraph_node_id, subgraph_info in subgraph_output_mappings.items():
            subgraph_def = subgraph_info['subgraph_def']
            id_map = subgraph_info['id_map']
            subgraph_node = subgraph_info['subgraph_node']
            
            # Find connections from external inputs to subgraph input node (-10)
            for i, subgraph_input in enumerate(subgraph_def.get('inputs', [])):
                # Find which external node feeds this input
                external_source = None
                for link in self.workflow_data.get('links', []):
                    if link[3] == subgraph_node_id and link[4] == i:  # target is subgraph input slot
                        external_source = (link[1], link[2])  # (source_node, source_slot)
                        break
                
                # Now remap all internal references from -10 to this external source
                if external_source:
                    self._remap_subgraph_input(api_workflow, subgraph_def, id_map, i, external_source)
            
            # Find connections from subgraph output node (-20) to external nodes
            for link in self.workflow_data.get('links', []):
                if link[1] == subgraph_node_id:  # origin is subgraph output
                    output_slot = link[2]
                    target_node_id = link[3]
                    target_slot = link[4]
                    
                    # Find which internal node produces this output
                    output_link = self._find_output_connection(subgraph_def, output_slot)
                    if output_link and target_node_id not in subgraph_node_ids:
                        internal_origin_id = output_link['origin_id']
                        new_origin_id = id_map.get(internal_origin_id, internal_origin_id)
                        
                        # Update the target node
                        target_node_str = str(target_node_id)
                        if target_node_str in api_workflow:
                            target_node = api_workflow[target_node_str]
                            # Find the input name
                            for orig_node in self.workflow_data['nodes']:
                                if orig_node['id'] == target_node_id:
                                    if target_slot < len(orig_node.get('inputs', [])):
                                        input_item = orig_node['inputs'][target_slot]
                                        input_name = input_item.get('name')
                                        if input_name:
                                            target_node['inputs'][input_name] = [str(new_origin_id), output_link['origin_slot']]
                                    break
        
        # Update prompt node if specified
        if update_prompt:
            self._update_prompt_node(api_workflow, update_prompt)
        
        return api_workflow
    
    def _remap_subgraph_input(self, api_workflow: Dict, subgraph_def: Dict, id_map: Dict, 
                             input_idx: int, external_source: Tuple[int, int]):
        """Remap subgraph input node (-10) references to external source."""
        external_node_id, external_slot = external_source
        
        # Find all links from -10 to internal nodes
        for link in subgraph_def.get('links', []):
            if link['origin_id'] == -10 and link['origin_slot'] == input_idx:
                # This link needs to be updated
                target_id = link['target_id']
                new_target_id = id_map.get(target_id, target_id)
                target_node_str = str(new_target_id)
                
                if target_node_str in api_workflow:
                    target_node = api_workflow[target_node_str]
                    # Find the input that uses this link
                    for node_def in subgraph_def['nodes']:
                        if node_def['id'] == target_id:
                            for input_item in node_def.get('inputs', []):
                                if input_item.get('link') == link['id']:
                                    input_name = input_item.get('name')
                                    if input_name:
                                        target_node['inputs'][input_name] = [str(external_node_id), external_slot]
                            break
    
    def _add_node_to_api(self, api_workflow: Dict, node: Dict, link_map: Dict = None, subgraph_info: Dict = None):
        """Add a node to the API workflow format."""
        node_id = str(node['id'])
        
        api_node = {
            "inputs": {},
            "class_type": node['type']
        }
        
        # Extract widget values
        if 'widgets_values' in node:
            widget_values = node['widgets_values']
            widget_idx = 0
            
            # Match widgets with inputs
            for input_item in node.get('inputs', []):
                if 'widget' in input_item and input_item['widget']:
                    if widget_idx < len(widget_values):
                        input_name = input_item.get('name', f'input_{widget_idx}')
                        api_node['inputs'][input_name] = widget_values[widget_idx]
                        widget_idx += 1
            
            # Add remaining widget values
            while widget_idx < len(widget_values):
                api_node['inputs'][f'widget_{widget_idx}'] = widget_values[widget_idx]
                widget_idx += 1
        
        # Process input links
        if link_map:
            for idx, input_item in enumerate(node.get('inputs', [])):
                link_id = input_item.get('link')
                if link_id is not None and link_id in link_map:
                    link = link_map[link_id]
                    origin_id = str(link[1])
                    origin_slot = link[2]
                    input_name = input_item.get('name', f'input_{idx}')
                    api_node['inputs'][input_name] = [origin_id, origin_slot]
        
        # Handle external source markers from flattening
        for idx, input_item in enumerate(node.get('inputs', [])):
            if '_link_ref' in input_item:
                origin_id, origin_slot = input_item['_link_ref']
                input_name = input_item.get('name', f'input_{idx}')
                api_node['inputs'][input_name] = [str(origin_id), origin_slot]
        
        api_workflow[node_id] = api_node
        print(f"    Node {node_id}: {node['type']}")
    
    def _update_prompt_node(self, api_workflow: Dict, new_prompt: str):
        """Update the prompt node (ID 58) with new text."""
        print(f"\n  Updating prompt node 58")
        target_node = api_workflow.get('58')
        if target_node:
            if 'value' in target_node['inputs']:
                target_node['inputs']['value'] = new_prompt
            else:
                target_node['inputs']['value'] = new_prompt
            print(f"    Updated prompt")
    
    def submit_to_comfyui(self, api_workflow: Dict, server_url: str = "http://192.168.29.60:8188") -> Dict:
        """Submit the converted workflow to ComfyUI API."""
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
                print(f"  Response: {response.text[:200]}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                    'response': response.text
                }
        except requests.exceptions.RequestException as e:
            print(f"  [ERROR] Connection failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def save_api_workflow(self, api_workflow: Dict, output_path: str = None) -> str:
        """Save the converted API workflow to a JSON file."""
        if output_path is None:
            output_path = self.workflow_path.parent / "z_image_turbo_api.json"
        
        output_path = Path(output_path)
        with open(output_path, 'w') as f:
            json.dump(api_workflow, f, indent=2)
        
        print(f"  Saved API workflow to: {output_path}")
        return str(output_path)


def main():
    """Main execution function."""
    
    # Configuration
    workflow_path = "\\\\192.168.29.60\\workflows\\image_z_image_turbo.json"
    new_prompt = "Siena is standing in garden"
    comfyui_server = "http://192.168.29.60:8188"
    
    print("=" * 70)
    print("ComfyUI Workflow Converter - UI to API Format")
    print("=" * 70)
    
    try:
        # Initialize and run converter
        converter = ComfyUIWorkflowConverter(workflow_path)
        converter.load_workflow()
        api_workflow = converter.convert_to_api_format(update_prompt=new_prompt)
        converter.save_api_workflow(api_workflow)
        result = converter.submit_to_comfyui(api_workflow, comfyui_server)
        
        # Summary
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        if result['success']:
            print(f"[OK] Conversion and submission successful!")
            print(f"     Prompt ID: {result['prompt_id']}")
            return 0
        else:
            print(f"[FAIL] Submission failed")
            print(f"       Error: {result.get('error')}")
            return 1
            
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
