from accentnotifications.notifications.base import BaseNotification


class NotificationManager:
    async def send(self, options: BaseNotification):
        await options.backend().send(options)
