"""
Повторить действия из уроков:
1. Сгенерировать код функций и объединить в класс клиент, для каждого метода написать документационную строку.
2. Реализовать такой же сценарий для метода post_v1_account
3. Реализовать сценарий для метода put_v1_account_token
4. Реализовать сценарий для метода post_v1_account_login
5. Реализовать сценарий для метода put_v1_account_email
     - Регистрируемся
     - Получаем активационный токен
     - Активируем
     - Заходим
     - Меняем емейл
     - Пытаемся войти, получаем 403
     - На почте находим токен по новому емейлу для подтверждения смены емейла
     - .Активируем этот токен
     -  Логинимся
6. Добавить в репозиторий Github Action джоб для запуска автотестов
"""

import json

from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi


def test_post_v1_account():
    account_api = AccountApi("http://5.63.153.31:5051")
    login_api = LoginApi("http://5.63.153.31:5051")
    mailhog_api = MailhogApi("http://5.63.153.31:5025")

    login = "iponomarev_16"
    email = f"{login}@mail.ru"
    new_email = f"{login}_new@mail.ru"
    password = "qwerty"

    # Регистрация пользователя

    json_data = {
        "login": login,
        "email": email,
        "password": password,
    }

    response = account_api.post_v1_account(json_data)
    assert response.status_code == 201

    # Получить письма из почтового сервера

    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200

    # Получить активационный токен

    token = get_activation_token_by_login(login, response)
    assert token is not None

    # Активация пользователя

    response = account_api.put_v1_account_token(token)
    assert response.status_code == 200

    # Авторизуемся

    json_data = {
        "login": login,
        "password": password,
        "rememberMe": True,
    }

    response = login_api.post_v1_account_login(json_data)
    assert response.status_code == 200

    # Меняем email

    json_data = {
        "login": login,
        "password": password,
        "email": new_email,
    }

    response = account_api.put_v1_account_email(json_data)
    assert response.status_code == 200

    # Пробуем авторизоваться

    json_data = {
        "login": login,
        "password": password,
        "rememberMe": True,
    }

    response = login_api.post_v1_account_login(json_data)
    assert response.status_code == 403

    # Получить письма из почтового сервера

    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200

    # Получаем токен по email

    token = get_activation_token_by_email(new_email, response)
    assert token is not None

    # Активация пользователя

    response = account_api.put_v1_account_token(token)
    assert response.status_code == 200

    # Авторизуемся

    response = login_api.post_v1_account_login(json_data)
    assert response.status_code == 200


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()["items"]:
        user_data = json.loads(item["Content"]["Body"])
        user_login = user_data["Login"]
        if user_login == login:
            token = user_data.get("ConfirmationLinkUrl").split("/")[-1]
            break
    return token


def get_activation_token_by_email(email, response):
    token = None
    for item in response.json()["items"]:
        if item["Content"]["Headers"]["To"][0] == email:
            token = (
                json.loads(item["Content"]["Body"])
                .get("ConfirmationLinkUrl")
                .split("/")[-1]
            )
            break
    return token
