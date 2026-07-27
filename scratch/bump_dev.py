import os
import re

configs = [
    'bambuddy/config.yaml',
    'obico-ml-api/config.yaml',
    'slicer-api-bambu/config.yaml',
    'slicer-api-orca/config.yaml'
]

print("Bumping dev version tags...")

def bump_version(match):
    base_version = match.group(1)
    dev_tag = match.group(2)
    
    if dev_tag:
        # Increment existing dev tag (e.g., "-4" becomes "-5")
        current_num = int(dev_tag[1:])
        new_tag = f"-{current_num + 1}"
    else:
        # No dev tag exists, append "-1"
        new_tag = "-1"
        
    return f'version: "{base_version}{new_tag}"'

for config in configs:
    if os.path.exists(config):
        with open(config, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex to match: version: "1.2.5.0-5" or version: "1.2.5.0"
        # Group 1: base version (e.g., 1.2.5.0)
        # Group 2: dev tag including the hyphen (e.g., -5), optional
        new_content = re.sub(r'^version:\s*"([0-9\.]+)(-\d+)?"', bump_version, content, flags=re.MULTILINE)
        
        if new_content != content:
            with open(config, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Bumped version in {config}")
        else:
            print(f"No version bump needed or found in {config}")

print("Done!")
