from typing import Type

import pytest

from accentnotifications.manager import NotificationManager
from accentnotifications.notifications.base import BaseBackend, BaseNotification


class MyNotification(BaseNotification):
    name: str

    @property
    def backend(self) -> Type["MyBackend"]:
        return MyBackend


class MyBackend(BaseBackend):
    options: MyNotification

    async def send(self):
        # do stuff with self.option
        pass


@pytest.mark.asyncio
async def test_send_with_custom_notification(mocker):
    notification = MyNotification(name="me")
    spy = mocker.spy(MyBackend, "send")
    await NotificationManager().send(notification)
    spy.assert_called_once()
