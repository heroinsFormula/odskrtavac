from rest_framework.test import APITestCase
from django.urls import reverse


class BookAPITestCaseMixin(APITestCase):

    def login_user(
            self,
            username: str = 'test_user',
            password: str = 'password123') -> dict:
        url = reverse('user_api:login')
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        access_token = response.data['access']
        self.client.credentials(
                HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )
        return response

    def mark_book(
            self,
            slug: str) -> dict:
        url = reverse('books:toggle_read_status', kwargs={'slug': slug})
        response = self.client.post(url).json()
        return response

    def get_user_criteria(self) -> dict:
        url = reverse('books:get_user_criteria')
        response = self.client.get(url).json()
        return response

    def create_author(
            self,
            full_name: str,
            country: str) -> dict:
        url = reverse('books:post_author')
        data = {
            'full_name': full_name,
            'country': country,
        }
        response = self.client.post(url, data, format='json')
        return response

    def create_book(
            self,
            name: str,
            author_full_name: str,
            country: str,
            literary_type: str,
            publish_year: int,
            no_author: bool = False) -> dict:
        url = reverse('books:post_book')
        data = {
            'name': name,
            'author_full_name': author_full_name,
            'country': country,
            'literary_type': literary_type,
            'publish_year': publish_year,
            'no_author': no_author
        }
        response = self.client.post(url, data, format='json')
        return response

    def get_books(
            self,
            name: str = "",
            prose: bool = False,
            poetry: bool = False,
            drama: bool = False,
            country: str = "",
            century: str = "") -> dict:
        url = reverse('books:get_books')
        data = {
            'name': name,
            'prose': prose,
            'poetry': poetry,
            'drama': drama,
            'country': country,
            'century': century
        }
        response = self.client.get(url, data, format='json')
        return response
