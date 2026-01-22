import requests


class ForecastService:

    def __init__(self, client):
        self.client = client

    def get_forecast(self, city=None, api_key=None, units=None) -> requests.Response:

        params = {}

        if city is not None:
            params["q"] = city
        if api_key is not None:
            params["appid"] = api_key
        if units is not None:
            params["units"] = units

        return self.client.get("/forecast", params=params)
