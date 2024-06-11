import decimal

from collects.models import Collect
from payments.serializers import PaymentSerializer
from rest_framework import pagination, serializers


PAYMENTS_PAGE_SIZE = 5


class PaymentPagination(pagination.PageNumberPagination):
    page_size = PAYMENTS_PAGE_SIZE
    page_query_param = "page"


class CollectListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Collect
        fields = [
            "name",
            "cause",
            "description",
            "goal_amount",
            "image",
            "close_date",
            "author",
            "current_amount",
            "bakers_count",
        ]


class CollectSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    payments = serializers.SerializerMethodField("get_paginated_payments")

    def get_paginated_payments(self, obj) -> list:
        payments = obj.payments.all()
        paginator = PaymentPagination()
        page = paginator.paginate_queryset(payments, self.context["request"])
        serializer = PaymentSerializer(
            page,
            many=True,
            context={"request": self.context["request"]},
        )
        return serializer.data

    class Meta:
        model = Collect
        fields = [
            "name",
            "cause",
            "description",
            "goal_amount",
            "image",
            "close_date",
            "author",
            "current_amount",
            "bakers_count",
            "payments",
        ]
        extra_kwargs = {
            "current_amount": {"read_only": True},
            "bakers_count": {"read_only": True},
            "payments": {"read_only": True},
            "goal_amount": {
                "default": decimal.Decimal("0.00"),
                "min_value": decimal.Decimal("0.00"),
            },
        }
