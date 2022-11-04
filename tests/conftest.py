import os

import pytest
from notification_lib.novu import Novu


@pytest.fixture
def novu():
    yield Novu(os.environ["API_KEY"], os.environ["API_URL"])
