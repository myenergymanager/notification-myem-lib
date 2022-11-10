from uuid import uuid4

import pytest
from notification_lib.exceptions import NotificationException


class TestSubscribersManager:
    def test_subscriber_creation(self, novu, created_subscriber):
        subscriber = novu.subscribers_manager.get_subscriber(
            subscriber_id=created_subscriber["subscriber_id"]
        )
        assert subscriber["first_name"] == "first_name"
        assert subscriber["last_name"] == "last_name"
        assert subscriber["email"] == "email@myem.fr"
        assert subscriber["phone"] == "0123456789"
        assert subscriber["channels"] == []

    def test_get_subscriber(self, novu, created_subscriber):
        subscriber = novu.subscribers_manager.get_subscriber(created_subscriber["subscriber_id"])
        assert subscriber["subscriber_id"] == created_subscriber["subscriber_id"]
        assert subscriber["first_name"] == created_subscriber["first_name"]
        assert subscriber["last_name"] == created_subscriber["last_name"]
        assert subscriber["email"] == created_subscriber["email"]
        assert subscriber["phone"] == created_subscriber["phone"]
        assert subscriber["channels"] == created_subscriber["channels"]

    def test_delete_subscriber(self, novu):
        subscriber = novu.subscribers_manager.create_subscriber(
            subscriber_id=str(uuid4()),
            first_name="first_name",
            last_name="last_name",
            email="email@myem.fr",
            phone="0123456789",
        )
        novu.subscribers_manager.delete_subscriber(subscriber["subscriber_id"])
        assert novu.subscribers_manager.get_subscriber(subscriber["subscriber_id"]) is None

    def test_update_subscriber_one_field(self, novu, created_subscriber):
        novu.subscribers_manager.update_subscriber(
            subscriber_id=created_subscriber["subscriber_id"], first_name="updated first_name"
        )
        updated_subscriber = novu.subscribers_manager.get_subscriber(
            created_subscriber["subscriber_id"]
        )
        assert updated_subscriber["subscriber_id"] == created_subscriber["subscriber_id"]
        assert updated_subscriber["first_name"] == "updated first_name"
        assert updated_subscriber["last_name"] == "last_name"
        assert updated_subscriber["email"] == "email@myem.fr"
        assert updated_subscriber["phone"] == "0123456789"
        assert updated_subscriber["channels"] == []

    def test_update_all_fields_of_a_subscriber(self, novu, created_subscriber):
        novu.subscribers_manager.update_subscriber(
            subscriber_id=created_subscriber["subscriber_id"],
            first_name="updated first_name",
            last_name="updated last_name",
            email="updatedemail@myem.fr",
            phone="6545246454",
        )
        updated_subscriber = novu.subscribers_manager.get_subscriber(
            created_subscriber["subscriber_id"]
        )
        assert updated_subscriber["subscriber_id"] == created_subscriber["subscriber_id"]
        assert updated_subscriber["first_name"] == "updated first_name"
        assert updated_subscriber["last_name"] == "updated last_name"
        assert updated_subscriber["email"] == "updatedemail@myem.fr"
        assert updated_subscriber["phone"] == "6545246454"
        assert updated_subscriber["channels"] == []

    def test_get_subscribers_using_pagination(self, novu, created_subscriber):
        subscribers = novu.subscribers_manager.get_subscribers(page=1)
        assert subscribers["size"] == 10
        assert subscribers["total"] == 1
        assert subscribers["page"] == 1
        assert subscribers["items"][0]["subscriber_id"] == created_subscriber["subscriber_id"]
        assert subscribers["items"][0]["first_name"] == created_subscriber["first_name"]
        assert subscribers["items"][0]["last_name"] == created_subscriber["last_name"]
        assert subscribers["items"][0]["email"] == created_subscriber["email"]
        assert subscribers["items"][0]["phone"] == created_subscriber["phone"]
        assert subscribers["items"][0]["channels"] == created_subscriber["channels"]

    def test_get_all_subscribers(self, novu):
        subs = []
        ids = [str(i) for i in range(12)]
        for i in ids:
            subs.append(
                novu.subscribers_manager.create_subscriber(
                    subscriber_id=i,
                    first_name=f"first_name{i}",
                    last_name=f"last_name{i}",
                    email=f"email{i}@myem.fr",
                    phone=f"0123456789{i}",
                )
            )
        subscribers = novu.subscribers_manager.get_subscribers()
        assert len(subscribers) == 12
        for sub in subs:
            novu.subscribers_manager.delete_subscriber(sub["subscriber_id"])

    def test_get_subscribers_with_specefic_ids(self, novu):
        subs = []
        for i in range(3):
            subs.append(
                novu.subscribers_manager.create_subscriber(
                    subscriber_id=str(i),
                    first_name=f"first_name{str(i)}",
                    last_name=f"last_name{str(i)}",
                    email=f"email{str(i)}@myem.fr",
                    phone=f"0123456789{str(i)}",
                )
            )
        subscribers = novu.subscribers_manager.get_subscribers(subscribers_ids=["0", "1"])
        assert len(subscribers) == 2
        for i, subscriber in enumerate(subscribers):
            assert subscriber["subscriber_id"] in ["0", "1"]
        for sub in subs:
            novu.subscribers_manager.delete_subscriber(sub["subscriber_id"])

    # -------------------
    # non-happy flow
    # -------------------

    def test_get_subscriber_not_found(self, novu):
        subscriber = novu.subscribers_manager.get_subscriber("999999999")
        assert subscriber is None

    def test_create_existed_subscriber(self, novu, created_subscriber):
        novu.subscribers_manager.create_subscriber(
            subscriber_id=created_subscriber["subscriber_id"],
            first_name=created_subscriber["first_name"],
            last_name=created_subscriber["last_name"],
            email=created_subscriber["email"],
            phone=created_subscriber["phone"],
        )
        assert len(novu.subscribers_manager.get_subscribers()) == 1

    def test_get_subscribers_when_they_does_not_exists(self, novu):
        assert novu.subscribers_manager.get_subscribers() == []
        assert novu.subscribers_manager.get_subscribers(page=1) == {
            "items": [],
            "page": 1,
            "size": 10,
            "total": 0,
        }
        assert novu.subscribers_manager.get_subscribers(subscribers_ids=["11", "22"]) == []

    def test_update_subscriber_does_not_exists(self, novu):
        with pytest.raises(NotificationException):
            novu.subscribers_manager.update_subscriber(
                subscriber_id=uuid4(),
                first_name="first_name",
                last_name="last_name",
                email="email@myem.fr",
                phone="0123456789",
            )

    def test_update_subscriber_with_not_allowed_fields(self, novu):
        with pytest.raises(NotificationException):
            novu.subscribers_manager.update_subscriber(subscriber_id=uuid4(), address="address")

    def test_delete_subscriber_does_not_exists(self, novu):
        with pytest.raises(NotificationException):
            novu.subscribers_manager.delete_subscriber(subscriber_id=uuid4())
