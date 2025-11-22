import requests
class ApiClient:
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def get(self, endpoint, params=None) -> requests.Response:
        url = f"{self.BASE_URL}{endpoint}"
        return requests.get(url, params=params)