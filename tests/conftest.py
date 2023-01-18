import os
from uuid import uuid4

import pytest
from notification_lib.http_requests import HttpRequester
from notification_lib.novu import Novu


@pytest.fixture(scope="session")
def novu():
    yield Novu(
        os.environ["API_KEY"],
        os.environ["API_URL"],
        os.environ["NOVU_ADMIN_EMAIL"],
        os.environ["NOVU_ADMIN_PASSWORD"],
        os.environ["API_URL_FOR_GENERIC_NOVU"],
        os.environ["ADMIN_EMAIL_FOR_GENERIC_NOVU"],
        os.environ["ADMIN_PASSWORD_FOR_GENERIC_NOVU"],
    )


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


@pytest.fixture
def created_integration(novu):
    novu.integrations_manager.create_update_integration(
        channel="channel", provider="fcm", credentials={"serviceAccount": "testing"}
    )
    integration_id = novu.integrations_manager.get_integration_id_by_provider_and_channel(
        provider="fcm", channel="channel"
    )
    yield
    HttpRequester.send_request(operation="DELETE", endpoint=f"/v1/integrations/{integration_id}")
