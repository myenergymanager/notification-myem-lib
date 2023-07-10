"""Handle functions to the generic novu."""
import json
import logging
from typing import Any

import requests
from notification_lib.exceptions import NotificationException


logging.getLogger().setLevel(logging.INFO)


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
            return response.json()["data"]

        logging.error(f"status code: {response.status_code}")
        logging.error(f"response : {response.json()}")
        raise NotificationException("Erreur lors de l'importation des templates")

    @staticmethod
    def format_filter_to_create_update(filter_from_generic: dict[str, Any]) -> dict[str, Any]:
        """Take useful fields for the filter."""

        return {
            key: filter_from_generic[key]
            for key in filter_from_generic.keys()
            if key in {"children", "isNegated", "type", "value"}
        }

    @staticmethod
    def format_steps_to_create_update(
        steps_from_generic: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Format the steps that we get from generic novu so that we can use it in creation and update."""
        logging.info(f"generic steps: {steps_from_generic}")
        steps = []

        for step in steps_from_generic:
            formated_template = {
                "type": step["template"]["type"],
                "active": step["template"]["active"],
                "variables": step["template"]["variables"],
                "content": step["template"]["content"],
            }
            if step["template"]["type"] == "push":
                # Push notification has "title" as their content key
                formated_template["title"] = step["template"]["title"]

            # If customHtml is true, it means we are passing a custom html
            if (
                step["template"]["type"] == "email"
                and step["template"]["contentType"] == "customHtml"
            ):
                # Subject is the title of the email
                formated_template["subject"] = step["template"]["subject"]
                # Content is body of the email
                formated_template["content"] = step["template"]["content"]
                # contentType = customHtml indicates that the content is a custom html
                formated_template["contentType"] = "customHtml"

            steps.append(
                {
                    "active": step["active"],
                    "filters": [
                        GenericNovuManager.format_filter_to_create_update(step_filter)
                        for step_filter in step["filters"]
                    ],
                    "template": formated_template,
                }
            )

        logging.info(f"formatted steps: {steps}")
        return steps

    @classmethod
    def get_generic_template_by_id(cls, template_id: str) -> dict[str, Any]:
        """Get generic template by providing his id."""
        response = requests.get(
            url=f"{cls.api_url_generic_novu}/v1/notification-templates/{template_id}",
            headers={"Authorization": f"Bearer {cls.get_novu_jwt_bearer_token()}"},
            timeout=5,
        )

        if response.status_code == 200:
            result = response.json()["data"]
            return {
                "template_name": result["name"],
                "id": result["_id"],
                "steps": cls.format_steps_to_create_update(result["steps"]),
            }

        logging.error(f"status code: {response.status_code}")
        logging.error(f"response : {response.json()}")
        raise NotificationException("Erreur lors de l'importation du template")
