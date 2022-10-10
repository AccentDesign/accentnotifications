from email.message import EmailMessage, Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pytest
from pydantic import BaseModel

from accentnotifications.types import Email


def basic():
    msg = EmailMessage()
    msg["Subject"] = "Hi"
    msg["From"] = "me@email.com"
    msg["To"] = "you@email.com"
    msg.set_content("How you doin?")
    return msg


def alternative():
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Hi"
    msg["From"] = "me@email.com"
    msg["To"] = "you@email.com"
    msg.attach(MIMEText("How you doin?", "plain", _charset="utf-8"))
    msg.attach(MIMEText("<p>How you doin?</p>", "html", _charset="utf-8"))
    return msg


@pytest.mark.parametrize(
    "email",
    [
        basic(),
        basic().as_bytes(),
        basic().as_string(),
        alternative(),
        alternative().as_bytes(),
        alternative().as_string(),
    ],
)
def test_email_success(email):
    class Model(BaseModel):
        e: Email

    model = Model(e=email)
    assert isinstance(model.e, Message)
