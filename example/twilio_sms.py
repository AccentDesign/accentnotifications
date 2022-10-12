import asyncio
import os

from accentnotifications.manager import NotificationManager
from accentnotifications.notifications import TwilioSMSNotification

# create the loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# setting config defaults
os.environ["NOTIFICATIONS_TWILIO_SMS_ACCOUNT_SID"] = "ACCOUNT SID HERE"
os.environ["NOTIFICATIONS_TWILIO_SMS_AUTH_TOKEN"] = "ACCOUNT AUTH TOKEN HERE"


async def send(notification):
    await NotificationManager().send(notification)
    print(notification.response)


def options():
    sms = {
        "to_number": "To Number in E.164 Format",
        "from_number": "From Number in E.164 format OR alphanumeric if enabled in account",
        "body": "Body Text",
    }
    return sms


async def twilio_sms():
    await asyncio.gather(
        send(TwilioSMSNotification(**options())),
    )


# run all
asyncio.run(twilio_sms())
