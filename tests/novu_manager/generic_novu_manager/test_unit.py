"""Test Novu utils functions."""
from unittest.mock import Mock

import pytest
from notification_lib.exceptions import NotificationException
from notification_lib.novu_manager.generic_novu_manager import GenericNovuManager, requests


@pytest.fixture
def mock_request_call(monkeypatch):
    def mock_call(operation, response_body, status_code):
        mock_operation = Mock()
        mock_operation.return_value.status_code = status_code
        mock_operation.return_value.json.return_value = response_body
        monkeypatch.setattr(requests, operation, mock_operation)

    yield mock_call


templates = [
    {
        "id": "template_id",
        "name": "template_name",
        "steps": [
            {
                "template": {},
                "filters": [
                    {
                        "isNegated": True,
                        "type": "BOOLEAN",
                        "value": "AND",
                        "children": [
                            {
                                "field": "string",
                                "value": "string",
                                "operator": "LARGER",
                                "on": "payload",
                            }
                        ],
                    }
                ],
                "active": True,
            }
        ],
    }
]


class TestGenericNovuManager:
    def test_get_novu_jwt_bearer_token(self, novu, mock_request_call):
        token = "ifdllxwco xcsdflkxcvoxwvnkqofsdsd"
        mock_request_call(
            response_body={
                "data": {
                    "token": token,
                }
            },
            status_code=200,
            operation="post",
        )
        response = novu.generic_novu_manager.get_novu_jwt_bearer_token()

        assert requests.post.call_count == 1
        assert response == token

    def test_get_novu_jwt_bearer_token_error(self, novu, mock_request_call):
        mock_request_call(
            response_body={"data": "toeoetouiet"},
            status_code=500,
            operation="post",
        )
        with pytest.raises(NotificationException) as e:
            novu.generic_novu_manager.get_novu_jwt_bearer_token()

        assert str(e.value) == "Erreur lors de l'authentification au novu generic"
        assert requests.post.call_count == 1

    def test_get_generic_novu_templates(self, novu, monkeypatch, mock_request_call):
        mock_request_call(
            response_body=templates,
            status_code=200,
            operation="get",
        )

        monkeypatch.setattr(novu.generic_novu_manager, "get_novu_jwt_bearer_token", lambda: "")
        response = novu.generic_novu_manager.get_generic_novu_templates()

        assert requests.get.call_count == 1
        assert response[0]["name"] == "template_name"

    def test_get_generic_novu_templates_fails(self, novu, monkeypatch, mock_request_call):
        mock_request_call(
            response_body={},
            status_code=500,
            operation="get",
        )

        monkeypatch.setattr(novu.generic_novu_manager, "get_novu_jwt_bearer_token", lambda: "")

        with pytest.raises(NotificationException) as e:
            novu.generic_novu_manager.get_generic_novu_templates()

        assert str(e.value) == "Erreur lors de l'importation des templates"
        assert requests.get.call_count == 1

    def test_update_novu_local_template_no_templates(self, novu, monkeypatch):
        monkeypatch.setattr(GenericNovuManager, "get_generic_novu_templates", lambda: templates)

        novu.notification_groups_manager.get_notification_group_id_by_name = Mock()
        novu.notification_groups_manager.get_notification_group_id_by_name.return_value = []

        novu.notification_groups_manager.create_notification_group = Mock()
        novu.notification_groups_manager.create_notification_group.return_value = "id"

        novu.notification_templates_manager.create_update_notification_template = Mock()
        novu.notification_templates_manager.create_update_notification_template.return_value = []

        novu.generic_novu_manager.update_novu_local_templates()

        assert novu.notification_groups_manager.create_notification_group.call_count == 1
        assert (
            novu.notification_groups_manager.create_notification_group.call_args[1]["name"]
            == "General"
        )
        assert (
            novu.notification_templates_manager.create_update_notification_template.call_count == 1
        )
        assert (
            novu.notification_templates_manager.create_update_notification_template.call_args[1][
                "template_name"
            ]
            == templates[0]["name"]
        )
        assert (
            novu.notification_templates_manager.create_update_notification_template.call_args[1][
                "steps"
            ]
            == templates[0]["steps"]
        )
