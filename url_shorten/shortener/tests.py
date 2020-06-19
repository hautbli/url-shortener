from django.test import TestCase
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from shortener.models import Shortener


class ShortenerTestCase(APITestCase):
    def setUp(self) -> None:
        self.origin_url = "http://www.naver.com"
        self.user = baker.make('auth.User')

    def test_create_shortener(self):

        self.client.force_authenticate(user=self.user)
        data = {'url_bf': self.origin_url}
        response = self.client.post('/shortener/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_response = response.data
        self.assertTrue(user_response['url_af'])
        self.assertEqual(user_response['url_bf'], self.origin_url)

    def test_redirect(self):
        shortener = Shortener.objects.create(url_bf='https://www.fc.com')

        response = self.client.get(shortener.url_af)

        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        self.assertEqual(response.url, shortener.url_bf)

    def test_uuid(self):
        shortener = Shortener()
        shortener. uuid_long_to_short()

        # self.fail()
