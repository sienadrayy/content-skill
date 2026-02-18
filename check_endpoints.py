import requests

base_url = "http://192.168.29.60:8188"

# Try to get the root endpoint
try:
    resp = requests.get(f"{base_url}/", timeout=5)
    print(f"Root (status {resp.status_code}):")
    print(resp.text[:500])
except Exception as e:
    print(f"Root: {e}")

# Try /api
try:
    resp = requests.get(f"{base_url}/api", timeout=5)
    print(f"\n/api (status {resp.status_code}):")
    print(resp.text[:500])
except Exception as e:
    print(f"/api: {e}")

# Try /system
try:
    resp = requests.get(f"{base_url}/system", timeout=5)
    print(f"\n/system (status {resp.status_code}):")
    print(resp.text[:500])
except Exception as e:
    print(f"/system: {e}")

# Try /info
try:
    resp = requests.get(f"{base_url}/info", timeout=5)
    print(f"\n/info (status {resp.status_code}):")
    print(resp.text[:200])
except Exception as e:
    print(f"/info: {e}")
