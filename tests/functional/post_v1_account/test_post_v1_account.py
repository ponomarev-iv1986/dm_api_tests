import datetime

import structlog

from dm_api_account.apis.account_api import AccountApi
from restclient.configuration import Configuration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=False)
    ]
)


def test_post_v1_account():
    account_api = AccountApi(configuration=Configuration("http://5.63.153.31:5051"))

    timestamp = str(datetime.datetime.now().timestamp())[:-4]
    login = f"iponomarev_{timestamp}"
    email = f"{login}@mail.ru"
    password = "qwerty"

    # Регистрация пользователя
    json_data = {
        "login": login,
        "email": email,
        "password": password,
    }

    response = account_api.post_v1_account(json_data)
    assert response.status_code == 201
