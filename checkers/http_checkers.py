from contextlib import contextmanager

import requests


@contextmanager
def check_status_code_http(
    expected_status_code=requests.codes.OK,
    expected_message="",
):
    try:
        yield
        if expected_status_code != requests.codes.OK:
            raise AssertionError(
                f"Ожидаемый статус код должен быть равен {expected_status_code}"
            )
        if expected_message:
            raise AssertionError(
                f"Должно быть получено сообщение {expected_message}, "
                f"но запрос прошел успешно"
            )
    except requests.exceptions.HTTPError as err:
        assert err.response.status_code == expected_status_code
        assert err.response.json()["title"] == expected_message
