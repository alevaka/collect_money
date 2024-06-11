from datetime import datetime, timezone
import decimal

from payments.models import Payment
from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if isinstance(instance, Payment):
            collect_instance = instance.collect
            ret["collect"] = (
                collect_instance.name if collect_instance else None
            )
        return ret

    def validate(self, data):
        date = data['collect'].close_date
        if datetime.now(timezone.utc) > date:
            raise serializers.ValidationError("Сбор уже закрыт!")
        return data

    class Meta:
        model = Payment
        fields = [
            "amount",
            "date",
            "collect",
            "user",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
            "date": {"read_only": True},
            "amount": {
                "default": decimal.Decimal("0.00"),
                "min_value": decimal.Decimal("0.00"),
            },
        }
