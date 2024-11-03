from django.contrib.auth.models import User
from .mixins import BookAPITestCaseMixin


class BookTestCase(BookAPITestCaseMixin):
    fixtures = ["books/tests/test_fixture.json"]

    def setUp(self):
        User.objects.create_user(
            username='test_user',
            password='password123'
        )

        self.login_user()

    def test_mark_18_century_books(self):
        """
        1701-1800 => 18. století
        """
        self.mark_book(slug='test_18stol')
        response = self.get_user_criteria()
        self.assertEqual(response['Světová a česká do 18. století'], 1)

    def test_mark_19_century_books(self):
        """
        1801-1900 => 19. století
        """
        self.mark_book(slug='test_19stol')
        response = self.get_user_criteria()
        self.assertEqual(response['Světová a česká 19. století'], 1)

    def test_mark_world_books(self):
        """
        1901-2xxx, autor country != CZ
        """
        self.mark_book(slug='test_20a21_svet')
        response = self.get_user_criteria()
        self.assertEqual(response['Světová 20. a 21. století'], 1)

    def test_mark_czech_books(self):
        """
        1901-2xxx, autor country == CZ
        """
        self.mark_book(slug='test_20a21_cesko')
        response = self.get_user_criteria()
        self.assertEqual(response['Česká 20. a 21. století'], 1)

    def test_mark_prose(self):
        self.mark_book(slug='test_proza')
        response = self.get_user_criteria()
        self.assertEqual(response['Próza'], 1)

    def test_mark_poetry(self):
        self.mark_book(slug='test_poezie')
        response = self.get_user_criteria()
        self.assertEqual(response['Poezie'], 1)

    def test_mark_drama(self):
        self.mark_book(slug='test_drama')
        response = self.get_user_criteria()
        self.assertEqual(response['Drama'], 1)

    def test_mark_duplicate_authors(self):
        """
        Pokud má uživatel od jednoho autora označené víc jak 2 knihy,
        tak je autor zapsán v duplicitních autorech
        """
        self.mark_book(slug='test_1')
        response = self.get_user_criteria()
        self.assertEqual(response['Duplicitní autoři'], [])

        self.mark_book(slug='test_2')
        response = self.get_user_criteria()
        self.assertEqual(response['Duplicitní autoři'], [])

        self.mark_book(slug='test_3')
        response = self.get_user_criteria()
        self.assertEqual(response['Duplicitní autoři'], ['John Doe'])

    def test_mark_no_author(self):
        self.mark_book(slug='no_author')
        response = self.get_user_criteria()
        self.assertEqual(response['Česká 20. a 21. století'], 1)
