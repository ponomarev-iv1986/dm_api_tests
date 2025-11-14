import allure
from allure_commons.types import Severity

from checkers.http_checkers import check_status_code_http


@allure.parent_suite("DM.API Account Tests")
@allure.suite("Проверка метода PUT /v1/account/email")
class TestPutV1AccountEmail:

    @allure.title("Проверка смены email пользователя")
    @allure.sub_suite("Позитивные тесты")
    @allure.severity(Severity.NORMAL)
    @allure.tag("API", "REGRESS")
    def test_put_v1_account_email(self, account_helper, user):
        login = user.login
        email = user.email
        new_email = user.new_email
        password = user.password

        # Регистрация и активация пользователя
        account_helper.register_and_activate_user(login, email, password)

        # Авторизация пользователя
        account_helper.login_user(login, password)

        # Смена email
        account_helper.change_user_email(login, password, new_email)

        # Попытка авторизоваться
        with check_status_code_http(
            expected_status_code=403,
            expected_message="User is inactive. Address the technical support for more details",
        ):
            account_helper.login_user(login, password, enable_validation=False)

        # Активация токена по email
        account_helper.activate_token_by_login(login)

        # Авторизация пользователя
        account_helper.login_user(login, password)
