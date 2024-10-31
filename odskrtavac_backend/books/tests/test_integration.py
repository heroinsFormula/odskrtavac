from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from books.models import Author, Book
from .helper_functions import login_user, mark_book, create_author, create_book


class BookTestCase(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='test_user',
            password='password123'
        )
        self.test_author = Author.objects.create(
            full_name='test_author_1',
            country='CZ'
        )
        Book.objects.create(
            name='můj kemp',
            slug='muj-kemp',
            author=self.test_author,
            publish_year=0
        )

        login_user(self)

    def test_get_all_books(self):
        url = reverse('books:get_books')
        response = self.client.get(url)
        self.assertEqual(response.data[0]['name'], 'můj kemp')

    def test_create_author(self):
        response = create_author(
            self,
            full_name='test_author_2',
            country='GB'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.last().full_name, 'test_author_2')
        self.assertEqual(Author.objects.last().country, 'GB')

    def test_create_book(self):
        response = create_book(
            self,
            name='test_book',
            author_full_name='test_author_1',
            country='CZ',
            literary_type='Próza',
            publish_year=1234
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.last().name, 'test_book')
        self.assertEqual(Book.objects.last().literary_type, 'Próza')

    def test_mark_book(self):
        read_status = mark_book(self, slug='muj-kemp').get('is_read')
        self.assertEqual(read_status, True)
        read_status = mark_book(self, slug='muj-kemp').get('is_read')
        self.assertEqual(read_status, False)

    def test_mark_nonexistent_book(self):
        response = mark_book(self, slug='blbost').get('error')
        self.assertEqual(response, 'Kniha nebyla nalezena')
