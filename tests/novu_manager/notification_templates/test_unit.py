class TestNotificationTemplatesManager:
    def test_get_non_existent_template_id_by_name(self, novu):
        assert (
            novu.notification_templates_manager.get_template_by_name(template_name="999999") is None
        )

    def test_create_notif_template(self, novu):
        novu.notification_templates_manager.create_update_notification_template(
            template_name="template name",
            template={"title": "hello world", "description": "i'am a notif"},
        )
        template = novu.notification_templates_manager.get_template_by_name(
            template_name="template name"
        )
        assert isinstance(template["id"], str)
        assert template["template_name"] == {"title": "hello world", "description": "i'am a notif"}
        assert template["template"] == "template name"
