import pytest

from checkers.http_checkers import check_status_code_http


def test_post_v1_account(account_helper, user):
    login = user.login
    email = user.email
    password = user.password

    # Регистрация и активация пользователя
    account_helper.register_and_activate_user(login, email, password)


@pytest.mark.parametrize(
    "login, email, password, status_code, err_msg",
    [
        ("i", "iponomarev_50@mail.ru", "qwerty", 400, "Validation failed"),
        ("iponomarev_50", "iponomarev_50", "qwerty", 400, "Validation failed"),
        ("iponomarev_50", "iponomarev_50@mail.ru", "qwe", 400, "Validation failed"),
    ],
)
def test_post_v1_account_negative(
    account_helper,
    login,
    email,
    password,
    status_code,
    err_msg,
):
    with check_status_code_http(status_code, err_msg):
        account_helper.register_and_activate_user(login, email, password)
