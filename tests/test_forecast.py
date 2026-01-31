from jsonschema import validate
from constants import TEMPERATURE_CONVERSION_TOLERANCE, DEFAULT_CITY, UNKNOWN_CITY
from helpers.assertions import assert_error_message_present, assert_status_code_and_valid_json, assert_within_tolerance, assert_error_message
from helpers.get_temperature import get_temperature_for_city, get_temperature_in_celsius
from utils.temp_converter import kelvin_to_celsius
import pytest

@pytest.mark.forecast
@pytest.mark.negative
def test_forecast_returns_400_when_city_param_missing(forecast, api_key):

    error_substring = "nothing"
    
    response = forecast.get_forecast(api_key=api_key)
    data = assert_status_code_and_valid_json(response, expected_status=400)

    assert_error_message_present(data)
    assert_error_message(data, error_substring)

@pytest.mark.forecast
@pytest.mark.positive
def test_forecast_returns_5_day_forecast_for_city(forecast, api_key):

    city = DEFAULT_CITY

    response = forecast.get_forecast(city, api_key)
    data = assert_status_code_and_valid_json(response)

    assert "list" in data
    assert isinstance(data["list"], list)
    assert len(data["list"]) >= 30

    timestamps = [item["dt"] for item in data["list"]]
    assert timestamps == sorted(timestamps)

    for entry in data["list"]:
        assert "main" in entry
        assert "weather" in entry
        assert "dt" in entry

        temp = entry["main"]["temp"]
        assert isinstance(temp, (int, float))

        assert isinstance(entry["weather"], list)
        assert len(entry["weather"]) > 0

    assert data["city"]["name"] == city

@pytest.mark.forecast
@pytest.mark.positive
def test_forecast_response_matches_schema(forecast, api_key, forecast_schema):

    city = DEFAULT_CITY

    response = forecast.get_forecast(city, api_key)

    data = assert_status_code_and_valid_json(response)
    schema = forecast_schema

    validate(instance=data, schema=schema)

@pytest.mark.forecast
@pytest.mark.negative
def test_forecast_returns_404_when_city_unknown(forecast, api_key):

    city = UNKNOWN_CITY
    error_substring = "city"

    response = forecast.get_forecast(city, api_key)

    data = assert_status_code_and_valid_json(response, expected_status=404)

    assert_error_message_present(data)
    assert_error_message(data, error_substring)

@pytest.mark.forecast
@pytest.mark.positive
def test_forecast_returns_temperature_in_celsius_when_units_metric(forecast, api_key):

    city = DEFAULT_CITY

    response_kelvin = forecast.get_forecast(city, api_key)
    response_celsius = forecast.get_forecast(city, api_key, units="metric")

    assert_status_code_and_valid_json(response_kelvin)
    assert_status_code_and_valid_json(response_celsius)

    temp_kelvin = get_temperature_for_city(forecast, api_key, city)
    temp_celsius = get_temperature_in_celsius(forecast, api_key, city)
    
    temp_converted = kelvin_to_celsius(temp_kelvin)

    assert_within_tolerance(temp_celsius, temp_converted, TEMPERATURE_CONVERSION_TOLERANCE)
    