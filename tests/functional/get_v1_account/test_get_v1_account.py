def test_get_v1_account(auth_account_helper_and_auth_user):
    auth_account_helper = auth_account_helper_and_auth_user[0]

    # Получаем информацию о пользователе
    auth_account_helper.get_current_user()
