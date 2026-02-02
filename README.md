# API Tests — OpenWeatherMap

Automated API tests for [OpenWeatherMap](https://openweathermap.org/api) (weather and forecast endpoints). Built with **Python**, **pytest**, and **requests**.

## What's tested

- **Auth:** Valid/invalid API key, missing key, key with leading whitespace.
- **Weather:** Happy path (single city, all cities), units (metric/imperial), language, by city ID, by coordinates, schema validation, error cases (404, 400, invalid/empty city, invalid coordinates).
- **Forecast:** 5-day structure, schema, units, missing city (400), unknown city (404).
- **Integration:** Consistency between current weather and first forecast temperature for the same city.

## Requirements

- Python 3.10+
- Dependencies: `requests`, `pytest`, `python-dotenv`, `jsonschema` (see `requirements.txt`)

## Setup

1. Clone the repo and create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenWeatherMap API key (get one at [openweathermap.org/api](https://openweathermap.org/api)):
   - Create a `.env` file in the project root with:
     ```
     API_KEY=your_api_key_here
     ```
   - Or set the environment variable `API_KEY` before running tests.

## Run tests

```bash
# All tests
pytest

# Only positive tests
pytest -m positive

# Only weather tests
pytest -m weather

# Exclude integration tests
pytest -m "not integration"
```

## Project layout

- `conftest.py` — pytest fixtures (client, weather, forecast, cities, schemas, api_key).
- `services/` — API client and service wrappers (weather, forecast).
- `helpers/` — assertion helpers and temperature helpers.
- `utils/` — JSON/schema/cities loaders, temp conversion.
- `tests/` — test modules (auth, weather, forecast, integration).
- `data/` — test data (e.g. `cities.json`).
- `schemas/` — JSON schemas for response validation.
- `constants.py` — shared constants (tolerances, default city, etc.).

```

```
