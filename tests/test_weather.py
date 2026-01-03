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

def test_weather_returns_temperature_in_celsius_when_units_metric(weather, api_key):
    
    response_default = weather.get_weather("Warsaw", api_key)
    response_metric = weather.get_weather("Warsaw", api_key, units="metric")
    
    assert response_default.status_code == 200
    assert response_metric.status_code == 200
    
    temp_default = response_default.json()["main"]["temp"]
    temp_metric = response_metric.json()["main"]["temp"]
    
    difference = abs((temp_default - 273.15) - temp_metric)

    assert  difference < 0.2, (
        f"Temperature difference too large: "
        f"{difference} vs 0.2 allowed"
        f"Default = {temp_default}K, Metric={temp_metric}C"
        )

def test_weather_returns_temperature_in_f_when_units_imperial(weather, api_key):
    
    response_default = weather.get_weather("Warsaw", api_key)
    response_imperial = weather.get_weather("Warsaw", api_key, units="imperial")
    
    assert response_default.status_code == 200
    assert response_imperial.status_code == 200
    
    temp_default = response_default.json()["main"]["temp"]
    temp_imperial = response_imperial.json()["main"]["temp"]
    
    expected_fahrenheit = (temp_default - 273.15) * 1.8 + 32
    
    difference = abs(expected_fahrenheit - temp_imperial)
    
    assert difference < 0.2
    

# test na sprawdzanie języka zwróconej odpowiedzi (np. polski)