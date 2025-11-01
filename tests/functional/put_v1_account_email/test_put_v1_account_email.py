import datetime

import structlog

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration
from services.api_mailhog_service import ApiMailhogService
from services.dm_api_account_service import DmApiAccountService

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=False)
    ]
)


def test_put_v1_account_email():
    account = DmApiAccountService(
        configuration=Configuration("http://5.63.153.31:5051")
    )
    mailhog = ApiMailhogService(
        configuration=Configuration("http://5.63.153.31:5025", disable_log=True)
    )

    api_helper = AccountHelper(account, mailhog)

    timestamp = str(datetime.datetime.now().timestamp())[:-4]
    login = f"iponomarev_{timestamp}"
    email = f"{login}@mail.ru"
    new_email = f"{login}_new@mail.ru"
    password = "qwerty"

    # Регистрация и активация пользователя
    api_helper.register_and_activate_user(login, email, password)

    # Авторизация пользователя
    assert (
        api_helper.login_user(login, password).status_code == 200
    ), "Не удалось залогиниться пользователю"

    # Смена email
    api_helper.change_user_email(login, password, new_email)

    # Попытка авторизоваться
    assert (
        api_helper.login_user(login, password).status_code == 403
    ), "Пользователь не должен был залогиниться"

    # Активация токена по email
    api_helper.activate_token_by_email(new_email)

    # Авторизация пользователя
    assert (
        api_helper.login_user(login, password).status_code == 200
    ), "Не удалось залогиниться пользователю"
