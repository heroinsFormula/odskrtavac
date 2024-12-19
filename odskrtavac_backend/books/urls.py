from django.urls import path
from .views import (
    post_book,
    post_author,
    get_books,
    toggle_read_status,
    getUsersBooklistAttributes,
)

app_name = "books"
urlpatterns = [
    path("get-books/", get_books, name="get_books"),
    path(
        "mark-read/<slug:slug>/",
        toggle_read_status,
        name='toggle_read_status',
    ),
    path("get-user-criteria/", getUsersBooklistAttributes, name='get_user_criteria'),
    path("post-book/", post_book, name="post_book"),
    path("post-author/", post_author, name="post_author"),
]
