"""Handle functions to the generic novu."""
import json
import logging
from typing import Any

import requests
from notification_lib.exceptions import NotificationException


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

    @classmethod
    def get_generic_template_by_id(cls, template_id: str) -> dict[str, Any]:
        """Get generic template by providing his id."""
        response = requests.get(
            url=f"{cls.api_url_generic_novu}/v1/notification-templates/{template_id}",
            headers={"Authorization": f"Bearer {cls.get_novu_jwt_bearer_token()}"},
            timeout=5,
        )

        if response.status_code // 100 == 2:
            result = response.json()["data"]
            steps = []

            def construct_filters(step_filter: dict[str, Any]) -> dict[str, Any]:
                """Take useful fields for the filter."""

                needed_fields = ["children", "isNegated", "type", "value"]
                formated_filter = {}
                for key in step_filter.keys():
                    if key in needed_fields:
                        formated_filter[key] = step_filter[key]
                return formated_filter

            for step in result["steps"]:
                steps.append(
                    {
                        "active": step["active"],
                        "filters": [
                            construct_filters(step_filter) for step_filter in step["filters"]
                        ],
                        "template": {
                            "type": step["template"]["type"],
                            "active": step["template"]["active"],
                            "variables": step["template"]["variables"],
                            "content": step["template"]["content"],
                            "title": step["template"]["title"],
                        },
                    }
                )

            return {"template_name": result["name"], "id": result["_id"], "steps": steps}

        logging.error(f"status code: {response.status_code}")
        logging.error(f"response : {response.json()}")
        raise NotificationException("Erreur lors de l'importation du template")
