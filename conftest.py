import os
import pytest
from services.api_client import ApiClient
from services.weather_service import WeatherService
from services.forecast_service import ForecastService
from dotenv import load_dotenv
from utils.cities_loader import load_cities
from utils.schema_loader import load_schema

load_dotenv()


@pytest.fixture
def api_key() -> str | None:
    
    key = os.getenv("API_KEY")
    
    if not key:
        pytest.skip("API KEY is not set")
    return key 


@pytest.fixture
def client() -> ApiClient:
    return ApiClient()


@pytest.fixture
def weather(client) -> WeatherService:
    return WeatherService(client)


@pytest.fixture
def forecast(client) -> ForecastService:
    return ForecastService(client)


@pytest.fixture
def cities() -> list[str]:
    return load_cities()


@pytest.fixture
def weather_schema() -> dict:
    return load_schema("weather_schema.json")


@pytest.fixture
def forecast_schema() -> dict:
    return load_schema("forecast_schema.json")

