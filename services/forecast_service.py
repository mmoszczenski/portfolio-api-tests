import requests
class ForecastSerivce:
    
    def init(self, client):
        self.client = client
        
    def get_forecast(self, city=None, api_key=None) -> requests.Response:
        
        params = {}
        
        if city is not None:
            params["q"] = city
        if api_key is not None:
            params["appid"] = api_key
            
        return self.client.get("forecast", params=params)