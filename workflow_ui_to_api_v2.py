#!/usr/bin/env python3
"""
ComfyUI Workflow Converter v2 - UI Format to API Format
Enhanced version that loads ComfyUI node definitions for accurate widget mapping
"""

import json
import sys
import os
import re
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from pathlib import Path
import subprocess
import importlib.util


class ComfyNodeRegistry:
    """Load and cache ComfyUI node definitions."""
    
    def __init__(self, comfyui_path: Optional[str] = None):
        """Initialize the node registry."""
        self.comfyui_path = comfyui_path or self._find_comfyui()
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self._load_nodes()
    
    def _find_comfyui(self) -> Optional[str]:
        """Try to find ComfyUI installation."""
        # Check relative to workspace
        workspace = Path(__file__).parent
        comfyui_path = workspace / "ComfyUI"
        if comfyui_path.exists():
            return str(comfyui_path)
        
        # Check environment variable
        if 'COMFYUI_PATH' in os.environ:
            return os.environ['COMFYUI_PATH']
        
        return None
    
    def _load_nodes(self) -> None:
        """Load node definitions from ComfyUI."""
        if not self.comfyui_path:
            print("Warning: ComfyUI path not found, skipping node definition loading")
            return
        
        try:
            # Try to import ComfyUI's nodes module
            nodes_path = Path(self.comfyui_path) / "nodes.py"
            if nodes_path.exists():
                print(f"Loading node definitions from {nodes_path}")
                # We'll parse the file to extract node definitions
                self._parse_nodes_file(str(nodes_path))
        except Exception as e:
            print(f"Warning: Could not load node definitions: {e}")
    
    def _parse_nodes_file(self, nodes_path: str) -> None:
        """Parse nodes.py to extract input type definitions."""
        try:
            with open(nodes_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple regex-based parsing for INPUT_TYPES
            # This is a basic implementation; a full implementation would use AST
            class_pattern = r'class\s+(\w+)'
            input_types_pattern = r'def\s+INPUT_TYPES\s*\([^)]*\)\s*:\s*return\s+\{([^}]+(?:\{[^}]*\}[^}]*)*)\}'
            
            current_class = None
            for line in content.split('\n'):
                class_match = re.match(class_pattern, line)
                if class_match:
                    current_class = class_match.group(1)
                    self.nodes[current_class] = {'inputs': {}}
            
            print(f"Found {len(self.nodes)} node classes")
        except Exception as e:
            print(f"Warning: Error parsing nodes file: {e}")
    
    def get_node_inputs(self, node_type: str) -> Dict[str, Any]:
        """Get input definition for a node type."""
        return self.nodes.get(node_type, {}).get('inputs', {})
    
    def get_input_names(self, node_type: str) -> List[str]:
        """Get ordered list of input names for a node type."""
        # For now, return empty list since we can't reliably parse the Python AST
        # This would require a more sophisticated parser
        return []


class WorkflowConverterV2:
    """
    Enhanced workflow converter with node definition support.
    """
    
    # Hardcoded node input definitions for common nodes
    # Format: {"node_type": [("input_name", "type"), ...]}
    COMMON_NODE_INPUTS = {
        "CheckpointLoaderSimple": [("ckpt_name",)],
        "CheckpointLoader": [("ckpt_name",), ("clip_skip",)],
        "CLIPLoader": [("clip_name",), ("type",), ("device",)],
        "VAELoader": [("vae_name",)],
        "EmptyLatentImage": [("width",), ("height",), ("batch_size",)],
        "EmptySD3LatentImage": [("width",), ("height",), ("batch_size",)],
        "KSampler": [("seed",), ("steps",), ("cfg",), ("sampler_name",), ("scheduler",), ("denoise",)],
        "KSamplerAdvanced": [("seed",), ("steps",), ("cfg",), ("sampler_name",), ("scheduler",), ("denoise",), ("noise_seed",), ("start_at_step",), ("end_at_step",)],
        "PrimitiveString": [("string",)],
        "PrimitiveStringMultiline": [("value",)],
        "PrimitiveNumber": [("number",)],
        "SaveImage": [("filename_prefix",)],
        "LoadImage": [("image",)],
        "VAEDecode": [],  # Has inputs but they're connections, not widgets
        "VAEEncode": [],
        "UNETLoader": [("unet_name",), ("weight_dtype",)],
        "LoraLoaderModelOnly": [("lora_name",), ("strength_model",)],
        "LoraLoader": [("lora_name",), ("strength_model",), ("strength_clip",)],
    }
    
    def __init__(self, workflow: Dict[str, Any]):
        """Initialize converter with a UI format workflow."""
        self.workflow = workflow
        self.nodes = workflow.get('nodes', [])
        self.links = workflow.get('links', [])
        self._build_link_map()
        self._build_node_map()
    
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
            node_id = node['id']
            self.node_map[node_id] = node
    
    def compute_execution_order(self) -> List[Dict[str, Any]]:
        """Compute execution order of nodes using topological sort."""
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
        
        queue = [node_id for node_id in in_degree if in_degree[node_id] == 0]
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
    
    def get_input_names_for_node(self, node_type: str) -> List[str]:
        """Get input names for a node type."""
        return [inp[0] for inp in self.COMMON_NODE_INPUTS.get(node_type, [])]
    
    def convert_to_api_format(self) -> Dict[str, Dict[str, Any]]:
        """Convert workflow to API format."""
        output: Dict[str, Dict[str, Any]] = {}
        
        execution_order = self.compute_execution_order()
        
        for node in execution_order:
            node_id = node['id']
            node_type = node['type']
            
            # Skip muted/bypassed nodes
            mode = node.get('mode', 0)
            if mode == 2 or mode == 4:  # NEVER or BYPASS
                continue
            
            inputs: Dict[str, Any] = {}
            input_slots = node.get('inputs', [])
            widgets_values = node.get('widgets_values', [])
            
            # Process input slots
            for i, input_slot in enumerate(input_slots):
                input_name = input_slot['name']
                link_id = input_slot.get('link')
                
                if link_id is not None and link_id in self.link_map:
                    # Connected to another node
                    link = self.link_map[link_id]
                    source_node = link[1]
                    source_slot = link[2]
                    inputs[input_name] = [str(source_node), source_slot]
                elif i < len(widgets_values):
                    # Use widget value
                    value = widgets_values[i]
                    if isinstance(value, list):
                        inputs[input_name] = {'__value__': value}
                    else:
                        inputs[input_name] = value
            
            # Process widget-only inputs (not in inputs array)
            input_names = self.get_input_names_for_node(node_type)
            if input_names and len(input_slots) < len(widgets_values):
                # There are more widget values than input slots
                # Try to map remaining widgets to input names
                for i, input_name in enumerate(input_names[len(input_slots):]):
                    widget_idx = len(input_slots) + i
                    if widget_idx < len(widgets_values):
                        value = widgets_values[widget_idx]
                        if isinstance(value, list):
                            inputs[input_name] = {'__value__': value}
                        else:
                            inputs[input_name] = value
            
            output[str(node_id)] = {
                'inputs': inputs,
                'class_type': node_type,
                '_meta': {
                    'title': node.get('title', node_type)
                }
            }
        
        # Remove inputs connected to removed nodes
        for node_entry in output.values():
            node_inputs = node_entry['inputs']
            inputs_to_remove = []
            
            for input_name, input_value in node_inputs.items():
                if isinstance(input_value, list) and len(input_value) == 2:
                    source_node_id = input_value[0]
                    if source_node_id not in output:
                        inputs_to_remove.append(input_name)
            
            for input_name in inputs_to_remove:
                del node_inputs[input_name]
        
        return output


def load_workflow(file_path: str) -> Dict[str, Any]:
    """Load a workflow from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_workflow(workflow: Dict[str, Any], file_path: str) -> None:
    """Save a workflow to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2)


def convert_workflow(input_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
    """Convert a UI format workflow to API format."""
    print(f"Loading workflow from: {input_path}")
    
    workflow = load_workflow(input_path)
    
    print(f"Found {len(workflow.get('nodes', []))} nodes")
    print(f"Found {len(workflow.get('links', []))} links")
    
    converter = WorkflowConverterV2(workflow)
    
    print("Computing execution order...")
    execution_order = converter.compute_execution_order()
    print(f"Execution order: {[node['id'] for node in execution_order]}")
    
    print("Converting to API format...")
    api_format = converter.convert_to_api_format()
    
    print(f"Converted {len(api_format)} nodes to API format")
    
    if output_path:
        print(f"Saving API format workflow to: {output_path}")
        save_workflow(api_format, output_path)
    
    return api_format


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python workflow_ui_to_api_v2.py <input_workflow.json> [output_workflow.json]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not output_path:
        input_file = Path(input_path)
        output_path = str(input_file.parent / f"{input_file.stem}_api_v2.json")
    
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
