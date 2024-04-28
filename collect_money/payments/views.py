from datetime import datetime, timezone
from django.db.models import F
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from collects.models import Collect
from payments.models import Payment
from payments.serializers import PaymentSerializer


class CreateRetrieveViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pass


class PaymentViewSet(CreateRetrieveViewSet):
    """Вьюсет для модели Payment"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Создание нового платежа"""

        user = self.request.user
        serializer.is_valid(raise_exception=True)
        collect_id = serializer.initial_data["collect"]
        collect = Collect.objects.get(pk=collect_id)
        collect.current_amount = (
            F("current_amount") + serializer.initial_data["amount"]
        )
        collect.bakers_count = F("bakers_count") + 1
        collect.save()
        payment = serializer.save(user=user, date=datetime.now(timezone.utc))

    @method_decorator(cache_page(60 * 15))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
