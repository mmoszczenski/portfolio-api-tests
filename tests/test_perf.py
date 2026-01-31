from constants import DEFAULT_CITY
import pytest

@pytest.mark.performance
@pytest.mark.positive
def test_weather_endpoint_response_time(weather, api_key):
    
    city = DEFAULT_CITY
    max_seconds = 5.0
    
    response = weather.get_weather(city, api_key)
    response.raise_for_status()
    elapsed = response.elapsed.total_seconds()
    
    assert elapsed < max_seconds, (
        f"Weather endpoint took {elapsed:.2f}s, expected < {max_seconds}s"
    )