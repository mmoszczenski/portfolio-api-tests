# Full Code Review — API Tests Portfolio

**Scope:** All project files. Focus: best practices, type hints, helpers/constants/fixtures, test coverage, readability, no duplication.  
**Context:** API tests only; testing 3rd-party OpenWeatherMap API; no application source code.

---

## 1. Project structure and organization

**Good:**

- Clear separation: `services/` (API), `helpers/` (assertions + temperature), `utils/` (loaders, converters), `tests/`, `data/`, `schemas/`.
- Fixtures centralized in `conftest.py`; tests import assertion helpers directly (no fixture wrapper).
- Constants in one place; JSON schemas for contract validation; data-driven cities list.

**To improve:**

- **`conftest.py`** still imports `_assert_status_code_and_valid_json` but no longer exposes it as a fixture. Remove the unused import and alias (lines 9–10) to avoid dead code.
- **`pytest.ini`** has a typo: "tests cases" → "test cases" in marker descriptions (lines 8–11).

---

## 2. Functions — do they all make sense?

### 2.1 `helpers/get_temperature.py`

| Function                        | Purpose                                                                            | Verdict                                                                                                                                                                                                                                                                                                         |
| ------------------------------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `get_temperature_for_city`      | Returns `main.temp` from weather or first forecast item depending on service type. | **Makes sense.** Single place to get "current" temp from either API.                                                                                                                                                                                                                                            |
| `get_temperature_in_celsius`    | Gets Kelvin temp then converts.                                                    | **Makes sense.** But it always calls the API with default units (Kelvin). For consistency with "celsius" you could pass `units="metric"` into `get_temperature_for_city` and then read the value directly instead of converting—would avoid conversion tolerance issues. Optional improvement, not wrong as-is. |
| `get_temperature_in_fahrenheit` | Same pattern for Fahrenheit.                                                       | **Makes sense.** Same note as above for `units="imperial"`.                                                                                                                                                                                                                                                     |

**Issue:** If `get_temperature_for_city` is called with a type that is neither `WeatherService` nor `ForecastService`, the function exits without returning → returns `None`. Consider raising a clear error, e.g. `raise TypeError("service must be WeatherService or ForecastService")` after the two `if` blocks, so misuse fails fast with a clear message.

**Indentation:** The body of `get_temperature_for_city` (lines 7–13) is over-indented by one level. Should align with the function body (4 spaces from def).

---

### 2.2 `helpers/assertions.py`

| Function                            | Purpose                                                                 | Verdict                                                 |
| ----------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------- |
| `assert_status_code_and_valid_json` | Asserts status, parses JSON, optionally checks root type, returns data. | **Makes sense.** Core helper; reduces duplication.      |
| `assert_city_name`                  | Ensures `data["name"]` matches expected (case-insensitive).             | **Makes sense.** Reused in auth and weather tests.      |
| `assert_error_message`              | Ensures `data` has a non-empty `message` key.                           | **Makes sense.** Shared for 400/404 error tests.        |
| `assert_within_tolerance`           | Asserts \|actual − expected\| < tolerance.                              | **Makes sense.** Used for temperatures and coordinates. |

**Typos:**

- Line 18: `"Expeced"` → **"Expected"**.
- Line 18: Missing space/newline between the two f-strings in the assertion message (same as in `assert_within_tolerance` below).

**Message formatting:** In `assert_within_tolerance` (lines 55–58), the two f-strings are concatenated with no space. Add `"\n"` or `" "` between them so both parts are readable when the assertion fails.

---

### 2.3 `services/`

- **ApiClient.get:** Thin wrapper around `requests.get`; builds URL from `BASE_URL` + endpoint. **Makes sense.**
- **WeatherService / ForecastService:** Build params and delegate to client. **Make sense.**
- **Missing:** No `timeout` on `requests.get` in `api_client.py`. For production-style tests, add e.g. `timeout=30` (or `(10, 30)`) so the suite does not hang on a slow or stuck 3rd-party API.

---

### 2.4 `utils/`

- **load_json:** Loads JSON from path relative to project root. **Makes sense.**
- **load_schema:** Wraps load_json with `schemas/` prefix. **Makes sense.**
- **load_cities:** Wraps load_json for `data/cities.json`. **Makes sense.**
- **kelvin_to_celsius / kelvin_to_fahrenheit:** Pure conversion. **Make sense.**

No function is redundant; each has a clear responsibility.

---

## 3. Type hints — where missing and whether to add

**Best practice for this repo:** Type hints improve readability, enable static checking (mypy, Pyright), and document contracts. For a portfolio and maintainability, adding them is recommended, especially on public helpers and services.

### 3.1 Currently missing (recommended to add)

| File | Location | Suggested annotation |
| ---- | -------- | -------------------- |

| **utils/schema_loader.py** | `load_schema(name)` | `name: str`, return e.g. `-> dict` (JSON Schema is an object). |
| **utils/cities_loader.py** | `load_cities()` | `-> list` (list of city strings). |

| **conftest.py** | `weather_schema()` / `forecast_schema()` | `-> dict`. |

### 3.2 Style

- **temp_converter.py:** Use space after colon in type hints: `kelvin: float` instead of `kelvin:float` (PEP 8).
- **constants.py:** Remove the leading blank line (line 1) for consistency.

### 3.3 Summary

Adding the above hints is good practice: they document the API, help IDEs, and allow mypy/pyright. Start with `helpers/` and `services/`; then `utils/` and `conftest.py`.

---

## 4. Helpers, constants, and fixtures for readability

### 4.1 Constants to introduce

| Constant              | Current usage                                                | Suggested name                           | File           |
| --------------------- | ------------------------------------------------------------ | ---------------------------------------- | -------------- |
| `1.5`                 | Integration test tolerance (weather vs forecast temp)        | `WEATHER_FORECAST_TEMPERATURE_TOLERANCE` | `constants.py` |
| `756135`              | Warsaw city ID in `test_weather_can_be_requested_by_city_id` | `DEFAULT_CITY_ID` or `WARSAW_CITY_ID`    | `constants.py` |
| `"NON_EXISTING_CITY"` | test_forecast (404)                                          | `UNKNOWN_CITY`                           | `constants.py` |
| `"NOT_EXISTING_CITY"` | test_weather (404)                                           | Same `UNKNOWN_CITY`                      | `constants.py` |

Using one `UNKNOWN_CITY` in both test files avoids magic strings and keeps naming consistent.

### 4.2 Fixtures

- **Optional fixture:** `valid_weather_response(weather, api_key)` in conftest that returns already-validated weather JSON for DEFAULT_CITY. Not strictly necessary; current "get response then assert" is clear. Only add if you see repeated "get weather for default city and assert success" in many tests.
- **api_key when missing:** If `API_KEY` is unset, tests that need it fail inside the test with a generic error. Consider a fixture that checks `os.getenv("API_KEY")` and calls `pytest.skip(reason="API_KEY not set")` or `pytest.exit()` so the reason is obvious. Document in README that API_KEY is required for most tests.

### 4.3 Helpers

- **Schema validation pattern:** In tests you often do:
  - `data = assert_status_code_and_valid_json(response)`
  - `validate(instance=data, schema=schema)`
    You could add a small helper, e.g. `assert_response_matches_schema(response, schema, expected_status=200)` that does both and returns `data`. This would shorten schema tests and keep the pattern in one place. Optional.
- **Coordinates assertion:** In `test_weather_can_be_requested_by_lat_and_lon` you have:
  - `assert abs(data["coord"]["lat"] - lat) < COORDINATES_TOLERANCE`
  - `assert abs(data["coord"]["lon"] - lon) < COORDINATES_TOLERANCE`
    A helper `assert_coordinates_match(data["coord"], lat, lon, COORDINATES_TOLERANCE)` would make the test more readable and reuse the tolerance logic. Optional.

---

## 5. Test coverage and suggested additional tests

**Principle:** Do not duplicate. If weather already checks a behavior (e.g. 400 when city missing), forecast does not need the same test unless the API contract differs.

### 5.1 Already well covered

- **Auth:** Valid key, invalid key, no key, key with whitespace (weather only is enough; same API key for forecast).
- **Weather:** Single city, all cities, units (metric/imperial), lang, by coords, by city id, schema, 404/400 cases, empty string, special chars, long name, invalid/null coords.
- **Forecast:** Missing city (400), happy path (5-day structure, order, schema), unknown city (404), units metric.
- **Integration:** Weather vs forecast temperature consistency.

### 5.2 Gaps / suggested additions (without duplicating weather)

1. **Forecast-specific**
   - **Forecast without city but with api_key returns 400:** You have this. Good.
   - **Forecast with invalid API key returns 401:** You test auth on weather only; one 401 test is enough for the whole API. Optional: add a single test in `test_forecast.py` that forecast with invalid key returns 401, if you want each module to be self-contained. Otherwise skip.
   - **Forecast with empty city string:** Weather has it; forecast might behave the same. Only add if you want to document forecast’s behavior explicitly (low priority).

2. **Integration**
   - **Same city in weather and forecast:** You already assert temperature consistency. Optionally assert that `forecast_data["city"]["name"]` matches the requested city to tie the integration test to the same location.

3. **Edge cases (optional)**
   - **Weather:** Response time or timeout (e.g. with `pytest-timeout` or a simple `assert response.elapsed.total_seconds() < 10`). Put in `test_perf.py` and mark as `@pytest.mark.slow` or `@pytest.mark.perf` so it can be excluded in quick runs.
   - **Rate limiting / 429:** If the 3rd-party API can return 429, one test that at least handles it (e.g. skip or expect) could be useful. Only if relevant.

4. **test_perf.py**
   - File is empty. Either remove it or add at least one test (e.g. "weather response returns within X seconds") and mark it (e.g. `@pytest.mark.perf`). Register the marker in `pytest.ini` to avoid warnings. Avoid leaving an empty test file.

### 5.3 Tests not recommended (avoid duplication)

- Do not add forecast tests for: invalid key, no key, 400 missing city, 404 unknown city, schema, units—weather (and existing forecast tests) already cover the same API contract. Only add forecast-specific variants if the API docs say forecast behaves differently.

---

## 6. File-by-file specifics

### 6.1 `constants.py`

- Leading blank line (line 1): remove.
- Consider adding: `UNKNOWN_CITY`, `WEATHER_FORECAST_TEMPERATURE_TOLERANCE`, `DEFAULT_CITY_ID` (or `WARSAW_CITY_ID`) as above.

### 6.2 `conftest.py`

- Remove unused import and alias: `assert_status_code_and_valid_json` / `_assert_status_code_and_valid_json`.
- Consider failing or skipping when `API_KEY` is missing (see 4.2).

### 6.3 `helpers/assertions.py`

- Fix typo: "Expeced" → "Expected".
- Add newline or space between the two f-strings in the `assert isinstance(...)` message (line 17–19) and in `assert_within_tolerance` (lines 56–58).
- Add type hints (see section 3).

### 6.4 `helpers/get_temperature.py`

- Fix indentation of the body of `get_temperature_for_city` (one level less).
- If `service` is neither `WeatherService` nor `ForecastService`, raise `TypeError` instead of returning `None`.
- Add type hints for all parameters (see section 3).

### 6.5 `services/api_client.py`

- Add `timeout=30` (or similar) to `requests.get`.
- Add parameter type hints for `endpoint` and `params`.
- Blank line between `import requests` and `class ApiClient` (PEP 8).

### 6.6 `services/weather_service.py` & `forecast_service.py`

- Add type hints for `client` in `__init__` and for all method parameters (see section 3).

### 6.7 `utils/temp_converter.py`

- Use `kelvin: float` (space after colon).
- Remove trailing blank lines at end of file (lines 9–11).

### 6.8 `utils/json_loader.py`

- Add return type, e.g. `-> Union[dict, list]`.
- Optionally document or handle missing file (e.g. clearer error message); not mandatory.

### 6.9 `utils/schema_loader.py` & `cities_loader.py`

- Add return type hints (see section 3).

### 6.10 `tests/test_weather.py`

- Line 1: remove leading blank line.
- Line 191: use constant for Warsaw city ID (e.g. `DEFAULT_CITY_ID`) and use `UNKNOWN_CITY` for 404 tests (lines 120, etc.) once defined.
- Line 76–77: You use `response_eng.json()` and `response_pl.json()` after `assert_status_code_and_valid_json` has already parsed the body. Consider storing the returned `data` from the assertion and using it (e.g. `data_eng["weather"][0]["description"]`) to avoid double parsing and to be consistent with other tests.

### 6.11 `tests/test_forecast.py`

- Use `UNKNOWN_CITY` constant (line 55) once added to constants.
- Line 79: Inline conversion `(temp_k - 273.15)` could use `kelvin_to_celsius(temp_k)` from utils for consistency (optional).

### 6.12 `tests/test_integration_weather_vs_forecast.py`

- Use constant for tolerance, e.g. `WEATHER_FORECAST_TEMPERATURE_TOLERANCE` from constants, instead of local `tolerance = 1.5`.
- Consider adding `@pytest.mark.integration` so you can run e.g. `pytest -m "not integration"` for fast feedback.

### 6.13 `tests/test_auth.py`

- No issues; consider using `UNKNOWN_CITY` only if you ever switch auth tests to a different city (not required).

### 6.14 `tests/test_perf.py`

- Either add at least one performance-related test (and register marker) or delete the file.

### 6.15 `data/cities.json`

- Add trailing newline at end of file (common convention).

### 6.16 `pytest.ini`

- Fix marker descriptions: "tests cases" → "test cases".

---

## 7. Summary table

| Area       | Status         | Priority actions                                                                                                         |
| ---------- | -------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Structure  | Good           | Remove dead import in conftest; fix pytest.ini typos.                                                                    |
| Functions  | All make sense | Fix get_temperature indentation and add fallback error; fix assertion typos and message formatting.                      |
| Type hints | Partial        | Add in helpers, services, utils, conftest (see section 3).                                                               |
| Constants  | Good           | Add UNKNOWN_CITY, WEATHER_FORECAST_TEMPERATURE_TOLERANCE, DEFAULT_CITY_ID; use them in tests.                            |
| Fixtures   | Good           | Optional: api_key skip/exit when unset; optional valid_weather_response.                                                 |
| Helpers    | Good           | Optional: assert_response_matches_schema, assert_coordinates_match.                                                      |
| Tests      | Strong         | Use new constants; fix test_weather double parse; add one perf test or remove test_perf.py; optional integration marker. |
| Robustness | Good           | Add timeout in api_client; optional docstrings/README/requirements if not present.                                       |

---

## 8. Checklist (no code changes from reviewer)

- [ ] Remove unused `_assert_status_code_and_valid_json` import/alias from conftest.
- [ ] Fix "Expeced" and message formatting in assertions.py; add newline in assert_within_tolerance message.
- [ ] Fix indentation and add fallback TypeError in get_temperature_for_city.
- [ ] Add timeout to ApiClient.get.
- [ ] Add constants: UNKNOWN_CITY, WEATHER_FORECAST_TEMPERATURE_TOLERANCE, DEFAULT_CITY_ID (or WARSAW_CITY_ID).
- [ ] Use those constants in test_weather.py, test_forecast.py, test_integration_weather_vs_forecast.py.
- [ ] Add type hints (helpers, services, utils, conftest) as in section 3.
- [ ] Fix pytest.ini marker text ("test cases"); temp_converter spacing; constants/schema_loader/cities_loader return types.
- [ ] Either implement one test in test_perf.py (with marker) or remove the file.
- [ ] Optional: assert_response_matches_schema helper; assert_coordinates_match; @pytest.mark.integration; reuse data from assert_status_code_and_valid_json in test_weather_returns_polish_when_language_PL.

End of code review.
