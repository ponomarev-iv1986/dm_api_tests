from contextlib import contextmanager

import requests


# @contextmanager
# def check_status_code_http(
#     expected_status_code=requests.codes.OK,
#     expected_message="",
# ):
#     try:
#         yield
#         if expected_status_code != requests.codes.OK:
#             raise AssertionError(
#                 f"Ожидаемый статус код должен быть равен {expected_status_code}"
#             )
#         if expected_message:
#             raise AssertionError(
#                 f"Должно быть получено сообщение {expected_message}, "
#                 f"но запрос прошел успешно"
#             )
#     except requests.exceptions.HTTPError as err:
#         assert err.response.status_code == expected_status_code
#         assert err.response.json()["title"] == expected_message


class check_status_code_http:

    def __init__(self, expected_status_code, expected_message):
        self.expected_status_code = expected_status_code
        self.expected_message = expected_message

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == requests.exceptions.HTTPError:
            assert exc_val.response.status_code == self.expected_status_code
            assert exc_val.response.json()["title"] == self.expected_message
        return True
