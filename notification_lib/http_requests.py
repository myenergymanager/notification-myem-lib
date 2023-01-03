"""Http requests file."""
import json
import logging
import os
from typing import Any

import requests
from typing_extensions import Literal
from notification_lib.exceptions import NotificationException


class HttpRequester:
    """Http requester class helps to send requests using the module requests and handle response."""

    api_url: str
    api_key: str

    @classmethod
    def send_request(
        cls,
        operation: Literal["POST", "GET", "DELETE", "PATCH", "PUT"],
        endpoint: str,
        body: dict[str, Any] | None = None,
    ) -> requests.Response:
        """Send a request based on the operation and params."""
        # TODO : to remove the bearer token once the bug is resolved in the novu platform
        #  and replace it with the api key {"Authorization": f"ApiKey {cls.api_key}}"}
        params: dict[str, Any] = {
            "headers": {"Authorization": f"Bearer {cls.get_jwt_bearer_token()}"}
        }
        if body:
            params.update({"data": json.dumps(body)})
        if operation in {"POST", "PATCH", "PUT"}:
            params["headers"].update({"Content-Type": "application/json"})
        return getattr(requests, operation.lower())(f"{cls.api_url}{endpoint}", **params)

    @classmethod
    def handle_response(cls, response: requests.Response, exception_msg: str) -> requests.Response:
        """Return the response if the status code belongs to 2xx otherwise raise an exception."""
        if response.status_code // 100 == 2:
            return response
        logging.error(f"status code: {response.status_code}")
        logging.error(f"response : {response.json()}")
        raise NotificationException(exception_msg)

    @classmethod
    def get_jwt_bearer_token(cls) -> str:
        """Get jwt bearer token."""
        # TODO : to remove this function once the bug is resolved in the novu plateforme
        login_response = requests.post(
            f"{cls.api_url}/v1/auth/login",
            headers={"Content-Type": "application/json"},
            data=json.dumps(
                {
                    "email": os.environ["NOVU_ADMIN_EMAIL"],
                    "password": os.environ["NOVU_ADMIN_PASSWORD"],
                }
            ),
            timeout=10,
        )
        return login_response.json()["data"]["token"]
