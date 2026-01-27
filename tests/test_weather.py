
from jsonschema import validate
from helpers.assertions import assert_city_name
from constants import TEMPERATURE_CONVERTION_TOLERANCE, COORDINATES_TOLERANCE


def test_weather_returns_valid_data_for_single_city(weather, api_key, assert_response):

    response = weather.get_weather("Warsaw", api_key)
    data = assert_response(response)

    assert_city_name(data, "warsaw")


def test_weather_returns_valid_data_for_all_tested_cities(weather, api_key, cities, assert_response):

    for city in cities:
        response = weather.get_weather(city, api_key)
        data = assert_response(response)

        assert_city_name(data, city)


def test_weather_returns_temperature_in_celsius_when_units_metric(weather, api_key, assert_response):

    response_default = weather.get_weather("Warsaw", api_key)
    response_metric = weather.get_weather("Warsaw", api_key, units="metric")

    assert_response(response_default)
    assert_response(response_metric)

    temp_default = response_default.json()["main"]["temp"]
    temp_metric = response_metric.json()["main"]["temp"]

    difference = abs((temp_default - 273.15) - temp_metric)

    assert difference < TEMPERATURE_CONVERTION_TOLERANCE, (
        f"Temperature difference too large: "
        f"{difference} vs {TEMPERATURE_CONVERTION_TOLERANCE} allowed"
        f"Default = {temp_default}K, Metric={temp_metric}C"
    )


def test_weather_returns_temperature_in_f_when_units_imperial(weather, api_key, assert_response):

    response_default = weather.get_weather("Warsaw", api_key)
    response_imperial = weather.get_weather(
        "Warsaw", api_key, units="imperial")

    assert_response(response_default)
    assert_response(response_imperial)

    temp_default = response_default.json()["main"]["temp"]
    temp_imperial = response_imperial.json()["main"]["temp"]

    expected_fahrenheit = (temp_default - 273.15) * 1.8 + 32

    difference = abs(expected_fahrenheit - temp_imperial)

    assert difference < TEMPERATURE_CONVERTION_TOLERANCE


def test_weather_returns_polish_when_language_PL(weather, api_key, assert_response):

    response_eng = weather.get_weather("Warsaw", api_key)
    response_pl = weather.get_weather("Warsaw", api_key, lang="pl")

    assert_response(response_eng)
    assert_response(response_pl)

    description_eng = response_eng.json()["weather"][0]["description"]
    description_pl = response_pl.json()["weather"][0]["description"]

    assert description_eng != description_pl, (
        "Weather description should differ between languages "
        f"(en='{description_eng}', pl='{description_pl}')"
    )


def test_weather_can_be_requested_by_lat_and_lon(weather, api_key, assert_response):

    lat = 52.2297
    lon = 21.0122

    response = weather.get_weather_by_coordinates(lat, lon, api_key)

    data = assert_response(response)

    temp = data["main"]["temp"]

    assert "weather" in data
    assert "main" in data
    assert "coord" in data

    assert abs(data["coord"]["lat"] - lat) < COORDINATES_TOLERANCE
    assert abs(data["coord"]["lon"] - lon) < COORDINATES_TOLERANCE

    assert isinstance(temp, (int, float))


def test_weather_response_matches_schema(weather, api_key, weather_schema, assert_response):

    response = weather.get_weather("Warsaw", api_key)
    data = assert_response(response)
    schema = weather_schema

    validate(instance=data, schema=schema)


def test_weather_returns_404_for_non_existing_city(weather, api_key, assert_response):

    response = weather.get_weather("NOT_EXISTING_CITY", api_key)
    data = assert_response(response, expected_status=404)

    assert "city not found" in data["message"]


def test_weather_returns_400_when_city_param_missing(weather, api_key, assert_response):

    response = weather.get_weather(api_key=api_key)
    data = assert_response(response, expected_status=400)
    message = data["message"]

    assert "Nothing to geocode" in message


def test_weather_returns_400_when_city_param_empty_string(weather, api_key, assert_response):

    response = weather.get_weather("", api_key)
    data = assert_response(response, expected_status=400)
    message = data["message"]

    assert "Nothing to geocode" in message


def test_weather_returns_400_when_city_param_with_special_characters(weather, api_key, assert_response):

    response = weather.get_weather("Wa%^()*raw", api_key)
    data = assert_response(response, expected_status=404)
    message = data["message"]

    assert "city not found" in message


def test_weather_returns_success_for_city_long_value(weather, api_key, assert_response):

    response = weather.get_weather(
        "Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch", api_key)
    data = assert_response(response)

    assert data["name"] == "Llanfairpwllgwyngyll"


def test_weather_returns_400_when_coordinates_invalid(weather, api_key, assert_response):

    lat = 123123123
    lon = -98123

    response = weather.get_weather_by_coordinates(lat, lon, api_key)
    data = assert_response(response, expected_status=400)

    assert data["message"] == "wrong latitude"


def test_weather_returns_400_when_coordinates_null(weather, api_key, assert_response):

    lat = None
    lon = None

    response = weather.get_weather_by_coordinates(lat, lon, api_key)
    data = assert_response(response, expected_status=400)

    assert data["message"] == "Nothing to geocode"


def test_weather_can_be_requested_by_city_id(weather, api_key, assert_response):

    city_ID = 756135

    response = weather.get_weather(city_ID, api_key)
    data = assert_response(response)

    assert data["name"] == "Warsaw"
