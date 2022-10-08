import asyncio
import os
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

# send an EmailMessage
email = EmailMessage()
email['Subject'] = 'Hi'
email['From'] = "me@email.com"
email['To'] = "you@email.com"
email.set_content("How you doin?")
notification = SmtpNotification(email=email)
loop.run_until_complete(NotificationManager().send(notification))

# send an MIMEMultipart
email = MIMEMultipart("alternative")
email['Subject'] = 'Hi'
email['From'] = "me@email.com"
email['To'] = "you@email.com"
email.attach(MIMEText("How you doin?", "plain", _charset="utf-8"))
email.attach(MIMEText("<p>How you doin?</p>", "html", _charset="utf-8"))
notification = SmtpNotification(email=email)
loop.run_until_complete(NotificationManager().send(notification))

print(notification.dict())

# send an sms
notification = TwilioNotification(
    number="07917759123",
)
loop.run_until_complete(NotificationManager().send(notification))
