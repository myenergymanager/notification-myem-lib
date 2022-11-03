"""Http requests file."""
import json
import logging
from typing import Any, Dict, Optional

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
        body: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """Send a request based on the operation and params."""
        params: Dict[str, Any] = {"headers": {"Authorization": f"ApiKey {cls.api_key}"}}
        if body:
            params.update({"data": json.dumps(body)})
        if operation in ["POST", "PATCH", "PUT"]:
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
