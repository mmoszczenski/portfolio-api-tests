import requests
from conftest import api_key
class WeatherService:
    
    def __init__(self, client):
        self.client = client
        
    def get_weather(self, city, api_key=None, units=None, lang=None) -> requests.Response:
        params  = {"q": city}
        if api_key is not None:
            params["appid"] = api_key
        if units is not None:
            params["units"] = units
        if lang is not None:
            params["lang"] = lang
            
        return self.client.get("/weather", params = params)
    
    
    def get_weather_by_coordinates(self, lat, lon, api_key) -> requests.Response:
        
        params = {
            "lat": lat,
            "lon": lon,
            "api_key": api_key
        }
        
        return self.client.get("/weather", params=params)
        
    
