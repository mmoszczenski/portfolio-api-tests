import requests

class WeatherService:
    
    def __init__(self, client):
        self.client = client
        
        
    def get_weather(self, city, api_key=None):
        params  = {"q": city}
        if api_key is not None:
            params["appid"] = api_key
            
        return self.client.get("/weather", params = params)