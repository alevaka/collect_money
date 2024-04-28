from djoser.serializers import UserSerializer
from users.models import User


class CustomUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "middle_name",
            "last_name",
        )
