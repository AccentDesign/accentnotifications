try:
    from aiohttp import BasicAuth, ClientSession
except ImportError:  # pragma: no cover
    BasicAuth = None
    ClientSession = None

from typing import Type

from .base import BaseBackend, BaseNotification, BaseResponse


class TwilioSMSResponse(BaseResponse):
    success: bool
    status_code: int = None


class TwilioSMSNotification(BaseNotification):
    from_number: str
    to_number: str
    body: str
    account_sid: str
    auth_token: str
    fail_silently: bool = False
    response: TwilioSMSResponse = None

    class Config:
        env_prefix = "notifications_twilio_sms_"

    @property
    def backend(self) -> Type["TwilioSMSBackend"]:
        return TwilioSMSBackend


class TwilioSMSBackend(BaseBackend):
    options: TwilioSMSNotification
    connection = None

    def __init__(self, options: TwilioSMSNotification) -> None:
        super().__init__(options)

    async def send(self) -> bool:
        auth = BasicAuth(
            login=self.options.account_sid, password=self.options.auth_token
        )
        async with ClientSession(auth=auth) as connection:
            self.connection = connection
            try:
                data = {
                    "From": self.options.from_number,
                    "To": self.options.to_number,
                    "Body": self.options.body,
                }
                post_data = await self.connection.post(
                    f"https://api.twilio.com/2010-04-01/Accounts/{self.options.account_sid}/Messages.json",
                    data=data,
                )
                # Twilio uses 201 for success
                if post_data.status != 201:
                    self.options.response = TwilioSMSResponse(
                        status_code=post_data.status, success=False
                    )
                    return False
                else:
                    self.options.response = TwilioSMSResponse(
                        status_code=post_data.status, success=True
                    )
                    return True
            except Exception:
                self.options.response = TwilioSMSResponse(success=False)
                if self.options.fail_silently:
                    return False
                raise
