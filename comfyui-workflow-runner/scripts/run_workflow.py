#!/usr/bin/env python3
"""
ComfyUI Workflow Runner
Executes ComfyUI workflows via HTTP API with input parameter substitution.
"""

import json
import urllib.request
import urllib.error
import sys
import time
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional


class ComfyUIRunner:
    def __init__(self, server_url: str = "http://192.168.29.60:8188"):
        self.server_url = server_url.rstrip("/")
        self.prompt_endpoint = f"{self.server_url}/prompt"
        self.history_endpoint = f"{self.server_url}/history"
        self.queue_endpoint = f"{self.server_url}/queue"

    def load_workflow(self, workflow_path: str) -> Dict[str, Any]:
        """Load workflow JSON file (both old and new formats supported)."""
        path = Path(workflow_path)
        if not path.exists():
            raise FileNotFoundError(f"Workflow file not found: {workflow_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _convert_workflow_format(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Convert new ComfyUI graph format to old flat prompt format."""
        # Check if already in old format
        if 'nodes' not in workflow:
            return workflow  # Already in old format
        
        old_format = {}
        node_id_map = {}
        
        # Skip non-executable node types
        SKIP_TYPES = {'MarkdownNote', 'Note', 'Reroute', 'UI'}
        
        # Step 1: Build basic structure - only convert executable nodes
        for node in workflow.get('nodes', []):
            node_id = str(node.get('id'))
            node_type = node.get('type', 'Unknown')
            
            # Skip documentation and UI nodes
            if node_type in SKIP_TYPES:
                continue
            
            node_id_map[node.get('id')] = node_id
            title = node.get('title', '')
            
            inputs = {}
            
            # Only extract values from widgets_values for known types
            if 'Bypasser' in node_type:
                inputs['mode'] = node.get('mode', 0)
            elif 'widgets_values' in node and isinstance(node['widgets_values'], list):
                widgets = node['widgets_values']
                # For text nodes, just take first widget value
                if node_type in ['PrimitiveStringMultiline', 'Text Multiline']:
                    if widgets:
                        inputs['value'] = widgets[0]
                else:
                    # For other nodes, preserve widget values as-is
                    if len(widgets) == 1:
                        inputs['value'] = widgets[0]
                    elif len(widgets) > 0:
                        for i, val in enumerate(widgets):
                            inputs[f'widget_{i}'] = val
            
            old_format[node_id] = {
                'inputs': inputs,
                'class_type': node_type,
                '_meta': {'title': title}
            }
        
        # Step 2: Process links to add connections (only between executable nodes)
        for link in workflow.get('links', []):
            if len(link) < 5:
                continue
            
            link_id, source_id, output_idx, target_id, input_idx = link[:5]
            
            # Convert IDs to ints for comparison
            try:
                source_id_int = int(source_id) if not isinstance(source_id, int) else source_id
                target_id_int = int(target_id) if not isinstance(target_id, int) else target_id
            except:
                continue
            
            # Skip if either node is not in our map (i.e., was skipped)
            if source_id_int not in node_id_map or target_id_int not in node_id_map:
                continue
            
            source_node_id = node_id_map[source_id_int]
            target_node_id = node_id_map[target_id_int]
            
            # Find input name from target node
            target_node = None
            for node in workflow.get('nodes', []):
                if node.get('id') == target_id_int:
                    target_node = node
                    break
            
            if not target_node:
                continue
            
            # Get input name
            input_name = f'input_{input_idx}'
            if 'inputs' in target_node and isinstance(target_node['inputs'], list):
                if input_idx < len(target_node['inputs']):
                    input_name = target_node['inputs'][input_idx].get('name', f'input_{input_idx}')
            
            # Add connection
            if target_node_id in old_format:
                old_format[target_node_id]['inputs'][input_name] = [source_node_id, output_idx]
        
        return old_format

    def substitute_inputs(self, workflow: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Substitute input values in workflow widgets_values (new format only).
        Does NOT convert format - modifies in-place and returns.
        
        inputs format: {"node_id.field": value}
        For new format: Updates widgets_values[0] for nodes with that widget name
        """
        workflow_copy = json.loads(json.dumps(workflow))  # Deep copy
        
        # Only works with new format (has 'nodes' array)
        if 'nodes' not in workflow_copy:
            return workflow_copy  # Old format, return as-is
        
        # Build node map by ID for quick lookup
        node_map = {node.get('id'): node for node in workflow_copy.get('nodes', [])}
        
        for key, value in inputs.items():
            if "." not in key:
                continue
            
            node_id_str, field = key.split(".", 1)
            
            try:
                node_id = int(node_id_str)
            except:
                continue
            
            if node_id not in node_map:
                continue
            
            node = node_map[node_id]
            
            # Update widgets_values (first element for text nodes)
            if 'widgets_values' in node and isinstance(node['widgets_values'], list):
                if len(node['widgets_values']) > 0:
                    # For nodes like PrimitiveStringMultiline, update first widget
                    if field == 'value' or field == 'text':
                        node['widgets_values'][0] = value
                        print(f"[OK] Updated node {node_id} - {field}: {str(value)[:50]}")
            
            # Update mode for Bypasser nodes
            if 'mode' in field and 'Bypasser' in node.get('type', ''):
                node['mode'] = value
                print(f"[OK] Updated node {node_id} - mode: {value}")
        
        return workflow_copy

    def validate_workflow(self, workflow: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate workflow structure (accepts both old flat and new graph formats)."""
        if not isinstance(workflow, dict):
            return False, "Workflow must be a JSON object"
        
        if not workflow:
            return False, "Workflow is empty"
        
        # Accept both formats:
        # New: has 'nodes' and 'links' keys
        # Old: has node IDs as keys with 'inputs' and 'class_type'
        has_nodes = 'nodes' in workflow
        has_node_ids = any(isinstance(k, str) and (k.isdigit() or ':' in k) for k in workflow.keys())
        
        if not (has_nodes or has_node_ids or len(workflow) > 0):
            return False, "Workflow structure not recognized"
        
        return True, None

    def submit_workflow(self, workflow: Dict[str, Any]) -> Optional[str]:
        """
        Submit workflow to ComfyUI server as-is (no conversion).
        Returns prompt_id if successful, None otherwise.
        """
        valid, error = self.validate_workflow(workflow)
        if not valid:
            print(f"Validation error: {error}")
            return None
        
        try:
            # Send workflow directly without any conversion
            payload = {"prompt": workflow}
            payload_json = json.dumps(payload).encode('utf-8')
            
            req = urllib.request.Request(
                self.prompt_endpoint,
                data=payload_json,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                prompt_id = data.get("prompt_id")
                if prompt_id:
                    print(f"[OK] Workflow submitted. Prompt ID: {prompt_id}")
                    return prompt_id
                else:
                    print(f"Error response: {data}")
                    return None
        
        except urllib.error.HTTPError as e:
            error_data = e.read().decode('utf-8')
            try:
                error_json = json.loads(error_data)
                print(f"HTTP Error {e.code}: {error_json.get('error', {}).get('message', e.reason)}")
            except:
                print(f"HTTP Error {e.code}: {error_data}")
            return None
        except urllib.error.URLError as e:
            print(f"Connection error: Cannot reach ComfyUI at {self.server_url}")
            return None
        except Exception as e:
            print(f"Error submitting workflow: {e}")
            return None

    def check_execution_status(self, prompt_id: str) -> Dict[str, Any]:
        """
        Check execution status of a prompt.
        Returns execution status dict.
        """
        try:
            with urllib.request.urlopen(
                f"{self.history_endpoint}/{prompt_id}",
                timeout=10
            ) as response:
                history = json.loads(response.read().decode('utf-8'))
                if prompt_id in history:
                    return {
                        "status": "completed",
                        "data": history[prompt_id]
                    }
                else:
                    # Check queue
                    try:
                        with urllib.request.urlopen(self.queue_endpoint, timeout=10) as queue_response:
                            queue_data = json.loads(queue_response.read().decode('utf-8'))
                            queue_list = queue_data.get("queue_pending", [])
                            
                            for item in queue_list:
                                if item[1] == prompt_id:
                                    return {"status": "queued"}
                            
                            return {"status": "unknown"}
                    except Exception:
                        return {"status": "error", "message": "Cannot check queue"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def wait_for_completion(self, prompt_id: str, timeout: int = 300, poll_interval: int = 2) -> bool:
        """
        Wait for workflow execution to complete.
        Returns True if completed, False if timeout.
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.check_execution_status(prompt_id)
            
            if status["status"] == "completed":
                print(f"✓ Workflow completed!")
                return True
            elif status["status"] == "error":
                print(f"✗ Error: {status.get('message', 'Unknown error')}")
                return False
            elif status["status"] == "queued":
                print(f"⏳ Workflow queued...")
            else:
                print(f"⏳ Executing... (elapsed: {int(time.time() - start_time)}s)")
            
            time.sleep(poll_interval)
        
        print(f"✗ Timeout: Workflow did not complete within {timeout} seconds")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run ComfyUI workflows")
    parser.add_argument("workflow", help="Path to workflow JSON file")
    parser.add_argument("--inputs", help="Input parameters as JSON string or key=value pairs", default=None)
    parser.add_argument("--server", default="http://192.168.29.60:8188", help="ComfyUI server URL")
    parser.add_argument("--wait", action="store_true", help="Wait for execution to complete")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout in seconds (default: 300)")
    
    args = parser.parse_args()
    
    runner = ComfyUIRunner(args.server)
    
    # Load workflow
    try:
        workflow = runner.load_workflow(args.workflow)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Apply input substitutions if provided
    if args.inputs:
        try:
            # Try parsing as JSON first
            inputs = json.loads(args.inputs)
        except json.JSONDecodeError:
            # Parse as key=value pairs
            inputs = {}
            for pair in args.inputs.split(","):
                key, value = pair.split("=", 1)
                try:
                    inputs[key.strip()] = json.loads(value.strip())
                except json.JSONDecodeError:
                    inputs[key.strip()] = value.strip()
        
        workflow = runner.substitute_inputs(workflow, inputs)
        print(f"Applied {len(inputs)} input substitutions")
    
    # Submit workflow
    prompt_id = runner.submit_workflow(workflow)
    
    if not prompt_id:
        sys.exit(1)
    
    # Wait for completion if requested
    if args.wait:
        success = runner.wait_for_completion(prompt_id, timeout=args.timeout)
        sys.exit(0 if success else 1)
    else:
        print(f"Submitted with prompt_id: {prompt_id}")
        sys.exit(0)


if __name__ == "__main__":
    main()
