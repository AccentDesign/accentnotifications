import asyncio
import os

from accentnotifications.manager import NotificationManager
from accentnotifications.notifications import SmtpNotification, TwilioNotification

# create the loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# setting config defaults
os.environ["NOTIFICATIONS_SMTP_HOST"] = "mail"
os.environ["NOTIFICATIONS_SMTP_PORT"] = "1025"
os.environ["NOTIFICATIONS_SMTP_FROM_ADDRESS"] = "from@example.com"

# send an email
opts = SmtpNotification(
    to_address="stu@foo.com",
    subject="Hi",
    content_text="...",
    content_html="...",
)
loop.run_until_complete(NotificationManager().send(opts))

# send an sms
opts = TwilioNotification(
    number="07917759123",
)
loop.run_until_complete(NotificationManager().send(opts))
