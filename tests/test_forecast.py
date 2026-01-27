from jsonschema import validate
from constants import TEMPERATURE_CONVERTION_TOLERANCE, DEFAULT_CITY


def test_forecast_returns_5_day_forecast_for_city(forecast, api_key, assert_response):

    city = DEFAULT_CITY

    response = forecast.get_forecast(city, api_key)
    data = assert_response(response)

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


def test_forecast_response_matches_schema(forecast, api_key, forecast_schema, assert_response):

    city = DEFAULT_CITY

    response = forecast.get_forecast(city, api_key)

    data = assert_response(response)
    schema = forecast_schema

    validate(instance=data, schema=schema)


def test_forecast_returns_404_when_city_unknown(forecast, api_key, assert_response):

    city = "NON_EXISTING_CITY"

    response = forecast.get_forecast(city, api_key)

    data = assert_response(response, expected_status=404)
    assert "city not found" in data["message"]


def test_forecast_returns_temperature_in_celsius_when_units_metric(forecast, api_key, assert_response):

    city = DEFAULT_CITY

    response_default = forecast.get_forecast(city, api_key)
    response_metric = forecast.get_forecast(city, api_key, "metric")

    data_default = assert_response(response_default)
    data_metric = assert_response(response_metric)

    default_item = data_default["list"][0]
    metric_item = data_metric["list"][0]

    temp_k = default_item["main"]["temp"]
    temp_c = metric_item["main"]["temp"]

    difference = abs((temp_k - 273.15) - temp_c)

    assert difference < TEMPERATURE_CONVERTION_TOLERANCE
