from constants import DEFAULT_CITY, WEATHER_FORECAST_TEMPERATURE_TOLERANCE
from helpers.get_temperature import get_temperature_for_city
from helpers.assertions import assert_within_tolerance, assert_status_code_and_valid_json
import pytest

@pytest.mark.integration
def test_weather_and_forecast_return_consistent_temperature(weather, forecast, api_key):

    city = DEFAULT_CITY
    tolerance = WEATHER_FORECAST_TEMPERATURE_TOLERANCE

    weather_response = weather.get_weather(city, api_key, units="metric")
    forecast_response = forecast.get_forecast(city, api_key, units="metric")

    assert_status_code_and_valid_json(weather_response)
    assert_status_code_and_valid_json(forecast_response)

    current_temp = get_temperature_for_city(weather, api_key, city)
    forecast_temp = get_temperature_for_city(forecast, api_key, city)

    assert_within_tolerance(current_temp, forecast_temp, tolerance)
