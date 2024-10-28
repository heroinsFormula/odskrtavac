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

    def register_user(self, username, password='heslo'):
        url = reverse('user_api:register')
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        return response

    def test_registering_with_existing_username_not_possible(self):
        response = self.register_user('test_user')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST,)
        self.assertEqual(User.objects.count(), 1)

    def test_registering_without_password_not_possible(self):
        response = self.register_user(username='sample_name',
                                      password='')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registering_without_username_not_possible(self):
        response = self.register_user(username='',
                                      password='sample_password')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logging_in_with_incorrect_username_not_possible(self):
        response = self.login_user(username='incorrect_username',
                                   password='password123')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
