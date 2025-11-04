from dm_api_account.models.requests.login_credentials import LoginCredentials
from restclient.client import RestClient


class LoginApi(RestClient):

    def post_v1_account_login(self, login_credentials: LoginCredentials):
        """
        Authenticate via credentials.

        :param login_credentials:
        :return:
        """
        response = self.post(
            path="/v1/account/login",
            json=login_credentials.model_dump(exclude_none=True, by_alias=True),
        )
        return response

    def delete_v1_account_login(self):
        """
        Logout as current user

        :return:
        """
        response = self.delete(path="/v1/account/login", headers=self.headers)
        return response

    def delete_v1_account_login_all(self):
        """
        Logout from every device

        :return:
        """
        response = self.delete(path="/v1/account/login/all", headers=self.headers)
        return response
