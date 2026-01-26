

def assert_response(response, expected_status: int = 200, expected_type: type = dict):

    assert response.status_code == expected_status, (
        f"Expected status {expected_status}, got {response.status_code}"
        f"Response text: {response.text}"
    )
