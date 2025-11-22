import pytest

def test_weather_returns_valid_data_for_single_city(weather, api_key):
        
    response = weather.get_weather("Warsaw", api_key)
    data = response.json()
    
    assert response.status_code == 200
    assert data["name"] == "Warsaw"
    
def test_weather_returns_valid_data_for_all_tested_cities(weather, api_key, cities):
    
  for city in cities:
      response = weather.get_weather(city, api_key)
      data = response.json()
      assert response.status_code == 200
      assert data["name"].lower() == city.lower()