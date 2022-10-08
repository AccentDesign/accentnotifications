import pytest
from pydantic import BaseSettings

from accentnotifications.notifications.base import BaseNotification


def test_is_correct_subclass():
    assert issubclass(BaseNotification, BaseSettings)


def test_backend_must_be_defined():
    notification = BaseNotification()
    with pytest.raises(NotImplementedError):
        assert notification.backend is not None
