#!/usr/bin/env python3
"""
ComfyUI Export API v6 - Correct Group Node Expansion based on ComfyUI source

WIDGET VALUE MAPPING:
- widgets_values array contains values for ALL inputs with widget=yes, in slot order
- This includes inputs that now have links (link overrides widget value)
- Must iterate through node.inputs, consume value for each widget slot
- Only SET the value if slot has no link (link takes precedence)
- Control widgets (fixed/randomize/increment/decrement) are UI-only, skip them

SUBGRAPH EXPANSION:
- definitions.subgraphs contains group node definitions
- Each subgraph has inputs[].linkIds and outputs[].linkIds
- inputs[i].linkIds = inner links that receive external input (replace origin)
- outputs[i].linkIds = inner links that produce output (use origin as producer)
- Must remap all node IDs and link IDs to avoid collisions
"""

import json
import sys
import requests
from typing import Any, Dict, List, Optional, Tuple

class ComfyUIExporter:
    def __init__(self, workflow: Dict[str, Any], server_url: str = "http://192.168.29.60:8188"):
        self.server_url = server_url
        self.node_defs = self._fetch_node_defs()
        self.workflow = json.loads(json.dumps(workflow))
        
        self._expand_all_subgraphs()
        
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
            return requests.get(f"{self.server_url}/object_info", timeout=10).json()
        except:
            return {}
    
    def _expand_all_subgraphs(self):
        subgraphs = self.workflow.get('definitions', {}).get('subgraphs', [])
        if not subgraphs:
            return
        
        sg_map = {sg['id']: sg for sg in subgraphs}
        group_nodes = [(n, sg_map[n['type']]) for n in self.workflow.get('nodes', []) 
                       if n.get('type') in sg_map]
        
        if not group_nodes:
            return
        
        print(f"Expanding {len(group_nodes)} group node(s)...")
        
        max_node_id = max(n['id'] for n in self.workflow['nodes'])
        max_link_id = max(l[0] for l in self.workflow['links']) if self.workflow['links'] else 0
        
        for group_node, sg_def in group_nodes:
            group_id = group_node['id']
            
            inner_nodes = json.loads(json.dumps(sg_def.get('nodes', [])))
            inner_links_raw = sg_def.get('links', [])
            sg_inputs = sg_def.get('inputs', [])
            sg_outputs = sg_def.get('outputs', [])
            
            # Build inner link map (original IDs)
            inner_link_map = {}
            for link in inner_links_raw:
                if isinstance(link, dict):
                    inner_link_map[link['id']] = link
            
            # Remap node IDs
            node_remap = {}
            for n in inner_nodes:
                max_node_id += 1
                node_remap[n['id']] = max_node_id
                n['id'] = max_node_id
            
            # Remap link IDs and node references
            link_remap = {}
            inner_links = []
            for link in inner_links_raw:
                if isinstance(link, dict):
                    max_link_id += 1
                    link_remap[link['id']] = max_link_id
                    new_link = {
                        'id': max_link_id,
                        'origin_id': node_remap.get(link['origin_id'], link['origin_id']),
                        'origin_slot': link['origin_slot'],
                        'target_id': node_remap.get(link['target_id'], link['target_id']),
                        'target_slot': link['target_slot'],
                        'type': link.get('type', '*')
                    }
                    inner_links.append(new_link)
            
            # Update inner node link references
            for n in inner_nodes:
                for inp in n.get('inputs', []):
                    if inp.get('link') in link_remap:
                        inp['link'] = link_remap[inp['link']]
                for out in n.get('outputs', []):
                    if out.get('links'):
                        out['links'] = [link_remap.get(l, l) for l in out['links']]
            
            # CRITICAL: Wire external inputs to inner nodes
            # sg_inputs[i].linkIds tells which inner links receive this external input
            for i, sg_input in enumerate(sg_inputs):
                inner_link_ids = sg_input.get('linkIds', [])
                ext_input = group_node['inputs'][i] if i < len(group_node.get('inputs', [])) else None
                ext_link_id = ext_input.get('link') if ext_input else None
                
                if ext_link_id:
                    # Find external link source
                    ext_link = next((l for l in self.workflow['links'] if l[0] == ext_link_id), None)
                    if ext_link:
                        ext_source_node = ext_link[1]
                        ext_source_slot = ext_link[2]
                        
                        # Update each inner link that expects this input
                        for old_inner_lid in inner_link_ids:
                            new_inner_lid = link_remap.get(old_inner_lid)
                            if new_inner_lid:
                                for link in inner_links:
                                    if link['id'] == new_inner_lid:
                                        # Replace the origin with external source
                                        link['origin_id'] = ext_source_node
                                        link['origin_slot'] = ext_source_slot
                                        break
            
            # CRITICAL: Wire inner outputs to external targets
            # sg_outputs[i].linkIds tells which inner link produces this output
            for i, sg_output in enumerate(sg_outputs):
                inner_link_ids = sg_output.get('linkIds', [])
                ext_output = group_node['outputs'][i] if i < len(group_node.get('outputs', [])) else None
                ext_output_links = ext_output.get('links', []) if ext_output else []
                
                if inner_link_ids and ext_output_links:
                    # Find the inner node that produces the output
                    old_inner_lid = inner_link_ids[0]
                    new_inner_lid = link_remap.get(old_inner_lid)
                    
                    # Find the link in inner_links
                    producer_node = None
                    producer_slot = None
                    for link in inner_links:
                        if link['id'] == new_inner_lid:
                            # The origin of this link is the producer
                            producer_node = link['origin_id']
                            producer_slot = link['origin_slot']
                            break
                    
                    if producer_node is not None:
                        # Update all external links from this output to point to the producer
                        for ext_lid in ext_output_links:
                            for link in self.workflow['links']:
                                if link[0] == ext_lid:
                                    link[1] = producer_node
                                    link[2] = producer_slot
                                    break
            
            # Add inner nodes
            self.workflow['nodes'].extend(inner_nodes)
            
            # Add inner links (convert to list format)
            for link in inner_links:
                self.workflow['links'].append([
                    link['id'], link['origin_id'], link['origin_slot'],
                    link['target_id'], link['target_slot'], link.get('type', '*')
                ])
            
            # Remove group node
            self.workflow['nodes'] = [n for n in self.workflow['nodes'] if n['id'] != group_id]
            
            print(f"  Expanded {group_id}: +{len(inner_nodes)} nodes")
    
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
    
    def _resolve_link(self, link_id: int, visited: set = None) -> Optional[Tuple[int, int]]:
        if visited is None:
            visited = set()
        if link_id in visited:
            return None  # Circular reference
        visited.add(link_id)
        
        if link_id not in self.links:
            return None
        link = self.links[link_id]
        src, slot = link[1], link[2]
        node = self.nodes.get(src)
        
        if not node:
            return None
        
        # Follow through bypassed nodes and Reroute nodes
        if src in self.bypassed or node.get('type') == 'Reroute':
            for inp in node.get('inputs', []):
                if inp.get('link'):
                    return self._resolve_link(inp['link'], visited)
            return None
        
        return (src, slot)
    
    def export(self) -> Dict[str, Dict[str, Any]]:
        output = {}
        
        for nid, node in self.nodes.items():
            ntype = node.get('type')
            if not ntype or node.get('mode') in [2, 4] or ntype in ['Note', 'Reroute']:
                continue
            if len(ntype) == 36 and ntype.count('-') == 4 and ntype not in self.node_defs:
                continue
            
            inputs = {}
            connected = {inp['name'] for inp in node.get('inputs', []) if inp.get('link')}
            
            for inp in node.get('inputs', []):
                if inp.get('link'):
                    resolved = self._resolve_link(inp['link'])
                    if resolved:
                        inputs[inp['name']] = [str(resolved[0]), resolved[1]]
            
            wv = node.get('widgets_values', [])
            node_inputs = node.get('inputs', [])
            
            if isinstance(wv, dict):
                for k, v in wv.items():
                    if k not in connected:
                        inputs[k] = v
            elif isinstance(wv, list):
                # widgets_values contains values for ALL widget inputs (even those with links)
                # We consume values for all widget inputs, but only SET for unlinked ones
                idx = 0
                for inp in node_inputs:
                    inp_name = inp.get('name')
                    has_widget = 'widget' in inp
                    has_link = inp.get('link') is not None
                    
                    # Consume widget value if this is a widget input
                    if has_widget:
                        if idx < len(wv):
                            v = wv[idx]
                            idx += 1
                            
                            # Skip control_after_generate values
                            while isinstance(v, str) and v in ['fixed', 'increment', 'decrement', 'randomize']:
                                if idx < len(wv):
                                    v = wv[idx]
                                    idx += 1
                                else:
                                    v = None
                                    break
                            
                            # Only set value if no link (link takes precedence)
                            if not has_link and inp_name not in inputs and v is not None:
                                inputs[inp_name] = {'__value__': v} if isinstance(v, list) else v
                
                # Fallback: use server definitions for nodes without widget slots
                if not node_inputs or not any('widget' in inp for inp in node_inputs):
                    widget_names = self._get_widget_inputs(ntype)
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
        print("Usage: python comfyui_export_api_v6.py <workflow.json> [output.json]")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else sys.argv[1].rsplit('.', 1)[0] + '_api.json')
