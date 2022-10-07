from typing import Optional, Type

from pydantic import EmailStr, SecretStr

from .base import BaseBackend, BaseNotification


class SmtpNotification(BaseNotification):
    host: str
    port: int
    username: Optional[SecretStr] = None
    password: Optional[SecretStr] = None
    use_tls: bool = False
    starttls: bool = False
    timeout: Optional[int] = None
    from_address: EmailStr
    to_address: EmailStr
    subject: str
    content_text: str
    content_html: str

    class Config:
        env_prefix = "notifications_smtp_"

    @property
    def backend(self) -> Type["SmtpBackend"]:
        return SmtpBackend


class SmtpBackend(BaseBackend):
    async def send(self, options: SmtpNotification):
        print(options)
