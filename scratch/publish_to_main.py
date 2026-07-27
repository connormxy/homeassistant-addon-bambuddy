import os
import subprocess

def run_cmd(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

print("Starting Release Preparation Script...")

configs = [
    'bambuddy/config.yaml',
    'obico-ml-api/config.yaml',
    'slicer-api-bambu/config.yaml',
    'slicer-api-orca/config.yaml'
]

print("Stripping DEV labels from config.yaml files...")
for config in configs:
    if os.path.exists(config):
        with open(config, 'r', encoding='utf-8') as f:
            content = f.read()
        
        import re
        
        # Strip (DEV) prefix or suffix from names
        content = re.sub(r'^(name:\s*"?)\(DEV\)\s*', r'\1', content, flags=re.MULTILINE)
        content = re.sub(r'^(name:.*?)\s*\(DEV\)', r'\1', content, flags=re.MULTILINE)
        
        # Strip DEV from descriptions
        content = re.sub(r'^(description:\s*"?)\(DEV\)\s*', r'\1', content, flags=re.MULTILINE)
        content = re.sub(r'^(description:.*?)\s*\(DEV\)', r'\1', content, flags=re.MULTILINE)
        
        # Fallback for any other loose (DEV) tags
        content = content.replace(' (DEV)', '')
        content = content.replace('"(DEV) ', '"')
        
        # Clean slugs
        content = content.replace('slug: bambuddy-dev', 'slug: bambuddy')
        content = content.replace('_dev\n', '\n')
        
        # Strip URL dev suffixes
        content = content.replace('#dev', '')
        
        # Remove experimental stage
        content = content.replace('stage: experimental\n', '')
        
        # Strip trailing modifiers like -0 or -dev from the version string
        content = re.sub(r'^(version:\s*".*?)-.*?"', r'\1"', content, flags=re.MULTILINE)
        
        with open(config, 'w', encoding='utf-8') as f:
            f.write(content)

repo_json_path = 'repository.json'
if os.path.exists(repo_json_path):
    print("Stripping DEV references from repository.json...")
    with open(repo_json_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    import re
    content = re.sub(r'("name":\s*".*?)\s*\(DEV\)', r'\1', content)
    content = content.replace('#dev', '')
    
    with open(repo_json_path, 'w', encoding='utf-8') as f:
        f.write(content)

readme_path = 'README.md'
if os.path.exists(readme_path):
    print("Stripping DEV references from README.md...")
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove Dev Branch heading
    content = content.replace('# Dev Branch\n\n', '')
    
    # Clean installation badges
    content = content.replace('**Dev Branch:** [![Open your', '[![Open your')
    content = content.replace('homeassistant-addon-bambuddy#dev)', 'homeassistant-addon-bambuddy)')
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)

import shutil
github_dir = '.github'
if os.path.exists(github_dir):
    print("Stripping DEV auto-updater workflows by deleting .github directory...")
    shutil.rmtree(github_dir)

print("Done! The files are now ready to be pushed to main.")
print("If you want to push this to main automatically, you can run:")
print("git checkout main && git merge dev --allow-unrelated-histories -X theirs && python scratch/publish_to_main.py && git commit -am 'chore: prepare release' && git push origin main && git checkout dev")
