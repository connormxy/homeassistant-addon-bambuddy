---
description: Automatically increments the `-X` dev tag in all add-on `config.yaml` versions (e.g., `1.2.5.0-4` to `1.2.5.0-5`) to force a fresh Home Assistant OS build during local testing.
---

# Bump Dev Version

**Description**: Automatically increments the `-X` dev tag in all add-on `config.yaml` versions (e.g., `1.2.5.0-4` to `1.2.5.0-5`) to force a fresh Home Assistant OS build during local testing.

## Prerequisites

- You must be on the `dev` branch.
- Your Home Assistant repository must be using standard `-X` trailing tags for versions.

## Workflow Execution Steps

When you need to force Home Assistant OS to pull new changes without creating a new official version bump, run the following pipeline exactly:

```bash
python scratch/bump_dev.py && git commit -am "chore: bump dev version flag for HAOS rebuild" && git push
```

### Breakdown of Pipeline

- `python scratch/bump_dev.py`: Parses all 4 add-on `config.yaml` files and increments the trailing `-X` tag by 1. If no tag exists, it appends `-1`.
- `git commit -am "..."`: Commits the new config changes.
- `git push`: Pushes the changes so your local Home Assistant OS can see the new dev version and prompt you to "Update".
