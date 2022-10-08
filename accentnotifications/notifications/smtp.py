from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Type

try:
    from aiosmtplib import SMTP
except ImportError:  # pragma: no cover
    SMTP = None

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
    fail_silently: bool = False
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
    options: SmtpNotification
    connection = None

    def __init__(self, options: BaseNotification) -> None:
        super().__init__(options)

        if not SMTP:  # pragma: no cover
            raise ModuleNotFoundError("python library aiosmtplib required")

    async def open(self):
        params = {
            "hostname": self.options.host,
            "port": self.options.port,
            "use_tls": self.options.use_tls and not self.options.starttls,
        }
        if self.options.timeout is not None:
            params["timeout"] = self.options.timeout

        try:
            self.connection = SMTP(**params)

            await self.connection.connect()

            if self.options.starttls:
                await self.connection.starttls()

            if self.options.username and self.options.password:
                await self.connection.login(
                    self.options.username.get_secret_value(),
                    self.options.password.get_secret_value(),
                )

            return True
        except OSError:
            if not self.options.fail_silently:
                raise

    async def close(self):
        if self.connection is None:  # pragma: no cover
            return

        try:
            await self.connection.quit()
        except Exception:
            if self.options.fail_silently:
                return
            raise
        finally:
            self.connection = None

    async def send(self):
        msg = MIMEMultipart("alternative")
        msg["From"] = self.options.from_address
        msg["To"] = self.options.to_address
        msg["Subject"] = self.options.subject
        if self.options.content_text:
            msg.attach(MIMEText(self.options.content_text, "plain", _charset="utf-8"))
        if self.options.content_html:
            msg.attach(MIMEText(self.options.content_html, "html", _charset="utf-8"))

        try:
            await self.connection.send_message(msg)
        except Exception:
            if self.options.fail_silently:
                return False
            raise

        return True
