import allure
from allure_commons.types import Severity


@allure.parent_suite("DM.API Account Tests")
@allure.suite("Проверка метода PUT /v1/account/password")
class TestPutV1AccountPassword:

    @allure.title("Проверка смены пароля пользователя")
    @allure.sub_suite("Позитивные тесты")
    @allure.severity(Severity.NORMAL)
    @allure.tag("API", "REGRESS")
    def test_put_v1_account_password(self, auth_account_helper):
        auth_user = auth_account_helper.get_auth_user()
        login = auth_user.login
        email = auth_user.email
        password = auth_user.password
        new_password = auth_user.new_password

        # Меняем пароль пользователю
        auth_account_helper.change_password(login, email, password, new_password)

        # Логинимся с новым паролем
        auth_account_helper.login_user(login, new_password)
