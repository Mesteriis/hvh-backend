import json
from json import JSONDecodeError

from httpx import Response
from starlette import status


def assert_response(response: Response, status_code: int = status.HTTP_200_OK, data: dict | None = None):
    try:
        data_ = response.json()
        type_data = "json"
        assert data_, "Response is empty"
    except JSONDecodeError:
        data_ = response.text
        type_data = "text"
        assert data_, "Response is empty"

    assert response.status_code == status_code, f"\nExpected: {status_code} Actual: {response.status_code} \nDitail: \n{json.dumps(data_, indent=2) if type_data == 'json' else data_}"
    if data:
        for key, value in data.items():
            try:
                assert data_[key] == value, f"ditail: \n{json.dumps(data_, indent=2) if type_data == 'json' else data_}"
            except KeyError:
                assert False, f"Key {key} not found in response data: \n{json.dumps(data_, indent=2) if type_data == 'json' else data_}"