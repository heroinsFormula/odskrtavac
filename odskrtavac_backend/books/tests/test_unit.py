from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from books.models import Author, Book
from django.contrib.auth.models import User


class BookTestCase(APITestCase):
    fixtures = ["books/tests/test_fixure.json"]
    def setUp(self):
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
    


    def test_18_stoleti(self):
        """
        1701-1800 => 18. století
        """
        response = self.mark_book(slug='test_18stol').get('criteria')
        self.assertEqual(response['Světová a česká do 18. století'], 1)
    
    def test_19_stoleti(self):
        """
        1801-1900 => 19. století
        """
        response = self.mark_book(slug='test_19stol').get('criteria')
        self.assertEqual(response['Světová a česká 19. století'], 1)

    def test_20_a_21_stoleti_svetova(self):
        """
        1901-2xxx, autor NEMÁ country = CZ
        """
        response = self.mark_book(slug='test_20a21_svet').get('criteria')
        self.assertEqual(response['Světová 20. a 21. století'], 1)

    def test_20_a_21_stoleti_ceska(self):
        """
        1901-2xxx, autor má country = CZ
        """
        response = self.mark_book(slug='test_20a21_cesko').get('criteria')
        self.assertEqual(response['Česká 20. a 21. století'], 1)


    def test_proza(self):
        response = self.mark_book(slug='test_proza').get('criteria')
        self.assertEqual(response['Próza'], 1)
    
    def test_poezie(self):
        response = self.mark_book(slug='test_poezie').get('criteria')
        self.assertEqual(response['Poezie'], 1)    

    def test_drama(self):
        response = self.mark_book(slug='test_drama').get('criteria')
        self.assertEqual(response['Drama'], 1)


    def test_oznaceni_duplicitniho_autora(self):
        """
        Pokud má uživatel od jednoho autora označené víc jak 2 knihy,
        tak je autor zapsán v duplicitních autorech
        """
        response = self.mark_book(slug='test_1').get('criteria')
        self.assertEqual(response['Duplicitní autoři'], [])
        response = self.mark_book(slug='test_2').get('criteria')
        self.assertEqual(response['Duplicitní autoři'], [])
        response = self.mark_book(slug='test_3').get('criteria')
        self.assertEqual(response['Duplicitní autoři'], ['John Doe'])

