def test_post_v1_account(account_helper, user):
    login = user.login
    email = user.email
    password = user.password

    # Регистрация и активация пользователя
    account_helper.register_and_activate_user(login, email, password)
