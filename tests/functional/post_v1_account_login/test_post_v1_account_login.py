import allure
from allure_commons.types import Severity


@allure.parent_suite("DM.API Account Tests")
@allure.suite("Проверка метода POST /v1/account/login")
class TestPostV1AccountLogin:

    @allure.title("Проверка аутентификации пользователя")
    @allure.sub_suite("Позитивные тесты")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("API", "REGRESS")
    def test_post_v1_account_login(self, account_helper, user):
        login = user.login
        email = user.email
        password = user.password

        # Регистрация и активация пользователя
        account_helper.register_and_activate_user(login, email, password)

        # Аутентификация пользователя
        account_helper.login_user(login, password)
