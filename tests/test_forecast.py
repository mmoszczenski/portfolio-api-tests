from utils.schema_loader import load_schema
from jsonschema import validate

def test_forecast_returns_5_day_forecast_for_city(forecast, api_key):
    
    city = "Warsaw"
    
    response = forecast.get_forecast(city, api_key)
    data = response.json()
      
    assert response.status_code == 200
    
    assert "list" in data
    assert isinstance(data["list"], list)
    assert len(data["list"]) >= 30

    timestamps = [item["dt"] for item in data ["list"]]
    assert timestamps == sorted(timestamps)
    
    for entry in data ["list"]:
        assert "main" in entry
        assert "weather" in entry 
        assert "dt" in entry
        
        temp = entry["main"]["temp"]
        assert isinstance(temp, (int, float))

        assert isinstance(entry["weather"], list)
        assert len(entry["weather"]) > 0

    assert data["city"]["name"] == city
    
    
def test_forecast_response_matches_schema(forecast, api_key):
    
    response = forecast.get_forecast("Warsaw", api_key)
    assert response.status_code == 200
    
    data = response.json()
    schema = load_schema("forecast_schema.json")
    
    validate(instance = data, schema = schema)
    
    
    