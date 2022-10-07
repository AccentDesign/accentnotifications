from typing import Type

from pydantic import BaseSettings


class BaseNotification(BaseSettings):
    @property
    def backend(self) -> Type["BaseBackend"]:
        raise NotImplementedError()


class BaseBackend:
    options: BaseNotification

    def __init__(self, options: BaseNotification) -> None:
        self.options = options

    async def __aenter__(self):
        try:
            await self.open()
        except Exception:
            await self.close()
            raise
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def open(self):
        pass

    async def close(self):
        pass

    async def send(self):
        raise NotImplementedError()
