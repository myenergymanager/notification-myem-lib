"""Subscribers manager file."""
from math import ceil
from typing import Any, cast

from notification_lib.exceptions import NotificationException
from notification_lib.http_requests import HttpRequester
from notification_lib.types import (
    SubscriberCredentials,
    subscriberPageType,
    subscriberPreferencesInputChannelType,
    subscriberTemplatePreferencesType,
    subscriberType,
    updateSubscriberPreferencesTypeOut,
)


subscriber_mirror = {
    "subscriberId": "subscriber_id",
    "firstName": "first_name",
    "lastName": "last_name",
    "email": "email",
    "phone": "phone",
    "createdAt": "created_at",
    "updatedAt": "updated_at",
    "channels": "channels",
}

reversed_subscriber_mirror = {item: key for key, item in subscriber_mirror.items()}


class SubscribersManager(HttpRequester):
    """Novu manages users in a specific subscribers data model.

    This manager is built to communicate.
    With the novu subscribers api, it provides a crud for now.
    """

    # PS: we are using casts to keep our typing clean, because list comprehensions
    # and dict comprehensions gives back a type of dict[str, Any]
    @classmethod
    def get_subscriber(cls, subscriber_id: str) -> subscriberType | None:
        """Get subscriber by id."""
        response = cls.send_request(
            operation="GET",
            endpoint=f"/v1/subscribers/{subscriber_id}",
        )
        json_response = cls.handle_response(response, "Can't retrieve subscriber !").json()
        if json_response["data"] is None:
            return None
        subscriber = cast(
            subscriberType,
            {value: json_response["data"].get(key) for key, value in subscriber_mirror.items()},
        )
        return subscriber

    @classmethod
    def get_subscribers_based_on_page(cls, page: int) -> subscriberPageType:
        """Get subscribers per page."""
        response = cls.send_request(
            operation="GET",
            endpoint=f"/v1/subscribers?page={page - 1}",
        )
        json_response = cls.handle_response(response, "Can't retrieve subscribers !").json()
        return {
            "items": cast(
                list[subscriberType],
                [
                    {value: subscriber.get(key) for key, value in subscriber_mirror.items()}
                    for subscriber in json_response["data"]
                ],
            ),
            "page": page,
            "size": json_response["pageSize"],
            "total": json_response["totalCount"],
        }

    @classmethod
    def get_subscribers(
        cls, page: int | None = None, subscribers_ids: list[str] | None = None
    ) -> list[subscriberType] | subscriberPageType:
        """Get subscribers, apply pagination if required."""

        if subscribers_ids:
            # in case of specific subscribers ids where giving to retrieve
            # we use the function get_subscriber to fetch them one by one
            subscribers_by_ids: list[subscriberType] = []
            for subscriber_id in subscribers_ids:
                if subscriber := cls.get_subscriber(subscriber_id):
                    subscribers_by_ids.append(subscriber)
            return subscribers_by_ids

        if page is None:
            # in this case we have to return all subscribers from the database
            # novu api have a limit of 10, so we will fetch 10 by 10 until we get all subscribers
            page = 1
            subscriber_page = cls.get_subscribers_based_on_page(page)
            subscribers = subscriber_page["items"]
            # fetching from page 1 to last page
            for p in range(
                2,
                (subscriber_page["total"] // subscriber_page["size"])
                + ceil(subscriber_page["total"] % subscriber_page["size"] / subscriber_page["size"])
                + 1,
            ):
                subscriber_page = cls.get_subscribers_based_on_page(p)
                subscribers += subscriber_page["items"]
            return subscribers

        # final case is when we want to fetch per page
        # here we do page - 1 because novu api first page begins from 0 :/
        # if page is inferior to 1 we have to raise an exception
        if page <= 0:
            raise NotificationException("page must be superior than O")
        if page > 0:
            return cls.get_subscribers_based_on_page(page)
        raise NotificationException

    @classmethod
    def create_subscriber(
        cls,
        subscriber_id: str,
        email: str,
        first_name: str,
        last_name: str,
        phone: str,
    ) -> subscriberType:
        """Create a subscriber."""
        body = {
            "subscriberId": subscriber_id,
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "phone": phone,
        }
        response = cls.send_request(operation="POST", endpoint="/v1/subscribers", body=body)
        json_response = cls.handle_response(response, "Can't create subscriber !").json()
        created_subscriber = cast(
            subscriberType,
            {value: json_response["data"][key] for key, value in subscriber_mirror.items()},
        )
        return created_subscriber

    @classmethod
    def update_subscriber(cls, subscriber_id: str, **kwargs: Any) -> subscriberType:
        """Update a subscriber, raise an exception if it doesn't exist."""

        if any(
            item not in ["first_name", "last_name", "email", "phone"]
            for item in list(kwargs.keys())
        ):
            raise NotificationException("field is not allowed !")
        body = {reversed_subscriber_mirror[key]: item for key, item in kwargs.items()}
        response = cls.send_request(
            operation="PUT", endpoint=f"/v1/subscribers/{subscriber_id}", body=body
        )
        json_response = cls.handle_response(response, "Can't update subscriber !").json()
        updated_subscriber = cast(
            subscriberType,
            {value: json_response["data"][key] for key, value in subscriber_mirror.items()},
        )
        return updated_subscriber

    @classmethod
    def delete_subscriber(cls, subscriber_id: str) -> None:
        """Delete a subscriber, raise an exception if it doesn't exist."""

        response = cls.send_request(
            operation="DELETE",
            endpoint=f"/v1/subscribers/{subscriber_id}",
        )

        cls.handle_response(response, "Can't delete subscriber !").json()

    @classmethod
    def update_subscriber_credentials(
        cls, subscriber_id: str, provider: str, credentials: SubscriberCredentials
    ) -> None:
        """Update subscriber credentials."""

        response = cls.send_request(
            operation="PUT",
            endpoint=f"/v1/subscribers/{subscriber_id}/credentials",
            body={"providerId": provider, "credentials": credentials},
        )

        cls.handle_response(response, "Can't set subscriber credentials !").json()

    @classmethod
    def get_subscriber_preferences(cls, subscriber_id: str) -> list[subscriberTemplatePreferencesType]:
        """Get subscriber preferences for all templates."""

        response = cls.send_request(
            operation="GET",
            endpoint=f"/v1/subscribers/{subscriber_id}/preferences",
        )

        json_response = \
            cls.handle_response(response, "Can't get subscriber preferences for specified template !").json()

        result = [
            cast(
                subscriberTemplatePreferencesType,
                {
                    "preference": template["preference"],
                    "template": {
                        "id": template["template"]["_id"],
                        "template_name": template["template"]["name"]
                    }
                }
            ) for template in json_response["data"]
        ]

        return result

    @classmethod
    def update_subscriber_preferences(
            cls,
            subscriber_id: str,
            template_id: str,
            channel: subscriberPreferencesInputChannelType,
            enabled_template: bool | None = None
    ) -> updateSubscriberPreferencesTypeOut:
        """Update subscriber notification preferences for specific template known by his id.

        You can disable for example a channel for a specific template, or disable the whole template.
        """

        body: dict[str, Any] = {
            "channel": channel,
        }
        if enabled_template is not None:
            body["enabled"] = enabled_template

        response = cls.send_request(
            operation="PATCH",
            endpoint=f"/v1/subscribers/{subscriber_id}/preferences/{template_id}",
            body=body,
        )

        json_response = \
            cls.handle_response(response, "Can't update subscriber preferences for specified template !").json()

        return {
            "channels": json_response["data"]["preference"]["channels"],
            "enabled": json_response["data"]["preference"]["enabled"]
        }

    @classmethod
    def add_push_notification_device_token(cls, subscriber_id: str, device_token: str) -> None:
        """Add a new device token to the push notif tokens for a subscriber."""
        # get subscriber
        if not (subscriber := cls.get_subscriber(subscriber_id)):
            # if it does not exist we raise an exception
            raise NotificationException("subscriber doesn't exists !")
        subscriber_fcm_credentials: SubscriberCredentials | None = None
        for channel in subscriber["channels"]:
            if channel["providerId"] == "fcm":
                # if fcm credentials exists we add token to it
                subscriber_fcm_credentials = channel["credentials"]
        if not subscriber_fcm_credentials:
            # if fcm credentials doesn't exist we initialize it with the new token
            subscriber_fcm_credentials = {"deviceTokens": [device_token]}
        else:
            subscriber_fcm_credentials["deviceTokens"].append(device_token)
        cls.update_subscriber_credentials(subscriber_id, "fcm", subscriber_fcm_credentials)
