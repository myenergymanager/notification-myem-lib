"""Events manager file."""
import logging
from typing import Any

from notification_lib.exceptions import NotificationException
from notification_lib.http_requests import HttpRequester
from notification_lib.novu_manager.notification_templates_manager import (
    NotificationTemplatesManager,
)
from notification_lib.types import subscriberType


logging.getLogger().setLevel(logging.INFO)


class EventsManager(HttpRequester):
    """Trigger event is the main (and the only) way to send notifications to subscribers.

    The trigger identifier is used to match the particular template associated with it.
    The events manager helps us to trigger events to one subscriber or more.
    We can also broadcast and cancel an event.
    """

    @classmethod
    def trigger_event(
        cls,
        template_name: str,
        payload: dict[str, Any],
        recipients: subscriberType | list[subscriberType] | str | list[str] | None = None,
        broadcast: bool = False,
        overrides: dict[str, Any] | None = None,
        default_payload: dict[str, Any] | None = None,
    ) -> None:
        """Trigger an event using the template name and link it to recipients or broadcast it.

        It's possible also to override template config.
        """

        logging.info(f"template_name: {template_name}")
        logging.info(f"payload: {payload}")
        logging.info(f"default_payload: {default_payload}")

        if not broadcast and not recipients:
            raise NotificationException("you must specify recipients or set a broadcast trigger!")
        template = NotificationTemplatesManager.get_template_by_name(template_name=template_name)
        if not template:
            raise NotificationException("template doesn't exist !")
        body: dict[str, Any] = {
            "payload": {**(default_payload or {}), **payload},
            "name": template["trigger_identifier"],
        }
        if recipients and not broadcast:
            body.update({"to": recipients})
        if overrides:
            body.update({"overrides": overrides})
        response = cls.send_request(
            operation="POST",
            endpoint=f"/v1/events/trigger{'/broadcast' if broadcast else ''}",
            body=body,
        )
        logging.info(f"trigger event response: {response}")
        cls.handle_response(response, "Trigger creation has failed !")
