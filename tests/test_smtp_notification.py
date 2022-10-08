import os

import pytest
from pydantic import ValidationError

from accentnotifications.notifications import SmtpBackend, SmtpNotification
from accentnotifications.notifications.base import BaseNotification


def test_is_correct_subclass():
    assert issubclass(SmtpNotification, BaseNotification)


def test_valid():
    model = SmtpNotification(
        host="host",
        port=1234,
        username="username",
        password="pass",
        use_tls=True,
        starttls=False,
        timeout=0,
        fail_silently=True,
        from_address="me@email.com",
        to_address="you@email.com",
        subject="hello",
        content_text="how are you",
        content_html="<p>how are you</p>",
    )

    assert model.host == "host"
    assert model.port == 1234
    assert model.username.get_secret_value() == "username"
    assert model.password.get_secret_value() == "pass"
    assert model.use_tls is True
    assert model.starttls is False
    assert model.timeout == 0
    assert model.fail_silently is True
    assert model.from_address == "me@email.com"
    assert model.to_address == "you@email.com"
    assert model.subject == "hello"
    assert model.content_text == "how are you"
    assert model.content_html == "<p>how are you</p>"


def test_required_values():
    with pytest.raises(ValidationError) as exc_info:
        SmtpNotification()

    expected = [
        {
            "loc": ("host",),
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ("port",),
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ("from_address",),
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ("to_address",),
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ("subject",),
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ("content_text",),
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ("content_html",),
            "msg": "field required",
            "type": "value_error.missing",
        },
    ]

    assert exc_info.value.errors() == expected


def test_defaults():
    model = SmtpNotification(
        host="host",
        port=1234,
        from_address="me@email.com",
        to_address="you@email.com",
        subject="hello",
        content_text="how are you",
        content_html="<p>how are you</p>",
    )

    assert model.username is None
    assert model.password is None
    assert model.use_tls is False
    assert model.starttls is False
    assert model.timeout is None
    assert model.fail_silently is False


def test_values_from_environment():
    os.environ["NOTIFICATIONS_SMTP_HOST"] = "host"
    os.environ["NOTIFICATIONS_SMTP_PORT"] = "1234"
    os.environ["NOTIFICATIONS_SMTP_FROM_ADDRESS"] = "me@email.com"
    model = SmtpNotification(
        to_address="you@email.com",
        subject="hello",
        content_text="how are you",
        content_html="<p>how are you</p>",
    )

    assert model.host == "host"
    assert model.port == 1234
    assert model.from_address == "me@email.com"


def test_has_correct_backend():
    model = SmtpNotification(
        host="host",
        port=1234,
        from_address="me@email.com",
        to_address="you@email.com",
        subject="hello",
        content_text="how are you",
        content_html="<p>how are you</p>",
    )
    assert model.backend == SmtpBackend
