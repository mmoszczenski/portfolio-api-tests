from constants import DEFAULT_CITY
from helpers.assertions import assert_city_name

def test_auth_valid_key(weather, api_key, assert_status_code_and_valid_json):

    city = DEFAULT_CITY
    
    response = weather.get_weather(city, api_key)
    data = assert_status_code_and_valid_json(response)
        
    assert_city_name(data, city)
    
def test_auth_invalid_key(weather, assert_status_code_and_valid_json):
     
    city = DEFAULT_CITY
    response = weather.get_weather(city, api_key = "11111")
    data = assert_status_code_and_valid_json(response, expected_status=401)

    assert "Invalid" in data["message"]
    
def test_auth_no_key_provided(weather, assert_status_code_and_valid_json):
    
    city = DEFAULT_CITY
    response = weather.get_weather(city)
    data = assert_status_code_and_valid_json(response, expected_status=401)
    
    assert "Invalid" in data["message"]

def test_auth_key_with_white_spaces(weather, api_key, assert_status_code_and_valid_json):
    
    city = DEFAULT_CITY
    invalid_key = " " + api_key

    response = weather.get_weather(city, invalid_key)
    data = assert_status_code_and_valid_json(response, expected_status=401)
    
    assert "Invalid" in data["message"]