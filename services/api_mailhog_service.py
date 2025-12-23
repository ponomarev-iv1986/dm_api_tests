from clients.http.api_mailhog.apis.mailhog_api import MailhogApi
from clients.http.configuration import Configuration


class ApiMailhogService:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.mailhog_api = MailhogApi(configuration=self.configuration)
