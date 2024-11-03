from rest_framework import status
from django.contrib.auth.models import User
from books.models import Author, Book
from .mixins import BookAPITestCaseMixin


class BookTestCase(BookAPITestCaseMixin):
    fixtures = ["books/tests/test_fixture.json"]

    def setUp(self):
        User.objects.create_user(
            username='test_user',
            password='password123'
        )

        self.login_user()

    def test_create_book_with_no_country(self):
        response = self.create_book(
            name='test_book',
            author_full_name=None,
            literary_type='Próza',
            publish_year=0,
            country=None
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Musí být vyplněna země!')

    def test_create_book_with_blank_author(self):
        response = self.create_book(
            name='test_book',
            author_full_name=None,
            literary_type='Próza',
            publish_year=0,
            country='CZ',
            no_author=True
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_book_with_author_unintentionally_left_blank(self):
        response = self.create_book(
            name='test_book',
            author_full_name='',
            literary_type='Próza',
            publish_year=0,
            country='IR',
            no_author=False
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Autorovi chybí jméno!')

    def test_create_book_with_new_author(self):
        response = self.create_book(
            name='test_book',
            author_full_name='new_author',
            literary_type='Próza',
            publish_year=0,
            country='CZ'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        author_full_name = Author.objects.get(full_name='new_author').full_name
        author_country = Author.objects.get(full_name='new_author').country
        self.assertEqual(author_full_name, 'new_author')
        self.assertEqual(author_country, 'CZ')

    def test_create_book_with_existing_name_author_combination(self):
        author = Author.objects.create(
            full_name='existing_author',
            country='CZ'
        )
        Book.objects.create(
            name='existing_book',
            author=author,
            literary_type='Próza',
            publish_year=0,
            country='CZ'
        )
        response = self.create_book(
            name='existing_book',
            author_full_name='existing_author',
            literary_type='Próza',
            publish_year=0,
            country='CZ'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'],
            'Kniha s tímto názvem a autorem již existuje!'
        )
