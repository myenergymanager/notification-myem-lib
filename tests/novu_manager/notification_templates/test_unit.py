from unittest.mock import MagicMock, Mock

from notification_lib.http_requests import HttpRequester


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


class TestNotificationTemplatesManager:
    def test_get_non_existent_template_id_by_name(self, novu):
        assert (
            novu.notification_templates_manager.get_template_by_name(template_name="999999") is None
        )

    def test_create_notif_template(self, novu, created_notification_template):
        template = novu.notification_templates_manager.get_template_by_name(
            template_name="template name"
        )
        assert template["trigger_identifier"] == "template-name"
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

    def test_update_novu_local_template_no_templates(self, novu, monkeypatch):
        monkeypatch.setattr(
            novu.generic_novu_manager, "get_generic_novu_templates", lambda: templates
        )

        # save to restore them once finished with tests
        get_notification_group_id_by_name = (
            novu.notification_groups_manager.get_notification_group_id_by_name
        )
        create_notification_group = novu.notification_groups_manager.create_notification_group
        create_update_notification_template = (
            novu.notification_templates_manager.create_update_notification_template
        )

        novu.notification_groups_manager.get_notification_group_id_by_name = Mock()
        novu.notification_groups_manager.get_notification_group_id_by_name.return_value = []

        novu.notification_groups_manager.create_notification_group = Mock()
        novu.notification_groups_manager.create_notification_group.return_value = "id"

        novu.notification_templates_manager.create_update_notification_template = Mock()
        novu.notification_templates_manager.create_update_notification_template.return_value = []

        novu.notification_templates_manager.update_novu_local_templates()

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

        # clean what have been created
        novu.notification_groups_manager.get_notification_group_id_by_name = (
            get_notification_group_id_by_name
        )
        novu.notification_groups_manager.create_notification_group = create_notification_group
        novu.notification_templates_manager.create_update_notification_template = (
            create_update_notification_template
        )

        for template in templates:
            HttpRequester.send_request(
                operation="DELETE",
                endpoint=f"/v1/notification-templates/{template['id']}",
            )
