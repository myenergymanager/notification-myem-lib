"""Subscribers manager file."""
from math import ceil
from typing import Any, cast, List, Optional, Union
from uuid import UUID

from notification_lib.exceptions import NotificationException
from notification_lib.http_requests import HttpRequester
from notification_lib.types import subscriberPageType, subscriberType


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
    # and dict comprehensions gives back a type of Dict[str, Any]
    def get_subscriber(self, subscriber_id: Union[str, UUID]) -> Optional[subscriberType]:
        """Get subscriber by id."""
        if isinstance(subscriber_id, UUID):
            subscriber_id = str(subscriber_id)
        response = self.send_request(
            operation="GET",
            endpoint=f"/v1/subscribers/{subscriber_id}",
        )
        json_response = super().handle_response(response, "Can't retrieve subscriber !").json()
        if json_response["data"] is None:
            return None
        subscriber = cast(
            subscriberType,
            {value: json_response["data"][key] for key, value in subscriber_mirror.items()},
        )
        return subscriber

    def get_subscribers(
        self, page: Optional[int] = None, subscribers_ids: Optional[List[Union[str, UUID]]] = None
    ) -> Union[List[subscriberType], subscriberPageType]:
        """Get subscribers, apply pagination if required."""

        if subscribers_ids:
            # in case of specific subscribers ids where giving to retrieve
            # we use the function get_subscriber to fetch them one by one
            subscribers_by_ids: List[subscriberType] = []
            for subscriber_id in subscribers_ids:
                subscriber = self.get_subscriber(subscriber_id)
                if subscriber:
                    subscribers_by_ids.append(subscriber)
            return subscribers_by_ids

        if page is None:
            # in this case we have to return all subscribers from the database
            # novu api have a limit of 10, so we will fetch 10 by 10 until we get all subscribers
            page = 0
            # fetching page 0
            response = self.send_request(
                operation="GET",
                endpoint=f"/v1/subscribers?page={page}",
            )
            json_response = super().handle_response(response, "Can't retrieve subscribers !").json()
            subscribers = cast(
                List[subscriberType],
                [
                    {value: subscriber[key] for key, value in subscriber_mirror.items()}
                    for subscriber in json_response["data"]
                ],
            )
            # fetching from page 1 to last page
            for p in range(
                1,
                json_response["totalCount"] // json_response["pageSize"]
                + ceil(
                    json_response["totalCount"]
                    % json_response["pageSize"]
                    / json_response["pageSize"]
                ),
            ):
                response = self.send_request(
                    operation="GET",
                    endpoint=f"/v1/subscribers?page={p}",
                )
                response = super().handle_response(response, "Can't retrieve subscribers !").json()
                subscribers.extend(
                    cast(
                        List[subscriberType],
                        [
                            {value: subscriber[key] for key, value in subscriber_mirror.items()}
                            for subscriber in response["data"]
                        ],
                    )
                )
            return subscribers

        # final case is when we want to fetch per page
        # here we do page - 1 because novu api first page begins from 0 :/
        # if page is inferior to 1 we have to raise an exception
        if page <= 0:
            raise NotificationException("page must be superior than O")
        if page > 0:
            response = self.send_request(
                operation="GET",
                endpoint=f"/v1/subscribers?page={page - 1}",
            )
            json_response = super().handle_response(response, "Can't retrieve subscribers !").json()
            # return a special format of pagination
            returned_response: subscriberPageType = {
                "items": cast(
                    List[subscriberType],
                    [
                        {value: subscriber[key] for key, value in subscriber_mirror.items()}
                        for subscriber in json_response["data"]
                    ],
                ),
                "page": json_response["page"] + 1,
                "size": json_response["pageSize"],
                "total": json_response["totalCount"],
            }
            return returned_response
        raise NotificationException

    def create_subscriber(
        self,
        subscriber_id: Union[str, UUID],
        email: str,
        first_name: str,
        last_name: str,
        phone: str,
    ) -> subscriberType:
        """Create a subscriber."""
        if isinstance(subscriber_id, UUID):
            subscriber_id = str(subscriber_id)
        body = {
            "subscriberId": subscriber_id,
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "phone": phone,
        }
        response = self.send_request(operation="POST", endpoint="/v1/subscribers", body=body)
        json_response = super().handle_response(response, "Can't create subscriber !").json()
        created_subscriber = cast(
            subscriberType,
            {value: json_response["data"][key] for key, value in subscriber_mirror.items()},
        )
        return created_subscriber

    def update_subscriber(self, subscriber_id: Union[str, UUID], **kwargs: Any) -> subscriberType:
        """Update a subscriber, raise an exception if it doesn't exist."""

        if isinstance(subscriber_id, UUID):
            subscriber_id = str(subscriber_id)

        assert all(
            item in ["first_name", "last_name", "email", "phone"] for item in list(kwargs.keys())
        )
        body = {reversed_subscriber_mirror[key]: item for key, item in kwargs.items()}
        response = self.send_request(
            operation="PUT", endpoint=f"/v1/subscribers/{subscriber_id}", body=body
        )
        json_response = super().handle_response(response, "Can't update subscriber !").json()
        updated_subscriber = cast(
            subscriberType,
            {value: json_response["data"][key] for key, value in subscriber_mirror.items()},
        )
        return updated_subscriber

    def delete_subscriber(self, subscriber_id: Union[str, UUID]) -> None:
        """Delete a subscriber, raise an exception if it doesn't exist."""

        if isinstance(subscriber_id, UUID):
            subscriber_id = str(subscriber_id)

        response = self.send_request(
            operation="DELETE",
            endpoint=f"/v1/subscribers/{subscriber_id}",
        )

        super().handle_response(response, "Can't delete subscriber !").json()
