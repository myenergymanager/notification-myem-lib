import pytest
from notification_lib.exceptions import NotificationException
from notification_lib.http_requests import HttpRequester


class TestEventsManager:
    def test_trigger_event(self, novu, created_notification_template, created_subscriber):
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
