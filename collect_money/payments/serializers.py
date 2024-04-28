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
                "default": 0,
                "min_value": 0,
            },
        }
