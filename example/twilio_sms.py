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
    # To Number in E.164 Format
    # From Number in E.164 format OR alphanumeric if enabled in account
    sms = {
        "to_number": "+447777777777",
        "from_number": "+441111111111",
        "body": "Body Text",
        "base_url": "https://api.twilio.com/2010-04-01",
    }
    return sms


async def twilio_sms():
    await asyncio.gather(
        send(TwilioSMSNotification(**options())),
    )


# run all
asyncio.run(twilio_sms())
