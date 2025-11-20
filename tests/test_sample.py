import requests
from dotenv import load_dotenv
import os

load_dotenv()

def test_auth_valid_key():
    api_key = os.getenv('API_KEY')
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": "London",
        "appid": api_key
    }

    response = requests.get(base_url, params=params)

    # --- Assercje ---
    assert response.status_code == 200
    data = response.json()

    # Sprawdzamy czy odpowiedź wygląda jak dane pogodowe
    assert "weather" in data
    assert "main" in data
    assert data["name"] == "London"