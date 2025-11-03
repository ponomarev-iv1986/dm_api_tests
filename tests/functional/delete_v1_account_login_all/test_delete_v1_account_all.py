def test_delete_v1_account_all(auth_account_helper_and_auth_user):
    auth_account_helper = auth_account_helper_and_auth_user[0]

    # Выходим из аккаунта на всех устройствах
    auth_account_helper.logout_user_from_every_device()
