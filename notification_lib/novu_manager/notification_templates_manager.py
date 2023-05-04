"""Notification templates manager file."""
from typing import Any

from notification_lib.exceptions import NotificationException
from notification_lib.http_requests import HttpRequester
from notification_lib.novu_manager.generic_novu_manager import GenericNovuManager
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
        steps: list[dict[str, Any]],
        notification_group_name: str = "General",
    ) -> None:
        """Create notification template."""
        notification_group_id = NotificationGroupsManager.get_notification_group_id_by_name(
            name=notification_group_name
        )
        if not notification_group_id:
            raise NotificationException("Can't create notification template !")
        if not (old_template := cls.get_template_by_name(template_name=template_name)):
            response = cls.send_request(
                operation="POST",
                endpoint="/v1/notification-templates",
                body={
                    "notificationGroupId": notification_group_id,
                    "name": template_name,
                    "steps": steps,
                    "active": True,
                    "draft": False,
                    "preferenceSettings": {  # set up all the default preferences for the users
                        "email": False,
                        "sms": False,
                        "in_app": True,
                        "chat": False,
                        "push": False,
                    },
                },
            )
            cls.handle_response(response, "Can't create notification template !")
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
            cls.handle_response(response, "Can't update notification template !")

    @classmethod
    def get_template_by_name(cls, template_name: str) -> notificationTemplateType | None:
        """Get notification template by id."""
        response = cls.send_request(
            operation="GET",
            endpoint="/v1/notification-templates",
        )
        json_response = cls.handle_response(
            response, "Can't retrieve notification templates !"
        ).json()
        for notification_template in json_response["data"]:
            if notification_template["name"] == template_name:
                return {
                    "id": notification_template["id"],
                    "template_name": notification_template["name"],
                    # not sure why there are many trrigers ids in one notification
                    # template, for now we take the first
                    "trigger_identifier": notification_template["triggers"][0]["identifier"],
                }
        return None

    @classmethod
    def update_novu_local_templates(cls, template_values: list[str]) -> None:
        """Function that checks if there is templates, if not create them."""

        if not (generic_templates := GenericNovuManager.get_generic_novu_templates()):
            raise NotificationException("Aucun template généric")

        # Before creating templates, if there is no default notification group, we have to create it
        # be aware that General is the default name used in notification_lib for template creation
        notification_group = NotificationGroupsManager.get_notification_group_id_by_name(
            name="General"
        )
        if not notification_group:
            NotificationGroupsManager.create_notification_group(name="General")

        # Check if every template_values that were passed to the function exists among the generic templates.
        # This way we only use the relevant templates and not all of them.
        for item in template_values:
            for generic_template_dict in generic_templates:
                if item is not None and "name" in generic_template_dict:
                    if item in generic_template_dict["name"]:
                        full_template = GenericNovuManager.get_generic_template_by_id(
                            template_id=generic_template_dict["id"]
                        )
                        # if it exists, it will override it to update, if it does not exist, it will create it
                        cls.create_update_notification_template(
                            template_name=full_template["template_name"],
                            steps=full_template["steps"],
                        )
