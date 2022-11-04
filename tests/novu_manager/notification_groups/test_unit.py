import pytest


class TestNotificationGroupsManager:
    @pytest.fixture
    def created_notification_group(self, novu):
        created_notification_template = novu.notification_groups_manager.create_notification_group(
            name="notification_group"
        )
        yield created_notification_template

    def test_create_and_get_notification_group(self, novu, created_notification_group):
        assert isinstance(
            novu.notification_groups_manager.get_notification_group_id_by_name(
                name="notification_group"
            ),
            str,
        )

    def test_get_notification_group_not_found(self, novu):
        assert (
            novu.notification_groups_manager.get_notification_group_id_by_name(name="77777") is None
        )
