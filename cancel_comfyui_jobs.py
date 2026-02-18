#!/usr/bin/env python3
"""
Cancel all ComfyUI jobs
"""

import urllib.request
import json

server_url = "http://192.168.29.60:8188"

try:
    # Get current queue
    print("[*] Checking current queue...")
    with urllib.request.urlopen(f"{server_url}/queue", timeout=5) as response:
        queue_data = json.loads(response.read().decode('utf-8'))
        queue_pending = queue_data.get("queue_pending", [])
        queue_running = queue_data.get("queue_running", [])
        
        print(f"   Pending jobs: {len(queue_pending)}")
        print(f"   Running jobs: {len(queue_running)}")
        
        # Send interrupt signal to stop current execution
        if queue_running or queue_pending:
            print("\n[*] Sending interrupt signal...")
            try:
                req = urllib.request.Request(
                    f"{server_url}/interrupt",
                    method="POST"
                )
                urllib.request.urlopen(req, timeout=5)
                print("   [OK] Interrupt signal sent")
            except Exception as e:
                print(f"   [!] Error sending interrupt: {e}")
        
        if not queue_pending and not queue_running:
            print("\n[OK] No active jobs in queue")
        else:
            print("\n[SUCCESS] All jobs interrupted/canceled")
        
except Exception as e:
    print(f"[ERROR] Cannot connect to ComfyUI: {e}")
    print("\nTip: You can also manually clear queue at:")
    print(f"  {server_url}/ui")
