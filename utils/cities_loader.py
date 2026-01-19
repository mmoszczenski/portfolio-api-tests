import json

def cities_loader(name):
    with open(f"data/{name}") as f:
        return json.load(f)