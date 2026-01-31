import requests
from services.api_client import ApiClient


class WeatherService:

    def __init__(self, client: ApiClient):
        self.client = client

    def get_weather(
        self, 
        city: str | None = None,
        api_key: str | None = None, 
        lat: float | None = None,
        lon: float | None = None,
        units: str | None = None, 
        lang: str | None = None, 
        city_id: int | None = None
        )-> requests.Response:

        params = {}

        if city is not None:
            params["q"] = city
        if lat is not None:
            params["lat"] = lat
        if lon is not None:
            params["lon"] = lon
        if api_key is not None:
            params["appid"] = api_key
        if units is not None:
            params["units"] = units
        if lang is not None:
            params["lang"] = lang
        if city_id is not None:
            params["id"] = city_id

        return self.client.get("/weather", params=params)
