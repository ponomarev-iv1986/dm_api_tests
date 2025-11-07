def test_delete_v1_account_all(auth_account_helper):

    # Выходим из аккаунта на всех устройствах
    auth_account_helper.logout_user_from_every_device()
