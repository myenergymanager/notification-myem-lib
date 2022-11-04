"""Notification templates manager file."""
from requests import Response
from notification_lib.http_requests import HttpRequester


class NotificationTemplatesManager(HttpRequester):
    """A template holds the entire flow of messages sent to the subscriber.

    This is where all the different channels are tied together under a single entity.
    this manager helps us crud templates.
    """

    def create_notification_template(self) -> Response:
        """Create notification template."""
        response = self.send_request(
            operation="POST",
            endpoint="/v1/notification-templates",
            body={
                "notificationGroupId": "6363a48ac66370e4a218a4fb",
                "name": "fdsfsdfsd",
                "description": "fsdfsdfds",
                "steps": [],
                "active": True,
                "draft": False,
            },
        )
        return response

    def get_notification_template(self, template_id: str) -> None:
        """Get notification template by id."""
        response = self.send_request(
            operation="GET",
            endpoint=f"/v1/notification-templates/{template_id}",
        )
        json_response = (
            super().handle_response(response, "Can't retrieve notification template !").json()
        )
        if json_response["data"] is None:
            return None
