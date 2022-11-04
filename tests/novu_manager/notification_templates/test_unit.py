class TestNotificationTemplatesManager:
    def test_get_template(self, novu):
        subscriber = novu.notification_templates_manager.get_notification_template(
            template_id="999999"
        )

    def test_create_notif_template(self, novu):
        response = novu.notification_templates_manager.create_notification_template()
        assert response.json() == ""
