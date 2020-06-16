from django.contrib.auth.models import User
from django.test import TestCase
from model_bakery import baker
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        # self.users = baker.make('auth.User', _quantity=3)

        self.data = {'username': 'user', 'password': '1111'}
        response = self.client.post('/users/', data=self.data)

        data = {'username': 'user22', 'password': '1111'}
        self.client.post('/users/', data=data)

        self.user = User.objects.first()
        print(self.user)

    def test_should_create(self):
        data = {'username': 'abc', 'password': '1111'}
        response = self.client.post('/users/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_response = response.data

        self.assertEqual(user_response['username'], data['username'])

    def test_should_get(self):
        user = self.user
        # 로그인 상태
        self.client.force_authenticate(user=user)

        response = self.client.get(f'/users/{user.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_response = response.data
        self.assertEqual(user_response['username'], user.username)

    def test_should_update(self):
        user = self.user
        prev_username = user.username
        self.client.force_authenticate(user=user)

        data = {'username': 'newname', 'password': '2222'}
        response = self.client.put(f'/users/{user.id}/', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_response = response.data
        self.assertEqual(user_response['username'], data['username'])
        self.assertNotEqual(user_response['username'], prev_username)

    def test_should_delete(self):
        user = self.user
        self.client.force_authenticate(user=user)

        response = self.client.delete(f'/users/{user.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(User.objects.filter(pk=user.id).exists())

    def test_should_logout(self):
        # 로그인할 유저의 토큰을 구한다
        response_login = self.client.post('/login/', data=self.data)  # return -> 사용자의 토큰 {'token' : 'sdfsdf}
        token = response_login.data['token']

        # 토큰을 가진 유저가 request를 한다
        self.client.force_authenticate(user=self.user, token=token)

        response = self.client.get('/users/logout/')

        is_token_exists = Token.objects.filter(pk=token).exists()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(is_token_exists)

    def test_should_login(self):
        response = self.client.post('/login/', data=self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 응답한 토큰이 토큰모델에 있는지
        token = Token.objects.filter(pk=response.data['token']).exists()

        self.assertTrue(token)
