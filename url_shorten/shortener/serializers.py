
from rest_framework.serializers import ModelSerializer
from shortener.models import Shortener


class ShortenerSerializer(ModelSerializer):
    class Meta:
        model = Shortener
        fields = ('url_bf', 'url_af','count',)
