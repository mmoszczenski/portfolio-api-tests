import requests


def assert_status_code_and_valid_json(
    response: requests.Response, expected_status: int = 200, expected_type: type = dict
) -> dict:
    assert response.status_code == expected_status, (
        f"Expected status {expected_status}, got {response.status_code}\n"
        f"Response text: {response.text}"
    )

    try:
        data = response.json()
    except ValueError as exc:
        raise AssertionError(
            f"Response body is not valid JSON. Response text: {response.text}"
        ) from exc

    assert isinstance(data, expected_type), (
        f"Expected response type {expected_type}, got {type(data)}\n"
        f"Response data: {data}"
    )

    return data


def assert_city_name(data: dict, expected_name: str):
    city_name = data.get("name")

    assert city_name is not None, "Response missing 'name' key"
    assert city_name.lower() == expected_name.lower(), (
        f"Expected '{expected_name}', got '{city_name}'"
    )


def assert_error_message_present(data: dict):
    assert "message" in data, (
        f"Response JSON does not contain 'message' field.\n"
        f"Got keys: {list(data.keys())}, full response: {data}"
    )

    assert data["message"], (
        f"'message' field is empty or falsy.\n"
        f"Value: {data['message']!r}, full response: {data}"
    )


def assert_error_message(data: dict, *expected_substrings: str):
    assert "message" in data, (
        f"Response JSON does not contain 'message' field, got {data}"
    )

    message = data["message"]
    assert isinstance(message, str), f"message is not a string: {message}"

    for substring in expected_substrings:
        assert substring in message.lower(), (
            f"Expected substring: '{substring}', not found in message: '{message}'"
        )


def assert_within_tolerance(actual: float, expected: float, tolerance: float):
    difference = abs(actual - expected)
    assert difference < tolerance, (
        f"Difference too big. Expected {expected}, got {actual}\n"
        f"Difference is {difference}, allowed tolerance is {tolerance}"
    )


def assert_coordinates_match(
    expected_lat: float,
    expected_lon: float,
    actual_lat: float,
    actual_lon: float,
    tolerance: float,
):
    lat_difference = abs(actual_lat - expected_lat)

    assert lat_difference <= tolerance, (
        f"Difference too big. Expected lat: {expected_lat}, got {actual_lat}\n"
        f"Difference is {lat_difference}, allowed tolerance is {tolerance}"
    )

    lon_difference = abs(actual_lon - expected_lon)

    assert lon_difference <= tolerance, (
        f"Difference too big. Expected lon: {expected_lon}, got {actual_lon}\n"
        f"Difference is {lon_difference}, allowed tolerance is {tolerance}"
    )
