import os
import pytest
from services.api_client import ApiClient
from services.weather_service import WeatherService
from services.forecast_service import ForecastSerivce
from dotenv import load_dotenv
from utils.cities_loader import load_cities
from utils.schema_loader import load_schema

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
    return load_cities()

@pytest.fixture
def weather_schema():
    return load_schema("weather_schema.json")

@pytest.fixture
def forecast_schema():
    return load_schema("forecast_schema.json")