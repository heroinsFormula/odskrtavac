from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        User.objects.create_user(username='test_user', password='password123')

    def login_user(self, username='test_user', password='password123'):
        url = reverse('user_api:login')
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        return response

    def logout_user(self):
        response = self.login_user()
        access_token = response.data['access']
        refresh_token = response.data['refresh']
        url = reverse('user_api:logout')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(url,
                                    {'refresh_token': refresh_token},
                                    format='json')
        return response

    def register_user(self, username, password='heslo'):
        url = reverse('user_api:register')
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        return response

    def test_login_user(self):
        response = self.login_user()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_user(self):
        response = self.register_user('franta')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(id=2).username, 'franta')

    def test_logout_user(self):
        response = self.logout_user()
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
