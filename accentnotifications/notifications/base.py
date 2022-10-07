from typing import Type

from pydantic import BaseSettings


class BaseNotification(BaseSettings):
    @property
    def backend(self) -> Type["BaseBackend"]:
        raise NotImplementedError()


class BaseBackend:
    async def send(self, options: BaseNotification):
        raise NotImplementedError()
