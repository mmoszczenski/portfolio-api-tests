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
      
      
# test na sprawdzanie wartości pogodowej zwróconej w stopniach C

def test_weather_returns_value_in_C(weather, api_key):
    pass

# test na sprawdzenie wartości pogodowej zwróconej w F

# test na sprawdzanie języka zwróconej odpowiedzi (np. polski)