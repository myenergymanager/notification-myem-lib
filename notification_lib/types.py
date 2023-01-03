"""Novu types."""
from typing import Literal

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

TemplateChannelTypes = Literal["push", "email", "sms", "in_app", "chat"]

subscriberPreferencesInputChannelType = TypedDict(
    "subscriberPreferencesInputChannelType", {"type": TemplateChannelTypes, "enabled": bool}
)

updateSubscriberPreferencesTypeOut = TypedDict(
    "updateSubscriberPreferencesTypeOut",
    {"channels": dict[TemplateChannelTypes, bool], "enabled": bool},
)

subscriberTemplatePreferencesType = TypedDict(
    "subscriberTemplatePreferencesType",
    {
        "preference": updateSubscriberPreferencesTypeOut,
        "template": dict[Literal["id", "template_name"], str],
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
