#!/usr/bin/env python3
"""
ComfyUI Export API v4 - With Group Node (Subgraph) Expansion
"""

import json
import sys
import requests
from typing import Any, Dict, List, Optional, Tuple

class ComfyUIExporter:
    def __init__(self, workflow: Dict[str, Any], server_url: str = "http://192.168.29.60:8188"):
        self.workflow = workflow
        self.server_url = server_url
        self.node_defs = self._fetch_node_defs()
        
        # Expand subgraphs first
        self._expand_subgraphs()
        
        # Build node/link maps
        self.nodes = {n['id']: n for n in self.workflow.get('nodes', [])}
        # Handle both list and dict link formats
        self.links = {}
        for link in self.workflow.get('links', []):
            if isinstance(link, list):
                self.links[link[0]] = link
            elif isinstance(link, dict):
                self.links[link.get('id')] = [
                    link.get('id'), link.get('origin_id'), link.get('origin_slot'),
                    link.get('target_id'), link.get('target_slot'), link.get('type')
                ]
        
        # Track bypassed nodes
        self.bypassed_nodes = set()
        for node in self.workflow.get('nodes', []):
            if node.get('mode') in [2, 4]:
                self.bypassed_nodes.add(node['id'])
    
    def _fetch_node_defs(self) -> Dict[str, Any]:
        try:
            resp = requests.get(f"{self.server_url}/object_info", timeout=10)
            return resp.json() if resp.status_code == 200 else {}
        except:
            return {}
    
    def _expand_subgraphs(self):
        """Expand all subgraph/group nodes into their inner nodes."""
        subgraphs = self.workflow.get('definitions', {}).get('subgraphs', [])
        if not subgraphs:
            return
        
        # Build subgraph definition map
        sg_map = {sg['id']: sg for sg in subgraphs}
        
        # Find group nodes (UUID types that match subgraph IDs)
        nodes_to_expand = []
        for node in self.workflow.get('nodes', []):
            node_type = node.get('type', '')
            if node_type in sg_map:
                nodes_to_expand.append((node, sg_map[node_type]))
        
        if not nodes_to_expand:
            return
        
        print(f"Expanding {len(nodes_to_expand)} group node(s)...")
        
        # Get max IDs for generating new unique IDs
        max_node_id = max(n['id'] for n in self.workflow['nodes'])
        max_link_id = max(l[0] for l in self.workflow['links']) if self.workflow['links'] else 0
        
        for group_node, subgraph_def in nodes_to_expand:
            group_id = group_node['id']
            group_inputs = group_node.get('inputs', [])
            group_outputs = group_node.get('outputs', [])
            
            # Map old inner node IDs to new IDs
            inner_nodes = subgraph_def.get('nodes', [])
            inner_links = subgraph_def.get('links', [])
            
            id_remap = {}
            for inner_node in inner_nodes:
                max_node_id += 1
                id_remap[inner_node['id']] = max_node_id
                inner_node['id'] = max_node_id
            
            # Remap inner links
            for link in inner_links:
                max_link_id += 1
                old_link_id = link[0] if isinstance(link, list) else link.get('id')
                link_source = link[1] if isinstance(link, list) else link.get('origin_id')
                link_target = link[3] if isinstance(link, list) else link.get('target_id')
                
                if isinstance(link, list):
                    link[0] = max_link_id
                    if link[1] in id_remap:
                        link[1] = id_remap[link[1]]
                    if link[3] in id_remap:
                        link[3] = id_remap[link[3]]
            
            # Update inner node input/output link references
            for inner_node in inner_nodes:
                for inp in inner_node.get('inputs', []):
                    if inp.get('link') is not None:
                        # Find and update link reference
                        pass
                for out in inner_node.get('outputs', []):
                    if out.get('links'):
                        # Update link references
                        pass
            
            # Connect group node inputs to inner graph input nodes
            # Connect inner graph output nodes to group node outputs
            # This requires finding the IO nodes in the subgraph
            
            # Add inner nodes to main workflow
            self.workflow['nodes'].extend(inner_nodes)
            if inner_links:
                self.workflow['links'].extend(inner_links)
            
            # Remove the group node from main workflow
            self.workflow['nodes'] = [n for n in self.workflow['nodes'] if n['id'] != group_id]
            
            print(f"  Expanded group {group_id}: +{len(inner_nodes)} nodes")
    
    def _get_widget_inputs(self, node_type: str) -> List[str]:
        if node_type not in self.node_defs:
            return []
        
        node_def = self.node_defs[node_type]
        input_def = node_def.get('input', {})
        
        widget_inputs = []
        for category in ['required', 'optional']:
            for name, spec in input_def.get(category, {}).items():
                if isinstance(spec, list) and len(spec) > 0:
                    input_type = spec[0]
                    if isinstance(input_type, str) and input_type.upper() in [
                        'MODEL', 'VAE', 'CLIP', 'CONDITIONING', 'LATENT', 'IMAGE',
                        'MASK', 'CONTROL_NET', 'SIGMAS', 'SAMPLER', 'NOISE',
                        'GUIDER', 'UPSCALE_MODEL', '*'
                    ]:
                        continue
                widget_inputs.append(name)
        
        return widget_inputs
    
    def _resolve_link(self, link_id: int) -> Optional[Tuple[int, int]]:
        if link_id not in self.links:
            return None
        
        link = self.links[link_id]
        source_node_id = link[1]
        source_slot = link[2]
        
        if source_node_id in self.bypassed_nodes:
            source_node = self.nodes.get(source_node_id)
            if source_node and source_node.get('inputs'):
                for inp in source_node['inputs']:
                    if inp.get('link') is not None:
                        return self._resolve_link(inp['link'])
            return None
        
        return (source_node_id, source_slot)
    
    def export(self) -> Dict[str, Dict[str, Any]]:
        output = {}
        
        for node_id, node in self.nodes.items():
            node_type = node.get('type')
            if not node_type:
                continue
            
            mode = node.get('mode', 0)
            if mode in [2, 4]:
                continue
            
            if node_type in ['Note', 'Reroute']:
                continue
            
            # Skip unregistered group nodes
            if len(node_type) == 36 and node_type.count('-') == 4:
                if node_type not in self.node_defs:
                    continue
            
            inputs = {}
            node_inputs = node.get('inputs', [])
            widgets_values = node.get('widgets_values', [])
            
            connected_inputs = set()
            for inp in node_inputs:
                if inp.get('link') is not None:
                    connected_inputs.add(inp['name'])
            
            for inp in node_inputs:
                link_id = inp.get('link')
                if link_id is not None:
                    resolved = self._resolve_link(link_id)
                    if resolved:
                        inputs[inp['name']] = [str(resolved[0]), resolved[1]]
            
            widget_names = self._get_widget_inputs(node_type)
            
            if isinstance(widgets_values, dict):
                for name, value in widgets_values.items():
                    if name not in connected_inputs:
                        inputs[name] = value
            elif isinstance(widgets_values, list) and widget_names:
                widget_idx = 0
                for name in widget_names:
                    if name in inputs or name in connected_inputs:
                        continue
                    
                    if widget_idx < len(widgets_values):
                        value = widgets_values[widget_idx]
                        widget_idx += 1
                        
                        while isinstance(value, str) and value in ['fixed', 'increment', 'decrement', 'randomize']:
                            if widget_idx < len(widgets_values):
                                value = widgets_values[widget_idx]
                                widget_idx += 1
                            else:
                                value = None
                                break
                        
                        if value is not None:
                            if isinstance(value, list):
                                inputs[name] = {'__value__': value}
                            else:
                                inputs[name] = value
            
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


def convert(input_path: str, output_path: str = None):
    print(f"Loading: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        workflow = json.load(f)
    
    print(f"Nodes: {len(workflow.get('nodes', []))}, Links: {len(workflow.get('links', []))}")
    
    exporter = ComfyUIExporter(workflow)
    api = exporter.export()
    print(f"Exported: {len(api)} nodes")
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(api, f, indent=2)
        print(f"Saved: {output_path}")
    
    return api


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python comfyui_export_api_v4.py <workflow.json> [output.json]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.rsplit('.', 1)[0] + '_api.json'
    convert(input_file, output_file)
