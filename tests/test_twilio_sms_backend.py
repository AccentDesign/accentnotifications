import pytest

from accentnotifications.notifications import TwilioSMSBackend, TwilioSMSNotification
from accentnotifications.notifications.base import BaseBackend

TEST_TWILIO_SMS = {
    "account_sid": "account_sid",
    "auth_token": "auth_token",
    "to_number": "To Number in E.164 Format",
    "from_number": "From Number in E.164 format OR alphanumeric if enabled in account",
    "body": "Body Text",
    "base_url": "Base url",
}


class MockSMSResponse:
    status = None
    headers = {"Twilio-Request-Id": "request_id"}

    def __init__(self, status):
        self.status = status

    async def json(self):
        return {"message": "message"}


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
    mock = mocker.patch(
        "accentnotifications.notifications.twilio_sms.ClientSession",
        return_value=MockSMS(),
    )
    notification = TwilioSMSNotification(**TEST_TWILIO_SMS)
    spy = mocker.spy(mock.return_value, "post")
    async with TwilioSMSBackend(notification) as backend:
        assert await backend.send() is True
        spy.assert_called_once()
    # check the response
    assert notification.response.success is True
    assert notification.response.status_code == 201
    assert notification.response.request_id is not None
    assert notification.response.message is not None


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
    assert notification.response.status_code != 201
    assert notification.response.request_id is not None
    assert notification.response.message is not None


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
    assert notification.response.status_code != 201
    assert notification.response.request_id is None
    assert notification.response.message is None
