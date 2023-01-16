"""Handle functions to the generic novu."""
import json
import logging
from typing import Any

import requests
from notification_lib.exceptions import NotificationException
from notification_lib.novu_manager.notification_groups_manager import NotificationGroupsManager
from notification_lib.novu_manager.notification_templates_manager import (
    NotificationTemplatesManager,
)


class GenericNovuManager:
    """Novu utils, template creation/ update."""

    api_url_generic_novu: str | None
    admin_email_for_generic_novu: str | None
    admin_password_for_generic_novu: str | None

    @classmethod
    def get_novu_jwt_bearer_token(cls) -> str:
        """Get jwt bearer token."""
        login_response = requests.post(
            f"{cls.api_url_generic_novu}/v1/auth/login",
            headers={"Content-Type": "application/json"},
            data=json.dumps(
                {
                    "email": cls.admin_email_for_generic_novu,
                    "password": cls.admin_password_for_generic_novu,
                }
            ),
            timeout=10,
        )

        if login_response.status_code // 100 == 2:
            return login_response.json()["data"]["token"]

        logging.error(f"status code: {login_response.status_code}")
        logging.error(f"response : {login_response.json()}")
        raise NotificationException("Erreur lors de l'authentification au novu generic")

    @classmethod
    def get_generic_novu_templates(cls) -> list[dict[str, Any]]:
        """Get templates from the generic novu."""
        response = requests.get(
            url=f"{cls.api_url_generic_novu}/v1/notification-templates",
            headers={"Authorization": f"Bearer {cls.get_novu_jwt_bearer_token()}"},
            timeout=5,
        )

        if response.status_code // 100 == 2:
            return response.json()

        logging.error(f"status code: {response.status_code}")
        logging.error(f"response : {response.json()}")
        raise NotificationException("Erreur lors de l'importation des templates")

    @classmethod
    def update_novu_local_templates(cls) -> None:
        """Function that checks if there is templates, if not create them."""

        if not (generic_templates := cls.get_generic_novu_templates()):
            raise NotificationException("Aucun template généric")

        # Before creating templates, if there is no default notification group, we have to create it
        # be aware that General is the default name used in notification_lib for template creation
        notification_group = NotificationGroupsManager.get_notification_group_id_by_name(
            name="General"
        )
        if not notification_group:
            NotificationGroupsManager.create_notification_group(name="General")

        for template in generic_templates:
            # if it exists, it will override it, if it does not exist, it will create it
            NotificationTemplatesManager.create_update_notification_template(
                template_name=template["name"],
                steps=template["steps"],
            )
