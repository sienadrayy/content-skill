#!/usr/bin/env python3
"""
ComfyUI Export API v5 - Proper Group Node Expansion
"""

import json
import sys
import requests
from typing import Any, Dict, List, Optional, Tuple

class ComfyUIExporter:
    def __init__(self, workflow: Dict[str, Any], server_url: str = "http://192.168.29.60:8188"):
        self.original_workflow = workflow
        self.server_url = server_url
        self.node_defs = self._fetch_node_defs()
        
        # Deep copy for modification
        self.workflow = json.loads(json.dumps(workflow))
        
        # Expand subgraphs
        self._expand_all_subgraphs()
        
        # Build maps
        self.nodes = {n['id']: n for n in self.workflow.get('nodes', [])}
        self.links = {}
        for link in self.workflow.get('links', []):
            if isinstance(link, list):
                self.links[link[0]] = link
            elif isinstance(link, dict):
                lid = link.get('id')
                self.links[lid] = [lid, link.get('origin_id'), link.get('origin_slot'),
                                   link.get('target_id'), link.get('target_slot'), link.get('type')]
        
        self.bypassed = {n['id'] for n in self.workflow.get('nodes', []) if n.get('mode') in [2, 4]}
    
    def _fetch_node_defs(self) -> Dict[str, Any]:
        try:
            resp = requests.get(f"{self.server_url}/object_info", timeout=10)
            return resp.json() if resp.status_code == 200 else {}
        except:
            return {}
    
    def _expand_all_subgraphs(self):
        """Expand all subgraph nodes into their inner nodes."""
        subgraphs = self.workflow.get('definitions', {}).get('subgraphs', [])
        if not subgraphs:
            return
        
        sg_map = {sg['id']: sg for sg in subgraphs}
        
        # Find group nodes
        group_nodes = [(n, sg_map[n['type']]) for n in self.workflow.get('nodes', []) 
                       if n.get('type') in sg_map]
        
        if not group_nodes:
            return
        
        print(f"Expanding {len(group_nodes)} group node(s)...")
        
        max_node_id = max(n['id'] for n in self.workflow['nodes'])
        max_link_id = max(l[0] for l in self.workflow['links']) if self.workflow['links'] else 0
        
        for group_node, sg_def in group_nodes:
            group_id = group_node['id']
            
            # Get inner nodes and links
            inner_nodes = json.loads(json.dumps(sg_def.get('nodes', [])))
            inner_links = json.loads(json.dumps(sg_def.get('links', [])))
            sg_inputs = sg_def.get('inputs', [])
            sg_outputs = sg_def.get('outputs', [])
            
            # Create ID remapping
            node_remap = {}
            link_remap = {}
            
            for n in inner_nodes:
                max_node_id += 1
                node_remap[n['id']] = max_node_id
                n['id'] = max_node_id
            
            for link in inner_links:
                if isinstance(link, dict):
                    max_link_id += 1
                    old_id = link['id']
                    link_remap[old_id] = max_link_id
                    link['id'] = max_link_id
                    link['origin_id'] = node_remap.get(link['origin_id'], link['origin_id'])
                    link['target_id'] = node_remap.get(link['target_id'], link['target_id'])
            
            # Update inner node link references
            for n in inner_nodes:
                for inp in n.get('inputs', []):
                    if inp.get('link') in link_remap:
                        inp['link'] = link_remap[inp['link']]
                for out in n.get('outputs', []):
                    if out.get('links'):
                        out['links'] = [link_remap.get(l, l) for l in out['links']]
            
            # Wire external inputs to inner nodes
            for i, sg_input in enumerate(sg_inputs):
                inner_link_ids = sg_input.get('linkIds', [])
                external_link_id = group_node['inputs'][i].get('link') if i < len(group_node.get('inputs', [])) else None
                
                if external_link_id and inner_link_ids:
                    # Find the external link
                    ext_link = next((l for l in self.workflow['links'] if l[0] == external_link_id), None)
                    if ext_link:
                        source_node, source_slot = ext_link[1], ext_link[2]
                        
                        # Update each inner link that expects this input
                        for inner_lid in inner_link_ids:
                            new_lid = link_remap.get(inner_lid, inner_lid)
                            # Find inner link
                            for link in inner_links:
                                if isinstance(link, dict) and link['id'] == new_lid:
                                    link['origin_id'] = source_node
                                    link['origin_slot'] = source_slot
                                    break
            
            # Wire inner outputs to external targets
            for i, sg_output in enumerate(sg_outputs):
                inner_link_ids = sg_output.get('linkIds', [])
                ext_output_links = group_node['outputs'][i].get('links', []) if i < len(group_node.get('outputs', [])) else []
                
                if inner_link_ids and ext_output_links:
                    # Find the inner node that produces the output
                    inner_lid = inner_link_ids[0]
                    new_lid = link_remap.get(inner_lid, inner_lid)
                    inner_link = next((l for l in inner_links if isinstance(l, dict) and l['id'] == new_lid), None)
                    
                    if inner_link:
                        output_node_id = inner_link['target_id']  # Actually origin_id for output
                        output_slot = inner_link['target_slot']
                        
                        # Find the actual output node (it receives from some node)
                        # The output link goes INTO the output port, so origin is the producer
                        producer_node = inner_link['origin_id']
                        producer_slot = inner_link['origin_slot']
                        
                        # Update external links to point to the producer
                        for ext_lid in ext_output_links:
                            for link in self.workflow['links']:
                                if link[0] == ext_lid:
                                    link[1] = producer_node
                                    link[2] = producer_slot
                                    break
            
            # Add inner nodes and links
            self.workflow['nodes'].extend(inner_nodes)
            for link in inner_links:
                if isinstance(link, dict):
                    self.workflow['links'].append([
                        link['id'], link['origin_id'], link['origin_slot'],
                        link['target_id'], link['target_slot'], link.get('type', '*')
                    ])
            
            # Remove group node
            self.workflow['nodes'] = [n for n in self.workflow['nodes'] if n['id'] != group_id]
            
            print(f"  Expanded {group_id}: +{len(inner_nodes)} nodes, +{len(inner_links)} links")
    
    def _get_widget_inputs(self, node_type: str) -> List[str]:
        if node_type not in self.node_defs:
            return []
        
        widget_inputs = []
        input_def = self.node_defs[node_type].get('input', {})
        for cat in ['required', 'optional']:
            for name, spec in input_def.get(cat, {}).items():
                if isinstance(spec, list) and spec and isinstance(spec[0], str):
                    if spec[0].upper() in ['MODEL', 'VAE', 'CLIP', 'CONDITIONING', 'LATENT', 
                                           'IMAGE', 'MASK', 'CONTROL_NET', 'SIGMAS', 'SAMPLER', 
                                           'NOISE', 'GUIDER', 'UPSCALE_MODEL', '*']:
                        continue
                widget_inputs.append(name)
        return widget_inputs
    
    def _resolve_link(self, link_id: int) -> Optional[Tuple[int, int]]:
        if link_id not in self.links:
            return None
        link = self.links[link_id]
        src, slot = link[1], link[2]
        if src in self.bypassed:
            node = self.nodes.get(src)
            if node:
                for inp in node.get('inputs', []):
                    if inp.get('link'):
                        return self._resolve_link(inp['link'])
            return None
        return (src, slot)
    
    def export(self) -> Dict[str, Dict[str, Any]]:
        output = {}
        
        for nid, node in self.nodes.items():
            ntype = node.get('type')
            if not ntype or node.get('mode') in [2, 4] or ntype in ['Note', 'Reroute']:
                continue
            
            # Skip unregistered types
            if len(ntype) == 36 and ntype.count('-') == 4 and ntype not in self.node_defs:
                continue
            
            inputs = {}
            connected = {inp['name'] for inp in node.get('inputs', []) if inp.get('link')}
            
            for inp in node.get('inputs', []):
                if inp.get('link'):
                    resolved = self._resolve_link(inp['link'])
                    if resolved:
                        inputs[inp['name']] = [str(resolved[0]), resolved[1]]
            
            widget_names = self._get_widget_inputs(ntype)
            wv = node.get('widgets_values', [])
            
            if isinstance(wv, dict):
                for k, v in wv.items():
                    if k not in connected:
                        inputs[k] = v
            elif isinstance(wv, list) and widget_names:
                idx = 0
                for name in widget_names:
                    if name in inputs or name in connected:
                        continue
                    if idx < len(wv):
                        v = wv[idx]
                        idx += 1
                        while isinstance(v, str) and v in ['fixed', 'increment', 'decrement', 'randomize']:
                            if idx < len(wv):
                                v = wv[idx]
                                idx += 1
                            else:
                                v = None
                                break
                        if v is not None:
                            inputs[name] = {'__value__': v} if isinstance(v, list) else v
            
            output[str(nid)] = {
                'inputs': inputs,
                'class_type': ntype,
                '_meta': {'title': node.get('title', ntype)}
            }
        
        # Clean dangling refs
        valid = set(output.keys())
        for e in output.values():
            to_del = [k for k, v in e['inputs'].items() if isinstance(v, list) and len(v) == 2 and str(v[0]) not in valid]
            for k in to_del:
                del e['inputs'][k]
        
        return output


def convert(input_path: str, output_path: str = None):
    print(f"Loading: {input_path}")
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        wf = json.load(f)
    
    print(f"Nodes: {len(wf.get('nodes', []))}")
    
    exporter = ComfyUIExporter(wf)
    api = exporter.export()
    print(f"Exported: {len(api)} nodes")
    
    # Remove unsupported
    to_rm = [k for k, v in api.items() if 'rgthree' in v.get('class_type', '').lower()]
    for k in to_rm:
        del api[k]
    
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(api, f, indent=2)
        print(f"Saved: {output_path}")
    
    return api


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python comfyui_export_api_v5.py <workflow.json> [output.json]")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else sys.argv[1].rsplit('.', 1)[0] + '_api.json')
