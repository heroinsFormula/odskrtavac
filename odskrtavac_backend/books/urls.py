from django.urls import path
from . import views
from books.views import get_books, toggle_read_status

app_name = "books"
urlpatterns = [
    path("get_books/", get_books, name="get_books"),
    path("book/<slug:slug>/mark_read", toggle_read_status, name='toggle_read_status'),
]