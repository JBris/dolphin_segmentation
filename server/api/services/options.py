import json
import os

from decouple import config

SYSTEM_DIR =  config('SYSTEM_DIR', default = '/home/app/system')
OPTIONS_FILE = f"{SYSTEM_DIR}/options.json"

default_options = {
    "modules": {
        "dolphin": {
            "name": "Dolphin",
            "enabled": True,
            "editable": False
        },
    },
    "features": {
        "identification": {
            "name": "Identification",
            "enabled": True,
            "editable": False
        },
        "segmentation": {
            "name": "Segmentation",
            "enabled": True,
            "editable": False
        },
        "classification": {
            "name": "Classification",
            "enabled": True,
            "editable": True
        }
    },
    "solvers": {
        "triplet_loss": {
            "name": "Triplet Loss",
            "enabled": True,
            "editable": False
        },
        "umap": {
            "name": "UMAP",
            "enabled": False,
            "editable": True
        },
        "yolo": {
            "name": "Yolo",
            "enabled": True,
            "editable": False
        },
    },
    "autodownload_default": config('AUTODOWNLOAD_FILE', default = True, cast = bool),
    "cache_duration_default": config('CACHE_DURATION', default = 86400, cast = int),
    "hide_tasks": False,
    "hide_notebooks": False,
    "hide_containers": False
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
