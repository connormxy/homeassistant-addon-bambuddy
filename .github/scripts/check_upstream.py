import urllib.request
import json
import os
import re

# Configuration for upstream tracking
# Format: "Addon Directory": ("Upstream Repo", "Branch")
REPOS_TO_TRACK = {
    "slicer-api-orca": ("maziggy/orca-slicer-api", "bambuddy/profile-resolver"),
    "slicer-api-bambu": ("maziggy/orca-slicer-api", "bambuddy/profile-resolver")
    # Note: Bambuddy is intentionally excluded because auto-updating it could break the custom .patch files during build.
}

SHA_FILE = ".github/upstream_shas.json"

def get_latest_sha(repo, branch):
    url = f"https://api.github.com/repos/{repo}/commits/{branch}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data['sha']
    except Exception as e:
        print(f"Error fetching SHA for {repo}/{branch}: {e}")
        return None

def bump_config_version(config_path):
    with open(config_path, 'r') as f:
        content = f.read()
    
    match = re.search(r'version:\s*"([^"]+)"', content)
    if not match:
        return False, None
    
    current_version = match.group(1)
    parts = current_version.split('.')
    
    # Increment the last segment (or add .1 if not purely numeric)
    if parts[-1].isdigit():
        parts[-1] = str(int(parts[-1]) + 1)
        new_version = '.'.join(parts)
    else:
        new_version = current_version + ".1"
        
    new_content = content[:match.start(1)] + new_version + content[match.end(1):]
    
    with open(config_path, 'w') as f:
        f.write(new_content)
        
    return True, new_version

def main():
    if os.path.exists(SHA_FILE):
        with open(SHA_FILE, 'r') as f:
            known_shas = json.load(f)
    else:
        known_shas = {}

    changes_made = False

    for addon_dir, (repo, branch) in REPOS_TO_TRACK.items():
        print(f"Checking {addon_dir} against {repo} ({branch})...")
        latest_sha = get_latest_sha(repo, branch)
        
        if not latest_sha:
            continue
            
        current_sha = known_shas.get(addon_dir)
        
        if latest_sha != current_sha:
            print(f"New commit detected for {addon_dir}: {latest_sha[:7]}")
            config_path = os.path.join(addon_dir, 'config.yaml')
            if os.path.exists(config_path):
                success, new_version = bump_config_version(config_path)
                if success:
                    print(f"Successfully bumped {addon_dir} to version {new_version}")
                    known_shas[addon_dir] = latest_sha
                    changes_made = True
                else:
                    print(f"Failed to bump version for {addon_dir}")
        else:
            print(f"{addon_dir} is up to date.")

    if changes_made:
        os.makedirs(os.path.dirname(SHA_FILE), exist_ok=True)
        with open(SHA_FILE, 'w') as f:
            json.dump(known_shas, f, indent=4)
        
        # Set an output for the GitHub Action to know a commit is needed
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write("update_triggered=true\n")

if __name__ == "__main__":
    main()
