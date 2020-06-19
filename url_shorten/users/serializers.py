from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from shortener.serializers import ShortenerSerializer


class UserSerializer(ModelSerializer):
    # shorteners = ShortenerSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password',)
        # write_only_fields = ('password',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
