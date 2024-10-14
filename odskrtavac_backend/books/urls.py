from django.urls import path
from . import views
from books.views import post_book, get_books, get_authors, toggle_read_status

app_name = "books"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("get_books/", get_books, name="get_books"),
    path("get_authors/", get_authors, name="get_authors"),
    path("post_book/", post_book, name="post_book"),
    path("author/<slug:slug>", views.AuthorDetailView.as_view(), name="author_detail"),
    path("book/<slug:slug>", views.BookDetailView.as_view(), name="book_detail"),
    path("book/<slug:slug>/mark_read", toggle_read_status, name='toggle_read_status'),
]