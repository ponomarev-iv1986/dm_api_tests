import json
import time

import allure

from dm_api_account.models.requests.change_email import ChangeEmail
from dm_api_account.models.requests.change_password import ChangePassword
from dm_api_account.models.requests.login_credentials import LoginCredentials
from dm_api_account.models.requests.registration import Registration
from dm_api_account.models.requests.reset_password import ResetPassword
from services.api_mailhog_service import ApiMailhogService
from services.dm_api_account_service import DmApiAccountService


def get_token_retryer(f=None, *, timeout=5):
    def decorator(func):
        def wrapper(*args, **kwargs):
            now = time.monotonic()
            while True:
                result = func(*args, **kwargs)
                if result:
                    return result
                elif time.monotonic() - now < timeout:
                    print("\033[31mНеудачная попытка получения токена\033[0m")
                    time.sleep(1)
                    continue
                else:
                    print("\033[31mПолучить токен не удалось\033[0m")
                    return result

        return wrapper

    if f is None:
        return decorator
    else:
        return decorator(f)


class AccountHelper:
    def __init__(self, account: DmApiAccountService, mailhog: ApiMailhogService):
        self.account = account
        self.mailhog = mailhog
        self._auth_user = None

    @get_token_retryer
    def _get_activation_token_by_login(
        self,
        login,
        change_password=False,
    ):
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        token = None
        key = "ConfirmationLinkUri" if change_password else "ConfirmationLinkUrl"
        for item in response.json()["items"]:
            user_data = json.loads(item["Content"]["Body"])
            user_login = user_data["Login"]
            if user_login == login:
                token = user_data[key].split("/")[-1]
                break
        return token

    def get_auth_user(self):
        return self._auth_user

    def auth_client(self, user):
        response = self.login_user(user.login, user.password, enable_validation=False)

        token = {"X-Dm-Auth-Token": response.headers["X-Dm-Auth-Token"]}
        self.account.account_api.update_headers(token)
        self.account.login_api.update_headers(token)
        self._auth_user = user

    @allure.step("Регистрация и активация нового пользователя")
    def register_and_activate_user(self, login, email, password):
        registration = Registration(
            login=login,
            email=email,
            password=password,
        )

        self.account.account_api.post_v1_account(registration=registration)
        self.activate_token_by_login(login)

    @allure.step("Активация токена")
    def activate_token_by_login(self, login):
        token = self._get_activation_token_by_login(login)
        assert token is not None, "Не удалось получить токен"

        self.account.account_api.put_v1_account_token(token)

    @allure.step("Аутентификация пользователя")
    def login_user(self, login, password, remember_me=True, enable_validation=True):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me,
        )

        response = self.account.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            enable_validation=enable_validation,
        )
        return response

    @allure.step("Смена email пользователя")
    def change_user_email(self, login, password, new_email):
        change_email = ChangeEmail(
            login=login,
            password=password,
            email=new_email,
        )

        self.account.account_api.put_v1_account_email(change_email=change_email)

    @allure.step("Получение информации о текущем пользователе")
    def get_current_user(self, enable_validation=True):
        response = self.account.account_api.get_v1_account(
            enable_validation=enable_validation
        )
        return response

    @allure.step("Смена пароля пользователя")
    def change_password(self, login, email, password, new_password):
        reset_password = ResetPassword(
            login=login,
            email=email,
        )

        self.account.account_api.post_v1_account_password(reset_password=reset_password)

        token = self._get_activation_token_by_login(login, change_password=True)
        assert token is not None, "Не удалось получить токен"

        change_password = ChangePassword(
            login=login,
            token=token,
            old_password=password,
            new_password=new_password,
        )

        self.account.account_api.put_v1_account_password(
            change_password=change_password
        )

    @allure.step("Выход пользователя")
    def logout_user(self):
        self.account.login_api.delete_v1_account_login()

    @allure.step("Выход пользователя со всех устройств")
    def logout_user_from_every_device(self):
        self.account.login_api.delete_v1_account_login_all()
