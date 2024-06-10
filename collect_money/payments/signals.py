from collects.tasks import send_email_task
from django.core.cache import caches
from django.db.models.signals import post_save
from django.dispatch import receiver
from payments.models import Payment


@receiver(post_save, sender=Payment)
def payment_post_save(sender, instance, created, **kwargs):
    """Отправка e-mail после создания платежа.
    Отправляется при создании платежа."""

    if created:
        amount = getattr(instance, "amount", None)
        user = getattr(instance, "user", None)
        email = getattr(instance.user, "email", None)
        collect = getattr(instance.collect, "name", None)
        if amount is not None and user is not None and email is not None:
            subject = "Платеж принят!"
            body = (
                f"Дорогой пользователь, {user}!\n"
                f"Ваш платёж за сбор {collect} в размере {amount} принят.\n"
                "Спасибо!"
            )
            send_email_task.delay(
                subject,
                body,
                "info@groupcollect.site",
                [
                    email,
                ],
            )

    caches["default"].clear()
