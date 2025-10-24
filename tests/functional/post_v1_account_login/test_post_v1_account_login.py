from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from utils import utils


def test_post_v1_account_login():
    account_api = AccountApi("http://5.63.153.31:5051")
    login_api = LoginApi("http://5.63.153.31:5051")
    mailhog_api = MailhogApi("http://5.63.153.31:5025")

    login = "iponomarev_27"
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

    # Получение активационного токена
    token = utils.get_activation_token_by_login(login, response)
    assert token is not None

    # Активация пользователя
    response = account_api.put_v1_account_token(token)
    assert response.status_code == 200

    # Авторизация пользователя
    json_data = {
        "login": login,
        "password": password,
        "rememberMe": True,
    }

    response = login_api.post_v1_account_login(json_data)
    assert response.status_code == 200
