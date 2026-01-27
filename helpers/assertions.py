

def assert_status_code_and_valid_json(response, expected_status: int = 200, expected_type: type = dict):

    assert response.status_code == expected_status, (
        f"Expected status {expected_status}, got {response.status_code}"
        f"Response text: {response.text}"
    )

    try:
        data = response.json()
    except ValueError as exc:
        raise AssertionError(
            f"Response body is not valid JSON. Response text: {response.text}"
        ) from exc

    assert isinstance(data, expected_type), (
        f"Expecred response type {expected_type}, got {type(data)}"
        f"Response data: {data}"
    )

    return data


def assert_city_name(data, expected_name: str):

    city_name = data.get("name")

    assert city_name is not None, (
        f"Response missing 'name' key"
    )
    assert city_name.lower() == expected_name.lower(), (
        f"Expected '{expected_name}', got '{city_name}'"
    )
