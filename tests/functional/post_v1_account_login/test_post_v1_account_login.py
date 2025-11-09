def test_post_v1_account_login(account_helper, user):
    login = user.login
    email = user.email
    password = user.password

    # Регистрация и активация пользователя
    account_helper.register_and_activate_user(login, email, password)

    # Авторизация пользователя
    account_helper.login_user(login, password)
