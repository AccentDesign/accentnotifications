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
        to_number="+447777777777",
        body="body",
        base_url="http://url.com",
        account_sid="account_sid",
        auth_token="auth_token",
        fail_silently=False,
    )

    assert model.from_number == "from"
    assert model.to_number == "+447777777777"
    assert model.body == "body"
    assert model.base_url == "http://url.com"
    assert model.account_sid.get_secret_value() == "account_sid"
    assert model.auth_token.get_secret_value() == "auth_token"
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
            "loc": ("base_url",),
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
        to_number="+447777777777",
        body="body",
        base_url="http://url.com",
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
        to_number="+447777777777",
        body="body",
        base_url="http://url.com",
    )

    assert model.account_sid.get_secret_value() == "account_sid_1234"
    assert model.auth_token.get_secret_value() == "auth_token_abcd"


def test_has_correct_backend():
    model = TwilioSMSNotification(
        from_number="from",
        to_number="+447777777777",
        body="body",
        base_url="http://url.com",
        account_sid="account_sid",
        auth_token="auth_token",
    )
    assert model.backend == TwilioSMSBackend


def test_invalid():
    with pytest.raises(ValidationError) as exc_info:
        TwilioSMSNotification(
            from_number="from",
            to_number="07507788372",
            body="body",
            base_url="http://url.com",
            account_sid="account_sid",
            auth_token="auth_token",
        )

    expected = [
        {
            "loc": ("to_number",),
            "msg": 'string does not match regex "^\\+?[1-9]\\d{1,14}$"',
            "type": "value_error.str.regex",
            "ctx": {"pattern": "^\\+?[1-9]\\d{1,14}$"},
        },
    ]

    assert exc_info.value.errors() == expected
