from utils.json_loader import load_json

def load_cities() -> list[str]:
    return load_json("data/cities.json")