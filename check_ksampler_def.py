import requests
import json

resp = requests.get('http://192.168.29.60:8188/object_info')
info = resp.json()

ksampler = info.get('KSampler', {})
inputs = ksampler.get('input', {})

print("KSampler inputs from server:")
print("\nRequired:")
for name, spec in inputs.get('required', {}).items():
    print(f"  {name}: {spec[0] if spec else '?'}")

print("\nOptional:")
for name, spec in inputs.get('optional', {}).items():
    print(f"  {name}: {spec[0] if spec else '?'}")
