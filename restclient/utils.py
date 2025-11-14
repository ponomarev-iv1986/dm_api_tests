import json

import allure
import curlify
from requests import JSONDecodeError


def allure_attach(func):
    def wrapper(*args, **kwargs):
        body = kwargs.get("json")
        if body:
            allure.attach(
                json.dumps(body, indent=4),
                name="request_body",
                attachment_type=allure.attachment_type.JSON,
            )
        response = func(*args, **kwargs)
        curl = curlify.to_curl(response.request)
        allure.attach(curl, name="curl", attachment_type=allure.attachment_type.TEXT)
        allure.attach(
            str(response.status_code),
            name="status code",
            attachment_type=allure.attachment_type.TEXT,
        )
        try:
            response_json = response.json()
            allure.attach(
                json.dumps(response_json, indent=4),
                name="response body",
                attachment_type=allure.attachment_type.JSON,
            )
        except JSONDecodeError:
            response_text = response.text
            allure.attach(
                response_text,
                name="response text",
                attachment_type=allure.attachment_type.TEXT,
            )
        return response

    return wrapper
