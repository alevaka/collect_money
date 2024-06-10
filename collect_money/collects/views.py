from collects.models import Collect
from collects.permissions import IsAuthorOrAdmin
from collects.serializers import CollectListSerializer, CollectSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets


class CollectViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Collect"""

    queryset = Collect.objects.all()
    permission_classes = [IsAuthorOrAdmin]

    def get_serializer_class(self):
        """Выбор сериализатора для списка или одного сбора"""

        if self.action == "list":
            return CollectListSerializer
        return CollectSerializer

    def perform_create(self, serializer):
        """Создание нового сбора"""

        user = self.request.user

        serializer.is_valid(raise_exception=True)
        collect = serializer.save(author=user)

    @method_decorator(cache_page(60 * 15))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
