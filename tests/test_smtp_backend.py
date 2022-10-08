from email.message import EmailMessage

import pytest

from accentnotifications.notifications import SmtpBackend, SmtpNotification
from accentnotifications.notifications.base import BaseBackend


def get_email():
    email = EmailMessage()
    email["Subject"] = "Subject"
    email["From"] = "me@email.com"
    email["To"] = "you@email.com"
    email.set_content("Hello")
    return email


TEST_EMAIL = {
    "host": "host",
    "port": 1234,
    "email": get_email(),
}


class MockSMTP:
    def __init__(self, **kwargs):
        pass

    async def connect(self):
        pass

    async def starttls(self):
        pass

    async def login(self, username, password):
        pass

    async def send_message(self, msg):
        return msg

    async def quit(self):
        pass


class MockSMTPConnError(MockSMTP):
    async def connect(self):
        raise OSError()

    async def quit(self):
        raise OSError()


class MockSMTPSendError(MockSMTP):
    async def send_message(self, msg):
        raise OSError()


def test_is_correct_subclass():
    assert issubclass(SmtpBackend, BaseBackend)


@pytest.mark.asyncio
async def test_connection(mocker):
    mock = mocker.patch(
        "accentnotifications.notifications.smtp.SMTP", return_value=MockSMTP()
    )
    notification = SmtpNotification(**TEST_EMAIL)
    async with SmtpBackend(notification) as backend:
        mock.assert_called_once_with(hostname="host", port=1234, use_tls=False)
        assert backend.connection is not None


@pytest.mark.asyncio
async def test_connection_fail_silently_true(mocker):
    mock = mocker.patch(
        "accentnotifications.notifications.smtp.SMTP", return_value=MockSMTPConnError()
    )
    notification = SmtpNotification(fail_silently=True, **TEST_EMAIL)
    async with SmtpBackend(notification) as backend:
        mock.assert_called_once_with(hostname="host", port=1234, use_tls=False)
        assert backend.connection is not None


@pytest.mark.asyncio
async def test_connection_fail_silently_false(mocker):
    mocker.patch(
        "accentnotifications.notifications.smtp.SMTP", return_value=MockSMTPConnError()
    )
    notification = SmtpNotification(fail_silently=False, **TEST_EMAIL)
    with pytest.raises(OSError):
        async with SmtpBackend(notification):
            pass


@pytest.mark.asyncio
async def test_connection_timeout(mocker):
    mock = mocker.patch(
        "accentnotifications.notifications.smtp.SMTP", return_value=MockSMTP()
    )
    notification = SmtpNotification(timeout=10, **TEST_EMAIL)
    async with SmtpBackend(notification):
        mock.assert_called_once_with(
            hostname="host", port=1234, use_tls=False, timeout=10
        )


@pytest.mark.asyncio
async def test_starttls(mocker):
    mock = mocker.patch(
        "accentnotifications.notifications.smtp.SMTP", return_value=MockSMTP()
    )
    notification = SmtpNotification(starttls=True, **TEST_EMAIL)
    spy = mocker.spy(mock.return_value, "starttls")
    async with SmtpBackend(notification):
        spy.assert_called_once()


@pytest.mark.asyncio
async def test_login(mocker):
    mock = mocker.patch(
        "accentnotifications.notifications.smtp.SMTP", return_value=MockSMTP()
    )
    notification = SmtpNotification(username="me", password="pass", **TEST_EMAIL)
    spy = mocker.spy(mock.return_value, "login")
    async with SmtpBackend(notification):
        spy.assert_called_once_with("me", "pass")


@pytest.mark.asyncio
async def test_send(mocker):
    mock = mocker.patch(
        "accentnotifications.notifications.smtp.SMTP", return_value=MockSMTP()
    )
    notification = SmtpNotification(username="me", password="pass", **TEST_EMAIL)
    spy = mocker.spy(mock.return_value, "send_message")
    async with SmtpBackend(notification) as backend:
        assert await backend.send() is True
        spy.assert_called_once()


@pytest.mark.asyncio
async def test_send_fail_silently_true(mocker):
    mocker.patch(
        "accentnotifications.notifications.smtp.SMTP", return_value=MockSMTPSendError()
    )
    notification = SmtpNotification(fail_silently=True, **TEST_EMAIL)
    async with SmtpBackend(notification) as backend:
        assert await backend.send() is False


@pytest.mark.asyncio
async def test_send_fail_silently_false(mocker):
    mocker.patch(
        "accentnotifications.notifications.smtp.SMTP", return_value=MockSMTPSendError()
    )
    notification = SmtpNotification(fail_silently=False, **TEST_EMAIL)
    async with SmtpBackend(notification) as backend:
        with pytest.raises(OSError):
            assert await backend.send() is False
