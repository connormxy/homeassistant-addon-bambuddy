---
description: Automates the process of graduating experimental `dev` changes into stable production releases on the `main` branch, ensuring all `(DEV)` branding, slugs, URLs, and experimental tags are stripped out before publishing
---

# Publish to Main (Release Pipeline)

**Description**: Automates the process of graduating experimental `dev` changes into stable production releases on the `main` branch, ensuring all `(DEV)` branding, slugs, URLs, and experimental tags are stripped out before publishing.

## Prerequisites

- All active work must be fully committed and pushed to the `dev` branch.
- The `scratch/publish_to_main.py` cleanup script must exist and be functional.

## Workflow Execution Steps

When requested to push changes to main or release a new stable version, run the following pipeline exactly:

1. **Verify Dev State**
   Ensure you are currently on the `dev` branch and the working directory is clean. If there are uncommitted changes, commit and push them to `dev` first.

2. **Execute Pipeline**
   Run the following chained command to smoothly transition the code, execute the cleaner script, and publish:

   ```bash
   git checkout main && git merge dev --allow-unrelated-histories -X theirs && python scratch/publish_to_main.py && git commit -am 'chore: prepare release' && git push origin main && git checkout dev
   ```

### Breakdown of Pipeline

- `git checkout main`: Switches to the production branch.
- `git merge dev --allow-unrelated-histories -X theirs`: Forcefully merges the dev changes, resolving any history mismatches by heavily favoring the `dev` branch's state.
- `python scratch/publish_to_main.py`: Executes the custom python script that edits `config.yaml` and `README.md` to remove `slug: bambuddy-dev`, `(DEV)` names, experimental stages, and GitHub dev branch URL suffixes.
- `git commit -am 'chore: prepare release'`: Commits the newly cleaned production files.
- `git push origin main`: Pushes the stable release up to the GitHub repository, where Home Assistant users will receive the update.
- `git checkout dev`: Safely drops you back into the development environment to continue working.

> [!WARNING]
> Never manually edit production configurations directly on the `main` branch. All features, version bumps, and changelog updates must happen on `dev` first, and then flow through this automated pipeline.
