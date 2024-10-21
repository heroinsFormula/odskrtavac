from django.urls import path
from books.views import get_books, toggle_read_status, get_user_criteria

app_name = "books"
urlpatterns = [
    path("get-books/", get_books, name="get_books"),
    path("book/<slug:slug>/mark-read", toggle_read_status, name='toggle_read_status'),
    path("get-user-criteria/", get_user_criteria, name='get_user_criteria')
]