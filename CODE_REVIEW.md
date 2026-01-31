# Full Code Review — API Tests Portfolio

**Scope:** All project files. No code changes; output only.  
**Context:** API tests for 3rd-party OpenWeatherMap API; pytest, requests, jsonschema.

---

## 1. What's good

- **Structure:** Clear separation — `services/`, `helpers/`, `utils/`, `tests/`, `data/`, `schemas/`. Easy to navigate.
- **Fixtures:** Centralized in `conftest.py`; `client`, `weather`, `forecast`, `cities`, schemas, `api_key`. Good reuse.
- **Assertions:** Reusable helpers with clear failure messages; `assert_error_message(data, *expected_substrings)` strengthens 401/400 checks; `assert_error_message_present` (name has typo, see below) for presence; `assert_coordinates_match`, `assert_within_tolerance`.
- **Constants:** Tolerances, default city, coordinates, `UNKNOWN_CITY`, `DEFAULT_CITY_ID` in one place.
- **Type hints:** Used in helpers, services, utils, conftest. Improves readability.
- **API client:** Has `timeout=10`. Avoids hanging on slow 3rd-party API.
- **Parameter order:** `get_weather(city, api_key, ...)` and `get_forecast(city, api_key, ...)` — consistent; positional works.
- **Units:** Integration and forecast use `units="metric"` correctly.
- **Markers:** `@pytest.mark.positive`, `@pytest.mark.negative`, `@pytest.mark.weather`, `@pytest.mark.forecast` used; registered in `pytest.ini`. Enables running subsets (e.g. `pytest -m positive`).
- **Polish-language test:** Reuses `data_eng` / `data_pl` from assertion; no double `.json()`.
- **Schema validation:** JSON schemas used for weather and forecast.
- **Data-driven tests:** `cities.json` + test for all cities.
- **get_temperature:** Correct `isinstance` checks; fallback `TypeError`; supports both city and lat/lon via `get_weather`/`get_forecast`.

---

## 2. What to improve

### 2.1 Typo in assertion name — `assert_error_message_present`

In `helpers/assertions.py` the function is named **`assert_error_message_present`** (three r's). It is used in `test_weather.py` and `test_forecast.py`. Rename to **`assert_error_message_present`** and update all imports/calls so the name is consistent and correct.

---

### 2.2 `assert_error_message` — order of operations

In `helpers/assertions.py`, `assert_error_message(data, *expected_substrings)` does:

```python
message = data["message"].lower()
assert isinstance(message, str), ...
```

If `data["message"]` is not a string (e.g. a number), `.lower()` will raise `AttributeError` before the `isinstance` assert runs. Safer order: get `message = data["message"]`, then `assert isinstance(message, str)`, then use `message.lower()` for the substring checks.

---

### 2.3 `get_weather_by_coordinates` vs `get_weather(lat=..., lon=...)`

**Answer: Yes — `get_weather_by_coordinates` is redundant.**

- **`get_weather(lat=lat, lon=lon, api_key=api_key)`** sends the same query (same endpoint `/weather`, same params `lat`, `lon`, `appid`) as **`get_weather_by_coordinates(lat, lon, api_key)`**.
- So you can **always** use `get_weather(lat=lat, lon=lon, api_key=api_key)` (and optionally `units=`, `lang=`, etc.) and achieve the same result.

**Options:**

1. **Remove `get_weather_by_coordinates`** and everywhere use `weather.get_weather(lat=lat, lon=lon, api_key=api_key)` (and in `get_temperature_for_city` you already pass `lat`/`lon` into `get_weather`, so no need for a separate method). This keeps a single entry point for the weather API.
2. **Keep it as a convenience wrapper** if you like the explicit name “by coordinates” for readability; functionally it adds nothing.

So: it doesn’t add new behavior; you can safely use `get_weather` with `lat` and `lon` params only.

---

### 2.4 Integration test — marker

`test_integration_weather_vs_forecast.py` does not use `@pytest.mark.integration`. Adding it would match `pytest.ini` and allow runs like `pytest -m "not integration"` for faster feedback.

---

### 2.5 `api_key` fixture can be `None`

`api_key` returns `os.getenv("API_KEY")` → `str | None`. If unset or invalid, many tests get 401 with unclear cause. Optional improvement: session-scoped fixture that checks key is set and does one request; if missing or 401, `pytest.skip(...)` so the reason is obvious (as in previous review).

---

### 2.6 README.md

Still “# blank for now”. See **Section 5** below for example README content you can use.

---

### 2.7 test_perf.py

Still empty. See **Section 6** below for an example performance test you can add.

---

### 2.8 Minor style

- **test_auth.py:** PEP 8 suggests two blank lines between top-level function definitions; some tests are separated by only one. Optional cleanup.
- **api_client.py:** Blank line between `import requests` and `class ApiClient` (PEP 8).
- **assertions.py:** Trailing blank lines at end of file; optional to trim.

---

## 3. Summary table

| Area                       | Status    | Action                                                                                                                   |
| -------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------ |
| Structure / flow           | Good      | None.                                                                                                                    |
| Assertion naming           | Bug       | Rename `assert_error_message_present` → `assert_error_message_present`; fix `assert_error_message` order (see 2.1, 2.2). |
| get_weather_by_coordinates | Redundant | Use `get_weather(lat=, lon=, api_key=)` everywhere; optionally remove method (see 2.3).                                  |
| Integration marker         | Minor     | Add `@pytest.mark.integration` to integration test (see 2.4).                                                            |
| README / test_perf         | Pending   | Use example README (Section 5); add example perf test (Section 6).                                                       |
| Style                      | Minor     | Optional PEP 8 (see 2.8).                                                                                                |

---

## 4. Checklist (for you to implement)

- [ ] **helpers/assertions.py:** Rename `assert_error_message_present` → `assert_error_message_present`; in `assert_error_message`, get `message = data["message"]`, assert `isinstance(message, str)`, then use `message.lower()` for substring checks.
- [ ] **tests:** Update all imports/calls from `assert_error_message_present` to `assert_error_message_present`.
- [ ] **Optional:** Remove `get_weather_by_coordinates` from `WeatherService`; in tests and `get_temperature_for_city` use `get_weather(lat=lat, lon=lon, api_key=api_key)` (see 2.3).
- [ ] **test_integration_weather_vs_forecast.py:** Add `@pytest.mark.integration`.
- [ ] **README.md:** Replace with content from Section 5 (or adapt).
- [ ] **test_perf.py:** Add example from Section 6 (or similar) and register `perf` marker in `pytest.ini`.

---

## 5. Example README.md content

You can replace the current README with something like this (adjust as needed):

````markdown
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
````

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

# Verbose
pytest -v

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

````

---

## 6. Example performance test

You can add a simple performance test (e.g. in `tests/test_perf.py`) that asserts the weather endpoint responds within a time limit. Example below uses `response.elapsed` (no extra deps). Register the `perf` marker in `pytest.ini` (e.g. `perf: performance / response time tests`).

**Example content for `tests/test_perf.py`:**

```python
import pytest
from constants import DEFAULT_CITY


@pytest.mark.perf
def test_weather_endpoint_response_time(weather, api_key):
    """Assert /weather responds within 5 seconds for a simple request."""
    max_seconds = 5.0
    response = weather.get_weather(DEFAULT_CITY, api_key)
    response.raise_for_status()
    elapsed = response.elapsed.total_seconds()
    assert elapsed < max_seconds, (
        f"Weather endpoint took {elapsed:.2f}s, expected < {max_seconds}s"
    )
````

**Add to `pytest.ini` under `markers`:**

```ini
perf: performance / response time tests
```

Then run with: `pytest -m perf` or exclude with: `pytest -m "not perf"`.

---

End of code review. No code was modified; only this file (CODE_REVIEW.md) was written.
