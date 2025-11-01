import json
import time

from services.api_mailhog_service import ApiMailhogService
from services.dm_api_account_service import DmApiAccountService


def retryer(f=None, *, timeout=5):
    def decorator(func):
        def wrapper(*args, **kwargs):
            now = time.monotonic()
            while True:
                try:
                    func(*args, **kwargs)
                    break
                except AssertionError:
                    print(
                        f"\033[31mНеудачная попытка выполнения функции "
                        f"{func.__name__}\033[0m"
                    )
                    if time.monotonic() - now < timeout:
                        time.sleep(1)
                        continue
                    raise

        return wrapper

    if f is None:
        return decorator
    else:
        return decorator(f)


class AccountHelper:
    def __init__(self, account: DmApiAccountService, mailhog: ApiMailhogService):
        self.account = account
        self.mailhog = mailhog

    @staticmethod
    def _get_activation_token_by_login(login, response):
        token = None
        for item in response.json()["items"]:
            user_data = json.loads(item["Content"]["Body"])
            user_login = user_data["Login"]
            if user_login == login:
                token = user_data["ConfirmationLinkUrl"].split("/")[-1]
                break
        return token

    @staticmethod
    def _get_activation_token_by_email(email, response):
        token = None
        for item in response.json()["items"]:
            if item["Content"]["Headers"]["To"][0] == email:
                token = json.loads(item["Content"]["Body"])[
                    "ConfirmationLinkUrl"
                ].split("/")[-1]
                break
        return token

    def _get_emails(self):
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        return response

    @retryer
    def register_and_activate_user(self, login, email, password):
        json_data = {
            "login": login,
            "email": email,
            "password": password,
        }

        response = self.account.account_api.post_v1_account(json_data)
        assert response.status_code == 200, "Не удалось зарегистрировать пользователя"
        self.activate_token_by_login(login)

    @retryer
    def activate_token_by_login(self, login):
        response = self._get_emails()
        assert (
            response.status_code == 200
        ), "Не удалось получить письма из почтового ящика"

        token = self._get_activation_token_by_login(login, response)
        assert token is not None, "Не удалось получить токен"

        response = self.account.account_api.put_v1_account_token(token)
        assert response.status_code == 200, "Не удалось активировать токен"

    @retryer
    def activate_token_by_email(self, email):
        response = self._get_emails()
        assert (
            response.status_code == 200
        ), "Не удалось получить письма из почтового ящика"

        token = self._get_activation_token_by_email(email, response)
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

    @retryer
    def change_user_email(self, login, password, new_email):
        json_data = {
            "login": login,
            "password": password,
            "email": new_email,
        }

        response = self.account.account_api.put_v1_account_email(json_data)
        assert response.status_code == 200, "Не удалось поменять email пользователя"
