from utils.temp_converter import kelvin_to_celsius, kelvin_to_fahrenheit
from services.weather_service import WeatherService
from services.forecast_service import ForecastService

def get_temperature_for_city(service: WeatherService | ForecastService, api_key: str, city: str, units: str | None = None) -> float:
    
    if isinstance(service, WeatherService):
        response = service.get_weather(city=city, api_key=api_key, units=units)
        return response.json()["main"]["temp"]
        
    if isinstance(service, ForecastService):
        response = service.get_forecast(city=city, api_key=api_key, units=units)
        return response.json()["list"][0]["main"]["temp"]
        
    else: 
        raise TypeError("Service must be WeatherService or ForecastService")    

def get_temperature_in_celsius(service: WeatherService | ForecastService, api_key: str, city: str) -> float:
    
    temp_kelvin = get_temperature_for_city(service, api_key, city)
    return kelvin_to_celsius(temp_kelvin)

def get_temperature_in_fahrenheit(service: WeatherService | ForecastService, api_key: str, city: str) -> float:
    
    temp_kelvin = get_temperature_for_city(service, api_key, city)
    return kelvin_to_fahrenheit(temp_kelvin)