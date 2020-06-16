from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from django.utils.translation import ugettext_lazy
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from url_shorten import settings
from users.permissions import IsOwner
from users.serializers import UserSerializer
from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)


class UserModelViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    pass


class UserViewSet(UserModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False)
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            # pass
            response = Response({"detail": "log out -> fail! ! "},
                                status=status.HTTP_404_NOT_FOUND)
            return response
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)

        response = Response({"detail": "Successfully logged out."},
                            status=status.HTTP_200_OK)

        return response

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['update', 'destroy', 'retrieve']:
            return [IsOwner()]
        return super().get_permissions()

