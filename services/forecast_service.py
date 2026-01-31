import requests
from services.api_client import ApiClient


class ForecastService:

    def __init__(self, client: ApiClient):
        self.client = client

    def get_forecast(self, city: str | None = None, api_key: str | None = None, units: str | None = None) -> requests.Response:

        params = {}

        if city is not None:
            params["q"] = city
        if api_key is not None:
            params["appid"] = api_key
        if units is not None:
            params["units"] = units

        return self.client.get("/forecast", params=params)
