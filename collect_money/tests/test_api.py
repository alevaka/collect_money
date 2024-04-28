import time
from datetime import datetime, timedelta, timezone

from django.core import mail
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from collects.models import Collect
from payments.models import Payment

overriden_settings = {
    "CELERY_TASK_EAGER_PROPAGATES": True,
    "CELERY_TASK_ALWAYS_EAGER": True,
    "CELERY_BROKER_URL": "memory://",
    "CELERY_RESULT_BACKEND": "cache+memory://",
    "EMAIL_BACKEND": "django.core.mail.backends.locmem.EmailBackend",
    "CACHES": {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        },
    },
}


class APITests(APITestCase):
    @classmethod
    @override_settings(**overriden_settings)
    def setUpTestData(cls):
        cls.user1 = User.objects.create(
            username="user1",
            first_name="User1",
            last_name="Last1",
            email="user1@example.com",
            password="Password1",
        )

        cls.token = str(AccessToken.for_user(cls.user1))
        cls.collect1 = Collect.objects.create(
            author=cls.user1,
            name="Collect1",
            cause="wed",
            description="Description1",
            goal_amount=10000,
            current_amount=0,
            bakers_count=0,
            image="",
            close_date=datetime.now(timezone.utc) + timedelta(seconds=1),
        )
        cls.collect2 = Collect.objects.create(
            author=cls.user1,
            name="Collect2",
            cause="wed",
            description="Description2",
            goal_amount=100000,
            current_amount=90000,
            bakers_count=0,
            image="",
            close_date=datetime.now(timezone.utc) + timedelta(days=1),
        )

        cls.payments = [
            Payment.objects.create(
                amount=i * 100,
                user=cls.user1,
                date=datetime.now(timezone.utc),
                collect=cls.collect1 if i % 2 else cls.collect2,
            )
            for i in range(1, 20)
        ]

    @override_settings(**overriden_settings)
    def test_show_collect(self):
        """Тест списка коллекций."""

        response = self.client.get(
            reverse(
                "collects-detail",
                args=[self.collect1.pk],
            )
            + "?page=2",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "Collect1")
        self.assertEqual(
            [x["amount"] for x in response.data.get("payments")],
            [900, 700, 500, 300, 100],
            "Проверка, что к сбору возвращаются корректные платежи "
            "с учетом пагинации",
        )
        self.assertIn(
            "Expires",
            response.headers,
            "Проверка, что в ответе есть время жизни кэша",
        )

    @override_settings(**overriden_settings)
    def test_create_collect(self):
        """Создание сбора авторизованным пользователем возвращает 201"""

        collect_data = {
            "name": "Collect2",
            "cause": "wed",
            "description": "Description1",
            "goal_amount": 10000,
            "current_amount": 0,
            "bakers_count": 0,
            "image": "",
            "close_date": str(datetime.now(timezone.utc)),
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.client.post(reverse("collects-list"), collect_data)
        self.assertEqual(response.status_code, 201)

    @override_settings(**overriden_settings)
    def test_create_collect_email(self):
        """Создание сбора приводит к отправке письма о создании"""

        collect_data = {
            "name": "Collect3",
            "cause": "wed",
            "description": "Description1",
            "goal_amount": 10000,
            "current_amount": 0,
            "bakers_count": 0,
            "image": "",
            "close_date": str(datetime.now(timezone.utc)),
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        self.client.post(reverse("collects-list"), collect_data)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Сбор Collect3 создан!")

    @override_settings(**overriden_settings)
    def test_create_payment_email(self):
        """Создание платежа приводит к отправке письма о создании"""

        payment_data = {
            "collect": 2,
            "amount": 1000,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        self.client.post(reverse("payments-list"), payment_data)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Платеж принят!")

    @override_settings(**overriden_settings)
    def test_goal_amount_email(self):
        """Достижение цели сбора приводит к отправке письма"""

        payment_data = {
            "collect": 2,
            "amount": 10000,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        self.client.post(reverse("payments-list"), payment_data)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(
            mail.outbox[0].subject, "Цель сбора Collect2 достигнута!"
        )

    @override_settings(**overriden_settings)
    def test_goal_expires(self):
        """Дата платежа не может быть позже даты закрытия сбора"""

        payment_data = {
            "collect": 1,
            "amount": 10000,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        time.sleep(2)
        response = self.client.post(reverse("payments-list"), payment_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get("non_field_errors"),
            ["Сбор уже закрыт!"]
        )

    @override_settings(**overriden_settings)
    def test_collect_not_exist(self):
        """Нельзя заплатить за несуществующий сбор"""

        payment_data = {
            "collect": 6,
            "amount": 10000,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        time.sleep(2)
        response = self.client.post(reverse("payments-list"), payment_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get("collect"),
            ['Invalid pk "6" - object does not exist.']
        )

    @override_settings(**overriden_settings)
    def test_update_cache(self):
        """Создание платежа приводит к обновлению кэша"""

        payment_data = {
            "collect": 2,
            "amount": 1000,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.client.get(
            reverse(
                "collects-detail",
                args=[self.collect2.pk],
            ),
        )
        cache_expires = response.headers.get("Expires")
        bakers_count = response.data.get("bakers_count")
        current_amount = response.data.get("current_amount")
        self.client.post(reverse("payments-list"), payment_data)
        time.sleep(1)
        response = self.client.get(
            reverse(
                "collects-detail",
                args=[self.collect2.pk],
            ),
        )
        self.assertEqual(response.data.get("bakers_count"), bakers_count + 1)
        self.assertEqual(
            response.data.get("current_amount"), current_amount + 1000
        )
        self.assertNotEqual(response.headers.get("Expires"), cache_expires)

    @override_settings(**overriden_settings)
    def test_permission_denied(self):
        """Создание сбора неавторизованным пользователем возвращает 401"""

        collect_data = {
            "name": "Collect4",
            "cause": "wed",
            "description": "Description1",
            "goal_amount": 10000,
            "current_amount": 0,
            "bakers_count": 0,
            "image": "",
            "close_date": str(datetime.now(timezone.utc)),
        }
        response = self.client.post(reverse("collects-list"), collect_data)
        self.assertEqual(response.status_code, 401)
