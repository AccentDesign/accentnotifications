import asyncio
import os
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from accentnotifications.manager import NotificationManager
from accentnotifications.notifications import SmtpNotification

# start a mailhog docker container
# docker run -p 8025:8025 -p 1025:1025 mailhog/mailhog

# create the loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# setting config defaults
os.environ["NOTIFICATIONS_SMTP_HOST"] = "localhost"
os.environ["NOTIFICATIONS_SMTP_PORT"] = "1025"
os.environ["NOTIFICATIONS_SMTP_FAIL_SILENTLY"] = "True"


async def send(notification):
    await NotificationManager().send(notification)
    print(notification.response)


def plain():
    msg = EmailMessage()
    msg["Subject"] = "Hi"
    msg["From"] = "me@email.com"
    msg["To"] = "you@email.com"
    msg.set_content("How are you doing?")
    return msg


def html():
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Hi"
    msg["From"] = "me@email.com"
    msg["To"] = "you@email.com"
    msg.attach(MIMEText("How are you doing?", "plain", _charset="utf-8"))
    msg.attach(MIMEText("<p>How are you doing?</p>", "html", _charset="utf-8"))
    return msg


async def emails():
    await asyncio.gather(
        send(SmtpNotification(email=plain())),
        send(SmtpNotification(email=html())),
    )


# run all
asyncio.run(emails())
