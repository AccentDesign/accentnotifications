import pytest
from pydantic import BaseSettings

from accentnotifications.notifications.base import BaseNotification, BaseResponse


def test_is_correct_subclass():
    assert issubclass(BaseNotification, BaseSettings)


def test_backend_must_be_defined():
    notification = BaseNotification()
    with pytest.raises(NotImplementedError):
        assert notification.backend is not None


def test_response():
    notification = BaseNotification()
    assert notification.response is None

    response = BaseResponse(success=True)
    notification = BaseNotification(response=response)
    assert notification.response == response
