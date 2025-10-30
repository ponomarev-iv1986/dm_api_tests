import datetime

import structlog

from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account.apis.account_api import AccountApi
from restclient.configuration import Configuration
from utils import utils

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=False)
    ]
)


def test_put_v1_account_token():
    account_api = AccountApi(configuration=Configuration("http://5.63.153.31:5051"))
    mailhog_api = MailhogApi(
        configuration=Configuration("http://5.63.153.31:5025", disable_log=True)
    )

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

    # Получение писем из почтового ящика
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200

    # Получение активационного токена по login
    token = utils.get_activation_token_by_login(login, response)
    assert token is not None

    # Активация пользователя
    response = account_api.put_v1_account_token(token)
    assert response.status_code == 200
