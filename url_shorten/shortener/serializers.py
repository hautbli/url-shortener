import string

from rest_framework.serializers import ModelSerializer

from shortener.models import Shortener


def base62(index):
    result = ""  # Base62 인코딩의 기본이 되는 문자들(배열은 상관없이 중복이 없으면 됩니다.)
    words = string.ascii_letters + string.digits

    while index % 62 > 0 or result == "":
        # index가 62인 경우에도 적용되기 위해 do-while 형식이 되도록 구현했다.
        result = result + words[index % 62]
        index = int(index / 62)
    return result


class ShortenerSerializer(ModelSerializer):
    class Meta:
        model = Shortener
        fields = ('url_bf', 'url_af',)

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.url_af = ('http://happy.'+base62(instance.id))
        instance.save()
        return instance
