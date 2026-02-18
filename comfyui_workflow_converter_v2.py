#!/usr/bin/env python3
"""
ComfyUI Workflow Converter v2 - UI Format to API Format
Fixed to handle ALL node types, not just known ones.
"""

import json
import sys
import requests
from typing import Any, Dict, List, Optional, Tuple, Set


class ComfyWorkflowConverter:
    """Converts ComfyUI workflows from UI format to API format."""
    
    def __init__(self, workflow: Dict[str, Any], server_url: str = "http://192.168.29.60:8188"):
        self.workflow = workflow
        self.nodes = workflow.get('nodes', [])
        self.links = workflow.get('links', [])
        self.server_url = server_url
        self._build_link_map()
        self._build_node_map()
        self._fetch_node_definitions()
        self._build_bypass_map()
    
    def _build_link_map(self) -> None:
        """Build a map of link IDs to link data."""
        self.link_map: Dict[int, List[Any]] = {}
        for link in self.links:
            link_id = link[0]
            self.link_map[link_id] = link
    
    def _build_node_map(self) -> None:
        """Build a map of node IDs to node data."""
        self.node_map: Dict[int, Dict[str, Any]] = {}
        for node in self.nodes:
            self.node_map[node['id']] = node
    
    def _fetch_node_definitions(self) -> None:
        """Fetch node input definitions from ComfyUI server."""
        self.node_defs: Dict[str, Any] = {}
        try:
            resp = requests.get(f"{self.server_url}/object_info", timeout=5)
            if resp.status_code == 200:
                self.node_defs = resp.json()
        except Exception as e:
            print(f"Warning: Could not fetch node definitions from server: {e}")
    
    def _build_bypass_map(self) -> None:
        """Build a map of bypassed nodes and where their outputs should be re-routed."""
        self.bypassed_nodes: Dict[int, Dict[str, Any]] = {}
        self.output_redirects: Dict[Tuple[int, int], Tuple[int, int]] = {}
        
        # Identify all bypassed nodes
        for node in self.nodes:
            node_id = node['id']
            mode = node.get('mode', 0)
            if mode == 4:  # BYPASS mode
                self.bypassed_nodes[node_id] = node
        
        if not self.bypassed_nodes:
            return
        
        # For each bypassed node, build output redirects
        for bypassed_id, bypassed_node in self.bypassed_nodes.items():
            # Get the inputs of the bypassed node
            inputs = bypassed_node.get('inputs', [])
            
            if not inputs:
                # No inputs to pass through
                continue
            
            # For each output of the bypassed node, find where to redirect it
            outputs = bypassed_node.get('outputs', [])
            for output_slot in outputs:
                output_slot_idx = output_slot.get('index', outputs.index(output_slot))
                
                # Find the matching input that should pass through
                # By default, use the first input with matching type, or just the first input
                passthrough_input = None
                for input_slot in inputs:
                    input_link_id = input_slot.get('link')
                    if input_link_id is not None and input_link_id in self.link_map:
                        # This input has a connection - use it as passthrough
                        passthrough_input = input_slot
                        break
                
                if passthrough_input is None and inputs:
                    # No connection found, use first input anyway
                    passthrough_input = inputs[0]
                
                if passthrough_input:
                    input_link_id = passthrough_input.get('link')
                    if input_link_id is not None and input_link_id in self.link_map:
                        link = self.link_map[input_link_id]
                        # link format: [link_id, source_node, source_slot, target_node, target_slot, type]
                        source_node = link[1]
                        source_slot = link[2]
                        
                        # Store the redirect: (bypassed_id, output_slot) -> (source_node, source_slot)
                        self.output_redirects[(bypassed_id, output_slot_idx)] = (source_node, source_slot)
    
    def _resolve_node_source(self, node_id: int, slot: int) -> Optional[Tuple[int, int]]:
        """Resolve the actual source of a connection, tracing through bypassed nodes."""
        # Check if this is a bypassed node's output
        if (node_id, slot) in self.output_redirects:
            # Recursively resolve the source
            resolved = self.output_redirects[(node_id, slot)]
            return self._resolve_node_source(resolved[0], resolved[1])
        
        # Not a bypassed node or no redirect found
        if node_id in self.bypassed_nodes:
            # This is a bypassed node but we couldn't resolve its source
            return None
        
        # This is a normal node
        return (node_id, slot)
    
    def compute_execution_order(self) -> List[Dict[str, Any]]:
        """Compute execution order using topological sort."""
        in_degree: Dict[int, int] = {}
        adjacency: Dict[int, List[int]] = {}
        
        for node in self.nodes:
            node_id = node['id']
            in_degree[node_id] = 0
            adjacency[node_id] = []
        
        for link in self.links:
            source_node = link[1]
            target_node = link[3]
            if target_node in adjacency:
                adjacency[source_node].append(target_node)
                in_degree[target_node] += 1
        
        queue = [nid for nid in in_degree if in_degree[nid] == 0]
        execution_order = []
        
        while queue:
            queue.sort()
            node_id = queue.pop(0)
            execution_order.append(self.node_map[node_id])
            for neighbor in adjacency[node_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return execution_order
    
    def _get_input_order(self, node_type: str) -> List[str]:
        """Get ordered list of input names for a node type from server definitions."""
        if node_type not in self.node_defs:
            return []
        
        node_def = self.node_defs[node_type]
        input_def = node_def.get('input', {})
        
        # Combine required and optional inputs in order
        inputs_order = []
        for category in ['required', 'optional']:
            if category in input_def:
                inputs_order.extend(input_def[category].keys())
        
        return inputs_order
    
    def convert_to_api_format(self) -> Dict[str, Dict[str, Any]]:
        """Convert workflow to API format."""
        output: Dict[str, Dict[str, Any]] = {}
        execution_order = self.compute_execution_order()
        
        for node in execution_order:
            node_id = node['id']
            node_type = node.get('type')
            
            if not node_type:
                continue
            
            # Skip muted/bypassed nodes
            mode = node.get('mode', 0)
            if mode == 2 or mode == 4:
                continue
            
            # Skip Note nodes (documentation only, not executable)
            if node_type == 'Note':
                continue
            
            inputs: Dict[str, Any] = {}
            input_slots = node.get('inputs', [])
            output_slots = node.get('outputs', [])
            widgets_values = node.get('widgets_values', [])
            
            # Build slot map by name
            slots_by_name: Dict[str, Dict[str, Any]] = {}
            for slot in input_slots:
                slots_by_name[slot['name']] = slot
            
            # Get input names from server definitions
            input_names = self._get_input_order(node_type)
            
            # Process connections from input slots
            for slot in input_slots:
                slot_name = slot['name']
                link_id = slot.get('link')
                if link_id is not None and link_id in self.link_map:
                    link = self.link_map[link_id]
                    source_node = link[1]
                    source_slot = link[2]
                    
                    # Resolve through bypassed nodes
                    resolved = self._resolve_node_source(source_node, source_slot)
                    if resolved:
                        source_node, source_slot = resolved
                    else:
                        # Could not resolve (bypassed node with no input)
                        continue
                    
                    inputs[slot_name] = [str(source_node), source_slot]
            
            # Process widget values
            # Widget values fill in inputs that don't have connections
            if widgets_values and input_names:
                # Handle dict-type widgets_values (some nodes like VHS_VideoCombine use this)
                if isinstance(widgets_values, dict):
                    for input_name in input_names:
                        if input_name in inputs:
                            continue
                        if input_name in widgets_values:
                            inputs[input_name] = widgets_values[input_name]
                else:
                    # Use server definitions to map widget values (list format)
                    widget_idx = 0
                    for input_name in input_names:
                        # Skip if already has a connection
                        if input_name in inputs:
                            continue
                        
                        # Skip if this input has a slot with a link
                        if input_name in slots_by_name:
                            slot = slots_by_name[input_name]
                            if slot.get('link') is not None:
                                continue
                        
                        # Assign widget value
                        if widget_idx < len(widgets_values):
                            value = widgets_values[widget_idx]
                            widget_idx += 1
                            
                            # Skip control_after_generate values (usually "fixed"/"randomize")
                            # These appear AFTER seed values in the UI but shouldn't be assigned
                            # When we hit one, grab the NEXT value instead for this input
                            while isinstance(value, str) and value in ['fixed', 'increment', 'decrement', 'randomize']:
                                if widget_idx < len(widgets_values):
                                    value = widgets_values[widget_idx]
                                    widget_idx += 1
                                else:
                                    value = None
                                    break
                            
                            if value is not None:
                                inputs[input_name] = value
            
            elif widgets_values and not input_names:
                # Fallback: No server definitions, use slot-based approach
                # Process widget values based on input slots that have widget info
                widget_idx = 0
                
                # First, handle slots that expect widgets
                for slot in input_slots:
                    slot_name = slot['name']
                    if slot_name in inputs:
                        continue  # Already has connection
                    
                    # Check if slot has widget definition
                    if 'widget' in slot:
                        if widget_idx < len(widgets_values):
                            inputs[slot_name] = widgets_values[widget_idx]
                            widget_idx += 1
                
                # For outputs that also have widgets (like Text Multiline)
                # Some nodes have widget values for their output values
                for slot in output_slots:
                    slot_name = slot.get('name', '')
                    # Check if there's a matching widget
                    if widget_idx < len(widgets_values):
                        # For string output nodes, the widget value is the text content
                        if slot.get('type') == 'STRING' or node_type in ['Text Multiline', 'PrimitiveStringMultiline']:
                            inputs['text'] = widgets_values[widget_idx]
                            widget_idx += 1
                            break
            
            output[str(node_id)] = {
                'inputs': inputs,
                'class_type': node_type,
                '_meta': {'title': node.get('title', node_type)}
            }
        
        # Remove dangling references
        for node_entry in output.values():
            node_inputs = node_entry['inputs']
            to_remove = []
            for name, value in node_inputs.items():
                if isinstance(value, list) and len(value) == 2:
                    if value[0] not in output:
                        to_remove.append(name)
            for name in to_remove:
                del node_inputs[name]
        
        return output


def convert_workflow(input_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
    """Convert a UI format workflow to API format."""
    print(f"Loading workflow from: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        workflow = json.load(f)
    
    nodes = workflow.get('nodes', [])
    links = workflow.get('links', [])
    print(f"Found {len(nodes)} nodes, {len(links)} links")
    
    converter = ComfyWorkflowConverter(workflow)
    print("Fetching node definitions from server...")
    print(f"Server has {len(converter.node_defs)} node types")
    
    print("Converting to API format...")
    api_format = converter.convert_to_api_format()
    print(f"Converted {len(api_format)} nodes")
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(api_format, f, indent=2)
        print(f"Saved to: {output_path}")
    
    return api_format


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python comfyui_workflow_converter_v2.py <input.json> [output.json]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not output_file:
        base = input_file.rsplit('.', 1)[0]
        output_file = f"{base}_api.json"
    
    api = convert_workflow(input_file, output_file)
    print(f"\n[SUCCESS] Conversion completed!")
    print(f"Output file: {output_file}")
