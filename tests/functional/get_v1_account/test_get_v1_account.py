import allure
from allure_commons.types import Severity

from checkers.get_v1_account import GetV1Account


@allure.parent_suite("DM.API Account Tests")
@allure.suite("Проверка метода GET /v1/account")
class TestGetV1Account:

    @allure.title("Проверка получения профиля пользователя")
    @allure.sub_suite("Позитивные тесты")
    @allure.severity(Severity.NORMAL)
    @allure.tag("API", "REGRESS")
    def test_get_v1_account(self, auth_account_helper):

        # Получаем информацию о пользователе
        response = auth_account_helper.get_current_user()

        # Проверяем поля тела ответа
        GetV1Account.check_response_values(response, "iponomarev")
