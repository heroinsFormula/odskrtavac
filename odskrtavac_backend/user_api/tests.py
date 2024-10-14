from django.test import TestCase
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


    def test_register_user(self):
        """
        User může být registrován
        """
        response = self.register_user('franta')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(id=2).username, 'franta')

    def test_register_same_usernames(self):
        """
        Dva useři nemůžou mít stejný jméno.
        """
        response = self.register_user('test_user')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_register_no_credentials(self):
        """
        User nebude registrován, pokud nevyplní údaje
        """
        response_blankusr = self.register_user(username='', password='heslo123')
        response_blankpswd = self.register_user(username='user', password='')
        self.assertEqual(response_blankusr.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_blankpswd.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        """
        User se může přihlásit
        """
        response = self.login_user()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_incorrect_credentials(self):
        """
        User se nemůže přihlásit, pokud má špatné údaje
        """
        response_badusr = self.login_user(username='incorrect_username')
        response_badpswd = self.login_user(password='incorrect_password')
        self.assertEqual(response_badpswd.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_badusr.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_user(self):
        """
        User se může odhlásit
        """
        response = self.login_user()
        access_token = response.data['access']
        refresh_token = response.data['refresh']
        url = reverse('user_api:logout')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(url, {'refresh_token': refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)


