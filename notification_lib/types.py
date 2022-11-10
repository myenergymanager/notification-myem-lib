"""Novu types."""
from typing import List

from typing_extensions import TypedDict


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
        "channels": List[str],
    },
)

subscriberPageType = TypedDict(
    "subscriberPageType", {"page": int, "size": int, "total": int, "items": List[subscriberType]}
)

notificationTemplateType = TypedDict("notificationTemplateType", {"id": str, "template_name": str})
