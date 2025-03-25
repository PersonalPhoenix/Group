import logging
import smtplib

from backend.config import settings
from backend.core.adapters.notifications import AbstractNotifications

logger = logging.getLogger(__name__)


class EmailNotifications(AbstractNotifications):
    def __init__(self, smpt_host=settings.EMAIL_HOST, smpt_port=settings.EMAIL_PORT):
        if smpt_host and smpt_port:
            self.server = smtplib.SMTP(smpt_host, smpt_port)
            self.server.noop()
        else:
            logger.debug('Email notification service is not configured')

    def send(self, destination, message):
        msg = f'Тема: уведомление сервиса\n{message}'
        self.server.sendmail(
            from_addr=settings.EMAIL_HOST_EMAIL,
            to_addrs=[destination],
            msg=msg,
        )
