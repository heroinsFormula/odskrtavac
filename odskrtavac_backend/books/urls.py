from django.urls import path
from .views import BookListView, AuthorListView, toggle_read_status, get_booklist_attributes

app_name = "books"
urlpatterns = [
    path("get-books/", BookListView.as_view(), name="get_books"),
    path(
        "mark-read/<slug:slug>/",
        toggle_read_status,
        name='toggle_read_status',
    ),
    path("get-authors/", AuthorListView.as_view(), name="get_authors"),
    path("get-booklist-attributes/", get_booklist_attributes, name='get_booklist_attributes'),
    path("post-book/", BookListView.as_view(), name="post_book"),
    path("post-author/", AuthorListView.as_view(), name="post_author"),
]