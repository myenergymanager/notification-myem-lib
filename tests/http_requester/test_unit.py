from unittest.mock import Mock

import pytest
from requests import Response
from notification_lib import http_requests
from notification_lib.exceptions import NotificationException
from notification_lib.http_requests import HttpRequester


class TestHttpRequester:
    HttpRequester.api_key = "api_key"
    HttpRequester.api_url = "http://api_url"
    HttpRequester.admin_email = "myem+dev@myem.fr"
    HttpRequester.admin_password = "admin1234"

    @pytest.fixture
    def mock_requests(self, monkeypatch):
        monkeypatch.setattr(HttpRequester, "get_jwt_bearer_token", lambda: "")
        monkeypatch.setattr(http_requests, "requests", Mock())

    def test_send_get_request(self, mock_requests):
        HttpRequester.send_request(operation="GET", endpoint="/endpoint")
        assert http_requests.requests.get.call_count == 1
        assert http_requests.requests.get.call_args[0][0] == "http://api_url/endpoint"
        # assert http_requests.requests.get.call_args[1] == {
        #     "headers": {"Authorization": f"ApiKey {HttpRequester.api_key}"}
        # }
        # TODO:  to replace one we migrate to api key
        assert http_requests.requests.get.call_args[1] == {"headers": {"Authorization": "Bearer "}}

    def test_send_post_request(self, mock_requests):
        HttpRequester.send_request(operation="POST", endpoint="/endpoint", body={"hello": "world"})
        assert http_requests.requests.post.call_count == 1
        assert http_requests.requests.post.call_args[0][0] == "http://api_url/endpoint"
        # assert http_requests.requests.post.call_args[1] == {
        #     "data": '{"hello": "world"}',
        #     "headers": {"Authorization": "ApiKey api_key", "Content-Type": "application/json"},
        # }
        # TODO:  to replace one we migrate to api key
        assert http_requests.requests.post.call_args[1] == {
            "data": '{"hello": "world"}',
            "headers": {"Authorization": "Bearer ", "Content-Type": "application/json"},
        }

    def test_handle_200_response(self):
        http_response = Response()
        http_response.status_code = 200
        response = HttpRequester.handle_response(http_response, "exception message")
        assert response.status_code == 200

    def test_handle_500_response(self):
        http_response = Response()
        http_response.status_code = 500
        http_response._content = b'{"message": "error !"}'  # pylint: disable=W0212
        with pytest.raises(NotificationException):
            HttpRequester.handle_response(http_response, "exception message")
