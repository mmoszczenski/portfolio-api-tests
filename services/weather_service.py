import requests
class WeatherService:
    
    def __init__(self, client):
        self.client = client
        
    def get_weather(self, city, api_key=None, units=None) -> requests.Response:
        params  = {"q": city}
        if api_key is not None:
            params["appid"] = api_key
        if units is not None:
            params["units"] = units
            
        return self.client.get("/weather", params = params)