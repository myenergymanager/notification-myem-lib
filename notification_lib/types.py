"""Novu types."""
from typing_extensions import TypedDict


class SubscriberCredentials(TypedDict, total=False):
    """Subscriber credentials notiffs type."""

    webhookUrl: str | None
    deviceTokens: list[str]


channelType = TypedDict(
    "channelType",
    {
        "providerId": str,
        "credentials": SubscriberCredentials,
    },
)


subscriberType = TypedDict(
    "subscriberType",
    {
        "subscriber_id": str,
        "first_name": str,
        "last_name": str,
        "email": str,
        "phone": str,
        "created_at": str,
        "updated_at": str,
        "channels": list[channelType],
    },
)

subscriberPageType = TypedDict(
    "subscriberPageType", {"page": int, "size": int, "total": int, "items": list[subscriberType]}
)

notificationTemplateType = TypedDict(
    "notificationTemplateType", {"id": str, "template_name": str, "trigger_identifier": str}
)
