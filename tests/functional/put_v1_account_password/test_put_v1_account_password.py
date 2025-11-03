def test_put_v1_account_password(auth_account_helper_and_auth_user):
    auth_account_helper = auth_account_helper_and_auth_user[0]
    auth_user = auth_account_helper_and_auth_user[1]
    login = auth_user.login
    email = auth_user.email
    password = auth_user.password
    new_password = auth_user.new_password

    # Меняем пароль пользователю
    auth_account_helper.change_password(login, email, password, new_password)
