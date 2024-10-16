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