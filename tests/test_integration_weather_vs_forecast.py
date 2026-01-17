
def test_weather_and_forecast_return_consistent_temperature(weather, forecast, api_key):
    
    city = "Warsaw"
    tolerance = 1.5 
    
    weather_response = weather.get_weather(city, api_key, "metric")
    forecast_response = forecast.get_forecast(city, api_key, "metric")

    assert weather_response.status_code == 200
    assert forecast_response.status_code == 200

    weather_data = weather_response.json()
    forecast_data = forecast_response.json()
    
    current_temp = weather_data["main"]["temp"]
    forecast_temp = forecast_data["list"][0]["main"]["temp"]
    
    difference = abs(current_temp - forecast_temp)
    
    assert difference < tolerance, ()