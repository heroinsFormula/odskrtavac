from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from books.models import Author, Book
from django.contrib.auth.models import User


class BookTestCase(APITestCase):
    def setUp(self):
        self.author1 = Author.objects.create(full_name="John Doe", country="GB")
        self.author2 = Author.objects.create(country="CZ")
        Book.objects.create(name='můj kemp', author=self.author1, publish_year=0)
        Book.objects.create(name='1', author=self.author1, publish_year=0)
        Book.objects.create(name='2', author=self.author1, publish_year=0)
        Book.objects.create(name='3', author=self.author1, publish_year=0)

        User.objects.create_user(username='test_user', password='password123')





    def login_user(self, username='test_user', password='password123'):
        url = reverse('user_api:login')
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        return response
    
    def mark_book(self, slug='muj-kemp'):
        response = self.login_user()
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        url = reverse('books:toggle_read_status', kwargs={'slug': slug})
        response = self.client.post(url, format='json')
        response = response.json()
        return response





