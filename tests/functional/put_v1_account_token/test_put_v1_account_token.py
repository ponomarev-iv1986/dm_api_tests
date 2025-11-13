import allure
from allure_commons.types import Severity


@allure.parent_suite("DM.API Account Tests")
@allure.suite("Проверка метода PUT /v1/account/token")
class TestPutV1AccountToken:

    @allure.title("Проверка активации токена")
    @allure.sub_suite("Позитивные тесты")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("API", "REGRESS")
    def test_put_v1_account_token(self, account_helper, user):
        login = user.login
        email = user.email
        password = user.password

        # Регистрация и активация пользователя
        account_helper.register_and_activate_user(login, email, password)
