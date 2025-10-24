from dm_api_account.apis.account_api import AccountApi


def test_post_v1_account():
    account_api = AccountApi("http://5.63.153.31:5051")

    login = "iponomarev_24"
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
