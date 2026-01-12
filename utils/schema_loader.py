import json

def load_schema(name):
    with open(f"schemas/{name}") as f:
        return json.load(f)