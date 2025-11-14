import allure
from allure_commons.types import Severity


@allure.parent_suite("DM.API Account Tests")
@allure.suite("Проверка метода DELETE /v1/account/login")
class TestDeleteV1AccountLogin:

    @allure.title("Проверка выхода пользователя")
    @allure.sub_suite("Позитивные тесты")
    @allure.severity(Severity.NORMAL)
    @allure.tag("API", "REGRESS")
    def test_delete_v1_account_login(self, auth_account_helper):

        # Выходим из аккаунта
        auth_account_helper.logout_user()
