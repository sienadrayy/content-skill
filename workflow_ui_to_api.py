#!/usr/bin/env python3
"""
ComfyUI Workflow Converter - UI Format to API Format
Replicates the exact logic from ComfyUI frontend's executionUtil.ts

This script converts ComfyUI workflows from UI format (LiteGraph format) to API format
that can be sent to the ComfyUI backend for execution.

UI Format: Graph representation with nodes, links, and canvas metadata
API Format: Flat dictionary with node ID as key, inputs/class_type as value
"""

import json
import sys
import os
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from pathlib import Path


class WorkflowConverter:
    """
    Converts ComfyUI workflows from UI format to API format.
    
    This class replicates the exact logic from:
    - executionUtil.ts: graphToPrompt() function
    - litegraphUtil.ts: compressWidgetInputSlots() function
    """
    
    def __init__(self, workflow: Dict[str, Any]):
        """
        Initialize converter with a UI format workflow.
        
        Args:
            workflow: Dictionary containing the UI format workflow
        """
        self.workflow = workflow
        self.nodes = workflow.get('nodes', [])
        self.links = workflow.get('links', [])
        # Create a map of link IDs to link data for fast lookup
        self._build_link_map()
        # Create a map of node IDs to node data for fast lookup
        self._build_node_map()
        
    def _build_link_map(self) -> None:
        """Build a map of link IDs to link data for O(1) lookup."""
        self.link_map: Dict[int, List[Any]] = {}
        for link in self.links:
            # Link format: [id, source_node, source_slot, target_node, target_slot, type]
            link_id = link[0]
            self.link_map[link_id] = link
    
    def _build_node_map(self) -> None:
        """Build a map of node IDs to node data for O(1) lookup."""
        self.node_map: Dict[int, Dict[str, Any]] = {}
        for node in self.nodes:
            node_id = node['id']
            self.node_map[node_id] = node
    
    def compute_execution_order(self) -> List[Dict[str, Any]]:
        """
        Compute execution order of nodes using topological sort.
        
        Returns:
            List of nodes in execution order
        """
        # Build adjacency list and in-degree count
        in_degree: Dict[int, int] = {}
        adjacency: Dict[int, List[int]] = {}
        
        for node in self.nodes:
            node_id = node['id']
            in_degree[node_id] = 0
            adjacency[node_id] = []
        
        # Build edges based on links
        for link in self.links:
            # Link format: [id, source_node, source_slot, target_node, target_slot, type]
            source_node = link[1]
            target_node = link[3]
            
            if target_node in adjacency:
                adjacency[source_node].append(target_node)
                in_degree[target_node] += 1
        
        # Kahn's algorithm for topological sort
        queue = [node_id for node_id in in_degree if in_degree[node_id] == 0]
        execution_order = []
        
        while queue:
            # Sort by node ID for deterministic order
            queue.sort()
            node_id = queue.pop(0)
            
            execution_order.append(self.node_map[node_id])
            
            for neighbor in adjacency[node_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return execution_order
    
    def resolve_input(
        self, 
        node: Dict[str, Any], 
        input_index: int
    ) -> Optional[Union[Any, Tuple[str, int]]]:
        """
        Resolve an input connection or widget value.
        
        Args:
            node: The node containing the input
            input_index: Index of the input slot
            
        Returns:
            Either the resolved value or [node_id, slot_index] for connections
        """
        # Check if this input slot exists
        if 'inputs' not in node or input_index >= len(node['inputs']):
            return None
        
        input_slot = node['inputs'][input_index]
        
        # If there's a link, resolve it
        if 'link' in input_slot and input_slot['link'] is not None:
            link_id = input_slot['link']
            if link_id in self.link_map:
                link = self.link_map[link_id]
                # Link format: [id, source_node, source_slot, target_node, target_slot, type]
                source_node = link[1]
                source_slot = link[2]
                return [str(source_node), source_slot]
        
        return None
    
    def serialize_workflow(self) -> Dict[str, Any]:
        """
        Serialize the workflow to a simpler format.
        
        This removes UI-specific information and keeps the essential node data.
        
        Returns:
            Serialized workflow
        """
        serialized_nodes = []
        for node in self.nodes:
            # Skip groups and other UI elements
            if 'type' not in node:
                continue
            
            serialized_node = {
                'id': node['id'],
                'type': node['type'],
                'inputs': node.get('inputs', []),
                'widgets_values': node.get('widgets_values', []),
                'mode': node.get('mode', 0),
            }
            
            serialized_nodes.append(serialized_node)
        
        return {
            'nodes': serialized_nodes,
            'links': self.links,
        }
    
    def convert_to_api_format(self) -> Dict[str, Dict[str, Any]]:
        """
        Convert workflow to API format.
        
        This is the main conversion function that replicates graphToPrompt() from executionUtil.ts
        
        Returns:
            API format workflow: {node_id: {inputs: {...}, class_type: "...", _meta: {...}}, ...}
        """
        output: Dict[str, Dict[str, Any]] = {}
        
        # Get execution order
        execution_order = self.compute_execution_order()
        
        # Process each node in execution order
        for node in execution_order:
            node_id = node['id']
            node_type = node['type']
            
            # Skip muted or bypassed nodes (mode: NEVER=2, BYPASS=4)
            mode = node.get('mode', 0)
            if mode == 2 or mode == 4:  # LGraphEventMode.NEVER or BYPASS
                continue
            
            inputs: Dict[str, Any] = {}
            
            # Process widgets (widget values)
            widgets_values = node.get('widgets_values', [])
            input_slots = node.get('inputs', [])
            
            # Build a map of input slot names to indices
            input_names = [slot['name'] for slot in input_slots]
            
            # Process each input slot
            for i, input_slot in enumerate(input_slots):
                input_name = input_slot['name']
                
                # Check if there's a connected link
                link_id = input_slot.get('link')
                
                if link_id is not None and link_id in self.link_map:
                    # This input is connected to another node
                    link = self.link_map[link_id]
                    source_node = link[1]
                    source_slot = link[2]
                    
                    inputs[input_name] = [str(source_node), source_slot]
                else:
                    # This input uses a widget value
                    # Find the corresponding widget value
                    if i < len(widgets_values):
                        value = widgets_values[i]
                        # If the value is an array, wrap it to avoid confusion with node links
                        if isinstance(value, list):
                            inputs[input_name] = {'__value__': value}
                        else:
                            inputs[input_name] = value
            
            # Create the output node entry
            output[str(node_id)] = {
                'inputs': inputs,
                'class_type': node_type,
                '_meta': {
                    'title': node.get('title', node_type)
                }
            }
        
        # Remove inputs connected to removed (muted/bypassed) nodes
        for node_entry in output.values():
            node_inputs = node_entry['inputs']
            inputs_to_remove = []
            
            for input_name, input_value in node_inputs.items():
                # Check if this is a node connection
                if isinstance(input_value, list) and len(input_value) == 2:
                    source_node_id = input_value[0]
                    # If source node is not in output, remove this input
                    if source_node_id not in output:
                        inputs_to_remove.append(input_name)
            
            for input_name in inputs_to_remove:
                del node_inputs[input_name]
        
        return output
    
    def compress_widget_input_slots(self, graph: Dict[str, Any]) -> None:
        """
        Compress widget input slots to match the legacy API format.
        
        This replicates the compressWidgetInputSlots() function from litegraphUtil.ts
        
        Args:
            graph: The serialized graph to compress
        """
        def matches_legacy_api(input_slot: Dict[str, Any]) -> bool:
            """Check if input slot should be kept in the legacy API."""
            # Remove if: has widget AND no link AND no label
            return not (
                input_slot.get('widget') and 
                input_slot.get('link') is None and 
                not input_slot.get('label')
            )
        
        for node in graph.get('nodes', []):
            # Filter inputs
            if 'inputs' in node:
                node['inputs'] = [
                    inp for inp in node['inputs'] 
                    if matches_legacy_api(inp)
                ]
                
                # Update link target slot indices
                for input_index, input_slot in enumerate(node['inputs']):
                    if 'link' in input_slot and input_slot['link'] is not None:
                        link_id = input_slot['link']
                        # Find the link and update its target slot
                        for link in graph.get('links', []):
                            if link[0] == link_id:
                                link[4] = input_index  # Update target_slot


def load_workflow(file_path: str) -> Dict[str, Any]:
    """
    Load a workflow from a JSON file.
    
    Args:
        file_path: Path to the workflow JSON file
        
    Returns:
        The loaded workflow dictionary
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_workflow(workflow: Dict[str, Any], file_path: str) -> None:
    """
    Save a workflow to a JSON file.
    
    Args:
        workflow: The workflow dictionary to save
        file_path: Path where to save the workflow
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2)


def convert_workflow(input_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Convert a UI format workflow to API format.
    
    Args:
        input_path: Path to the UI format workflow JSON file
        output_path: Optional path to save the API format workflow
        
    Returns:
        The API format workflow dictionary
    """
    print(f"Loading workflow from: {input_path}")
    
    # Load the UI format workflow
    workflow = load_workflow(input_path)
    
    print(f"Found {len(workflow.get('nodes', []))} nodes")
    print(f"Found {len(workflow.get('links', []))} links")
    
    # Create converter and convert
    converter = WorkflowConverter(workflow)
    
    print("Computing execution order...")
    execution_order = converter.compute_execution_order()
    print(f"Execution order: {[node['id'] for node in execution_order]}")
    
    print("Converting to API format...")
    api_format = converter.convert_to_api_format()
    
    print(f"Converted {len(api_format)} nodes to API format")
    
    # Save if output path provided
    if output_path:
        print(f"Saving API format workflow to: {output_path}")
        save_workflow(api_format, output_path)
    
    return api_format


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python workflow_ui_to_api.py <input_workflow.json> [output_workflow.json]")
        print("\nExample:")
        print("  python workflow_ui_to_api.py default_workflow.json api_format.json")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Generate output path if not provided
    if not output_path:
        input_file = Path(input_path)
        output_path = str(input_file.parent / f"{input_file.stem}_api.json")
    
    try:
        api_format = convert_workflow(input_path, output_path)
        print("\n[SUCCESS] Conversion successful!")
        print(f"Output saved to: {output_path}")
    except Exception as e:
        print(f"\n[ERROR] Conversion failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
