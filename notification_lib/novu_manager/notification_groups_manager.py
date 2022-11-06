"""Notification groups manager file."""
from typing import Optional

from notification_lib.http_requests import HttpRequester


class NotificationGroupsManager(HttpRequester):
    """The notification group is used to group multiple notification templates into a single group.

    Currently only used behind the scenes for organisational purposes.
    This Manager helps us create and get notification groups.
    """

    @classmethod
    def get_notification_group_id_by_name(cls, name: str) -> Optional[str]:
        """Get notification group id by name."""
        response = cls.send_request(
            operation="GET",
            endpoint="/v1/notification-groups",
        )
        json_response = cls.handle_response(response, "Can't get notifications groups !").json()
        for notification_group in json_response["data"]:
            if notification_group["name"] == name:
                return notification_group["_id"]
        return None

    @classmethod
    def create_notification_group(cls, name: str) -> None:
        """Create a notification group."""
        response = cls.send_request(
            operation="POST", endpoint="/v1/notification-groups", body={"name": name}
        )
        cls.handle_response(response, "Can't create notification group !").json()
