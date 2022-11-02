"""Integrations manager file."""

from notification_lib.http_requests import HttpRequester


class IntegrationsManager(HttpRequester):
    """Novu's integrations used to configure the final delivery providers for each channel.

    Provider channels are E-MAIL, SMS and In-app notification center for now.
    This manager helps us crud providers (with credentials).
    """

    pass  # NotImplementedYet
