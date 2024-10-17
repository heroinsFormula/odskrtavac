from django.urls import path
from books.views import get_books, toggle_read_status, get_user_criteria

app_name = "books"
urlpatterns = [
    path("get_books/", get_books, name="get_books"),
    path("book/<slug:slug>/mark_read", toggle_read_status, name='toggle_read_status'),
    path("get_user_criteria/", get_user_criteria, name='get_user_criteria')
]