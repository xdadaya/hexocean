from rest_framework import serializers

from users.models import User, Tier


class TierSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    thumbnails_sizes = serializers.ListField(child=serializers.IntegerField())
    have_original_url = serializers.BooleanField()
    can_create_links = serializers.BooleanField()

    class Meta:
        model = Tier
        fields = ("name", "thumbnails_sizes", "have_original_url", "can_create_links")


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=64, write_only=True)
    username = serializers.CharField(min_length=4, max_length=32)
    email = serializers.EmailField()
    tier = TierSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'tier', 'role')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data: dict[str, str]) -> User:
        user = User.objects.create_user(**validated_data)
        user.role = User.Roles.USER
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    username = serializers.CharField()
    role = serializers.ChoiceField([User.Roles.USER, User.Roles.ADMIN])
    tier = TierSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "role", "tier")
