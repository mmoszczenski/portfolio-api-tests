import requests

class ForecastSerivce:
    
    def init(self, client):
        self.client = client
        
    def get_forecast(self, city=None) -> requests.Response:
        
        params = {}
        
        if city is not None:
            params["q"]= city
            
            
        return self.client.get("forecast", params=params)