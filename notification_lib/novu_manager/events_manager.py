"""Events manager file."""
from notification_lib.http_requests import HttpRequester


class EventsManager(HttpRequester):
    """Trigger event is the main (and the only) way to send notifications to subscribers.

    The trigger identifier is used to match the particular template associated with it.
    The events manager helps us to trigger events to one subscriber or more.
    We can also broadcast and cancel an event.
    """

    raise NotImplementedError
