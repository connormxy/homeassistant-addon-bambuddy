import os
import json
import sys

options_file = '/data/options.json'

if os.path.exists(options_file):
    try:
        with open(options_file, 'r') as f:
            options = json.load(f)
            if 'draw_bounding_boxes' in options:
                os.environ['DRAW_BOUNDING_BOXES'] = str(options['draw_bounding_boxes']).lower()
    except Exception as e:
        print(f"Error reading options.json: {e}", file=sys.stderr)

# Exec gunicorn
os.execvp("gunicorn", ["gunicorn", "--bind", "0.0.0.0:3333", "--chdir", "/app", "--limit-request-line", "0", "--workers", "1", "wsgi"])
