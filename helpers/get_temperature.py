from utils.temp_converter import kelvin_to_celsius, kelvin_to_fahrenheit

def get_temperature_for_city(weather_service, api_key, city, units=None):
    
    response = weather_service.get_weather(city=city, api_key=api_key, units=units)
    return response.json()["main"]["temp"]

def get_temperature_in_celsius(weather_service, api_key, city):
    
    temp_kelvin = get_temperature_for_city(weather_service, api_key, city)
    return kelvin_to_celsius(temp_kelvin)

def get_temperature_in_fahrenheit(weather_service, api_key, city):
    
    temp_kelvin = get_temperature_for_city(weather_service, api_key, city)
    return kelvin_to_fahrenheit(temp_kelvin)