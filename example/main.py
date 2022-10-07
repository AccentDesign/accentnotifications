import asyncio
import os

from accentnotifications.manager import NotificationManager
from accentnotifications.notifications import SmtpNotification, TwilioNotification

# create the loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# start a mailhog docker container
# docker run -p 8025:8025 -p 1025:1025 mailhog/mailhog

# setting config defaults
os.environ["NOTIFICATIONS_SMTP_HOST"] = "localhost"
os.environ["NOTIFICATIONS_SMTP_PORT"] = "1025"
os.environ["NOTIFICATIONS_SMTP_FROM_ADDRESS"] = "me@example.com"

# send an email
notification = SmtpNotification(
    to_address="you@example.com",
    subject="Hi",
    content_text="Hi!\nHow u doin?",
    content_html="<h1>Hi!</h1><p>How u doin?</p>",
)
loop.run_until_complete(NotificationManager().send(notification))

# send an sms
notification = TwilioNotification(
    number="07917759123",
)
loop.run_until_complete(NotificationManager().send(notification))
