"""Notification templates manager file."""
from typing import Any, Dict, List, Optional

from notification_lib.exceptions import NotificationException
from notification_lib.http_requests import HttpRequester
from notification_lib.novu_manager.notification_groups_manager import NotificationGroupsManager
from notification_lib.types import notificationTemplateType


class NotificationTemplatesManager(HttpRequester):
    """A template holds the entire flow of messages sent to the subscriber.

    This is where all the different channels are tied together under a single entity.
    this manager helps us crud templates.
    """

    @classmethod
    def create_update_notification_template(
        cls,
        template_name: str,
        steps: List[Dict[str, Any]],
        notification_group_name: str = "General",
    ) -> None:
        """Create notification template."""
        notification_group_id = NotificationGroupsManager.get_notification_group_id_by_name(
            name=notification_group_name
        )
        if not notification_group_id:
            raise NotificationException("Can't create notification template !")
        old_template = cls.get_template_by_name(template_name=template_name)
        if not old_template:
            response = cls.send_request(
                operation="POST",
                endpoint="/v1/notification-templates",
                body={
                    "notificationGroupId": notification_group_id,
                    "name": template_name,
                    "steps": steps,
                    "active": True,
                    "draft": False,
                },
            )
            super().handle_response(response, "Can't create notification template !")
        else:
            response = cls.send_request(
                operation="PUT",
                endpoint=f"/v1/notification-templates/{old_template['id']}",
                body={
                    "notificationGroupId": notification_group_id,
                    "name": template_name,
                    "identifier": template_name,
                    "steps": steps,
                    "active": True,
                },
            )
            super().handle_response(response, "Can't update notification template !")

    @classmethod
    def get_template_by_name(cls, template_name: str) -> Optional[notificationTemplateType]:
        """Get notification template by id."""
        response = cls.send_request(
            operation="GET",
            endpoint="/v1/notification-templates",
        )
        json_response = (
            super().handle_response(response, "Can't retrieve notification templates !").json()
        )
        for notification_template in json_response["data"]:
            if notification_template["name"] == template_name:
                return {
                    "id": notification_template["id"],
                    "template_name": notification_template["name"],
                }
        return None
