from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from django.utils.translation import ugettext_lazy
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from url_shorten import settings
from users.serializers import UserSerializer
from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False)
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            response = Response({"detail": "log out -> fail! ! "},
                                status=status.HTTP_404_NOT_FOUND)
            return response
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)

        response = Response({"detail": "Successfully logged out."},
                            status=status.HTTP_200_OK)

        return response
