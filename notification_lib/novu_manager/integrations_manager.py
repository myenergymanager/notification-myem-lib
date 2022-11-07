"""Integrations manager file."""
from typing import Any, Dict, Optional

from notification_lib.http_requests import HttpRequester


class IntegrationsManager(HttpRequester):
    """Novu's integrations used to configure the final delivery providers for each channel.

    Provider channels are E-MAIL, SMS and In-app notification center for now.
    This manager helps us crud providers (with credentials).
    """

    @classmethod
    def create_update_integration(
        cls, channel: str, credentials: Dict[str, Any], provider: str
    ) -> None:
        """Create integration."""
        integration_id = cls.get_integration_id_by_provider_and_channel(
            provider=provider, channel=channel
        )
        if integration_id:
            response = cls.send_request(
                operation="PUT",
                endpoint=f"/v1/integrations/{integration_id}",
                body={"credentials": credentials, "active": True, "check": True},
            )
        else:
            response = cls.send_request(
                operation="POST",
                endpoint="/v1/integrations",
                body={
                    "channel": channel,
                    "providerId": provider,
                    "credentials": credentials,
                    "active": True,
                    "check": True,
                },
            )
        cls.handle_response(response, "Can't create integration !")

    @classmethod
    def get_integration_id_by_provider_and_channel(
        cls, provider: str, channel: str
    ) -> Optional[str]:
        """Search integration id by provider id and channel."""
        response = cls.send_request(operation="GET", endpoint="/v1/integrations")
        integrations = cls.handle_response(response, "Can't get integrations !").json()["data"]
        for integration in integrations:
            if integration["channel"] == channel and integration["providerId"] == provider:
                return integration["_id"]
        return None
