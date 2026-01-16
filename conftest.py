import os
import pytest
import json
from services.api_client import ApiClient
from services.weather_service import WeatherService
from services.forecast_service import ForecastSerivce
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def api_key():
    return os.getenv("API_KEY")

@pytest.fixture
def client() -> ApiClient:
    return ApiClient()

@pytest.fixture
def weather(client) -> WeatherService:
    return WeatherService(client)

@pytest.fixture
def forecast(client) -> ForecastSerivce:
    return ForecastSerivce(client)

@pytest.fixture
def cities():
    with open("data/cities.json") as f:
        return json.load(f)