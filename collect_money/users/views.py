from djoser.views import UserViewSet
from users.models import User


class CustomUserViewSet(UserViewSet):
    """Вьюсет для пользователей"""

    serializer_class = User
    queryset = User.objects.all()
