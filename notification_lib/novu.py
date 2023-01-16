"""Novu base file."""
from notification_lib.http_requests import HttpRequester
from notification_lib.novu_manager.events_manager import EventsManager
from notification_lib.novu_manager.generic_novu_manager import GenericNovuManager
from notification_lib.novu_manager.integrations_manager import IntegrationsManager
from notification_lib.novu_manager.notification_groups_manager import NotificationGroupsManager
from notification_lib.novu_manager.notification_templates_manager import (
    NotificationTemplatesManager,
)
from notification_lib.novu_manager.subscribers_manager import SubscribersManager


class Novu:
    """Novu base class."""

    def __init__(
        self,
        api_key: str,
        api_url: str,
        admin_email: str,
        admin_password: str,
        api_url_generic_novu: str | None,
        admin_email_for_generic_novu: str | None,
        admin_password_for_generic_novu: str | None,
    ):
        """Init function of Novu Manager."""
        HttpRequester.api_key = api_key
        HttpRequester.api_url = api_url
        HttpRequester.admin_email = admin_email
        HttpRequester.admin_password = admin_password
        self.generic_novu_manager.api_url_generic_novu = api_url_generic_novu
        self.generic_novu_manager.admin_email_for_generic_novu = admin_email_for_generic_novu
        self.generic_novu_manager.admin_password_for_generic_novu = admin_password_for_generic_novu

    events_manager = EventsManager
    subscribers_manager = SubscribersManager
    notification_templates_manager = NotificationTemplatesManager
    notification_groups_manager = NotificationGroupsManager
    integrations_manager = IntegrationsManager
    generic_novu_manager = GenericNovuManager
