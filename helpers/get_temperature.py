from utils.temp_converter import kelvin_to_celsius, kelvin_to_fahrenheit

def get_tempeterature_for_city(weather_service, city, api_key, units=None):
    
    response = weather_service.get_weather(city=city, api_key=api_key, units=units)
    return response.json()["main"]["temp"]

def get_temperature_in_celsius(weather_service, city, api_key):
    
    temp_kelvin = get_tempeterature_for_city(weather_service, city, api_key)
    return kelvin_to_celsius(temp_kelvin)

def get_temperature_in_fahrenheit(weather_service, city, api_key):
    
    temp_kelvin = get_tempeterature_for_city(weather_service, city, api_key)
    return kelvin_to_fahrenheit(temp_kelvin)