def test_put_v1_account_password(auth_account_helper):
    auth_user = auth_account_helper.get_auth_user()
    login = auth_user.login
    email = auth_user.email
    password = auth_user.password
    new_password = auth_user.new_password

    # Меняем пароль пользователю
    auth_account_helper.change_password(login, email, password, new_password)

    # Логинимся с новым паролем
    assert (
        auth_account_helper.login_user(login, new_password).status_code == 200
    ), "Не удалось залогиниться пользователю"
