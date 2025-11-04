def test_delete_v1_account_login(auth_account_helper_and_auth_user):
    auth_account_helper = auth_account_helper_and_auth_user[0]

    # Выходим из аккаунта
    auth_account_helper.logout_user()
