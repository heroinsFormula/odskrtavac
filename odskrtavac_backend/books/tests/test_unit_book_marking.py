from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .helper_functions import (
    login_user,
    mark_book,
    get_user_criteria
)


class BookTestCase(APITestCase):
    fixtures = ["books/tests/test_fixture.json"]

    def setUp(self):
        User.objects.create_user(username='test_user',
                                 password='password123')

        login_user(self)

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

    def test_mark_prose(self):
        mark_book(self, slug='test_proza')
        response = get_user_criteria(self)
        self.assertEqual(response['Próza'], 1)

    def test_mark_poetry(self):
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

    def test_mark_no_author(self):
        mark_book(self, slug='no_author')
        response = get_user_criteria(self)
        self.assertEqual(response['Česká 20. a 21. století'], 1)
