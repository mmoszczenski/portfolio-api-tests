from utils.json_loader import load_json

def load_schema(name):
    return load_json(f"schemas/{name}")