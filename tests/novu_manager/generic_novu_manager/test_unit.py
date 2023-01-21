"""Test Novu utils functions."""
from unittest.mock import Mock

import pytest
from notification_lib.exceptions import NotificationException
from notification_lib.novu_manager.generic_novu_manager import requests


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
        "_id": "template_id",
        "name": "template_name",
        "steps": [
            {
                "template": {
                    "_id": "63ca524e2ad2a2b52691e52f",
                    "type": "push",
                    "active": True,
                    "variables": [],
                    "content": "signal rouge ou orange prévue pour les trois prochains jours ",
                    "title": "Ecowatt alerte periodique ",
                    "_environmentId": "63bee3fc2ad2a2b52691e0c3",
                    "_organizationId": "63bee3fc2ad2a2b52691e0bd",
                    "_creatorId": "63bee3fc2ad2a2b52691e0b6",
                    "_feedId": None,
                    "createdAt": "2023-01-20T08:35:26.395Z",
                    "updatedAt": "2023-01-20T13:59:27.506Z",
                    "__v": 0,
                    "id": "63ca524e2ad2a2b52691e52f",
                },
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
                        "_id": "63ca524e2ad2a2b52691e545",
                    }
                ],
                "active": True,
            },
            {
                "template": {
                    "_id": "63ca524e2ad2a2b52691e52f",
                    "type": "push",
                    "active": True,
                    "variables": [],
                    "content": "signal rouge ou orange prévue pour les trois prochains jours ",
                    "title": "Ecowatt alerte periodique ",
                    "_environmentId": "63bee3fc2ad2a2b52691e0c3",
                    "_organizationId": "63bee3fc2ad2a2b52691e0bd",
                    "_creatorId": "63bee3fc2ad2a2b52691e0b6",
                    "_feedId": None,
                    "createdAt": "2023-01-20T08:35:26.395Z",
                    "updatedAt": "2023-01-20T13:59:27.506Z",
                    "__v": 0,
                    "id": "63ca524e2ad2a2b52691e52f",
                },
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
                        "_id": "63ca524e2ad2a2b52691e545",
                    }
                ],
                "active": True,
            },
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
            response_body={"data": templates},
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

    def test_get_generic_template_by_id_fails(self, novu, monkeypatch, mock_request_call):
        mock_request_call(
            response_body={},
            status_code=500,
            operation="get",
        )

        monkeypatch.setattr(novu.generic_novu_manager, "get_novu_jwt_bearer_token", lambda: "")

        with pytest.raises(NotificationException) as e:
            novu.generic_novu_manager.get_generic_template_by_id(template_id=templates[0]["id"])

        assert str(e.value) == "Erreur lors de l'importation du template"
        assert requests.get.call_count == 1

    def test_get_generic_template_by_id_successful(self, novu, monkeypatch, mock_request_call):
        mock_request_call(
            response_body={"data": templates[0]},
            status_code=200,
            operation="get",
        )

        monkeypatch.setattr(novu.generic_novu_manager, "get_novu_jwt_bearer_token", lambda: "")
        response = novu.generic_novu_manager.get_generic_template_by_id(
            template_id=templates[0]["id"]
        )

        assert response["template_name"] == templates[0]["name"]
        assert response["id"] == templates[0]["id"]
        assert response["steps"] == [
            {
                "template": {
                    "type": "push",
                    "active": True,
                    "variables": [],
                    "content": "signal rouge ou orange prévue pour les trois prochains jours ",
                    "title": "Ecowatt alerte periodique ",
                },
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
            },
            {
                "template": {
                    "type": "push",
                    "active": True,
                    "variables": [],
                    "content": "signal rouge ou orange prévue pour les trois prochains jours ",
                    "title": "Ecowatt alerte periodique ",
                },
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
            },
        ]
