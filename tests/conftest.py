import datetime
from collections import namedtuple
from pathlib import Path

import pytest
import structlog
from vyper import v

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration
from services.api_mailhog_service import ApiMailhogService
from services.dm_api_account_service import DmApiAccountService

options = (
    "service.dm_api_account",
    "service.mailhog",
    "user.login",
    "user.password",
)


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="prod", help="environment")
    for option in options:
        parser.addoption(f"--{option}", action="store", default=None)


@pytest.fixture(scope="session", autouse=True)
def set_config(request):
    config = Path(__file__).resolve().parents[1] / "config"
    config_name = request.config.getoption("--env")
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(option, request.config.getoption(f"--{option}"))


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
        configuration=Configuration(host=v.get("service.dm_api_account"))
    )
    return account


@pytest.fixture(scope="session")
def mailhog_service():
    mailhog = ApiMailhogService(
        configuration=Configuration(host=v.get("service.mailhog"), disable_log=True)
    )
    return mailhog


@pytest.fixture(scope="session")
def account_helper(account_service, mailhog_service):
    return AccountHelper(account_service, mailhog_service)


@pytest.fixture
def auth_account_helper(user, mailhog_service):
    account_service = DmApiAccountService(
        configuration=Configuration(host=v.get("service.dm_api_account"))
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
    login = f"{l}_{timestamp}"
    email = f"{login}@mail.ru"
    new_email = f"{login}_new@mail.ru"
    password = p
    new_password = f"new_{p}"
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
