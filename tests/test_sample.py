import requests

def test_auth_valid_key():
    api_key = "915c4760f9b9288c55839f36908b1895"
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