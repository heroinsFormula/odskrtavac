from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .helper_functions import login_user, mark_book, get_user_criteria


class BookTestCase(APITestCase):
    fixtures = ["books/tests/test_fixure.json"]
    def setUp(self):
        User.objects.create_user(username='test_user',
                                 password='password123')
        
        login_user(self)


    def test_18_stoleti(self):
        """
        1701-1800 => 18. století
        """
        mark_book(self, slug='test_18stol')
        response = get_user_criteria(self)
        self.assertEqual(response['Světová a česká do 18. století'], 1)
    
    def test_19_stoleti(self):
        """
        1801-1900 => 19. století
        """
        mark_book(self, slug='test_19stol')
        response = get_user_criteria(self)
        self.assertEqual(response['Světová a česká 19. století'], 1)

    def test_svetova(self):
        """
        1901-2xxx, autor NEMÁ country = CZ
        """
        mark_book(self, slug='test_20a21_svet')
        response = get_user_criteria(self)
        self.assertEqual(response['Světová 20. a 21. století'], 1)

    def test_ceska(self):
        """
        1901-2xxx, autor má country = CZ
        """
        mark_book(self, slug='test_20a21_cesko')
        response = get_user_criteria(self)
        self.assertEqual(response['Česká 20. a 21. století'], 1)

    def test_proza(self):
        mark_book(self, slug='test_proza')
        response = get_user_criteria(self)
        self.assertEqual(response['Próza'], 1)

    def test_poezie(self):
        mark_book(self, slug='test_poezie')
        response = get_user_criteria(self)
        self.assertEqual(response['Poezie'], 1)

    def test_drama(self):
        mark_book(self, slug='test_drama')
        response = get_user_criteria(self)
        self.assertEqual(response['Drama'], 1)

    def test_oznaceni_duplicitniho_autora(self):
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