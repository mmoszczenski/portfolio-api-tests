
def test_single_city(weather, api_key):
        
    response = weather.get_weather("Warsaw", api_key)
    data = response.json()
    
    assert response.status_code == 200
    assert data["name"] == "Warsaw"
    
    
