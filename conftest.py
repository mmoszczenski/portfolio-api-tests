import os
import pytest
from services.api_client import ApiClient
from services.weather_service import WeatherService
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def api_key():
    return os.getenv("API_KEY")

@pytest.fixture
def client():
    return ApiClient()

@pytest.fixture
def weather(client):
    return WeatherService(client)
    