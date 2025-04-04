from django.urls import path
from .views import toggle_read_status, get_booklist_attributes, get_countries
from books import views

app_name = 'books'
urlpatterns = [
    path('get-books/', views.BookListView.as_view(), name='get_books'),
    path(
        'mark-read/<slug:slug>/',
        toggle_read_status,
        name='toggle_read_status',
    ),
    path('get-authors/', views.AuthorListView.as_view(), name='get_authors'),
    path('get-booklist-attributes/', get_booklist_attributes, name='get_booklist_attributes'),
    path('post-book/', views.BookListView.as_view(), name='post_book'),
    path('post-author/', views.AuthorListView.as_view(), name='post_author'),
    path('get-countries/', get_countries, name='get_countries'),
    path('edit-book/<slug:slug>/', views.BookListView.as_view(),name='edit_book'),
    path('delete-book/<slug:slug>/', views.BookListView.as_view(),name='delete_book')
]