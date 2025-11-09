from checkers.get_v1_account import GetV1Account


def test_get_v1_account(auth_account_helper):

    # Получаем информацию о пользователе
    response = auth_account_helper.get_current_user()

    # Проверяем поля тела ответа
    GetV1Account.check_response_values(response)
