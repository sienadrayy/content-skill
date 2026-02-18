#!/usr/bin/env python3
"""
ComfyUI UI-format to API-format workflow converter.
Handles subgraph flattening and API submission.
"""

import json
import uuid
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
                print(f"Found subgraph: {subgraph_id}")
        
        return self.workflow_data
    
    def get_available_node_id(self) -> int:
        """Get next available node ID."""
        current_max = max([node['id'] for node in self.workflow_data['nodes']], default=0)
        self.next_node_id = max(self.next_node_id, current_max + 1)
        node_id = self.next_node_id
        self.next_node_id += 1
        return node_id
    
    def flatten_subgraph(self, subgraph_node: Dict, subgraph_id: str) -> Tuple[List[Dict], Dict]:
        """
        Flatten a subgraph into individual nodes.
        Returns: (new_nodes, node_id_mapping)
        """
        print(f"\nFlattening subgraph {subgraph_id}...")
        
        if subgraph_id not in self.subgraph_definitions:
            raise ValueError(f"Subgraph {subgraph_id} not found in definitions")
        
        subgraph_def = self.subgraph_definitions[subgraph_id]
        new_nodes = []
        local_to_global_id = {}  # Map local subgraph node IDs to new global IDs
        
        # Step 1: Create copy of all nodes in subgraph with new IDs
        for node in subgraph_def['nodes']:
            new_node = json.loads(json.dumps(node))  # Deep copy
            old_local_id = node['id']
            new_global_id = self.get_available_node_id()
            local_to_global_id[old_local_id] = new_global_id
            new_node['id'] = new_global_id
            new_nodes.append(new_node)
        
        # Step 2: Update internal links to use new IDs
        if 'links' in subgraph_def:
            for new_node in new_nodes:
                # Update input links
                if 'inputs' in new_node:
                    for input_item in new_node['inputs']:
                        if 'link' in input_item and input_item['link'] is not None:
                            # Find the link in subgraph links
                            for link in subgraph_def['links']:
                                if link['id'] == input_item['link']:
                                    # Update origin_id and target_id
                                    origin_id = local_to_global_id.get(link['origin_id'], link['origin_id'])
                                    target_id = local_to_global_id.get(link['target_id'], link['target_id'])
                                    input_item['link'] = (origin_id, link['origin_slot'], target_id, link['target_slot'])
        
        # Step 3: Handle subgraph inputs - connect them to internal nodes
        print(f"Subgraph has {len(subgraph_def.get('inputs', []))} inputs")
        print(f"Subgraph node has {len(subgraph_node.get('inputs', []))} connected inputs")
        
        # Map subgraph input indices to internal nodes
        for i, subgraph_input in enumerate(subgraph_def.get('inputs', [])):
            input_name = subgraph_input.get('name', f'input_{i}')
            link_ids = subgraph_input.get('linkIds', [])
            
            # Find which subgraph node input this connects to
            for link_id in link_ids:
                for link in subgraph_def.get('links', []):
                    if link['id'] == link_id:
                        target_id = link['target_id']
                        global_target_id = local_to_global_id.get(target_id, target_id)
                        
                        # Find the node and update its link reference
                        for new_node in new_nodes:
                            if new_node['id'] == global_target_id:
                                # Update the input with external link info
                                if 'inputs' in new_node:
                                    for input_item in new_node['inputs']:
                                        if input_item.get('name') == link['target_name']:
                                            # Mark this for external connection
                                            input_item['_external_input'] = {
                                                'source_node': subgraph_node['id'],
                                                'source_slot': i,
                                                'target_slot': link['target_slot']
                                            }
        
        return new_nodes, local_to_global_id
    
    def convert_to_api_format(self, update_prompt: str = None) -> Dict:
        """Convert UI workflow to API format."""
        print("\n=== Converting Workflow to API Format ===\n")
        
        # Start with empty API format
        api_workflow = {}
        
        # Process all nodes
        nodes_to_process = list(self.workflow_data['nodes'])
        processed_node_ids = set()
        
        while nodes_to_process:
            node = nodes_to_process.pop(0)
            
            if node['id'] in processed_node_ids:
                continue
            
            # Check if this is a subgraph node
            if node['type'] in self.subgraph_definitions:
                print(f"Processing subgraph node {node['id']} (type: {node['type']})")
                subgraph_id = node['type']
                
                # Flatten the subgraph
                subgraph_nodes, local_id_map = self.flatten_subgraph(node, subgraph_id)
                
                # Add flattened nodes to API format
                for subgraph_node in subgraph_nodes:
                    self._add_node_to_api(api_workflow, subgraph_node)
                
                # Handle connections from subgraph output to next nodes
                self._connect_subgraph_outputs(api_workflow, node, subgraph_id, local_id_map)
                
                processed_node_ids.add(node['id'])
            else:
                # Regular node
                self._add_node_to_api(api_workflow, node)
                processed_node_ids.add(node['id'])
        
        # Update prompt node if specified
        if update_prompt:
            self._update_prompt_node(api_workflow, update_prompt)
        
        return api_workflow
    
    def _add_node_to_api(self, api_workflow: Dict, node: Dict):
        """Add a node to the API workflow format."""
        node_id = str(node['id'])
        
        api_node = {
            "inputs": {},
            "class_type": node['type']
        }
        
        # Add widget values as inputs
        if 'widgets_values' in node:
            widgets_values = node['widgets_values']
            if 'inputs' in node:
                widget_idx = 0
                for input_item in node['inputs']:
                    if 'widget' in input_item and input_item['widget']:
                        if widget_idx < len(widgets_values):
                            api_node['inputs'][input_item['name']] = widgets_values[widget_idx]
                            widget_idx += 1
                # Add remaining widget values (standalone widgets)
                remaining_widgets = widgets_values[widget_idx:]
                for i, val in enumerate(remaining_widgets):
                    # Try to find widget name from inputs
                    api_node['inputs'][f'widget_{i}'] = val
        
        # Add input connections (links)
        if 'inputs' in node:
            for input_item in node['inputs']:
                if 'link' in input_item and input_item['link'] is not None:
                    link = input_item['link']
                    if isinstance(link, tuple):
                        # (origin_id, origin_slot, target_id, target_slot)
                        origin_id, origin_slot = link[0], link[1]
                        api_node['inputs'][input_item['name']] = [str(origin_id), origin_slot]
                    elif isinstance(link, int):
                        # Find link in workflow links
                        for wf_link in self.workflow_data.get('links', []):
                            if wf_link['id'] == link:
                                origin_id = str(wf_link['origin_id'])
                                origin_slot = wf_link['origin_slot']
                                api_node['inputs'][input_item['name']] = [origin_id, origin_slot]
                                break
        
        api_workflow[node_id] = api_node
        print(f"  Added node {node_id}: {node['type']}")
    
    def _connect_subgraph_outputs(self, api_workflow: Dict, subgraph_node: Dict, 
                                  subgraph_id: str, local_id_map: Dict):
        """Connect subgraph outputs to nodes that consume them."""
        subgraph_def = self.subgraph_definitions[subgraph_id]
        
        # Find the output node in the subgraph
        output_node_id = subgraph_def.get('outputNode', {}).get('id', -20)
        
        # Find which internal nodes feed the output
        output_internal_node_id = None
        for link in subgraph_def.get('links', []):
            if link['target_id'] == output_node_id:
                output_internal_node_id = link['origin_id']
                break
        
        if output_internal_node_id:
            global_output_node_id = local_id_map.get(output_internal_node_id)
            
            # Find nodes that consume the subgraph output
            for link in self.workflow_data.get('links', []):
                if link['origin_id'] == subgraph_node['id']:
                    target_node_id = str(link['target_id'])
                    
                    if target_node_id in api_workflow:
                        target_node = api_workflow[target_node_id]
                        # Find the input on the target node
                        for node in self.workflow_data['nodes']:
                            if node['id'] == link['target_id']:
                                for input_item in node.get('inputs', []):
                                    if 'link' in input_item and input_item['link'] == link['id']:
                                        target_node['inputs'][input_item['name']] = [
                                            str(global_output_node_id),
                                            link['origin_slot']
                                        ]
    
    def _update_prompt_node(self, api_workflow: Dict, new_prompt: str):
        """Update the prompt node (ID 58) with new text."""
        # Find the prompt node
        for node_id, node_data in api_workflow.items():
            # Look for PrimitiveStringMultiline nodes
            if node_data.get('class_type') == 'PrimitiveStringMultiline':
                if int(node_id) == 58:
                    print(f"\nUpdating prompt node {node_id} with new text")
                    if 'value' in node_data['inputs']:
                        node_data['inputs']['value'] = new_prompt
                    else:
                        node_data['inputs']['value'] = new_prompt
                    print(f"  New prompt: {new_prompt[:100]}...")
                    break
    
    def submit_to_comfyui(self, api_workflow: Dict, server_url: str = "http://192.168.29.60:8188") -> Dict:
        """Submit the converted workflow to ComfyUI API."""
        print(f"\n=== Submitting to ComfyUI ===")
        print(f"Server: {server_url}")
        
        try:
            response = requests.post(
                f"{server_url}/prompt",
                json=api_workflow,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Successfully submitted!")
                print(f"  Prompt ID: {result.get('prompt_id')}")
                return {
                    'success': True,
                    'prompt_id': result.get('prompt_id'),
                    'response': result
                }
            else:
                print(f"✗ API Error: {response.status_code}")
                print(f"  Response: {response.text}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                    'response': response.text
                }
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection Error: {str(e)}")
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
        
        print(f"\n✓ API workflow saved to: {output_path}")
        return str(output_path)


def main():
    """Main execution function."""
    import sys
    
    # Configuration
    workflow_path = "\\\\192.168.29.60\\workflows\\image_z_image_turbo.json"
    new_prompt = "Siena is standing in garden"
    comfyui_server = "http://192.168.29.60:8188"
    
    print("=" * 60)
    print("ComfyUI Workflow Converter")
    print("=" * 60)
    
    try:
        # Initialize converter
        converter = ComfyUIWorkflowConverter(workflow_path)
        
        # Load and parse workflow
        converter.load_workflow()
        
        # Convert to API format
        api_workflow = converter.convert_to_api_format(update_prompt=new_prompt)
        
        # Save converted workflow
        converter.save_api_workflow(api_workflow)
        
        # Submit to ComfyUI
        result = converter.submit_to_comfyui(api_workflow, comfyui_server)
        
        # Print summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        if result['success']:
            print(f"✓ Workflow successfully submitted!")
            print(f"  Prompt ID: {result['prompt_id']}")
            return 0
        else:
            print(f"✗ Failed to submit workflow")
            print(f"  Error: {result.get('error')}")
            return 1
            
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
