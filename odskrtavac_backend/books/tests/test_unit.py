from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from books.models import Author
from .helper_functions import (
    login_user,
    mark_book,
    get_user_criteria,
    create_author,
    create_book
)


class BookTestCase(APITestCase):
    fixtures = ["books/tests/test_fixture.json"]

    def setUp(self):
        User.objects.create_user(username='test_user',
                                 password='password123')

        login_user(self)

    # TODO: Dopsat testy pro search

    # TODO hned teď: dopsat testy na
        # tvorbu knihy s novým autorem
        # tvorbu knihy s neplatnými údaji
        # view na get authors
        # pak odstranit tenhle komentář

    def test_create_book_with_invalid_author(self):
        response = create_book(self,
                               name='test_book',
                               author_full_name=None,
                               literary_type='Próza',
                               publish_year=0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json.message, 'Kniha musí mít autora!')

    def test_create_book_with_new_author(self):
        response = create_book(self,
                               name='test_book',
                               author_full_name='new_author',
                               literary_type='Próza',
                               publish_year=0,
                               new_author_country='CZ',)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        author_full_name = Author.objects.get(full_name='new_author').full_name
        author_country = Author.objects.get(full_name='new_author').country
        self.assertEqual(author_full_name, 'new_author')
        self.assertEqual(author_country, 'CZ')

    def test_mark_18_century_books(self):
        """
        1701-1800 => 18. století
        """
        mark_book(self, slug='test_18stol')
        response = get_user_criteria(self)
        self.assertEqual(response['Světová a česká do 18. století'], 1)

    def test_mark_19_century_books(self):
        """
        1801-1900 => 19. století
        """
        mark_book(self, slug='test_19stol')
        response = get_user_criteria(self)
        self.assertEqual(response['Světová a česká 19. století'], 1)

    def test_mark_world_books(self):
        """
        1901-2xxx, autor country != CZ
        """
        mark_book(self, slug='test_20a21_svet')
        response = get_user_criteria(self)
        self.assertEqual(response['Světová 20. a 21. století'], 1)

    def test_mark_czech_books(self):
        """
        1901-2xxx, autor country == CZ
        """
        mark_book(self, slug='test_20a21_cesko')
        response = get_user_criteria(self)
        self.assertEqual(response['Česká 20. a 21. století'], 1)

    def test_mark_proza(self):
        mark_book(self, slug='test_proza')
        response = get_user_criteria(self)
        self.assertEqual(response['Próza'], 1)

    def test_mark_poezie(self):
        mark_book(self, slug='test_poezie')
        response = get_user_criteria(self)
        self.assertEqual(response['Poezie'], 1)

    def test_mark_drama(self):
        mark_book(self, slug='test_drama')
        response = get_user_criteria(self)
        self.assertEqual(response['Drama'], 1)

    def test_mark_duplicate_authors(self):
        """
        Pokud má uživatel od jednoho autora označené víc jak 2 knihy,
        tak je autor zapsán v duplicitních autorech
        """
        mark_book(self, slug='test_1')
        response = get_user_criteria(self)
        self.assertEqual(response['Duplicitní autoři'], [])

        mark_book(self, slug='test_2')
        response = get_user_criteria(self)
        self.assertEqual(response['Duplicitní autoři'], [])

        mark_book(self, slug='test_3')
        response = get_user_criteria(self)
        self.assertEqual(response['Duplicitní autoři'], ['John Doe'])
