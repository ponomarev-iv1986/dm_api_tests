from dm_api_account.models.requests.change_email import ChangeEmail
from dm_api_account.models.requests.change_password import ChangePassword
from dm_api_account.models.requests.registration import Registration
from dm_api_account.models.requests.reset_password import ResetPassword
from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(self, registration: Registration):
        """
        Register new user.

        :param registration:
        :return:
        """
        response = self.post(
            path="/v1/account",
            json=registration.model_dump(exclude_none=True, by_alias=True),
        )
        return response

    def get_v1_account(self):
        """
        Get current user.

        :return:
        """
        response = self.get(path="/v1/account", headers=self.headers)
        return response

    def put_v1_account_token(self, token):
        """
        Activate registered user.

        :param token:
        :return:
        """
        response = self.put(path=f"/v1/account/{token}")
        return response

    def post_v1_account_password(self, reset_password: ResetPassword):
        """
        Reset registered user password

        :param reset_password:
        :return:
        """
        response = self.post(
            path="/v1/account/password",
            headers=self.headers,
            json=reset_password.model_dump(exclude_none=True, by_alias=True),
        )
        return response

    def put_v1_account_password(self, change_password: ChangePassword):
        """
        Change registered user password

        :param change_password:
        :return:
        """
        response = self.put(
            path="/v1/account/password",
            headers=self.headers,
            json=change_password.model_dump(exclude_none=True, by_alias=True),
        )
        return response

    def put_v1_account_email(self, change_email: ChangeEmail):
        """
        Change registered user email.

        :param change_email:
        :return:
        """
        response = self.put(
            path="/v1/account/email",
            json=change_email.model_dump(exclude_none=True, by_alias=True),
        )
        return response
