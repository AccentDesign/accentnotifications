import pytest

from accentnotifications.notifications import TwilioSMSBackend, TwilioSMSNotification
from accentnotifications.notifications.base import BaseBackend

TEST_TWILIO_SMS = {
    "account_sid": "account_sid",
    "auth_token": "auth_token",
    "to_number": "To Number in E.164 Format",
    "from_number": "From Number in E.164 format OR alphanumeric if enabled in account",
    "body": "Body Text",
}


class MockSMSResponse:
    status = None

    def __init__(self, status):
        self.status = status


class MockSMS:
    async def __aenter__(self):
        return self

    async def post(self, url, *, data, **kwargs):
        return MockSMSResponse(201)

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass


class MockFailSMS(MockSMS):
    async def post(self, url, *, data, **kwargs):
        return MockSMSResponse(400)


class MockExceptSMS(MockSMS):
    async def post(self, url, *, data, **kwargs):
        raise ValueError()


def test_is_correct_subclass():
    assert issubclass(TwilioSMSBackend, BaseBackend)


@pytest.mark.asyncio
async def test_send(mocker):
    mocker.patch(
        "accentnotifications.notifications.twilio_sms.ClientSession",
        return_value=MockSMS(),
    )
    notification = TwilioSMSNotification(**TEST_TWILIO_SMS)
    async with TwilioSMSBackend(notification) as backend:
        assert await backend.send() is True
    # check the response
    assert notification.response.success is True


@pytest.mark.asyncio
async def test_send_fail_silently_true(mocker):
    mocker.patch(
        "accentnotifications.notifications.twilio_sms.ClientSession",
        return_value=MockFailSMS(),
    )
    notification = TwilioSMSNotification(fail_silently=True, **TEST_TWILIO_SMS)
    async with TwilioSMSBackend(notification) as backend:
        assert await backend.send() is False
    # check the response
    assert notification.response.success is False


@pytest.mark.asyncio
async def test_send_fail_silently_false(mocker):
    mocker.patch(
        "accentnotifications.notifications.twilio_sms.ClientSession",
        return_value=MockExceptSMS(),
    )
    notification = TwilioSMSNotification(fail_silently=False, **TEST_TWILIO_SMS)
    async with TwilioSMSBackend(notification) as backend:
        with pytest.raises(Exception):
            assert await backend.send() is False
    # check the response
    assert notification.response.success is False
