from constants import DEFAULT_CITY
from helpers.get_temperature import get_temperature_for_city
from helpers.assertions import assert_within_tolerance
from constants import TEMPERATURE_CONVERSION_TOLERANCE


def test_weather_and_forecast_return_consistent_temperature(weather, forecast, api_key, assert_status_code_and_valid_json):

    city = DEFAULT_CITY
    tolerance = 1.5

    weather_response = weather.get_weather(city, api_key, "metric")
    forecast_response = forecast.get_forecast(city, api_key, "metric")

    assert_status_code_and_valid_json(weather_response)
    assert_status_code_and_valid_json(forecast_response)

    current_temp = get_temperature_for_city(weather, api_key, city)
    forecast_temp = get_temperature_for_city(forecast, api_key, city)

    assert current_temp - forecast_temp <= tolerance
