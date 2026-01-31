from jsonschema import validate
from helpers.assertions import assert_city_name
from helpers.assertions import assert_errorr_message_present
from helpers.assertions import assert_within_tolerance
from helpers.assertions import assert_status_code_and_valid_json
from helpers.assertions import assert_coordinates_match
from helpers.assertions import assert_error_message
from constants import TEMPERATURE_CONVERSION_TOLERANCE, COORDINATES_TOLERANCE
from constants import DEFAULT_CITY, DEFAULT_COORDINATES, INVALID_COORDINATES, DEFAULT_CITY_ID, UNKNOWN_CITY
from helpers.get_temperature import get_temperature_in_celsius, get_temperature_in_fahrenheit, get_temperature_for_city
from utils.temp_converter import kelvin_to_celsius, kelvin_to_fahrenheit

def test_weather_returns_valid_data_for_single_city(weather, api_key):

    city = DEFAULT_CITY

    response = weather.get_weather(city, api_key)
    data = assert_status_code_and_valid_json(response)

    assert_city_name(data, city)


def test_weather_returns_valid_data_for_all_tested_cities(weather, api_key, cities):

    for city in cities:
        response = weather.get_weather(city, api_key)
        data = assert_status_code_and_valid_json(response)

        assert_city_name(data, city)


def test_weather_returns_temperature_in_celsius_when_units_metric(weather, api_key):

    city = DEFAULT_CITY

    response_kelvin = weather.get_weather(city, api_key)
    response_celsius = weather.get_weather(city, api_key, units="metric")

    assert_status_code_and_valid_json(response_kelvin)
    assert_status_code_and_valid_json(response_celsius)

    temp_kelvin = get_temperature_for_city(weather, api_key, city)
    temp_celsius = get_temperature_in_celsius(weather, api_key, city)
    
    temp_converted = kelvin_to_celsius(temp_kelvin)

    assert_within_tolerance(temp_celsius, temp_converted, TEMPERATURE_CONVERSION_TOLERANCE)


def test_weather_returns_temperature_in_f_when_units_imperial(weather, api_key):

    city = DEFAULT_CITY

    response_kelvin = weather.get_weather(city, api_key)
    response_fahrenheit = weather.get_weather(city, api_key, units="imperial")

    assert_status_code_and_valid_json(response_kelvin)
    assert_status_code_and_valid_json(response_fahrenheit)

    temp_kelvin = get_temperature_for_city(weather, api_key, city)
    temp_fahrenheit = get_temperature_in_fahrenheit(weather, api_key, city)
    
    temp_converted = kelvin_to_fahrenheit(temp_kelvin)

    assert_within_tolerance(temp_fahrenheit, temp_converted, TEMPERATURE_CONVERSION_TOLERANCE)


def test_weather_returns_polish_when_language_PL(weather, api_key):

    city = DEFAULT_CITY

    response_eng = weather.get_weather(city, api_key)
    response_pl = weather.get_weather(city, api_key, lang="pl")

    data_eng = assert_status_code_and_valid_json(response_eng)
    data_pl = assert_status_code_and_valid_json(response_pl)

    description_eng = data_eng["weather"][0]["description"]
    description_pl = data_pl["weather"][0]["description"]

    assert description_eng != description_pl, (
        "Weather description should differ between languages "
        f"(en='{description_eng}', pl='{description_pl}')"
    )


def test_weather_can_be_requested_by_lat_and_lon(weather, api_key):

    lat = DEFAULT_COORDINATES["lat"]
    lon = DEFAULT_COORDINATES["lon"] 
    tolerance = COORDINATES_TOLERANCE

    response = weather.get_weather_by_coordinates(lat, lon, api_key)

    data = assert_status_code_and_valid_json(response)

    temp = get_temperature_for_city(weather, api_key=api_key, lat=lat, lon=lon)

    assert_coordinates_match(lat, lon, data["coord"]["lat"], data["coord"]["lon"], tolerance)
    assert isinstance(temp, (int, float))


def test_weather_response_matches_schema(weather, api_key, weather_schema):

    city = DEFAULT_CITY

    response = weather.get_weather(city, api_key)
    data = assert_status_code_and_valid_json(response)
    schema = weather_schema

    validate(instance=data, schema=schema)


def test_weather_returns_404_for_non_existing_city(weather, api_key):

    city = UNKNOWN_CITY
    error_substring = "city"

    response = weather.get_weather(city, api_key)
    data = assert_status_code_and_valid_json(response, expected_status=404)

    assert_errorr_message_present(data)
    assert_error_message(data, error_substring)


def test_weather_returns_400_when_city_param_missing(weather, api_key):

    error_substring = "geocode"
    
    response = weather.get_weather(api_key=api_key)
    data = assert_status_code_and_valid_json(response, expected_status=400)

    assert_errorr_message_present(data)
    assert_error_message(data, error_substring)


def test_weather_returns_400_when_city_param_empty_string(weather, api_key):

    city = ""
    error_substring = "geocode"

    response = weather.get_weather(city, api_key)
    data = assert_status_code_and_valid_json(response, expected_status=400)

    assert_errorr_message_present(data)
    assert_error_message(data, error_substring)


def test_weather_returns_404_when_city_param_with_special_characters(weather, api_key):

    city = "Wa%^()*raw"
    error_substring = "city"

    response = weather.get_weather(city, api_key)
    data = assert_status_code_and_valid_json(response, expected_status=404)

    assert_errorr_message_present(data)
    assert_error_message(data, error_substring)


def test_weather_returns_success_for_city_long_value(weather, api_key):

    city = "Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch"

    response = weather.get_weather(city, api_key)
    data = assert_status_code_and_valid_json(response)

    assert data["name"] == "Llanfairpwllgwyngyll"


def test_weather_returns_400_when_coordinates_invalid(weather, api_key):

    lat = INVALID_COORDINATES["lat"]
    lon = INVALID_COORDINATES["lon"]
    error_substring = "wrong"

    response = weather.get_weather_by_coordinates(lat, lon, api_key)
    data = assert_status_code_and_valid_json(response, expected_status=400)

    assert_errorr_message_present(data)
    assert_error_message(data, error_substring)


def test_weather_returns_400_when_coordinates_null(weather, api_key):

    lat = None
    lon = None
    error_substring = "geocode"

    response = weather.get_weather_by_coordinates(lat, lon, api_key)
    data = assert_status_code_and_valid_json(response, expected_status=400)

    assert_errorr_message_present(data)
    assert_error_message(data, error_substring)


def test_weather_can_be_requested_by_city_id(weather, api_key):

    city_id = DEFAULT_CITY_ID

    response = weather.get_weather(city_id=city_id, api_key=api_key)
    data = assert_status_code_and_valid_json(response)

    assert_city_name(data, "warsaw")
