import json


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()["items"]:
        user_data = json.loads(item["Content"]["Body"])
        user_login = user_data["Login"]
        if user_login == login:
            token = user_data.get("ConfirmationLinkUrl").split("/")[-1]
            break
    return token


def get_activation_token_by_email(email, response):
    token = None
    for item in response.json()["items"]:
        if item["Content"]["Headers"]["To"][0] == email:
            token = (
                json.loads(item["Content"]["Body"])
                .get("ConfirmationLinkUrl")
                .split("/")[-1]
            )
            break
    return token
