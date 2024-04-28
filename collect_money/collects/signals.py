from django.core.cache import caches
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from collects.tasks import send_email_task
from collects.models import Collect

from django.db.models.expressions import CombinedExpression


@receiver(post_save, sender=Collect)
def collect_post_save(sender, instance, created, **kwargs):
    """Отправка e-mail после создания/изменения сбора.
    Отправляется при создании сбора и при достижении цели."""

    if created:
        goal_amount = getattr(instance, "goal_amount", None)
        name = getattr(instance, "name", None)
        author = getattr(instance, "author", None)
        email = getattr(instance.author, "email", None)
        if (
            goal_amount is not None
            and name is not None
            and author is not None
            and email is not None
        ):
            subject = f"Сбор {name} создан!"
            body = (
                f"Дорогой пользователь, {author}!\n"
                f"Вы создали сбор {name} с целевой суммой {goal_amount}."
            )
            send_email_task.delay(
                subject,
                body,
                "info@groupcollect.site",
                [
                    email,
                ],
            )

    current_amount = getattr(instance, "current_amount", None)
    payment_value = None
    if isinstance(current_amount, CombinedExpression):
        if len(current_amount.get_source_expressions()) > 1:
            payment_value = int(
                current_amount.get_source_expressions()[1].value
            )
            instance.refresh_from_db()
            current_amount = getattr(instance, "current_amount", None)

    goal_amount = getattr(instance, "goal_amount", None)
    if current_amount is not None and goal_amount is not None:

        if (
            payment_value is not None
            and current_amount - payment_value <= goal_amount
            and goal_amount <= current_amount
            or payment_value is None
            and current_amount >= goal_amount
        ):
            name = getattr(instance, "name", None)
            author = getattr(instance, "author", None)
            email = getattr(instance.author, "email", None)
            if name is not None and author is not None and email is not None:
                subject = f"Цель сбора {name} достигнута!"
                body = (
                    f"Дорогой пользователь, {author}! Поздравляем!"
                    f"Ваш сбор {name} собрал {current_amount}  "
                    f"из требуемых {goal_amount}!"
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


@receiver(post_delete, sender=Collect)
def collect_post_delete(sender, instance, **kwargs):
    caches["default"].clear()
