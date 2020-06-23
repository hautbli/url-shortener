from django.http import HttpResponseRedirect
from django.shortcuts import render
import string

from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from shortener.models import Shortener
from shortener.permissions import IsOwner
from shortener.serializers import ShortenerSerializer


class ShortenerViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin, GenericViewSet):
    """ /shortener/ post -> origin url을 short url로 바꿔준다 """
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer

    def filter_queryset(self, queryset):
        """ user get했을 때 유저의 오브젝트만 보여준다 """
        if self.action == 'list':
            return queryset.filter(user=self.request.user)
        return super().filter_queryset(queryset)

    def perform_create(self, serializer):
        """url model에 user정보 저장 """
        if self.request.user.is_anonymous:
            serializer.save()
        else:
            serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['destroy', 'retrieve']:
            return [IsOwner()]
        return super().get_permissions()


class RedirecturlViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    """" url_bf가 request할 때 db에 저장된 url_bf로 redirect한다"""

    lookup_field = 'url_af'
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer
    permission_classes = [AllowAny]
    throttle_classes = []

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return HttpResponseRedirect(serializer.data['url_bf'])

    def get_object(self):
        """lookup_filed가 shortener url의 뒷부분이기 (sd)때문에 모델에 저장된 것을 모델(http://happy.sd)
        찾을 수가 없다. 그래서 filter_kwarg를 오버라이드함"""
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: 'http://127.0.0.1:8000/happy/' + self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.action == 'retrieve':
            pass
        return super().get_permissions()


