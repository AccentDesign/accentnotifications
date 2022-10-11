import json
import os
from email.message import EmailMessage

import pytest
from pydantic import ValidationError

from accentnotifications.notifications import SmtpBackend, SmtpNotification
from accentnotifications.notifications.base import BaseNotification


def get_email():
    email = EmailMessage()
    email["Subject"] = "Subject"
    email["From"] = "me@email.com"
    email["To"] = "you@email.com"
    email.set_content("Hello")
    return email


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
        email=get_email(),
    )

    assert model.host == "host"
    assert model.port == 1234
    assert model.username.get_secret_value() == "username"
    assert model.password.get_secret_value() == "pass"
    assert model.use_tls is True
    assert model.starttls is False
    assert model.timeout == 0
    assert model.fail_silently is True
    assert isinstance(model.email, EmailMessage)


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
            "loc": ("email",),
            "msg": "field required",
            "type": "value_error.missing",
        },
    ]

    assert exc_info.value.errors() == expected


def test_defaults():
    model = SmtpNotification(
        host="host",
        port=1234,
        email=get_email(),
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
    model = SmtpNotification(
        email=get_email(),
    )

    assert model.host == "host"
    assert model.port == 1234


def test_has_correct_backend():
    model = SmtpNotification(
        host="host",
        port=1234,
        email=get_email(),
    )
    assert model.backend == SmtpBackend


def test_json():
    model = SmtpNotification(
        host="host",
        port=1234,
        username="username",
        password="pass",
        use_tls=True,
        starttls=False,
        timeout=0,
        fail_silently=True,
        email=get_email(),
    )
    j = model.json()
    assert j == json.dumps(
        {
            "response": None,
            "host": "host",
            "port": 1234,
            "username": "**********",
            "password": "**********",
            "use_tls": True,
            "starttls": False,
            "timeout": 0,
            "fail_silently": True,
            "email": get_email().as_string(),
        }
    )
