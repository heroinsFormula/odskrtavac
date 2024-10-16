from django.urls import reverse
from rest_framework.test import APITestCase
from books.models import Author, Book
from django.contrib.auth.models import User
from .helper_functions import login_user, mark_book

class BookTestCase(APITestCase):
    def setUp(self):
        User.objects.create_user(username='test_user',
                                 password='password123')
        self.author = Author.objects.create(full_name='name',
                                            country='CZ')
        Book.objects.create(name='můj kemp',
                            slug='muj-kemp', 
                            author=self.author,
                            publish_year=0)
        
        login_user(self)
    


    def test_get_all_books(self):
        url = reverse('books:get_books')
        response = self.client.get(url)
        self.assertEqual(response.data[0]['name'], 'můj kemp')

    def test_mark_book(self):
        read_status = mark_book(self, slug='muj-kemp').get('read')
        self.assertEqual(read_status, True)
        read_status = mark_book(self, slug='muj-kemp').get('read')
        self.assertEqual(read_status, False)

    def test_mark_nonexistant_book(self):
        response = mark_book(self, slug='blbost').get('error')
        self.assertEqual(response, 'Kniha nebyla nalezena')