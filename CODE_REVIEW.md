# Full Code Review — API Tests Portfolio

**Scope:** All project files. No code changes; review output only.  
**Context:** API tests for 3rd-party OpenWeatherMap API; pytest, requests, jsonschema.

---

## 1. What’s good

- **Structure:** Clear separation — `services/`, `helpers/`, `utils/`, `tests/`, `data/`, `schemas/`. Easy to navigate.
- **Fixtures:** Centralized in `conftest.py`; `client`, `weather`, `forecast`, `cities`, schemas, `api_key`. Good reuse.
- **Assertions:** Reusable helpers (`assert_status_code_and_valid_json`, `assert_city_name`, `assert_errorr_message_present`, `assert_within_tolerance`, `assert_coordinates_match`) with clear failure messages and `\n` in messages.
- **Constants:** Tolerances, default city, coordinates, invalid coordinates, `UNKNOWN_CITY`, `DEFAULT_CITY_ID` in one place.
- **Type hints:** Used in helpers, services, utils, conftest (`list[str]`, `dict`, optional params). Improves readability.
- **API client:** Has `timeout=10`; avoids hanging on slow 3rd-party API.
- **Parameter order:** `WeatherService.get_weather(city, api_key, ...)` and `ForecastService.get_forecast(city, api_key, ...)` — consistent; positional `(city, api_key)` works.
- **Units:** Integration and forecast tests use `units="metric"` correctly (keyword argument).
- **Auth tests:** Assert both status 401 and message content (`"Invalid" in data["message"]`). Reduces risk of passing for wrong reason.
- **Schema validation:** JSON schemas used for weather and forecast responses.
- **Data-driven tests:** `cities.json` + test for all cities.
- **No debug code:** No stray `print` in `get_temperature.py`.
- **get_temperature:** Correct `isinstance(WeatherService)` / `isinstance(ForecastService)`; fallback `TypeError`; return type `-> float`.

---

## 2. What to improve

### 2.1 `api_key` fixture can be `None` — recommended fix (no code change here; document only)

**Problem:** `api_key` returns `os.getenv("API_KEY")` → `str | None`. If `API_KEY` is unset or invalid, many tests get 401 and fail in a way that looks like “random test failures” instead of “key missing or invalid”.

**Recommended fix:** Add a **session-scoped** fixture that runs once per test run and:

1. Reads `key = os.getenv("API_KEY")`.
2. If `not key or not key.strip()` → `pytest.skip("API_KEY not set. Set it in .env to run tests.")`.
3. Otherwise builds a one-off `ApiClient` and `WeatherService`, calls `get_weather(DEFAULT_CITY, key)`.
4. If `response.status_code == 401` → `pytest.skip("API_KEY is invalid or expired. Update .env.")`.

Then make the existing `api_key` fixture **depend** on this session-scoped fixture (e.g. name it `_valid_api_key_required` and add it as a parameter: `def api_key(_valid_api_key_required) -> str | None:`). The first test that requests `api_key` will trigger the check; if the key is bad, the whole run is skipped with a clear message. Tests that do not use `api_key` (e.g. `test_auth_no_key_provided`) do not trigger the check.

**Where:** `conftest.py`. You need to import `DEFAULT_CITY` from `constants` and add the session-scoped fixture above the `api_key` fixture; then add `_valid_api_key_required` as the first parameter of `api_key`.

---

### 2.2 Stronger 400 message check — recommended fix (no code change here; document only)

**Problem:** For 400 responses you only assert that the body has a non-empty `"message"` field (`assert_errorr_message_present(data)`). If the API ever returned 400 for a different reason (e.g. invalid key as 400 instead of 401), those tests could still pass even though you intend to test “missing city” or “validation error”.

**Recommended fix:**

1. **New helper in `helpers/assertions.py`:**  
   `assert_validation_error_message(data: dict, *expected_substrings: str) -> None`
   - Assert `"message"` in `data`.
   - Get `msg = data["message"]`; if it’s a string use it, else `str(msg)`; normalize to lowercase.
   - Assert that at least one of `expected_substrings` (case-insensitive) appears in that string.
   - On failure, raise with a message like: expected one of `expected_substrings`, got `data["message"]`.

2. **Use it in 400 tests that are about missing/invalid city:**  
   After `assert_errorr_message_present(data)` add:  
   `assert_validation_error_message(data, "geocode", "nothing", "city")`  
   in:
   - `test_weather_returns_400_when_city_param_missing`
   - `test_weather_returns_400_when_city_param_empty_string`
   - `test_forecast_returns_400_when_city_param_missing`

   OpenWeatherMap typically returns something like “Nothing to geocode” for missing/empty city, so one of these substrings should match.

3. **Optional:** For 400 tests about **coordinates** (invalid lat/lon, null), you can add a similar call with substrings that match the API’s coordinate-error message (e.g. `"invalid"`, `"coord"`, `"limit"`), or leave them with only `assert_errorr_message_present(data)`.

---

### 2.4 `test_perf.py` is empty

Either add at least one performance-related test (e.g. assert response time below a threshold, with a marker like `@pytest.mark.perf`) and register the marker in `pytest.ini`, or remove the file so the suite does not contain an empty test module.

---

### 2.5 README.md

Currently only “# blank for now”. For a portfolio, consider adding:

- Short description (e.g. “API tests for OpenWeatherMap”).
- How to run: `pytest`, optionally `pytest tests/ -v`.
- That `API_KEY` must be set (e.g. in `.env`).
- Optional: one-line overview of layout (services, helpers, tests, data, schemas).

---

### 2.6 requirements.txt encoding

If the file was saved as UTF-16 or with a BOM, it can cause issues on some systems. Save as **UTF-8** (no BOM). Ensure one dependency per line (e.g. `requests`, `pytest`, `python-dotenv`, `jsonschema`) with versions as desired.

---

### 2.7 Minor style

- **constants.py** line 6: `# Warsaw` — already has space after `#`; no change needed.
- **api_client.py:** Consider a blank line between `import requests` and `class ApiClient` (PEP 8).
- **assertions.py:** Trailing blank lines at end of file (lines 75–76); optional to trim.
- **utils/temp_converter.py:** No leading/trailing blank lines; good.

---

### 2.8 Optional: pytest markers

If you want to run subsets (e.g. exclude integration), add `@pytest.mark.integration` to `test_integration_weather_vs_forecast.py` and ensure the marker is registered in `pytest.ini`. Current `pytest.ini` already lists `integration`; just use the marker in the test if you need it.

---

## 3. Summary table

| Area             | Status  | Action                                                                             |
| ---------------- | ------- | ---------------------------------------------------------------------------------- |
| Structure / flow | Good    | None.                                                                              |
| API key handling | Improve | Add session-scoped validation fixture; make `api_key` depend on it (see 2.1).      |
| 400 verification | Improve | Add `assert_validation_error_message` and use in city-related 400 tests (see 2.2). |
| Polish test      | Minor   | Reuse `data` from assertion instead of calling `.json()` again (see 2.3).          |
| test_perf.py     | Pending | Add one perf test + marker or remove file (see 2.4).                               |
| README           | Minimal | Add description, run instructions, API_KEY (see 2.5).                              |
| requirements.txt | Check   | Ensure UTF-8 and correct deps (see 2.6).                                           |
| Style            | Minor   | Optional PEP 8 tweaks (see 2.7).                                                   |

---

## 4. Checklist (for you to implement; no code changes in this review)

- [ ] **conftest.py:** Add session-scoped fixture `_valid_api_key_required` (check key set + one request; skip if missing or 401). Make `api_key` depend on it.
- [ ] **helpers/assertions.py:** Add `assert_validation_error_message(data, *expected_substrings)` and use `\n` in its error message.
- [ ] **tests/test_weather.py:** In city-related 400 tests, after `assert_errorr_message_present(data)` add `assert_validation_error_message(data, "geocode", "nothing", "city")`. In Polish-language test, reuse `data_eng` / `data_pl` from assertion instead of `.json()`.
- [ ] **tests/test_forecast.py:** In `test_forecast_returns_400_when_city_param_missing`, after `assert_errorr_message_present(data)` add `assert_validation_error_message(data, "geocode", "nothing", "city")`.
- [ ] **test_perf.py:** Add at least one perf test (e.g. response time) and register marker, or remove the file.
- [ ] **README.md:** Add short description, run instructions, API_KEY requirement.
- [ ] **requirements.txt:** Save as UTF-8; verify dependency list.
- [ ] **Optional:** Add `@pytest.mark.integration` to integration test if you run subsets; optional PEP 8 cleanups (blank line in api_client, trim trailing blanks in assertions).

---

End of code review. No code was modified; only this file (CODE_REVIEW.md) was written.
