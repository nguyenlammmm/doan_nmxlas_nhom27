import json
import os

def load_names(path="data/known_faces.json"):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_names(data, path="data/known_faces.json"):
    with open(path, "w") as f:
        json.dump(data, f)
