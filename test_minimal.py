import requests
import json

# Minimal workflow - just load a VAE and save a latent
minimal = {
    "1": {
        "inputs": {
            "pixels": ["2", 0]
        },
        "class_type": "VAEEncode"
    },
    "2": {
        "inputs": {
            "vae_name": "sd15_vae.safetensors"
        },
        "class_type": "VAELoader"
    },
    "3": {
        "inputs": {
            "images": ["2", 0]
        },
        "class_type": "SaveImage"
    }
}

print("Submitting minimal test workflow...")
response = requests.post('http://192.168.29.60:8188/prompt', json=minimal)
print(f"Status: {response.status_code}")
result = response.json()
print(f"Response: {json.dumps(result, indent=2)[:500]}")
