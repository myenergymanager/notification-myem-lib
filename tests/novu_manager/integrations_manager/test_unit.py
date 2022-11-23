from notification_lib.http_requests import HttpRequester


class TestIntegrationsManager:
    def test_get_non_existent_integration(self, novu):
        assert (
            novu.integrations_manager.get_integration_id_by_provider_and_channel(
                provider="132456", channel="1324"
            )
            is None
        )

    def test_create_integration(self, novu, created_integration):

        assert isinstance(
            novu.integrations_manager.get_integration_id_by_provider_and_channel(
                provider="fcm", channel="channel"
            ),
            str,
        )

    def test_update_integration(self, novu, created_integration):
        novu.integrations_manager.create_update_integration(
            channel="channel", provider="fcm", credentials={"serviceAccount": "updated testing"}
        )
        response = HttpRequester.send_request(operation="GET", endpoint="/v1/integrations")
        integrations = HttpRequester.handle_response(response, "").json()["data"]
        for integration in integrations:
            if integration["channel"] == "channel" and integration["providerId"] == "fcm":
                assert integration["credentials"] == {"serviceAccount": "updated testing"}
