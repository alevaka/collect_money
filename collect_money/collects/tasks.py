from django.core import mail
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def send_email_task(subject, body, email_from, list_to):
    with mail.get_connection() as connection:
        mail.EmailMessage(
            subject,
            body,
            email_from,
            list_to,
            connection=connection,
        ).send()
