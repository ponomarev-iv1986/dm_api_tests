def test_put_v1_account_token(account_helper, user):
    login = user.login
    email = user.email
    password = user.password

    # Регистрация и активация пользователя
    account_helper.register_and_activate_user(login, email, password)
