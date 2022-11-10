import pytest
from notification_lib.http_requests import HttpRequester


class TestNotificationTemplatesManager:
    @pytest.fixture(scope="session")
    def created_notification_template(self, novu):
        novu.notification_templates_manager.create_update_notification_template(
            template_name="template name",
            steps=[
                {
                    "template": {
                        "content": "content",
                        "subject": "subject",
                        "type": "in_app",
                    },
                    "active": True,
                }
            ],
        )
        template = novu.notification_templates_manager.get_template_by_name(
            template_name="template name"
        )
        yield
        HttpRequester.send_request(
            operation="DELETE",
            endpoint=f"/v1/notification-templates/{template['id']}",
        )

    def test_get_non_existent_template_id_by_name(self, novu):
        assert (
            novu.notification_templates_manager.get_template_by_name(template_name="999999") is None
        )

    def test_create_notif_template(self, novu, created_notification_template):
        template = novu.notification_templates_manager.get_template_by_name(
            template_name="template name"
        )
        response = HttpRequester.send_request(
            operation="GET",
            endpoint=f"/v1/notification-templates/{template['id']}",
        ).json()["data"]
        assert isinstance(response["id"], str)
        assert response["name"] == "template name"
        assert len(response["steps"]) == 1
        assert response["steps"][0]["template"]["content"] == "content"
        assert response["steps"][0]["template"]["subject"] == "subject"
        assert response["steps"][0]["template"]["type"] == "in_app"

    def test_update_notif_template(self, novu):
        novu.notification_templates_manager.create_update_notification_template(
            template_name="template name",
            steps=[
                {
                    "template": {
                        "content": "updated_content",
                        "subject": "updated_subject",
                        "type": "in_app",
                    },
                    "active": True,
                }
            ],
        )
        template = novu.notification_templates_manager.get_template_by_name(
            template_name="template name"
        )
        response = HttpRequester.send_request(
            operation="GET",
            endpoint=f"/v1/notification-templates/{template['id']}",
        ).json()["data"]
        assert isinstance(response["id"], str)
        assert response["name"] == "template name"
        assert len(response["steps"]) == 1
        assert response["steps"][0]["template"]["content"] == "updated_content"
        assert response["steps"][0]["template"]["subject"] == "updated_subject"
        assert response["steps"][0]["template"]["type"] == "in_app"
