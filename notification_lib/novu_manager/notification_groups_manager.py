"""Notification groups manager file."""
from notification_lib.http_requests import HttpRequester


class NotificationGroupsManager(HttpRequester):
    """The notification group is used to group multiple notification templates into a single group.

    Currently only used behind the scenes for organisational purposes.
    This Manager helps us create and get notification groups.
    """

    raise NotImplementedError
