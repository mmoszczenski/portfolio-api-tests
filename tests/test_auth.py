from conftest import weather


def test_auth_valid_key(weather, api_key):

    response = weather.get_weather("London", api_key)

    data = response.json()
        
    assert response.status_code == 200
    assert "weather" in data
    assert "main" in data
    assert data["name"] == "London"
    
def test_auth_invalid_key(weather):
     
    response = weather.get_weather("London", api_key = "11111")
    data = response.json()

    assert response.status_code == 401
    assert "Invalid API key" in data["message"]
    
def test_auth_no_key_provided(weather):
    
    response = weather.get_weather("London")
    data = response.json()
    
    assert response.status_code == 401
    assert "Invalid API key" in data["message"]

def test_auth_key_with_white_spaces(weather, api_key):
    
    invalid_key = " " + api_key

    response = weather.get_weather("London", invalid_key)
    data = response.json()
    
    assert response.status_code == 401
    assert "Invalid API key" in data["message"]