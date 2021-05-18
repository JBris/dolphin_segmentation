import json
import os

from decouple import config

SYSTEM_DIR =  config('SYSTEM_DIR', default = '/home/app/system')
OPTIONS_FILE = f"{SYSTEM_DIR}/options.json"

default_options = {
    "modules": {
        "dolphin": {
            "name": "Dolphin",
            "enabled": 1,
            "editable": 0
        },
    },
    "features": {
        "segmentation": {
            "name": "Segmentation",
            "enabled": 1,
            "editable": 0
        },
        "classification": {
            "name": "Classification",
            "enabled": 1,
            "editable": 0
        },
        "identification": {
            "name": "Identification",
            "enabled": 1,
            "editable": 0
        }
    },
    "solvers": {
        "triplet_loss": {
            "name": "Triplet Loss",
            "enabled": 1,
            "editable": 0
        },
        "umap": {
            "name": "UMAP",
            "enabled": 0,
            "editable": 1
        }
    },
    "autodownload_default": config('AUTODOWNLOAD_FILE', default = 1, cast = int),
    "cache_duration_default": config('CACHE_DURATION', default = 86400, cast = int),
    "hide_tasks": 0,
    "hide_notebooks": 0
}

class Options:
    def get(self):
        if not os.path.isfile(OPTIONS_FILE): return self.reset()

        with open(OPTIONS_FILE, 'r') as f: 
            try: options = json.load(f)
            except ValueError: return self.reset()

        return options

    def reset(self):
        with open(OPTIONS_FILE, 'w') as f: json.dump(default_options, f)
        return default_options

    def update_from_request(self, req):
        options = req.get_json()
        if options is None: return None
        return self.update(options)

    def update(self, data):
        updated_options = {}

        for key in default_options:
            if key not in data: updated_options[key] = default_options[key]
            else: updated_options[key] = data[key]

        with open(OPTIONS_FILE, 'w') as f: json.dump(updated_options, f)
        return updated_options
