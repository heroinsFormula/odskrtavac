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

    def test_get_18_century_books(self):
        response = self.get_books(century='18th and prior')
        for book in response.data:
            self.assertLessEqual(book['publish_year'], 1800)

    def test_get_19_century_books(self):
        response = self.get_books(century='19th')
        for book in response.data:
            self.assertGreaterEqual(book['publish_year'], 1801)
            self.assertLessEqual(book['publish_year'], 1900)

    def test_get_20_and_21_century_books(self):
        response = self.get_books(century='20th-21st')
        for book in response.data:
            self.assertGreaterEqual(book['publish_year'], 1901)

    def test_get_czech_books(self):
        response = self.get_books(country='czech')
        for book in response.data:
            self.assertEqual(book['country'], 'CZ')

    def test_get_world_books(self):
        response = self.get_books(country='world')
        for book in response.data:
            self.assertNotEqual(book['country'], 'CZ')

    def test_get_multiple_literary_types(self):
        response = self.get_books(prose=True, poetry=True)
        for book in response.data:
            self.assertIn(book['literary_type'], ['Próza', 'Poezie'])

    def test_utf8_search(self):
        response = self.get_books(name='Nečeský autor')
        for book in response.data:
            self.assertIn(book['author']['full_name'], 'Nečeský autor')

    def test_case_sensitive_search(self):
        response = self.get_books(name='jOhN DoE')
        for book in response.data:
            self.assertIn(book['author']['full_name'], 'John Doe')
