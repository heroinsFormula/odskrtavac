from django.contrib.auth.models import User
from rest_framework import status
from books.models import Author, Book
from .mixins import BookAPITestCaseMixin


class BookTestCase(BookAPITestCaseMixin):
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
        Book.objects.create(
            name='test book',
            slug='test-book',
            author=self.test_author,
            publish_year=0
        )

        self.login_user()

    def test_get_all_books(self):
        response = self.get_books()
        self.assertEqual(response.data[0]['name'], 'můj kemp')

    def test_search_books(self):
        response = self.get_books(
            name='test book'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'test book')

    def test_create_author(self):
        response = self.create_author(
            full_name='test_author_2',
            country='GB'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.last().full_name, 'test_author_2')
        self.assertEqual(Author.objects.last().country, 'GB')

    def test_create_book(self):
        response = self.create_book(
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
        read_status = self.mark_book(slug='muj-kemp').get('is_read')
        self.assertEqual(read_status, True)
        read_status = self.mark_book(slug='muj-kemp').get('is_read')
        self.assertEqual(read_status, False)

    def test_mark_nonexistent_book(self):
        response = self.mark_book(slug='blbost').get('error')
        self.assertEqual(response, 'Kniha nebyla nalezena')
