import datetime
from collections import namedtuple

import pytest
import structlog

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration
from services.api_mailhog_service import ApiMailhogService
from services.dm_api_account_service import DmApiAccountService


@pytest.fixture(scope="session", autouse=True)
def config_logger():
    structlog.configure(
        processors=[
            structlog.processors.JSONRenderer(
                indent=4, ensure_ascii=True, sort_keys=False
            )
        ]
    )


@pytest.fixture(scope="session")
def account_service():
    account = DmApiAccountService(
        configuration=Configuration("http://5.63.153.31:5051")
    )
    return account


@pytest.fixture(scope="session")
def mailhog_service():
    mailhog = ApiMailhogService(
        configuration=Configuration("http://5.63.153.31:5025", disable_log=True)
    )
    return mailhog


@pytest.fixture(scope="session")
def account_helper(account_service, mailhog_service):
    return AccountHelper(account_service, mailhog_service)


@pytest.fixture
def auth_account_helper(user, mailhog_service):
    account_service = DmApiAccountService(
        configuration=Configuration("http://5.63.153.31:5051")
    )
    account_helper = AccountHelper(account_service, mailhog_service)
    account_helper.register_and_activate_user(
        user.login,
        user.email,
        user.password,
    )
    account_helper.auth_client(user)
    return account_helper


@pytest.fixture
def user():
    timestamp = str(datetime.datetime.now().timestamp())[:-4]
    login = f"iponomarev_{timestamp}"
    email = f"{login}@mail.ru"
    new_email = f"{login}_new@mail.ru"
    password = "qwerty"
    new_password = "new_qwerty"
    User = namedtuple(
        "User",
        [
            "login",
            "email",
            "new_email",
            "password",
            "new_password",
        ],
    )
    return User(login, email, new_email, password, new_password)
