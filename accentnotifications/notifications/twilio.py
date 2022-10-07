from typing import Type

from .base import BaseBackend, BaseNotification


class TwilioNotification(BaseNotification):
    number: str

    class Config:
        env_prefix = "notifications_twilio_"

    @property
    def backend(self) -> Type["TwilioBackend"]:
        return TwilioBackend


class TwilioBackend(BaseBackend):
    options: TwilioNotification

    async def send(self):
        print(self.options)
