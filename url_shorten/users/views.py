from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from django.utils.translation import ugettext_lazy
from rest_framework import status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
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


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=["post"], detail=False)
    def login(self, request):
        serializer = AuthTokenSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    @action(methods=["delete"], detail=False)
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            response = Response({"detail": "log out -> fail! ! "},
                                status=status.HTTP_404_NOT_FOUND)
            return response

        response = Response({"detail": "Successfully logged out."},
                            status=status.HTTP_200_OK)
        return response

    def get_permissions(self):

        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['update', 'destroy', 'retrieve']:
            return [IsOwner()]
        elif self.action == 'login' :
            return [AllowAny()]
        return super().get_permissions()
