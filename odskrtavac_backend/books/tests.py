from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from books.models import Author, Book
from django.contrib.auth.models import User


class BookTestCase(APITestCase):
    def setUp(self):
        self.author1 = Author.objects.create(full_name="John Doe", country="GB")
        self.author2 = Author.objects.create(country="CZ")
        Book.objects.create(name='můj kemp', author=self.author1, publish_year=0)
        Book.objects.create(name='1', author=self.author1, publish_year=0)
        Book.objects.create(name='2', author=self.author1, publish_year=0)
        Book.objects.create(name='3', author=self.author1, publish_year=0)

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

    def test_get_all_books(self):
        """
        Userovi jsou poslány knihy
        """
        url = reverse('books:get_books')
        response = self.client.get(url)
        self.assertEqual(response.data[0]['name'], 'můj kemp')

    def test_mark_book(self):
        """
        Přihlášený user si může označit nebo odoznačit knížku
        """
        read_status = self.mark_book().get('read')
        self.assertEqual(read_status, True)
        read_status = self.mark_book().get('read')
        self.assertEqual(read_status, False)

    def test_mark_nonexistant_book(self):
        """
        Nelze označit knížku, která neexistuje
        """
        response = self.mark_book(slug='blbost').get('error')
        self.assertEqual(response, 'Kniha nebyla nalezena')



    def test_18_stoleti(self):
        """
        1701-1800 => 18. století
        """
        Book.objects.create(name='18stol', 
                            publish_year=1800,
                            author=self.author1)
        response = self.mark_book(slug='18stol').get('criteria')
        self.assertEqual(response['Světová a česká do 18. století'], 1)
    
    def test_19_stoleti(self):
        """
        1801-1900 => 19. století
        """
        Book.objects.create(name='19stol', 
                            publish_year=1900,
                            author=self.author1)
        response = self.mark_book(slug='19stol').get('criteria')
        self.assertEqual(response['Světová a česká 19. století'], 1)

    def test_svet(self):
        """
        1901-202x, author GB
        """
        Book.objects.create(name='svet', 
                            publish_year=1901,
                            author=self.author1)
        response = self.mark_book(slug='svet').get('criteria')
        self.assertEqual(response['Světová 20. a 21. století'], 1)

    def test_cz(self):
        """
        1901-202x, author CZ
        """
        Book.objects.create(name='cz', 
                            publish_year=1901,
                            author=self.author2)
        response = self.mark_book(slug='cz').get('criteria')
        self.assertEqual(response['Česká 20. a 21. století'], 1)

    def test_proza(self):
        Book.objects.create(name='x', 
                            publish_year=0,
                            literary_type='Próza',
                            author=self.author1)
        response = self.mark_book(slug='x').get('criteria')
        self.assertEqual(response['Próza'], 1)
    
    def test_poezie(self):
        Book.objects.create(name='x', 
                            publish_year=0,
                            literary_type='Poezie',
                            author=self.author1)
        response = self.mark_book(slug='x').get('criteria')
        self.assertEqual(response['Poezie'], 1)    

    def test_drama(self):
        Book.objects.create(name='x', 
                            publish_year=0,
                            literary_type='Drama',
                            author=self.author1)
        response = self.mark_book(slug='x').get('criteria')
        self.assertEqual(response['Drama'], 1)

    def test_duplicitni_autor(self):
        self.mark_book(slug='1')
        self.mark_book(slug='2')
        response = self.mark_book(slug='3').get('criteria')
        self.assertEqual(response['Duplicitní autoři'][0], 'John Doe')

