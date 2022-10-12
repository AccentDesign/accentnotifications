import os

import pytest
from pydantic import ValidationError

from accentnotifications.notifications import TwilioSMSBackend, TwilioSMSNotification
from accentnotifications.notifications.base import BaseNotification


def test_is_correct_subclass():
    assert issubclass(TwilioSMSNotification, BaseNotification)


def test_valid():
    model = TwilioSMSNotification(
        from_number="from",
        to_number="to",
        body="body",
        account_sid="account_sid",
        auth_token="auth_token",
        fail_silently=False,
    )

    assert model.from_number == "from"
    assert model.to_number == "to"
    assert model.body == "body"
    assert model.account_sid == "account_sid"
    assert model.auth_token == "auth_token"
    assert model.fail_silently is False


def test_required_values():
    with pytest.raises(ValidationError) as exc_info:
        TwilioSMSNotification()

    expected = [
        {
            "loc": ("from_number",),
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ("to_number",),
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ("body",),
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ("account_sid",),
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ("auth_token",),
            "msg": "field required",
            "type": "value_error.missing",
        },
    ]

    assert exc_info.value.errors() == expected


def test_defaults():
    model = TwilioSMSNotification(
        from_number="from",
        to_number="to",
        body="body",
        account_sid="account_sid",
        auth_token="auth_token",
    )

    assert model.fail_silently is False
    assert model.response is None


def test_values_from_environment():
    os.environ["NOTIFICATIONS_TWILIO_SMS_ACCOUNT_SID"] = "account_sid_1234"
    os.environ["NOTIFICATIONS_TWILIO_SMS_AUTH_TOKEN"] = "auth_token_abcd"
    model = TwilioSMSNotification(
        from_number="from",
        to_number="to",
        body="body",
    )

    assert model.account_sid == "account_sid_1234"
    assert model.auth_token == "auth_token_abcd"


def test_has_correct_backend():
    model = TwilioSMSNotification(
        from_number="from",
        to_number="to",
        body="body",
        account_sid="account_sid",
        auth_token="auth_token",
    )
    assert model.backend == TwilioSMSBackend
