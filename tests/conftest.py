import os
from uuid import uuid4

import pytest
from notification_lib.http_requests import HttpRequester
from notification_lib.novu import Novu


@pytest.fixture(scope="session")
def novu():
    yield Novu(os.environ["API_KEY"], os.environ["API_URL"])


@pytest.fixture(scope="session")
def created_notification_template(novu):
    novu.notification_templates_manager.create_update_notification_template(
        template_name="template name",
        steps=[
            {
                "template": {
                    "content": "content",
                    "subject": "subject",
                    "type": "in_app",
                },
                "active": True,
            }
        ],
    )
    template = novu.notification_templates_manager.get_template_by_name(
        template_name="template name"
    )
    yield
    HttpRequester.send_request(
        operation="DELETE",
        endpoint=f"/v1/notification-templates/{template['id']}",
    )


@pytest.fixture
def created_subscriber(novu):
    subscriber = novu.subscribers_manager.create_subscriber(
        subscriber_id=str(uuid4()),
        first_name="first_name",
        last_name="last_name",
        email="email@myem.fr",
        phone="0123456789",
    )
    yield subscriber
    novu.subscribers_manager.delete_subscriber(subscriber["subscriber_id"])
