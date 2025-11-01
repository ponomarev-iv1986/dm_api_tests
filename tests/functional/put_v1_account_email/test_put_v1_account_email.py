def test_put_v1_account_email(account_helper, user):
    login = user.login
    email = user.email
    new_email = user.new_email
    password = user.password

    # Регистрация и активация пользователя
    account_helper.register_and_activate_user(login, email, password)

    # Авторизация пользователя
    assert (
        account_helper.login_user(login, password).status_code == 200
    ), "Не удалось залогиниться пользователю"

    # Смена email
    account_helper.change_user_email(login, password, new_email)

    # Попытка авторизоваться
    assert (
        account_helper.login_user(login, password).status_code == 403
    ), "Пользователь не должен был залогиниться"

    # Активация токена по email
    account_helper.activate_token_by_email(new_email)

    # Авторизация пользователя
    assert (
        account_helper.login_user(login, password).status_code == 200
    ), "Не удалось залогиниться пользователю"
