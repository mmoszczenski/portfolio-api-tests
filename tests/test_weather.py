
from jsonschema import validate


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

    assert difference < 0.3, (
        f"Temperature difference too large: "
        f"{difference} vs 0.2 allowed"
        f"Default = {temp_default}K, Metric={temp_metric}C"
    )


def test_weather_returns_temperature_in_f_when_units_imperial(weather, api_key):

    response_default = weather.get_weather("Warsaw", api_key)
    response_imperial = weather.get_weather(
        "Warsaw", api_key, units="imperial")

    assert response_default.status_code == 200
    assert response_imperial.status_code == 200

    temp_default = response_default.json()["main"]["temp"]
    temp_imperial = response_imperial.json()["main"]["temp"]

    expected_fahrenheit = (temp_default - 273.15) * 1.8 + 32

    difference = abs(expected_fahrenheit - temp_imperial)

    assert difference < 0.2


def test_weather_returns_polish_when_language_PL(weather, api_key):

    response_eng = weather.get_weather("Warsaw", api_key)
    response_pl = weather.get_weather("Warsaw", api_key, lang="pl")

    assert response_eng.status_code == 200
    assert response_pl.status_code == 200

    description_eng = response_eng.json()["weather"][0]["description"]
    description_pl = response_pl.json()["weather"][0]["description"]

    assert description_eng != description_pl,         (
        "Weather description should differ between languages "
        f"(en='{description_eng}', pl='{description_pl}')"
    )


def test_weather_can_be_requested_by_lat_and_lon(weather, api_key):

    lat = 52.2297
    lon = 21.0122

    response = weather.get_weather_by_coordinates(lat, lon, api_key)

    assert response.status_code == 200

    data = response.json()
    temp = data["main"]["temp"]

    assert "weather" in data
    assert "main" in data
    assert "coord" in data

    assert abs(data["coord"]["lat"] - lat) < 0.01
    assert abs(data["coord"]["lon"] - lon) < 0.01

    assert isinstance(temp, (int, float))


def test_weather_response_matches_schema(weather, api_key, weather_schema):

    response = weather.get_weather("Warsaw", api_key)
    assert response.status_code == 200

    data = response.json()
    schema = weather_schema

    validate(instance=data, schema=schema)


def test_weather_returns_404_for_non_existing_city(weather, api_key):

    response = weather.get_weather("NOT_EXISTING_CITY", api_key)

    assert response.status_code == 404

    data = response.json()

    assert "city not found" in data["message"]


def test_weather_returns_400_when_city_param_missing(weather, api_key):

    response = weather.get_weather(api_key=api_key)

    assert response.status_code == 400

    data = response.json()
    message = data["message"]

    assert "Nothing to geocode" in message

    #  test empty string as city name


def test_weather_returns_400_when_city_param_empty_string(weather, api_key):

    response = weather.get_weather("", api_key)

    assert response.status_code == 400

    data = response.json()
    message = data["message"]

    assert "Nothing to geocode" in message

    # test special characters in city name


def test_weather_returns_400_when_city_param_with_special_characters(weather, api_key):

    response = weather.get_weather("Wa%^()*raw", api_key)

    assert response.status_code == 404

    data = response.json()
    message = data["message"]

    assert "city not found" in message
    # test very long city name value
    # test invalid coordinates
    # test coordingates with None/null values
    # test with country code
    # test with city ID instead of name
