from django.urls import reverse


def login_user(self, username='test_user', password='password123'):
    url = reverse('user_api:login')
    data = {'username': username, 'password': password}
    response = self.client.post(url, data, format='json')
    access_token = response.data['access']
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return response


def mark_book(self, slug):
    url = reverse('books:toggle_read_status', kwargs={'slug': slug})
    response = self.client.post(url).json()
    return response


def get_user_criteria(self):
    url = reverse('books:get_user_criteria')
    response = self.client.get(url).json()
    return response


def create_author(self, full_name: str, country: str):
    url = reverse('books:post_author')
    data = {
        'full_name': full_name,
        'country': country,
    }
    response = self.client.post(url, data, format='json')
    return response


def create_book(self,
                name: str,
                author_full_name: str,
                literary_type: str,
                publish_year: int,
                **kwargs):
    url = reverse('books:post_book')

    data = {
        'name': name,
        'author_full_name': author_full_name,
        'country': kwargs['new_author_country'],
        'literary_type': literary_type,
        'publish_year': publish_year
    }
    response = self.client.post(url, data, format='json')
    return response
