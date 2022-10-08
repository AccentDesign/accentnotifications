import pytest

from accentnotifications.notifications.base import BaseBackend, BaseNotification


@pytest.mark.asyncio
async def test_send_must_be_defined():
    async with BaseBackend(BaseNotification()) as backend:
        with pytest.raises(NotImplementedError):
            await backend.send()


@pytest.mark.asyncio
async def test_defines_options():
    options = BaseNotification()
    async with BaseBackend(options) as backend:
        assert backend.options == options
