import allure
from allure_commons.types import Severity


@allure.parent_suite("DM.API Account Tests")
@allure.suite("Проверка метода DELETE /v1/account/login/all")
class TestDeleteV1AccountLoginAll:

    @allure.title("Проверка выхода пользователя со всех устройств")
    @allure.sub_suite("Позитивные тесты")
    @allure.severity(Severity.NORMAL)
    @allure.tag("API", "REGRESS")
    def test_delete_v1_account_all(self, auth_account_helper):

        # Выходим из аккаунта на всех устройствах
        auth_account_helper.logout_user_from_every_device()
