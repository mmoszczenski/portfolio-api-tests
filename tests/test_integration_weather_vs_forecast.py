
def test_weather_and_forecast_return_consistent_temperature(weather, forecast, api_key, assert_response):

    city = "Warsaw"
    tolerance = 1.5

    weather_response = weather.get_weather(city, api_key, "metric")
    forecast_response = forecast.get_forecast(city, api_key, "metric")

    weather_data = assert_response(weather_response)
    forecast_data = assert_response(forecast_response)

    current_temp = weather_data["main"]["temp"]
    forecast_temp = forecast_data["list"][0]["main"]["temp"]

    difference = abs(current_temp - forecast_temp)

    assert difference < tolerance, ()
