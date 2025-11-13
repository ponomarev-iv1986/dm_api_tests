import allure
import pytest
from allure_commons.types import Severity

from checkers.http_checkers import check_status_code_http


@allure.parent_suite("DM.API Account Tests")
@allure.suite("Проверка метода POST /v1/account")
class TestPostV1Account:

    @allure.title("Проверка регистрации нового пользователя")
    @allure.sub_suite("Позитивные тесты")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("API", "REGRESS")
    def test_post_v1_account(self, account_helper, user):
        login = user.login
        email = user.email
        password = user.password

        # Регистрация и активация пользователя
        account_helper.register_and_activate_user(login, email, password)

    @allure.title(
        "Проверка невозможности регистрации нового пользователя при неправильных данных"
    )
    @allure.sub_suite("Негативные тесты")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("API", "REGRESS")
    @pytest.mark.parametrize(
        "login, email, password, status_code, err_msg",
        [
            ("i", "iponomarev_50@mail.ru", "qwerty", 400, "Validation failed"),
            ("iponomarev_50", "iponomarev_50", "qwerty", 400, "Validation failed"),
            ("iponomarev_50", "iponomarev_50@mail.ru", "qwe", 400, "Validation failed"),
        ],
    )
    def test_post_v1_account_negative(
        self,
        account_helper,
        login,
        email,
        password,
        status_code,
        err_msg,
    ):
        with check_status_code_http(status_code, err_msg):
            account_helper.register_and_activate_user(login, email, password)
