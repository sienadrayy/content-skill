#!/usr/bin/env python3
import urllib.request
import urllib.error

server = "http://192.168.29.60:8188"

try:
    response = urllib.request.urlopen(f"{server}/prompt", timeout=5)
    print(f"[OK] Connected to {server}")
    print(f"Status: {response.status}")
except urllib.error.URLError as e:
    print(f"[ERROR] Cannot reach {server}")
    print(f"Reason: {e.reason}")
except Exception as e:
    print(f"[ERROR] {e}")
