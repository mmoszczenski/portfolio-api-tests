import requests


class WeatherService:

    def __init__(self, client):
        self.client = client

    def get_weather(self, city=None, api_key=None, units=None, lang=None, city_id=None) -> requests.Response:

        params = {}

        if city is not None:
            params["q"] = city
        if api_key is not None:
            params["appid"] = api_key
        if units is not None:
            params["units"] = units
        if lang is not None:
            params["lang"] = lang
        if city_id is not None:
            params["id"] = city_id

        return self.client.get("/weather", params=params)

    def get_weather_by_coordinates(self, lat, lon, api_key) -> requests.Response:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key
        }

        return self.client.get("/weather", params=params)
