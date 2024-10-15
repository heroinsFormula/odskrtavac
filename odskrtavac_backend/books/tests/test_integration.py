from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from books.models import Author, Book
from django.contrib.auth.models import User


class BookTestCase(APITestCase):
    def setUp(self):
        User.objects.create_user(username='test_user', password='password123')
        self.author = Author.objects.create(full_name='name', country='CZ')
        Book.objects.create(name='můj kemp', slug='muj-kemp', author=self.author, publish_year=0)

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
    


    def test_get_all_books(self):
        url = reverse('books:get_books')
        response = self.client.get(url)
        self.assertEqual(response.data[0]['name'], 'můj kemp')

    def test_mark_book(self):
        read_status = self.mark_book().get('read')
        self.assertEqual(read_status, True)
        read_status = self.mark_book().get('read')
        self.assertEqual(read_status, False)

    def test_mark_nonexistant_book(self):
        response = self.mark_book(slug='blbost').get('error')
        self.assertEqual(response, 'Kniha nebyla nalezena')