
from jsonschema import validate
from helpers.assertions import assert_city_name
from helpers.assertions import assert_error_message
from constants import TEMPERATURE_CONVERTION_TOLERANCE, COORDINATES_TOLERANCE
from constants import DEFAULT_CITY, DEFAULT_COORDINATES, INVALID_COORDINATES


def test_weather_returns_valid_data_for_single_city(weather, api_key, assert_status_code_and_valid_json):

    city = DEFAULT_CITY

    response = weather.get_weather(city, api_key)
    data = assert_status_code_and_valid_json(response)

    assert_city_name(data, city)


def test_weather_returns_valid_data_for_all_tested_cities(weather, api_key, cities, assert_status_code_and_valid_json):

    for city in cities:
        response = weather.get_weather(city, api_key)
        data = assert_status_code_and_valid_json(response)

        assert_city_name(data, city)


def test_weather_returns_temperature_in_celsius_when_units_metric(weather, api_key, assert_status_code_and_valid_json):

    city = DEFAULT_CITY

    response_default = weather.get_weather(city, api_key)
    response_metric = weather.get_weather(city, api_key, units="metric")

    assert_status_code_and_valid_json(response_default)
    assert_status_code_and_valid_json(response_metric)

    temp_default = response_default.json()["main"]["temp"]
    temp_metric = response_metric.json()["main"]["temp"]

    difference = abs((temp_default - 273.15) - temp_metric)

    assert difference < TEMPERATURE_CONVERTION_TOLERANCE, (
        f"Temperature difference too large: "
        f"{difference} vs {TEMPERATURE_CONVERTION_TOLERANCE} allowed"
        f"Default = {temp_default}K, Metric={temp_metric}C"
    )


def test_weather_returns_temperature_in_f_when_units_imperial(weather, api_key, assert_status_code_and_valid_json):

    city = DEFAULT_CITY

    response_default = weather.get_weather(city, api_key)
    response_imperial = weather.get_weather(city, api_key, units="imperial")

    assert_status_code_and_valid_json(response_default)
    assert_status_code_and_valid_json(response_imperial)

    temp_default = response_default.json()["main"]["temp"]
    temp_imperial = response_imperial.json()["main"]["temp"]

    expected_fahrenheit = (temp_default - 273.15) * 1.8 + 32

    difference = abs(expected_fahrenheit - temp_imperial)

    assert difference < TEMPERATURE_CONVERTION_TOLERANCE


def test_weather_returns_polish_when_language_PL(weather, api_key, assert_status_code_and_valid_json):

    city = DEFAULT_CITY

    response_eng = weather.get_weather(city, api_key)
    response_pl = weather.get_weather(city, api_key, lang="pl")

    assert_status_code_and_valid_json(response_eng)
    assert_status_code_and_valid_json(response_pl)

    description_eng = response_eng.json()["weather"][0]["description"]
    description_pl = response_pl.json()["weather"][0]["description"]

    assert description_eng != description_pl, (
        "Weather description should differ between languages "
        f"(en='{description_eng}', pl='{description_pl}')"
    )


def test_weather_can_be_requested_by_lat_and_lon(weather, api_key, assert_status_code_and_valid_json):

    lat = DEFAULT_COORDINATES["lat"]
    lon = DEFAULT_COORDINATES["lon"]

    response = weather.get_weather_by_coordinates(lat, lon, api_key)

    data = assert_status_code_and_valid_json(response)

    temp = data["main"]["temp"]

    assert "weather" in data
    assert "main" in data
    assert "coord" in data

    assert abs(data["coord"]["lat"] - lat) < COORDINATES_TOLERANCE
    assert abs(data["coord"]["lon"] - lon) < COORDINATES_TOLERANCE

    assert isinstance(temp, (int, float))


def test_weather_response_matches_schema(weather, api_key, weather_schema, assert_status_code_and_valid_json):

    city = DEFAULT_CITY

    response = weather.get_weather(city, api_key)
    data = assert_status_code_and_valid_json(response)
    schema = weather_schema

    validate(instance=data, schema=schema)


def test_weather_returns_404_for_non_existing_city(weather, api_key, assert_status_code_and_valid_json):

    city = "NOT_EXISTING_CITY"

    response = weather.get_weather(city, api_key)
    data = assert_status_code_and_valid_json(response, expected_status=404)

    assert_error_message(data)


def test_weather_returns_400_when_city_param_missing(weather, api_key, assert_status_code_and_valid_json):

    response = weather.get_weather(api_key=api_key)
    data = assert_status_code_and_valid_json(response, expected_status=400)

    assert_error_message(data)


def test_weather_returns_400_when_city_param_empty_string(weather, api_key, assert_status_code_and_valid_json):

    city = ""

    response = weather.get_weather(city, api_key)
    data = assert_status_code_and_valid_json(response, expected_status=400)

    assert_error_message(data)


def test_weather_returns_400_when_city_param_with_special_characters(weather, api_key, assert_status_code_and_valid_json):

    city = "Wa%^()*raw"

    response = weather.get_weather(city, api_key)
    data = assert_status_code_and_valid_json(response, expected_status=404)

    assert_error_message(data)


def test_weather_returns_success_for_city_long_value(weather, api_key, assert_status_code_and_valid_json):

    city = "Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch"

    response = weather.get_weather(city, api_key)
    data = assert_status_code_and_valid_json(response)

    assert data["name"] == "Llanfairpwllgwyngyll"


def test_weather_returns_400_when_coordinates_invalid(weather, api_key, assert_status_code_and_valid_json):

    lat = INVALID_COORDINATES["lat"]
    lon = INVALID_COORDINATES["lon"]

    response = weather.get_weather_by_coordinates(lat, lon, api_key)
    data = assert_status_code_and_valid_json(response, expected_status=400)

    assert_error_message(data)


def test_weather_returns_400_when_coordinates_null(weather, api_key, assert_status_code_and_valid_json):

    lat = None
    lon = None

    response = weather.get_weather_by_coordinates(lat, lon, api_key)
    data = assert_status_code_and_valid_json(response, expected_status=400)

    assert_error_message(data)


def test_weather_can_be_requested_by_city_id(weather, api_key, assert_status_code_and_valid_json):

    city_ID = 756135

    response = weather.get_weather(city_ID, api_key)
    data = assert_status_code_and_valid_json(response)

    assert_error_message(data)
