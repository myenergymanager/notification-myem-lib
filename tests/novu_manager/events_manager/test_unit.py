import pytest
from notification_lib.exceptions import NotificationException
from notification_lib.http_requests import HttpRequester


class TestEventsManager:
    def test_trigger_event(self, novu, created_notification_template, created_subscriber):

        # since we've made that the preferences of the templates will be set to False
        # the subscriber should not receive any targeted event.
        for _ in range(5):
            novu.events_manager.trigger_event(
                template_name="template name",
                recipients=created_subscriber["subscriber_id"],
                payload={},
            )
        messages = HttpRequester.send_request(
            operation="GET",
            endpoint=f"/v1/messages?channel=in_app&"
            f"subscriberId={created_subscriber['subscriber_id']}",
        ).json()

        assert len(messages["data"]) == 0

        # now we change the subscriber's preferences to True
        template = novu.notification_templates_manager.get_template_by_name(
            template_name="template name"
        )

        novu.subscribers_manager.update_subscriber_preferences(
            template_id=template["id"],
            subscriber_id=created_subscriber["subscriber_id"],
            channel={"type": "in_app", "enabled": True},
        )

        # we target again, this time the user should receive them.
        for _ in range(5):
            novu.events_manager.trigger_event(
                template_name="template name",
                recipients=created_subscriber["subscriber_id"],
                payload={},
            )
        messages = HttpRequester.send_request(
            operation="GET",
            endpoint=f"/v1/messages?channel=in_app&"
            f"subscriberId={created_subscriber['subscriber_id']}",
        ).json()

        assert len(messages["data"]) == 5
        assert messages["data"][0]["channel"] == "in_app"
        assert messages["data"][0]["content"] == "content"
        assert messages["data"][0]["templateIdentifier"] == "template-name"
        assert messages["data"][0]["status"] == "sent"
        assert messages["data"][0]["read"] is False
        assert messages["data"][0]["seen"] is False

    def test_trigger_event_with_in_existent_template(self, novu):
        with pytest.raises(NotificationException):
            novu.events_manager.trigger_event(
                template_name="99999", recipients="999999999", payload={}
            )
