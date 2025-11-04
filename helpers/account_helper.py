import json
import time

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

    @get_token_retryer
    def _get_activation_token_by_login(self, login):
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        token = None
        for item in response.json()["items"]:
            user_data = json.loads(item["Content"]["Body"])
            user_login = user_data["Login"]
            if user_login == login:
                token = user_data["ConfirmationLinkUrl"].split("/")[-1]
                break
        return token

    @get_token_retryer
    def _get_activation_token_by_email(self, email):
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        token = None
        for item in response.json()["items"]:
            if item["Content"]["Headers"]["To"][0] == email:
                token = json.loads(item["Content"]["Body"])[
                    "ConfirmationLinkUrl"
                ].split("/")[-1]
                break
        return token

    def register_and_activate_user(self, login, email, password):
        json_data = {
            "login": login,
            "email": email,
            "password": password,
        }

        response = self.account.account_api.post_v1_account(json_data)
        assert response.status_code == 201, "Не удалось зарегистрировать пользователя"
        self.activate_token_by_login(login)

    def activate_token_by_login(self, login):
        token = self._get_activation_token_by_login(login)
        assert token is not None, "Не удалось получить токен"

        response = self.account.account_api.put_v1_account_token(token)
        assert response.status_code == 200, "Не удалось активировать токен"

    def activate_token_by_email(self, email):
        token = self._get_activation_token_by_email(email)
        assert token is not None, "Не удалось получить токен"

        response = self.account.account_api.put_v1_account_token(token)
        assert response.status_code == 200, "Не удалось активировать токен"

    def login_user(self, login, password, remember_me=True):
        json_data = {
            "login": login,
            "password": password,
            "rememberMe": remember_me,
        }

        response = self.account.login_api.post_v1_account_login(json_data)
        return response

    def change_user_email(self, login, password, new_email):
        json_data = {
            "login": login,
            "password": password,
            "email": new_email,
        }

        response = self.account.account_api.put_v1_account_email(json_data)
        assert response.status_code == 200, "Не удалось поменять email пользователя"
