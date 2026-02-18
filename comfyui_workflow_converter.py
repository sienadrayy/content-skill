#!/usr/bin/env python3
"""
ComfyUI Export API v3 - Exact replication of graphToPrompt from executionUtil.ts

This converter replicates the exact behavior of ComfyUI's "Export (API)" feature.
"""

import json
import sys
import requests
from typing import Any, Dict, List, Optional, Tuple

class ComfyUIExporter:
    """Exact replication of ComfyUI's graphToPrompt function."""
    
    def __init__(self, workflow: Dict[str, Any], server_url: str = "http://192.168.29.60:8188"):
        self.workflow = workflow
        self.nodes = {n['id']: n for n in workflow.get('nodes', [])}
        self.links = {link[0]: link for link in workflow.get('links', [])}
        self.server_url = server_url
        self.node_defs = self._fetch_node_defs()
        
        # Track bypassed nodes for link resolution
        self.bypassed_nodes = set()
        for node in workflow.get('nodes', []):
            if node.get('mode') in [2, 4]:  # NEVER or BYPASS
                self.bypassed_nodes.add(node['id'])
    
    def _fetch_node_defs(self) -> Dict[str, Any]:
        """Fetch node definitions from server."""
        try:
            resp = requests.get(f"{self.server_url}/object_info", timeout=10)
            return resp.json() if resp.status_code == 200 else {}
        except:
            return {}
    
    def _get_widget_inputs(self, node_type: str) -> List[str]:
        """Get list of widget input names in order for a node type."""
        if node_type not in self.node_defs:
            return []
        
        node_def = self.node_defs[node_type]
        input_def = node_def.get('input', {})
        
        widget_inputs = []
        for category in ['required', 'optional']:
            for name, spec in input_def.get(category, {}).items():
                # Skip connection types - they're not widgets
                if isinstance(spec, list) and len(spec) > 0:
                    input_type = spec[0]
                    # These are connection types, not widgets
                    if isinstance(input_type, str) and input_type.upper() in [
                        'MODEL', 'VAE', 'CLIP', 'CONDITIONING', 'LATENT', 'IMAGE',
                        'MASK', 'CONTROL_NET', 'SIGMAS', 'SAMPLER', 'NOISE',
                        'GUIDER', 'UPSCALE_MODEL', '*'
                    ]:
                        continue
                widget_inputs.append(name)
        
        return widget_inputs
    
    def _resolve_link(self, link_id: int) -> Optional[Tuple[int, int]]:
        """Resolve a link, following through bypassed nodes."""
        if link_id not in self.links:
            return None
        
        link = self.links[link_id]
        # Link format: [id, source_node, source_slot, target_node, target_slot, type]
        source_node_id = link[1]
        source_slot = link[2]
        
        # If source is bypassed, follow through it
        if source_node_id in self.bypassed_nodes:
            source_node = self.nodes.get(source_node_id)
            if source_node and source_node.get('inputs'):
                # Find matching input slot to follow through
                for inp in source_node['inputs']:
                    if inp.get('link') is not None:
                        return self._resolve_link(inp['link'])
            return None
        
        return (source_node_id, source_slot)
    
    def export(self) -> Dict[str, Dict[str, Any]]:
        """Export workflow to API format."""
        output = {}
        
        for node_id, node in self.nodes.items():
            node_type = node.get('type')
            if not node_type:
                continue
            
            # Skip muted/bypassed nodes (mode 2 = NEVER, mode 4 = BYPASS)
            mode = node.get('mode', 0)
            if mode in [2, 4]:
                continue
            
            # Skip virtual nodes (Note, etc.)
            if node_type in ['Note', 'Reroute']:
                continue
            
            inputs = {}
            node_inputs = node.get('inputs', [])
            widgets_values = node.get('widgets_values', [])
            
            # Build map of connected inputs
            connected_inputs = set()
            for inp in node_inputs:
                if inp.get('link') is not None:
                    connected_inputs.add(inp['name'])
            
            # Process connections
            for inp in node_inputs:
                link_id = inp.get('link')
                if link_id is not None:
                    resolved = self._resolve_link(link_id)
                    if resolved:
                        inputs[inp['name']] = [str(resolved[0]), resolved[1]]
            
            # Process widget values
            widget_names = self._get_widget_inputs(node_type)
            
            if isinstance(widgets_values, dict):
                # Dict format (some nodes like VHS_VideoCombine)
                for name, value in widgets_values.items():
                    if name not in connected_inputs:
                        inputs[name] = value
            elif isinstance(widgets_values, list) and widget_names:
                # List format - map to widget names in order
                widget_idx = 0
                for name in widget_names:
                    # Skip if already connected
                    if name in inputs or name in connected_inputs:
                        continue
                    
                    if widget_idx < len(widgets_values):
                        value = widgets_values[widget_idx]
                        widget_idx += 1
                        
                        # Skip control_after_generate values
                        while isinstance(value, str) and value in ['fixed', 'increment', 'decrement', 'randomize']:
                            if widget_idx < len(widgets_values):
                                value = widgets_values[widget_idx]
                                widget_idx += 1
                            else:
                                value = None
                                break
                        
                        if value is not None:
                            # Wrap arrays to avoid confusion with node links
                            if isinstance(value, list):
                                inputs[name] = {'__value__': value}
                            else:
                                inputs[name] = value
            elif isinstance(widgets_values, list) and not widget_names:
                # Fallback: no server definition, use input slots with widgets
                widget_idx = 0
                for inp in node_inputs:
                    if 'widget' in inp and inp['name'] not in inputs:
                        if widget_idx < len(widgets_values):
                            inputs[inp['name']] = widgets_values[widget_idx]
                            widget_idx += 1
            
            output[str(node_id)] = {
                'inputs': inputs,
                'class_type': node_type,
                '_meta': {'title': node.get('title', node_type)}
            }
        
        # Remove dangling references
        valid_ids = set(output.keys())
        for node_entry in output.values():
            to_remove = []
            for name, value in node_entry['inputs'].items():
                if isinstance(value, list) and len(value) == 2:
                    if str(value[0]) not in valid_ids:
                        to_remove.append(name)
            for name in to_remove:
                del node_entry['inputs'][name]
        
        return output


def convert_and_submit(input_path: str, prompts: str = None, name: str = None):
    """Convert workflow and optionally submit to ComfyUI."""
    print(f"Loading: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        workflow = json.load(f)
    
    print(f"Nodes: {len(workflow.get('nodes', []))}, Links: {len(workflow.get('links', []))}")
    
    exporter = ComfyUIExporter(workflow)
    print(f"Server node definitions: {len(exporter.node_defs)}")
    
    api = exporter.export()
    print(f"Exported: {len(api)} nodes")
    
    # Remove unsupported nodes
    to_remove = []
    for nid, node in api.items():
        ct = node.get('class_type', '')
        # Remove UUID nodes (group nodes not registered)
        if len(ct) == 36 and ct.count('-') == 4:
            to_remove.append(nid)
        # Remove rgthree nodes if not installed
        elif 'rgthree' in ct.lower() and ct not in exporter.node_defs:
            to_remove.append(nid)
    
    for nid in to_remove:
        print(f"Removing unsupported: {nid} ({api[nid].get('class_type')})")
        del api[nid]
    
    # Set prompts and name if provided
    if prompts and '443' in api:
        api['443']['inputs']['value'] = prompts
        print("Set prompts in node 443")
    if name and '500' in api:
        api['500']['inputs']['value'] = name
        print(f"Set name in node 500: {name}")
    
    return api


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python comfyui_export_api_v3.py <workflow.json> [output.json]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.rsplit('.', 1)[0] + '_api.json'
    
    api = convert_and_submit(input_file)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(api, f, indent=2)
    
    print(f"\nSaved: {output_file}")
